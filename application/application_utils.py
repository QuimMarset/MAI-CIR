from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from constants import maroon_color, medium_font_size



def crete_markup_text(text, font_size, text_color):
    return f'[size={font_size}][color={text_color}][b]{text}[/b][/color][/size]'


def create_grid_layout(rows=1, cols=1, size_hint=(1, 1), spacing='20dp', padding='20dp'):
    return GridLayout(rows=rows, cols=cols, size_hint=size_hint, 
        padding=padding, spacing=spacing)


def create_label(text, font_size=medium_font_size, text_color=maroon_color, size_hint=(1, 1)):
    return Label(text=text, bold=True, font_size=font_size, color=text_color, size_hint=size_hint)
