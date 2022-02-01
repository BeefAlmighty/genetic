from pathlib import Path

root = Path(__file__).parent

PATHS = {
    "LOGS": root / "src/_logging/logs.txt"
}

def main():
    print(root)


if __name__ == "__main__":
    main()
