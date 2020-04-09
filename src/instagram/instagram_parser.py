import json
import re

from settings import INSTA_DOCUMENT_ROOT


def main():
    complete_hangul = r"[가-힣]+"
    partial_hangul = r"[ㄱ-ㅣ]+"
    english = r"[a-zA-Z]+"
    number = r"[0-9]+"
    # emoji = r"[^\w\s,.@:;)!'\"]+"

    hashtag = re.compile(r"#[\w]+")
    insta_id = re.compile(r"@[a-zA-Z0-9_.]+")

    compiled = re.compile("|".join([complete_hangul, partial_hangul, english, number]))
    with open(
        INSTA_DOCUMENT_ROOT / "/instagram_parsed.txt", "w", encoding="utf-8"
    ) as w:
        with open(INSTA_DOCUMENT_ROOT / "instagram.txt", encoding="utf-8") as f:
            for line in f:
                line = json.loads(line.strip())
                if line.startswith("Image may contain"):
                    continue

                line = insta_id.sub(" ", line)
                line = hashtag.sub(" ", line)

                words = compiled.findall(line)
                if not words:
                    continue

                for word in words:
                    w.write(word)
                    w.write(" ")
                w.write("\n")


if __name__ == "__main__":
    main()
