import arcade
from constants import *

class Dialog(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Tic Tac Toe")
        self.popup_visible = False
        self.panel = 

    def setup(self):
        

    def on_draw(self):
        arcade.start_render()
        arcade.set_background_color(arcade.color.WHITE)
        
        # Draw game elements

        if self.popup_visible:
            self.draw_background()
            self.draw_popup()
    
    def draw_background(self):
        arcade.draw_lrtb_rectangle_filled(0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, (0, 0, 0, 100))

    def draw_popup(self):
        popup_x = (SCREEN_WIDTH - POPUP_WIDTH) / 2
        popup_y = (SCREEN_HEIGHT - POPUP_HEIGHT) / 2
        arcade.draw_rectangle_filled(popup_x, popup_y, POPUP_WIDTH, POPUP_HEIGHT, arcade.color.LIGHT_GRAY)

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.SPACE:  # Replace with your desired key
            self.toggle_popup()

    def toggle_popup(self):
        self.popup_visible = not self.popup_visible

def main():
    game = Dialog()
    arcade.run()

if __name__ == "__main__":
    main()