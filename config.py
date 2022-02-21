from pathlib import Path

root = Path(__file__).parent

PATHS = {
    "LOGS": root / "src/_logging/logs.txt"
}

COLORS = {
    "DARK_GRAY": '#65696B',
    "LIGHT_GRAY": '#C4C5BF',
    "BLUE": '#0CA8F6',
    "DARK_BLUE": '#4204CC',
    "WHITE": '#FFFFFF',
    "BLACK": '#000000',
    "RED": '#F22810',
    "YELLOW":'#F7E806',
    "PINK": '#F50BED',
    "LIGHT_GREEN": '#05F50E',
    "PURPLE": '#BF01FB',
}

def main():
    print(root)


if __name__ == "__main__":
    main()
