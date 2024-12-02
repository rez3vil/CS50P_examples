import sys
import random
from pyfiglet import Figlet

def main():
    if len(sys.argv) not in [1, 3]:
        sys.exit("Usage: figlet.py or figlet.py -f font_name or figlet.py --font font_name")
    
    figlet = Figlet()

    if len(sys.argv) == 3:
        if sys.argv[1] in ["-f", "--font"]:
            font = sys.argv[2]
            if font in figlet.getFonts():
                figlet.setFont(font=font)
            else:
                sys.exit("Error: font_name is not available in the library")
        else:
            sys.exit("Error: Invalid first argument.. it should be -f or --font")
    else:
        figlet.setFont(font=random.choice(figlet.getFonts()))

    user = input("Input: ")
    
    print("Output: \n" + figlet.renderText(user))

if __name__ == "__main__":
    main()
