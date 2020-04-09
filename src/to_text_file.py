import json
import pathlib
import re

file_template = re.compile(r"\[\[(파일|분류):(.+?)\]\]")
youtube = re.compile(r"\[youtube\((.+?)\)\]", re.IGNORECASE)

template = re.compile(r"\[include\(틀(.+?)\)\]", re.IGNORECASE)

link_regex = re.compile(r"\[\[([^|]+?)(\|(.+?))?\]\]")
curly = re.compile(r"{{{(.+?)}}}", re.DOTALL)
header5 = re.compile(r"=====(.+?)=====")
header4 = re.compile(r"====(.+?)====")
header3 = re.compile(r"===(.+?)===")
header2 = re.compile(r"==(.+?)==")
header1 = re.compile(r"=(.+?)=")
three_quotes = re.compile(r"'''(.*?)'''")
double_quotes = re.compile(r"''(.*?)''")
single_quote = re.compile(r"'(.*?)'")
strike_1 = re.compile(r"~~(.+?)~~")
strike_2 = re.compile(r"--(.+?)--")
strike_3 = re.compile(r"----")
parenthesis = re.compile(r"\((.+?)\)")
square_bracket_1 = re.compile(r"『(.+?)』")
square_bracket_2 = re.compile(r"【(.+?)】")
square_bracket_3 = re.compile(r"「(.+?)」")
footnote = re.compile(r"\[\*(.+?)\]")
table = re.compile(r"\|\|(.+)\|\|$")
iframe = re.compile(r"<iframe(.*?)/iframe>", re.DOTALL)
curly_2 = re.compile(r"{{\|(.+?)\|}}", re.DOTALL)

to_space = re.compile(r"[\[\]*\\/·_\-+×:]")
delete_char = re.compile(r'[.?!\'",]')


def repl(m):
    if m.group(3):
        return m.group(3)
    candidate = m.group(1)
    return candidate


def definite_parser(text):
    text = file_template.sub("", text)
    text = template.sub("", text)
    text = youtube.sub("", text)
    text = header5.sub("", text)
    text = header4.sub("", text)
    text = header3.sub("", text)
    text = header2.sub("", text)
    text = header1.sub("", text)
    text = strike_1.sub("", text)
    text = strike_2.sub("", text)
    text = strike_3.sub("", text)
    text = iframe.sub("", text)
    text = curly_2.sub("", text)
    text = link_regex.sub(repl, text)
    text = three_quotes.sub(r"\1", text)
    text = double_quotes.sub(r"\1", text)
    text = footnote.sub("", text)
    return text


def text_parser(text):
    text = table.sub("", text)
    text = square_bracket_1.sub(r"\1", text)
    text = square_bracket_2.sub(r"\1", text)
    text = square_bracket_3.sub(r"\1", text)

    return text


def main():
    document_path = pathlib.Path("document")

    for filepath in document_path.glob("*.json"):
        with open(str(filepath), encoding="utf-8") as f:
            # with open(document_path / f'original_${filepath.name}.txt', 'w', encoding='utf-8') as orig:
            #     with open(document_path / 'text.txt', 'w', encoding='utf-8') as w:
            with open(
                document_path / f"parsed_{filepath.name}.txt", "w", encoding="utf-8"
            ) as parsed:
                for doc in f:
                    data = json.loads(doc)

                    text = data["text"]
                    definite = definite_parser(text)

                    for line in definite.split("\n"):
                        # orig.write(line)
                        # orig.write('\n')
                        # w.write(definite)
                        # w.write('\n')
                        cleaned_text = text_parser(line).strip()
                        if cleaned_text:
                            parsed.write(cleaned_text)
                            parsed.write("\n")

                    # break
                    parsed.write("\n")


if __name__ == "__main__":
    main()
