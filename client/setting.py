import arcade
from os import path
from constants import *
from common import Button

DIR = path.dirname(path.abspath(__file__))

BUTTON_WIDTH = 100
BUTTON_HEIGHT = 50
BUTTON_MARGIN = 20

class Setting():
    
    def __init__(self):
        self.panel = None
        self.btn_restart = None
        self.btn_exit = None

    def setup(self):
        popup_y = (SCREEN_HEIGHT - POPUP_HEIGHT) // 2
        button_x1 = SCREEN_WIDTH // 2 - BUTTON_WIDTH + BUTTON_MARGIN * 2
        button_y = popup_y + POPUP_HEIGHT // 4
        button_x2 = button_x1 + BUTTON_WIDTH + BUTTON_MARGIN

        self.panel = arcade.load_texture(f"{DIR}/assets/images/dialog/metalPanel_blueCorner.png")
        btn_restart_texture = arcade.load_texture(f"{DIR}/assets/images/common/blue_button/blue_button02.png")
        btn_exit_texture = arcade.load_texture(f"{DIR}/assets/images/common/red_button/red_button01.png")
        self.btn_restart = Button("Restart", btn_restart_texture, button_x1, button_y, 100, 50)
        self.btn_exit = Button("Exit", btn_exit_texture, button_x2, button_y, 100, 50)

    def draw_setting(self):
        # Draw game elements
        self.draw_background()
        self.draw_popup()
    
    def draw_background(self):
        arcade.draw_lrtb_rectangle_filled(0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, (0, 0, 0, 100))

    def draw_popup(self):
        popup_x = (SCREEN_WIDTH - POPUP_WIDTH) // 2
        popup_y = (SCREEN_HEIGHT - POPUP_HEIGHT) // 2
        arcade.draw_lrwh_rectangle_textured(popup_x, popup_y, POPUP_WIDTH, POPUP_HEIGHT, self.panel)
        arcade.draw_text("Setting", popup_x + 10, popup_y + POPUP_HEIGHT - 30, arcade.color.BLACK, 30, width=POPUP_WIDTH - 20, align="center", anchor_x="left", anchor_y="top")
        self.btn_restart.draw()
        self.btn_exit.draw()

    def control(self, x: int, y: int, parent_view):
        if (x >= self.btn_restart.start_btn_x and x <= self.btn_restart.end_btn_x) and (y >= self.btn_restart.start_btn_y and y <= self.btn_restart.end_btn_y):
            parent_view.is_restart = True
        if (x >= self.btn_exit.start_btn_x and x <= self.btn_exit.end_btn_x) and (y >= self.btn_exit.start_btn_y and y <= self.btn_exit.end_btn_y):
            # parent_view.thread.exit()
            parent_view.client_socket.close_connection()
            parent_view.window.close()

def main():
    game = Setting()
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()