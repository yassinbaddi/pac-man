import sys
from gui.graphic import Gui
from gui.banner import simple_progress, print_banner, print_final_art
from parsing.parsing import Config


def main():
    simple_progress()
    if len(sys.argv) != 2:
        raise ValueError("any Error")
    obj = Config(sys.argv[1])
    gui = Gui()
    print_banner()
    print_final_art()

if __name__ == "__main__":
    main()
