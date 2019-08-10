import collections
import os
import sys


class Parser:
    def __init__(self):
        self.container = []
        self.title_and_text = []
        self.started = False
        self.is_title = False
        self.is_key = True
        self.is_contributor = False
        self.key = None
        self.escaped = False
        self.file_count = 0
        self.line_count = 0
        self.f = None

        self.buffer = collections.deque()

        self.open_new_file()

    def open_new_file(self):
        if self.f:
            self.f.close()

        os.makedirs('./parsed_files', exist_ok=True)
        filename = './parsed_files/wiki_{:04d}.txt'.format(self.file_count)

        if os.path.exists(filename):
            enter = input("File {} already exists".format(filename))
            if enter != 'y':
                sys.exit(0)
        self.f = open(filename, 'w')
        self.file_count += 1

    def read_char(self, char):
        # 디버깅 용 buffer
        self.buffer.append(char)

        if len(self.buffer) == 1000:
            self.buffer.popleft()

        if self.is_contributor:
            # contributor list
            if not self.escaped and char == ']':
                self.is_contributor = False
                self.is_key = True
        else:
            if not self.escaped and char == '"':
                if self.started:
                    # ended
                    if self.is_key:
                        value = ''.join(self.container)
                        self.container.clear()

                        if 'contributor' in value:
                            self.is_contributor = True
                        else:
                            if 'title' in value or 'text' in value:
                                self.is_title = True
                                self.key = value
                            elif "namespace" in value:
                                self.is_title = False
                            else:
                                print('not title')
                                self.is_title = False
                                print(''.join(self.buffer))
                                sys.exit(0)

                    else:
                        if self.is_title:
                            title = self.key
                            text = ''.join(self.container)

                            self.title_and_text.append(title)
                            self.title_and_text.append(text)

                            if title == 'text':

                                try:
                                    pass
                                    print(self.title_and_text[1].replace('\/', '/').encode().decode(
                                        'unicode-escape').encode('utf-16', 'surrogatepass').decode('utf-16'))
                                    # print(''.join(self.buffer))
                                except Exception as e:
                                    print('DEBUG', self.title_and_text[1])
                                    raise e

                                self.line_count += 1

                                self.f.write('\t'.join(self.title_and_text))
                                self.f.write('\n')
                                self.title_and_text.clear()

                                if self.line_count % 10000 == 0:
                                    self.open_new_file()

                            self.container.clear()

                    self.is_key = not self.is_key

                self.started = not self.started

            elif self.started:

                if self.is_key or self.is_title:
                    self.container.append(char)

        if char == '\\':
            if self.escaped:
                self.escaped = False
            else:
                self.escaped = True
        else:
            self.escaped = False


def main():
    with open('/Users/yjpark/Documents/namuwiki190312/namuwiki_20190312.json', 'r') as f:
        line = 0
        parser = Parser()
        while True:
            x = f.read(100000000)

            if x == '':
                break

            # print(x)
            for char in x:
                parser.read_char(char)

            print(line)
            line += 1


if __name__ == '__main__':
    main()
