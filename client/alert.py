import arcade
from os import path
from constants import *
from common import Button

DIR = path.dirname(path.abspath(__file__))

class Alert():
    def __init__(self):
        self.panel = None
        self.btn_again = None

    def setup(self):
        popup_x = (SCREEN_WIDTH - POPUP_WIDTH) // 2
        popup_y = (SCREEN_HEIGHT - POPUP_HEIGHT) // 2
        self.panel = arcade.load_texture(f"{DIR}/assets/images/dialog/glassPanel.png")
        self.btn_again_texture = arcade.load_texture(f"{DIR}/assets/images/common/blue_button/blue_button02.png")
        self.btn_again = Button("Again", self.btn_again_texture, popup_x + POPUP_WIDTH // 2, popup_y + POPUP_HEIGHT // 2, 100, 50)
    
    def draw_alert(self, data):
        self.draw_background()
        self.draw_popup(data)

    def draw_background(self):
        arcade.draw_lrtb_rectangle_filled(0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, (0, 0, 0, 50))

    def draw_popup(self, data):
        popup_x = (SCREEN_WIDTH - POPUP_WIDTH) // 2
        popup_y = (SCREEN_HEIGHT - POPUP_HEIGHT) // 2
        arcade.draw_lrwh_rectangle_textured(popup_x, popup_y, POPUP_WIDTH, POPUP_HEIGHT, self.panel)
        arcade.draw_text(self.pick_content(data), popup_x + 10, popup_y + POPUP_HEIGHT - 30, arcade.color.BLACK, 30, width=POPUP_WIDTH - 20, align="center", anchor_x="left", anchor_y="top")
        self.btn_again.draw()
    
    
    def pick_content(self, data):
        if data != None:
            return f"{'X' if data == X_PATTERN else 'O'} is winner!"
        return "Draw!"
        
    def control(self, x: int, y: int, parent_view):
        if (x >= self.btn_again.start_btn_x and x <= self.btn_again.end_btn_x) and (y >= self.btn_again.start_btn_y and y <= self.btn_again.end_btn_y):
            parent_view.is_restart = True

def main():
    game = Alert()
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()