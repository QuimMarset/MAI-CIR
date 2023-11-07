import re
import os
from functools import partial
from kivy.uix.recycleview import RecycleView
from kivy.lang import Builder
from constants import kv_files_path
from application.widgets.video_popup import VideoPopup



def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(data, key=alphanum_key)


class CustomRecycleView(RecycleView):
    Builder.load_file(os.path.join(kv_files_path, 'recycle_view.kv'))

    def __init__(self, sign_visual_dict, **kwargs):
        super().__init__(**kwargs)
        signs = list(sign_visual_dict.keys())
        sorted_signs = sorted_alphanumeric(signs)

        self.data = [
            {
                'text': sign, 
                'video': sign_visual_dict[sign],
                'on_release': partial(self.button_callback, sign_visual_dict[sign])
            } 
            for sign in sorted_signs
        ]


    def button_callback(self, video_path):
        VideoPopup(video_source=video_path).open()
