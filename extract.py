import pathlib


def main():
    parsed = pathlib.Path('parsed_files')
    for child in parsed.iterdir():
        if 'txt.text' in str(child):
            with open(child, encoding='utf-8') as f:
                print(f.readline())


if __name__ == "__main__":
    main()
