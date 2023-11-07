import math
import numpy as np
import torch
import cv2


def get_ctc_vocab(char_list):
    # blank
    ctc_char_list = "_" + char_list
    ctc_map, inv_ctc_map = {}, {}
    for i, char in enumerate(ctc_char_list):
        ctc_map[char] = i
        inv_ctc_map[i] = char
    return ctc_map, inv_ctc_map, ctc_char_list


def iterative_levenshtein(s, t, costs=(1, 1, 1)):
    """
    Computes Levenshtein distance between the strings s and t.
    For all i and j, dist[i,j] will contain the Levenshtein
    distance between the first i characters of s and the
    first j characters of t

    s: source, t: target
    costs: a tuple or a list with three integers (d, i, s)
           where d defines the costs for a deletion
                 i defines the costs for an insertion and
                 s defines the costs for a substitution
    return:
    H, S, D, I: correct chars, number of substitutions, number of deletions, number of insertions
    """

    rows = len(s) + 1
    cols = len(t) + 1
    deletes, inserts, substitutes = costs

    dist = [[0 for x in range(cols)] for x in range(rows)]
    H, D, S, I = 0, 0, 0, 0
    for row in range(1, rows):
        dist[row][0] = row * deletes
    for col in range(1, cols):
        dist[0][col] = col * inserts

    for col in range(1, cols):
        for row in range(1, rows):
            if s[row - 1] == t[col - 1]:
                cost = 0
            else:
                cost = substitutes
            dist[row][col] = min(dist[row - 1][col] + deletes,
                                 dist[row][col - 1] + inserts,
                                 dist[row - 1][col - 1] + cost)
    row, col = rows - 1, cols - 1
    while row != 0 or col != 0:
        if row == 0:
            I += col
            col = 0
        elif col == 0:
            D += row
            row = 0
        elif dist[row][col] == dist[row - 1][col] + deletes:
            D += 1
            row = row - 1
        elif dist[row][col] == dist[row][col - 1] + inserts:
            I += 1
            col = col - 1
        elif dist[row][col] == dist[row - 1][col - 1] + substitutes:
            S += 1
            row, col = row - 1, col - 1
        else:
            H += 1
            row, col = row - 1, col - 1
    D, I = I, D
    return H, D, S, I


def compute_acc(preds, labels, costs=(7, 7, 10)):
    # cost according to HTK: http://www.ee.columbia.edu/~dpwe/LabROSA/doc/HTKBook21/node142.html

    if not len(preds) == len(labels):
        raise ValueError('# predictions not equal to # labels')
    Ns, Ds, Ss, Is = 0, 0, 0, 0
    for i, _ in enumerate(preds):
        H, D, S, I = iterative_levenshtein(preds[i], labels[i], costs)
        Ns += len(labels[i])
        Ds += D
        Ss += S
        Is += I
    try:
        acc = 100 * (Ns - Ds - Ss - Is) / Ns
    except ZeroDivisionError:
        raise ZeroDivisionError('Empty labels')
    return acc


