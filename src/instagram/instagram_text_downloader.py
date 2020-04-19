import json
import time

import requests
from absl import flags
from environs import Env

FLAGS = flags.FLAGS

env = Env()
env.read_env()
from settings import INSTA_DOCUMENT_ROOT


def main():
    token = env.str("Token")
    headers = {"Authorization": f"Token {token}"}
    response = requests.get("http://13.125.1.208/api/instagram/", headers=headers)

    response_dict = response.json()
    turn = 0
    print(turn, len(response_dict["results"]))

    with open(INSTA_DOCUMENT_ROOT / "instagram.txt", "w", encoding="utf-8") as w:
        while True:
            for line in response_dict["results"]:
                title = line["title"].strip().replace("\n", " ")
                if (
                    title
                    and len(title) > 10
                    and not title.startswith("#")
                    and not title.startswith("Photo")
                    and not title.startswith("Image may contain:")
                ):
                    w.write(json.dumps(line["title"]))
                    w.write("\n")
            turn += 1
            if response_dict["next"] is not None:
                try:
                    response = requests.get(response_dict["next"], headers=headers)
                    response_dict = response.json()
                except Exception as e:
                    print(e)
                    time.sleep(10)
                print(turn, len(response_dict["results"]))
            else:
                break
    print("Done Downloading")


if __name__ == "__main__":
    main()
