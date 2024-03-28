import arcade
from constants import *
from main_menu import MainMenu

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.show_view(MainMenu())
    window.run()

if __name__ == "__main__":
    main()