def beam_decode(prob, beam_size, int_to_char, char_to_int, digit=False, blank_index=0):
    # prob: [seq_len, num_labels+1], numpy array
    seqlen = len(prob)
    beam_idx = np.argsort(prob[0, :])[-beam_size:].tolist()
    beam_prob = list(map(lambda x: math.log(prob[0, x]), beam_idx))
    beam_idx = list(map(lambda x: [x], beam_idx))

    for t in range(1, seqlen):
        topk_idx = np.argsort(prob[t, :])[-beam_size:].tolist()
        topk_prob = list(map(lambda x: prob[t, x], topk_idx))
        aug_beam_prob, aug_beam_idx = [], []

        for b in range(beam_size*beam_size):
            aug_beam_prob.append(beam_prob[b//beam_size])
            aug_beam_idx.append(list(beam_idx[b//beam_size]))

        # allocate
        for b in range(beam_size*beam_size):
            i, j = b/beam_size, b % beam_size
            aug_beam_idx[b].append(topk_idx[j])
            aug_beam_prob[b] = aug_beam_prob[b]+math.log(topk_prob[j])

        # merge
        merge_beam_idx, merge_beam_prob = [], []
        for b in range(beam_size*beam_size):
            if aug_beam_idx[b][-1] == aug_beam_idx[b][-2]:
                beam, beam_prob = aug_beam_idx[b][:-1], aug_beam_prob[b]
            elif aug_beam_idx[b][-2] == blank_index:
                beam, beam_prob = aug_beam_idx[b][:-2]+[aug_beam_idx[b][-1]], aug_beam_prob[b]
            else:
                beam, beam_prob = aug_beam_idx[b], aug_beam_prob[b]
            beam_str = list(map(lambda x: int_to_char[x], beam))
            if beam_str not in merge_beam_idx:
                merge_beam_idx.append(beam_str)
                merge_beam_prob.append(beam_prob)
            else:
                idx = merge_beam_idx.index(beam_str)
                merge_beam_prob[idx] = np.logaddexp(merge_beam_prob[idx], beam_prob)

        ntopk_idx = np.argsort(np.array(merge_beam_prob))[-beam_size:].tolist()
        beam_idx = list(map(lambda x: merge_beam_idx[x], ntopk_idx))
        for b in range(len(beam_idx)):
            beam_idx[b] = list(map(lambda x: char_to_int[x], beam_idx[b]))
        beam_prob = list(map(lambda x: merge_beam_prob[x], ntopk_idx))

    if blank_index in beam_idx[-1]:
        pred = beam_idx[-1][:-1]
    else:
        pred = beam_idx[-1]

    if digit is False:
        pred = list(map(lambda x: int_to_char[x], pred))

    return pred


def frobenius_norm(img1, img2):
    """Calculates the average pixel squared distance between 2 gray scale images."""
    return np.power(img2 - img1, 2).sum() / np.prod(img1.shape)


def get_optical_flows(frames, img_size):
    """Calculates the optical flows for a sequence of image frames in gray scale.
    Returns the magnitude of the flows.

    :param frames: a list of images in gray scale.
    :param img_size: the image input size of the CNN.
    :return a list of optical flow matrices of the same length as `frames`.
    """

    # optical flows can be computed in smaller resolution w/o harming performance
    frames = [cv2.resize(frames[i], (img_size // 2, img_size // 2)) for i in range(len(frames))]
    frame1 = frames[0]

    # insert a black image to obtain a list with the same length as `frames`
    flow_mag = np.zeros(frame1.shape[:2], dtype=np.uint8)
    flows = [flow_mag]

    for i in range(1, len(frames)):
        frame2 = frames[i]

        # use the Frobenius norm to detect still frames
        if frobenius_norm(frame1, frame2) > 1:  # manually tuned at training time
            opt_flow = cv2.calcOpticalFlowFarneback(frame1, frame2, None, 0.5, 3, 15, 3, 5, 1.2, 0)
            mag, _ = cv2.cartToPolar(opt_flow[..., 0], opt_flow[..., 1])

            if (mag.max() - mag.min()) == 0:
                flow_mag = np.zeros_like(mag)
            elif mag.max() == np.inf:
                mag = np.nan_to_num(mag, copy=True, posinf=mag.min())
                flow_mag = (mag - mag.min()) / float(mag.max() - mag.min())
            else:
                flow_mag = (mag - mag.min()) / float(mag.max() - mag.min())

        # copy the new flow's magnitude or the previous one if a still frame was detected
        flows.append(flow_mag)
        frame1 = frame2
    return flows


def get_attention_priors(flows, window_size=3):
    """Priors are a moving average of optical flows of the
    requested `window_size` centered on the current frame."""

    # prepend & append black images to obtain a list with the same length as `flows`
    flows = [np.zeros_like(flows[0]) for _ in range(window_size//2)] + flows + \
            [np.zeros_like(flows[0]) for _ in range(window_size//2)]
    flows = np.stack(flows, axis=0)

    priors = []
    for i in range(len(flows) - 2*(window_size//2)):
        prior = 255 * np.mean(flows[i: i + window_size], axis=0)
        priors.append(prior.astype('uint8'))
    return priors


def get_attention_maps(priors, map_size):
    """Resize priors to obtain spatial attention maps of the same size
    as the output feature maps of the CNN."""

    maps = [cv2.resize(prior, (map_size, map_size)).astype(np.float32) for prior in priors]
    maps = torch.from_numpy(np.asarray(maps)).unsqueeze(0)
    return maps


def center_crop(img, target_shape):
        """
        Returns a center crop of the provided image.

        :param img: the image to crop.
        :param target_shape: the dimensions of the crop.
        :return the cropped image
        """
        h, w = target_shape
        y, x = img.shape[:2]
        start_y = max(0, y // 2 - (h // 2))
        start_x = max(0, x // 2 - (w // 2))
        return img[start_y:start_y + h, start_x:start_x + w]


def preprocess_video(video, transform, img_size):
    cap = cv2.VideoCapture(video)
    imgs, grays = [], []

    while cap.isOpened():
        ret, frame = cap.read()
        
        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #rgb = center_crop(rgb, (700, 700))
        rgb = cv2.resize(rgb, (img_size, img_size))
        gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
        imgs.append(rgb)
        grays.append(gray)

    cap.release()

    imgs, gray = np.stack(imgs), np.stack(grays)[..., np.newaxis]
    sample = {'imgs': imgs, 'gray': gray}
    sample = transform(sample)
    sample['imgs'] = sample['imgs'][None, ...]
    sample['gray'] = sample['gray'][None, ...]
    return sample