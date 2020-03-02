import json
import pathlib

import requests


def main():
    document_path = pathlib.Path("./document")
    headers = {'Content-Type': 'application/json; charset=utf-8'}

    for file in document_path.glob("*.json"):
        with open(file) as f:
            for line in f:
                data = json.loads(line.strip())
                requests.post("http://localhost:5000", json=data, headers=headers)


if __name__ == "__main__":
    main()
