from torchvision import transforms
from detectors.alphabet.mictranet.mictranet import MiCTRANet, init_lstm_hidden
from detectors.alphabet.mictranet.chicago_fs_wild import ToTensor, Normalize
from constants import letters_model_path
from detectors.alphabet.constants import *
from detectors.alphabet.mictranet.utils import *


class AlphabetDetector:


    def __init__(self):
        self.init_device()
        self.__init_class_dictionaries()
        self.__create_model()
        self.transform = transforms.Compose([ToTensor(), Normalize(img_mean, img_std)])

    
    def init_device(self):
        self.device = torch.device(
            'cuda:0' if torch.cuda.is_available() 
            else 'cpu')


    def predict_alphabet_sign(self, video_path):
        #torch.cuda.synchronize(self.device)

        img_size = img_shape[0]
        sample = preprocess_video(video_path, self.transform, img_size)
        imgs = sample['imgs']  # [B, L, C, H, W]

        flows = get_optical_flows(sample['gray'].numpy()[0], img_size)
        priors = get_attention_priors(flows)  # temporal averaging of optical flows
        maps = get_attention_maps(priors, map_size)  # resize priors to CNN features maps size

        imgs = imgs.to(self.device)
        maps = maps.to(self.device)

        with torch.no_grad():
            h0 = init_lstm_hidden(len(imgs), hidden_size, device=self.device)
            probs = self.model(imgs, h0, maps)[0].cpu().numpy()[0]

        #torch.cuda.synchronize(self.device)
        predictions = beam_decode(probs, beam_size, self.index_to_char, self.char_to_index, digit=False)
        return predictions


    def __create_model(self):
        self.model = MiCTRANet(backbone='resnet34',
            hidden_size=hidden_size,
            attn_size=512,
            output_size=32,
            mode='offline')

        self.model.load_state_dict(torch.load(letters_model_path))
        self.model.to(self.device)
        self.model.eval()
    

    def __init_class_dictionaries(self):
        self.char_to_index, self.index_to_char, self.characters = get_ctc_vocab(char_list)


    def __init_device(self):
        self.device = torch.device("cpu")
        if torch.cuda.is_available():
            self.device = torch.device("cuda")