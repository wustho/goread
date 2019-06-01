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

__version__ = "0.3.0"
__license__ = "GPL"
__author__ = "Benawi Adha"
__url__ = "https://github.com/wustho/goread"

import os
import sys
import requests
import re
import textwrap
import xml.etree.ElementTree as ET
from html import unescape
from urllib.parse import quote as UQ
from html.parser import HTMLParser


class HTMLtoText(HTMLParser):
    para = {"p", "div"}
    inde = {"q", "dt", "dd", "blockquote", "pre"}
    bull = {"li"}
    hide = {"script", "style", "head"}
    # hide = {"script", "style", "head", ", "sub}

    def __init__(self):
        HTMLParser.__init__(self)
        self.text = ""
        self.ishidden = False

    def handle_starttag(self, tag, attrs):
        if tag in self.hide:
            self.ishidden = True
        elif tag in self.inde:
            self.text += "    "
        elif tag in self.bull:
            self.text += "  - "
        elif tag == "sup":
            self.text += "^{"
        elif tag == "sub":
            self.text += "_{"
        elif tag == "code" and self.isinde:
            self.text += "\n"

    def handle_startendtag(self, tag, attrs):
        if tag == "br":
            self.text += "\n"
        elif tag in {"img", "image"}:
            self.text += " <img: {}>".format(attrs.get("src", ""))

    def handle_endtag(self, tag):
        if re.match("h[1-6]", tag) is not None:
            self.text += "\n\n"
            self.ishead = False
        elif tag in self.para:
            self.text += "\n\n"
        elif tag in self.hide:
            self.ishidden = False
        elif tag in self.inde | self.bull:
            self.text += "\n\n"
        elif tag in {"sub", "sup"}:
            self.text[-1] += "}"

    def handle_data(self, raw):
        if raw and not self.ishidden:
            self.text += unescape(re.sub(r"\s+", " ", raw))

    def getFormattedText(self, width=0):
        if width == 0:
            return self.text
        else:
            text = []
            for i in self.text.splitlines():
                text.append(textwrap.fill(i, width))
            return "\n".join(text)


def readGoodreadKey():
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
    return key

def fetchXML(api, arg):
    requests.packages.urllib3.disable_warnings()
    DATAxml = requests.Session().get(url=api, params=arg)
    return ET.fromstring(DATAxml.text.encode("utf-8"))

def printAuthorWorks(keyword, devkey):
    para = { "key" : devkey }
    auth = keyword
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

def printBookDesc(keyword, devkey, descwidth=70):
    para = { "key" : devkey }
    grapi_get_rev = "https://www.goodreads.com/book/title.xml"
    para["title"] = keyword
    DATA = fetchXML(grapi_get_rev, para)

    print("\n Title\t: ", DATA.find("book/title").text,
        "\n ISBN\t: ", DATA.find("book/isbn").text,
        "\n Year\t: ", DATA.find("book/publication_year").text,
        "\n Author\t: ", DATA.find("book/authors/author/name").text,
        "\n Rating\t:  *" + DATA.find("book/average_rating").text,
        "({:,} ratings)".format(int(DATA.find("book/work/ratings_count").text)),
        "\n Pages\t: ", DATA.find("book/num_pages").text, "\n")

    # try:
    raw_desc = DATA.find("book/description").text

    if raw_desc is None:
        print("! Description not found.")
    else:
        parser = HTMLtoText()
        parser.feed(raw_desc)
        parser.close()
        print(parser.getFormattedText(descwidth))

    print("\n<source:www.goodreads.com>\n")

def main():
    args = sys.argv[1:]
    if len(sys.argv) == 1 or len({"-h", "--help"} & set(args)) != 0:
        print(__doc__)
        sys.exit()

    if "-l" in args:
        args.remove("-l")
        authorkeyword = " ".join(args)
        printAuthorWorks(authorkeyword, readGoodreadKey())
    else:
        bookkeyword = " ".join(args)
        printBookDesc(bookkeyword, readGoodreadKey())

if __name__ == "__main__":
    main()
