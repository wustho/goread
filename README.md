# goread

Yet another [Goodreads](www.goodreads.com) cli client. This is not an official Goodreads app, but a script intended for my own personal use. This script will help you fetch informations about title, ISBN, publication year, author, rating, number of pages & description of a book and give a list of top 30 author books from resources belong to Goodreads.

This script won't let you manage your Goodreads account like adding/removing book to shelf, follow/unfollow an author or adding/removing reviews.

# Requirements

`python 3.7`

# Installation

Clone this repo, make `goread` executable and copy it to location in one of `PATH` variable, like `$HOME/.local/bin`.

``` shell
git clone https://github.com/benadha/goread.git
cd goread
chmod +x goread
cp goread /somepath/in/PATH/variable
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

# Note

This script is intended for my personal use. So, do not expect anything and use it at your own risk.

# License

MIT License

Copyright (c) 2019 Benawi Adha

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
