import time
BGRAY = "\033[1;90m"
YELLOW = "\033[0;93m"
BROWN = "\033[38;5;94m"
BBLUE = "\033[1;94m"
RED = "\033[0;91m"
CIAN = "\033[0;96m"
OR = "\033[38;5;214m"
PURPLE = "\033[0;95m"
BGREEN = "\033[1;92m"

PHA = "\033[1;107;94m"
RES = "\033[0m"
EYE = "\033[30;47m"


def print_banner():
    art = f"""
    █████████      ████████████   ████████████    ████████████
    █████████      ████████████   ████████████    ████████████
        █████             █████          █████         ███████
        █████      ████████████   ████████████        ███████
        █████              ████           ████       ███████
    ████████████   ████████████   ████████████      ███████
    ████████████   ████████████   ████████████     ███████{BGRAY} Rabat"""

    print(art)

def print_final_art():
    print()

    print(
        f" {YELLOW}▄████▄    {BGREEN}Ybaddi  "
        f"{BBLUE}▄█████▄  "
        f"{RED}▄█████▄  "
        f"{CIAN}▄█████▄  "
        f"{OR}▄█████▄  "
        f"{PURPLE}▄█████▄"
    )

    print(
        f"{YELLOW}████▄███     "
        f"{BROWN}▄▄    "
        f"{BBLUE}██{PHA}▄{RES}{BBLUE}█{PHA}▄{RES}{BBLUE}██  "
        f"{RED}█{EYE}▄ {RED}█{EYE}▄ {RED}█  "
        f"{CIAN}█{EYE} ▄{RES}{CIAN}█{EYE} ▄{RES}{CIAN}█{RES}  "
        f"{OR}█{EYE} ▀{OR}█{EYE} ▀{RES}{OR}█  "
        f"{PURPLE}█{EYE}▀ {PURPLE}█{EYE}▀ {RES}{PURPLE}█"
    )

    print(
        f"{YELLOW}████▄        "
        f"{BROWN}▀▀    "
        f"{BBLUE}█{PHA}▀▄▀▄▀{RES}{BBLUE}█{RES}  "
        f"{RED}███████  "
        f"{CIAN}███████  "
        f"{OR}███████  "
        f"{PURPLE}███████"
    )

    print(
        f"{YELLOW} ▀████▀   "
        f"{BGREEN}Ichtioui "
        f"{BBLUE}█▀█▀█▀█  "
        f"{RED}█▀█▀█▀█  "
        f"{CIAN}█▀█▀█▀█  "
        f"{OR}█▀█▀█▀█  "
        f"{PURPLE}█▀█▀█▀█"
    )

def simple_progress(total=50, delay=0.01):
    print()
    for i in range(total + 1):
        percent = int((i / total) * 100)
        filled = int((i / total) * 50)
        bar = "█" * filled + "-" * (50 - filled)
        print(f"\r{BGRAY}Loading: [{bar}] {percent}%{RES}", end="", flush=True)
        time.sleep(delay)
    print()
