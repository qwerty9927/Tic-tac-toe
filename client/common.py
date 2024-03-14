import arcade
from constants import *

class Button:
    def __init__(self, text, texture, x, y, button_width, button_height):
        self.text = text
        self.x = x
        self.y = y
        self.texture = texture
        self.start_btn_x = self.x - button_width // 2
        self.end_btn_x = self.x + button_width // 2
        self.start_btn_y = self.y - button_height // 2
        self.end_btn_y = self.y + button_height // 2
        self.button_width = button_width
        self.button_height = button_height

    def draw(self):
        arcade.draw_lrwh_rectangle_textured(self.x - self.button_width // 2, self.y - self.button_height // 2, self.button_width, self.button_height, self.texture)
        arcade.draw_text(self.text, self.x, self.y, arcade.color.BLACK, font_size=16, anchor_x="center", anchor_y="center")
    