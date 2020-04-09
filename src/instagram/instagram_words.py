from settings import INSTA_DOCUMENT_ROOT


def main():
    words = {}
    with open(INSTA_DOCUMENT_ROOT / "instagram_parsed.txt", encoding="utf-8") as f:
        for line in f:
            for word in line.split():
                try:
                    words[word] += 1
                except KeyError:
                    words[word] = 1

    with open(INSTA_DOCUMENT_ROOT / "instagram_words.txt", "w", encoding="utf-8") as w:
        for k, v in words.items():
            w.write(f"{k}\t{v}\n")


if __name__ == "__main__":
    main()
