from os.path import join
from kivy.uix.videoplayer import VideoPlayer
from constants import icons_path


class CustomVideoPlayer(VideoPlayer):
    image_play = join(icons_path, 'play_video.png')
    image_pause = join(icons_path, 'pause_video.png')
    image_stop = join(icons_path, 'stop_video.png')
    image_volumehigh = join(icons_path, 'volume_high.png')
    image_volumemuted = join(icons_path, 'volume_muted.png')
    allow_fullscreen = False
    allow_stretch = True
