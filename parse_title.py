import glob
import pathlib
import re
import typing
from multiprocessing import Pool

import tqdm

base_dir = pathlib.Path('parsed_files/word_count')

link_regex = re.compile(r"\[\[([^|]+?)(\|(.+?))?\]\]")
curly = re.compile(r"{{{(.)+?\}\}\}")
parenthesis = re.compile(r"\((.+?)\)")
three_quotes = re.compile(r"'''(.+?)'''")
single_quote = re.compile(r"'(.+?)'")
strike = re.compile(r"~~(.+?)~~")
to_space = re.compile(r'[\[\]*\\/·_\-+×:]')
square_bracket_1 = re.compile(r'『(.+?)』')
square_bracket_2 = re.compile(r'【(.+?)】')
bracket = re.compile(r'\[(.+?)\]')
delete_char = re.compile(r'[.?!\'",]')


def split_word_parallel(file_path, verbose=False):
    file_path = pathlib.Path(file_path)
    word_count_map = split_word(file_path, verbose)

    with open(base_dir / file_path.stem, 'w', encoding='utf-8') as w:
        for k, v in word_count_map.items():
            w.write(k)
            w.write('\t')
            w.write(str(v))
            w.write('\n')


def valid_word(w):
    if w.startswith('#'):
        return False
    if not w:
        return False

    return True


def repl(m):
    if m.group(3):
        return m.group(3)
    candidate = m.group(1)
    if candidate.startswith("파일") or \
            candidate.startswith("분류"):
        return ""

    return m.group(1)


def valid_line(w):
    if not w:
        return False
    if w.startswith("||") or w.startswith("##") or w.startswith("템플릿:") or w.startswith("==") or \
            w.startswith(" *상위 문서") or w.startswith(" * 상위 문서") or w.startswith(">") or \
            w.startswith("{{{#!") or w.startswith("}}}") or w.startswith("<iframe"):
        return False
    return True


def strip_line(w):
    if w.startswith("1."):
        w = w[2:]
    w = parenthesis.sub(r'', w)
    w = strike.sub(r' ', w)
    w = curly.sub(' ', w)
    w = link_regex.sub(repl, w)
    w = three_quotes.sub(r' \1 ', w)
    w = single_quote.sub(r'\1', w)
    w = square_bracket_1.sub(r'\1', w)
    w = square_bracket_2.sub(r'\1', w)
    w = bracket.sub(r'', w)

    return to_space.sub(' ', w)


def strip_word(w):
    w = delete_char.sub('', w).strip()
    return w


def split_word(file_path, verbose=False) -> typing.Dict[str, int]:
    word_count_map = {}

    with open(str(file_path) + '_parsed', 'w', encoding='utf-8') as w:
        with open(file_path, encoding='utf-8') as f:
            for line in f:
                line = line.strip()

                if valid_line(line):
                    word_list = strip_line(line).split()
                    if word_list:

                        word_list = [strip_word(w) for w in word_list if valid_word(w)]
                        if verbose:
                            print(line)
                            print(word_list)
                            input()
                        for word in word_list:
                            w.write(word)
                            w.write(' ')
                            if word in word_count_map:
                                word_count_map[word] += 1
                            else:
                                word_count_map[word] = 1
                        w.write('\n')
    return word_count_map


def debug(file):
    split_word_parallel(file, verbose=True)


def main():
    title_glob = 'parsed_files/*_title.txt'
    text_glob = 'parsed_files/*.text'
    title_files = glob.glob(title_glob)
    text_files = glob.glob(text_glob)
    base_dir.mkdir(parents=True, exist_ok=True)

    # debug(text_files[0])

    pool = Pool(8)
    with tqdm.tqdm(total=len(title_files)) as pbar:
        for _ in tqdm.tqdm(pool.imap_unordered(split_word_parallel, title_files)):
            pbar.update()

    # split_word_parallel(text_files[0])
    with tqdm.tqdm(total=len(text_files)) as pbar:
        for _ in tqdm.tqdm(pool.imap_unordered(split_word_parallel, text_files)):
            pbar.update()
    pool.close()


if __name__ == "__main__":
    main()
