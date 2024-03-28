import arcade
import threading
from os import path
from client import Client
from constants import *
from common import Button
from game import Game

DIR = path.dirname(path.abspath(__file__))

class MainMenu(arcade.View):
    def __init__(self, window: arcade.Window = None):
        super().__init__(window)
        self.menu = None
        self.btn_start = None
        self.btn_exit = None

    def on_show_view(self):
        # Init
        btn_start_texture = arcade.load_texture(f"{DIR}/assets/images/common/blue_button/blue_button02.png")
        btn_exit_texture = arcade.load_texture(f"{DIR}/assets/images/common/red_button/red_button01.png")

        # Premiere
        arcade.set_background_color(arcade.color.WHITE)
        self.menu = arcade.load_texture(f"{DIR}/assets/images/menu/blue_panel.png")
        self.btn_start = Button("Start", btn_start_texture, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + BUTTON_HEIGHT // 2 + GAP_BETWEEN_BUTTONS, 180, 40)
        self.btn_exit = Button("Exit", btn_exit_texture, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - GAP_BETWEEN_BUTTONS, 180, 40)

    def on_draw(self):
        self.clear()
        arcade.draw_text("Tic Tac Toe", SCREEN_WIDTH // 2, 2 * (SCREEN_HEIGHT // 3) + (SCREEN_HEIGHT // 6),
            arcade.color.BLACK, 30, anchor_x="center")
        self.draw_panel()
        self.btn_start.draw()
        self.btn_exit.draw()

    def draw_panel(self):
        x = SCREEN_WIDTH // 2
        y = SCREEN_HEIGHT // 2
        arcade.draw_lrwh_rectangle_textured(x - MENU_WIDTH // 2, y - MENU_HEIGHT // 2, MENU_WIDTH, MENU_HEIGHT, self.menu)
    
    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if (x >= self.btn_start.start_btn_x and x <= self.btn_start.end_btn_x) and (y >= self.btn_start.start_btn_y and y <= self.btn_start.end_btn_y):
            client_socket = Client()
            client_socket.connect_to_server()
            thread = threading.Thread(target=client_socket.receive_data)
            thread.start()
            self.window.show_view(Game(client_socket, thread))
            print("start")
        if (x >= self.btn_exit.start_btn_x and x <= self.btn_exit.end_btn_x) and (y >= self.btn_exit.start_btn_y and y <= self.btn_exit.end_btn_y):
            print("exit")
            self.window.close()

