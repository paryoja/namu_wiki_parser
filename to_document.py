import glob
from multiprocessing import Pool

import tqdm


def parse_line(file):
    with open(file) as f:
        with open(file + '.text', 'w') as w:
            for line in f:
                temp = line.split('\t')

                parsed_title = temp[1].replace('\/', '/').encode().decode('unicode-escape'). \
                    encode('utf-16', 'surrogatepass').decode('utf-16')

                assert len(temp) == 4, "{} {} {}".format(len(temp), '\t'.join(temp[::2]), parsed_title)
                assert temp[0] == 'title', temp[0]
                assert temp[2] == 'text', temp[2]

                try:
                    parsed_text = temp[3].replace('\/', '/').encode().decode('unicode-escape'). \
                        encode('utf-16', 'surrogatepass').decode('utf-16')

                    while '\n\n' in parsed_text:
                        parsed_text = parsed_text.replace('\n\n', '\n')

                    w.write(parsed_title)
                    w.write('\n')
                    w.write(parsed_text)
                    w.write('\n\n')

                except Exception as e:
                    print("Title ", parsed_title)

                    for token in temp[3].split():
                        print(token)
                        print(token.replace('\/', '/').encode().decode('unicode-escape'). \
                              encode('utf-16', 'surrogatepass').decode('utf-16'))
                        print(token, token.encode().decode('unicode-escape'))

                    raise e


def main():
    files = sorted(glob.glob("parsed_files/*.txt"))
    pool = Pool(8)
    with tqdm.tqdm(total=len(files)) as pbar:
        for _ in tqdm.tqdm(pool.imap_unordered(parse_line, files)):
            pbar.update()
    pool.close()


if __name__ == "__main__":
    main()
