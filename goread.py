#!/usr/bin/env python3

"""
USAGES
\tgoread TITLE [+AUTHOR]
\tgoread [-l] AUTHOR

OPTIONS
\t-h, --help\tdisplay this help message
\t-l AUTHOR\tlist top (max 30) most popular books by AUTHOR

EXAMPLES
\tgoread "ring"
\tgoread ring koji suzuki
\tgoread Ender\\'s Game
\tgoread -l tere liye
\tgoread eduardo sacheri -l
"""

import os
import sys
import requests
import re
import textwrap
import xml.etree.ElementTree as ET
from html import unescape

try:
    from urllib import quote as UQ
except ImportError:
    from urllib.parse import quote as UQ

if len(sys.argv) == 1 or sys.argv[1] == "-h" or sys.argv[1] == "--help":
    print(__doc__)
    exit()

devkey_file = os.path.join(os.getenv("HOME"), ".goread_key")

try:
    with open(devkey_file) as f:
        key = "".join(f.read().split())

except:
    key == input("""Get Goodreads developer key at www.goodreads.com.
Copy then paste below or just write it to `~/.goread_key`.
Goodreads dev key: """)
    with open(devkey_file, "w") as f:
        f.write(key)

para = { "key" : key }

def fetchXML(api, arg):
    requests.packages.urllib3.disable_warnings()
    DATAxml = requests.Session().get(url=api, params=arg)
    return ET.fromstring(DATAxml.text.encode("utf-8"))

try:
    sys.argv.remove("-l")
    auth = " ".join(sys.argv[1:])
    grapi_auth = "https://www.goodreads.com/api/author_url/" + UQ("<" + auth + ">")
    grapi_pagin_auth = "https://www.goodreads.com/author/list.xml"

    auth_id = fetchXML(grapi_auth, para).find("author").attrib["id"]
    para["id"] = auth_id
    DATA = fetchXML(grapi_pagin_auth, para)

    print()
    print(" Top",
          DATA.find("author/books").attrib["end"],
          "most popular of",
          DATA.find("author/books").attrib["total"],
          "books by", DATA.find("author/name").text,
          "<source:www.goodreads.com>")
    print("==============================================================================")

    rec, first_col_width = [], 0
    for i in DATA.findall("author/books/book"):
        rec.append([u" \u2605 "
                    + i.find("average_rating").text
                    + " ({:,})".format(int(i.find("ratings_count").text)),
                    i.find("title").text])
        if len(rec[-1][0]) > first_col_width:
            first_col_width = len(rec[-1][0])

    for i in rec:
        print("".join(n.ljust(first_col_width + 2) for n in i))

    print()

except ValueError:
    grapi_get_rev = "https://www.goodreads.com/book/title.xml"
    para["title"] = " ".join(sys.argv[1:])
    DATA = fetchXML(grapi_get_rev, para)

    print("\n Title\t: ", DATA.find("book/title").text,
          "\n ISBN\t: ", DATA.find("book/isbn").text,
          "\n Year\t: ", DATA.find("book/publication_year").text,
          "\n Author\t: ", DATA.find("book/authors/author/name").text,
          "\n Rating\t: ", DATA.find("book/average_rating").text,
          "({:,} ratings)".format(int(DATA.find("book/work/ratings_count").text)),
          "\n Pages\t: ", DATA.find("book/num_pages").text, "\n")

    try:
        raw_desc = DATA.find("book/description").text
        desc = re.sub(r"<.*?>", "", raw_desc.replace("<br />", "\n"))
        desc = unescape(desc)
        print(desc)

    except:
        print("(Description not found.)")

    print("\n<source:www.goodreads.com>\n")
