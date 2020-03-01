import json
import pathlib
import re

import ijson


def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    import unicodedata
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub('[^\w\s-]', '', value).strip().lower()
    value = re.sub('[-\s]+', '-', value)

    if not value:
        return "EMPTY.json"
    return value


class FileHandler:
    def __init__(self, directory):
        self.count = 0
        self.document_id = 0
        self.directory = directory
        self.file = None

    def get_file(self):
        if self.file is None:
            self.file = open(self.directory / 'document_{}.json'.format(self.document_id), 'w')

        if self.count == 10000:
            self.file.close()
            self.count = 0
            self.document_id += 1
            self.file = open(self.directory / 'document_{}.json'.format(self.document_id), 'w')

        self.count += 1
        return self.file

    def close(self):
        if self.file:
            self.file.close()


def main():
    base_dir = pathlib.Path('./document')
    base_dir.mkdir(parents=True, exist_ok=True)

    handler = FileHandler(base_dir)

    try:
        with open("F:/wiki/namuwiki_20190312.json") as file:
            parser = ijson.items(file, 'item')

            for data in parser:
                text = data["text"]

                if text.startswith('#redirect'):
                    continue

                del data["namespace"]
                del data["contributors"]

                w = handler.get_file()
                json.dump(data, w)
                w.write('\n')
    finally:
        handler.close()


if __name__ == "__main__":
    main()
