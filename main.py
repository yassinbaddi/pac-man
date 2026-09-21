import sys
from GUI.graphic import any_fun

def  main():
    if len(sys.argv) != 2:
        raise ValueError("any Error")

    any_fun()



if __name__ == "__main__":
    main()
