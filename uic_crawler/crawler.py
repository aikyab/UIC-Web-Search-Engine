import requests
import os
import pickle
from bs4 import BeautifulSoup
from collections import deque
import pathlib

domain = "uic.edu"

start_url = "https://cs.uic.edu"

current_path = pathlib.Path(__file__)
pages_folder = current_path.parent.parent / "uic_wse" / "webcrawler" / "new_docs"

skip_exts = [
    ".shtml",
    ".pdf",
    ".doc",
    ".docx",
    ".ppt",
    ".pptx",
    ".xls",
    ".xlsx",
    ".css",
    ".js",
    ".aspx",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".svg",
    ".ico",
    ".mp4",
    ".avi",
    ".tar",
    ".gz",
    ".tgz",
    ".zip",
]

crawl_limit = 1

error_file = "error_logs.txt"
f = open(error_file, "w+")
f.close()

# queue to perform BFS on all nodes in the web graph
url_q = deque()
url_q.append(start_url)

# this list keeps track of all nodes visited till the current point to avoid cycles
urls_crawled = []
urls_crawled.append(start_url)

# Stores the urls as values and their pagenos as keys in the dictionary
pages_crawled = {}
page_no = 1

while url_q:

    try:
        # fetch the first URL from the queue
        url = url_q.popleft()
        # get html code of web page
        rqst = requests.get(url)

        if rqst.status_code == 200:

            soup = BeautifulSoup(rqst.text, "html.parser")

            tags_extracted = soup.find_all("a")

            if len(tags_extracted) != 0:

                pages_crawled[page_no] = url

                output_file = pages_folder / str(page_no)

                os.makedirs(os.path.dirname(output_file), exist_ok=True)

                with open(output_file, "w", encoding="utf-8") as file:

                    file.write(rqst.text)
                file.close()

                for tag in tags_extracted:

                    link_to_add = tag.get("href")

                    if (
                        link_to_add is not None
                        and link_to_add.startswith("http")
                        and not any(ext in link_to_add.lower() for ext in skip_exts)
                    ):

                        link_to_add = link_to_add.lower()

                        link_to_add = link_to_add.split("#")[0]

                        link_to_add = link_to_add.split("?", maxsplit=1)[0]

                        link_to_add = link_to_add.rstrip("/")
                        link_to_add = link_to_add.strip()

                        if link_to_add not in urls_crawled and domain in link_to_add:

                            url_q.append(link_to_add)
                            urls_crawled.append(link_to_add)

                if len(pages_crawled) > crawl_limit:
                    # crawls the pages until some limit has been reached. 
                    break

                page_no += 1

    except Exception as e:
        # add error message to error logs
        with open(error_file, "a+") as logs:
            logs.write(f"Could not connect to {url}")
            logs.write(f"\nError occurred: {e}\n\n")
        logs.close()

        print("Could not connect to ", url)
        print("Error occurred: ", e, " \n")
        continue


# Creates a folder to store information on the all the pages extracted
pickle_folder = current_path.parent.parent / "uic_wse" / "webcrawler" / "pickle_files"

os.makedirs(pickle_folder, exist_ok=True)

with open(pickle_folder / "3000_pages_crawled.pickle", "wb") as f:
    pickle.dump(pages_crawled, f)