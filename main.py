import sys
from gui.graphic import Gui
from parsing.parsing import Config


def main():
    if len(sys.argv) != 2:
        raise ValueError("any Error")

    obj = Config(sys.argv[1])
    gui = Gui()

if __name__ == "__main__":
    main()
