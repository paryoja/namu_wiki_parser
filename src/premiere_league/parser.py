import logging
import os
import random
import re
import shutil
import time
import traceback

import requests
from bs4 import BeautifulSoup
from selenium import common
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

logger = logging.getLogger("Crawler")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
logger.propagate = 0


class Arguments:
    def __init__(self, site, chrome_idx):
        self.site = site
        self.chrome_idx = chrome_idx


class Chrome:
    def __init__(self, idx):
        logger.info("Setting Chrome Driver {}".format(idx))
        options = webdriver.ChromeOptions()
        # PROXY = "35.230.68.217:8000"
        # options.add_argument('--proxy-server=%s' % PROXY)
        # options.add_argument("headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)

        driver = webdriver.Chrome(chrome_options=options)

        if idx == 0:
            driver.set_window_position(100, 100)
        elif idx == 1:
            driver.set_window_position(100, 700)
        elif idx == 2:
            driver.set_window_position(700, 100)
        elif idx == 3:
            driver.set_window_position(700, 700)
        elif idx == 4:
            driver.set_window_position(1300, 100)
        else:
            driver.set_window_position(1300, 700)

        driver.set_window_size(600, 600)

        # wait(driver, 'aOOlW', By.CLASS_NAME)
        # driver.find_element_by_class_name("aOOlW")
        # driver.find_element_by_class_name("aOOlW").click()

        self.driver = driver

    def wait_for_count(self):
        wait(self.driver, "g47SY lOXF2", By.CLASS_NAME)

    def scroll_down(self, url):
        logger.debug("Getting {}".format(url))
        self.driver.get(url)

        yield self.driver.page_source

        last_height = self.driver.execute_script("return document.body.scrollHeight")
        fallback = 10.0
        while True:
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )
            time.sleep(6 * random.random())
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            else:
                yield self.driver.page_source

            last_height = new_height

    def quit(self):
        self.driver.quit()


def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    value = re.sub("[^\w\s-]", "", value).strip().lower()
    value = re.sub("[-\s]+", "-", value)

    return value


def get_filename(url):
    return url.split("/")[-1].split("?")[0]


def save_image(url, directory, filename):
    r = requests.get(url, stream=True)
    if os.path.exists(os.path.join(directory, filename)):
        # print("Path {} already exists skip download".format(filename))
        return True

    if r.status_code == 200:
        with open(os.path.join(directory, filename), "wb") as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
        return True
    else:
        print("error occurred while download")
        return False


def wait(driver, name, element_type=By.NAME):
    try:
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((element_type, name))
        )
    except common.exceptions.TimeoutException:
        pass
    except Exception as e:
        print(type(e), e)


def download_site(site, chrome):
    logger.info(site)

    for idx, html in enumerate(chrome.scroll_down(site)):
        print(idx)
        print(html)

    with open("debug.html", "w", encoding="utf-8") as w:
        w.write(chrome.driver.page_source)


def task(args: Arguments):
    site = args.site
    idx = args.chrome_idx

    chrome = Chrome(idx)

    try:
        download_site(site, chrome)
    except Exception as e:
        print("Error :", site)
        traceback.print_exc()
        print(type(e), e)
    finally:
        chrome.quit()


def main():
    visited = set()
    history = []

    process = 1
    arg = Arguments("https://www.premierleague.com/results", 0)
    candidate_group = []

    for i in range(process * 3):
        candidate_group.append((False, []))

    count = 0
    # for cand in candidate:
    #     candidate_group[count % (process * 3)][1].append(cand)
    #     count += 1

    # with multiprocessing.Pool(process) as p:
    #     p.map(task, enumerate(candidate_group))

    task(arg)


if __name__ == "__main__":
    main()
