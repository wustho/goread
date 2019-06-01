# ```$ goread```

![Screenshot](https://github.com/wustho/goread/blob/master/screenshot.png)

Yet another [Goodreads](www.goodreads.com) cli client. This is not an official Goodreads app, but a script intended for my own personal use. This script will help you fetch informations about title, ISBN, publication year, author, rating, number of pages & description of a book and give a list of top 30 author books from resources belong to Goodreads.

This script won't let you manage your Goodreads account like adding/removing book to shelf, follow/unfollow an author or adding/removing reviews.

# Requirements

`python 3.7`

# Installation

``` shell
$ pip install git+https://github.com/wustho/goread.git
```

`goread` needs Goodreads developer key which can be accessed from https://www.goodreads.com/api/keys and put it in `$HOME/.goread_key`.

# Usages

``` shell
USAGES
	goread TITLE [+AUTHOR]
	goread [-l] AUTHOR

OPTIONS
	-h, --help  display this help message
	-l AUTHOR   list top (max 30) most popular books by AUTHOR

EXAMPLES
	goread "ring"
	goread ring koji suzuki
	goread Ender\'s Game
	goread -l tere liye
	goread eduardo sacheri -l
```
