import arcade
import threading
from client import Client
from os import path
from constants import *
from setting import Setting
from alert import Alert

DIR = path.dirname(path.abspath(__file__))

class Game(arcade.View):
    def __init__(self, socket, thread, window: arcade.Window = None):
        super().__init__(window)
        # self.client_socket = Client()
        # self.client_socket.connect_to_server()
        # threading.Thread(target=self.client_socket.receive_data).start()
        self.thread = thread
        self.client_socket = socket
        self.board = None

        # State
        self.current_player = X_PATTERN
        self.is_locked = False
        self.is_game_over = False
        self.setting_popup_visible = False
        self.alert_popup_visible = False
        self.is_restart = False
        self.winner = None

        # Media
        self.video = None
        self.x_sound = None
        self.o_sound = None

        # Board game
        self.x = None
        self.o = None
        self.background = None

        # Screen
        self.setting = Setting()
        self.alert = Alert()

    def setup(self):
        self.board = [[' ' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

        # Load media
        self.x_sound = arcade.load_sound(f"{DIR}\\assets\\sounds\\rollover1.ogg")
        self.o_sound = arcade.load_sound(f"{DIR}\\assets\\sounds\\rollover2.ogg")

        # Load image
        self.x = arcade.load_texture(f"{DIR}\\assets\\images\\common\\cross.png")
        self.o = arcade.load_texture(f"{DIR}\\assets\\images\\common\\target.png")

    def on_show_view(self):
        self.setup()
        self.setting.setup()
        self.alert.setup()

    def on_draw(self):
        arcade.start_render()
        self.draw_board()
        self.draw_xo()
        if self.setting_popup_visible:
            self.setting.draw_setting()
        if self.alert_popup_visible:
            self.alert.draw_alert(self.winner)

    def draw_board(self):
        for i in range(1, BOARD_SIZE):
            # Draw horizontal lines
            arcade.draw_line(0, i * SQUARE_SIZE, SCREEN_WIDTH, i * SQUARE_SIZE, arcade.color.WHITE_SMOKE, LINE_WIDTH)

            # Draw vertical lines
            arcade.draw_line(i * SQUARE_SIZE, 0, i * SQUARE_SIZE, SCREEN_HEIGHT, arcade.color.WHITE_SMOKE, LINE_WIDTH)

    def draw_xo(self):
        for row in range(BOARD_SIZE):
            for column in range(BOARD_SIZE):
                cell_value = self.board[row][column]
                if cell_value == X_PATTERN:
                    self.draw_x(row, column)
                elif cell_value == O_PATTERN:
                    self.draw_o(row, column)

    def draw_x(self, row, column):
        x = column * SQUARE_SIZE
        y = row * SQUARE_SIZE
        arcade.draw_lrwh_rectangle_textured(x + CELL_PADDING, y + CELL_PADDING, SQUARE_SIZE - 2 * CELL_PADDING, SQUARE_SIZE - 2 * CELL_PADDING, self.x)

    def draw_o(self, row, column):
        x = column * SQUARE_SIZE
        y = row * SQUARE_SIZE
        arcade.draw_lrwh_rectangle_textured(x + CELL_PADDING, y + CELL_PADDING, SQUARE_SIZE - 2 * CELL_PADDING, SQUARE_SIZE - 2 * CELL_PADDING, self.o)

    def on_mouse_press(self, x, y, button, modifiers):
        if not self.setting_popup_visible and not self.alert_popup_visible:
            if self.is_locked:
                return
        
            column = x // SQUARE_SIZE
            row = y // SQUARE_SIZE

            if self.board[row][column] == ' ':
                self.board[row][column] = self.current_player
                self.is_game_over = self.game_over(self.current_player)
                self.client_socket.send_data({
                    "board": self.board, 
                    "player": self.current_player, 
                    "next_player": self.switch_player(), 
                    "is_game_over": self.is_game_over,
                    "is_new_response": True,
                    "is_restart": False
                })
                self.pick_sound(self.current_player)
                self.on_draw()
                self.is_locked = True
        elif self.setting_popup_visible:
            self.setting.control(x, y, self)
        elif self.alert_popup_visible:
            self.alert.control(x, y, self)

    def switch_player(self):
        return O_PATTERN if self.current_player == X_PATTERN else X_PATTERN

    def pick_sound(self, player):
        if player == X_PATTERN:
            arcade.play_sound(self.x_sound)
        else:
            arcade.play_sound(self.o_sound)

    def game_over(self, player):
        if self.check_win():
            self.toggle_alert_popup()
            self.winner = player
            print(f"Win {player}")
            return True
        elif self.check_tie():
            self.toggle_alert_popup()
            self.winner = None
            print("It's a tie!")
            return True
        return False

    def check_win(self):
        for row in range(BOARD_SIZE):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] != ' ':
                return True

        for col in range(BOARD_SIZE):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != ' ':
                return True

        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            return True

        return False

    def check_tie(self):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.board[row][col] == ' ':
                    return False
        return True
    
    def on_update(self, delta_time: float):
        data = self.client_socket.get_data()
        if self.client_socket and data:
            self.change_game_state(data)
        if self.is_restart:
            self.restart()
            self.is_restart = not self.is_restart

    def change_game_state(self, data):
        self.board = data['board']
        self.current_player = data['next_player']
        if data['is_new_response']:
            self.pick_sound(data['player'])
            self.is_locked = False
            data['is_new_response'] = False
        if data['is_game_over']:
            self.game_over(data['player'])
            self.is_game_over = data['is_game_over']
            self.is_locked = True
            data['is_game_over'] = False
        if data['is_restart']:
            self.alert_popup_visible = False
            
    def restart(self):
        self.client_socket.set_data(None)
        self.window.show_view(Game(self.client_socket, self.thread))
        self.setup()
        data = {
            "board": self.board, 
            "player": None, 
            "next_player": X_PATTERN, 
            "is_game_over": False,
            "is_new_response": True,
            "is_restart": True
        }
        self.client_socket.send_data(data)

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.SPACE:  # Replace with your desired key
            self.toggle_setting_popup()
            if self.setting_popup_visible and self.alert_popup_visible:
                self.toggle_alert_popup()
            if not self.setting_popup_visible and self.is_game_over:
                self.toggle_alert_popup()

    def toggle_setting_popup(self):
        self.setting_popup_visible = not self.setting_popup_visible

    def toggle_alert_popup(self):
        self.alert_popup_visible = not self.alert_popup_visible

def main():
    window = Game()
    window.setup()
    window.run()

if __name__ == "__main__":
    main()
