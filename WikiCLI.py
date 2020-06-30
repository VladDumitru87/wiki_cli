"""
Wikipedia command line interaction.
This program will help you find articles on wikipedia's main directly from the terminal.

thru webscraping it takes input from the user and it creates a link form where it takes
the title of the page and the first paragraph.

Example:
    # >>> rose
    will go on https://en.wikipedia.org/wiki/Rose and it will return the title: Rose
    and the first paragraph: A rose is a woody perennial flowering plant of the genus Rosa,
    in the family Rosaceae, or the flower it bears...

    # >>> python
    will go on https://en.wikipedia.org/wiki/Python and it will return the title: Python
    As this is a term that might refer to more than one descriptions,
    it will return a list with short descriptions for all instances.

    # >>> jdkjvghn
    will go on https://en.wikipedia.org/wiki/Rose and it will ask the user to rerun the
    program and search for a different term.


"""

from bs4 import BeautifulSoup as bs
import requests


def on_this_day_wiki():
    """ create a list with all entries form "On this day" section """

    url = "https://en.wikipedia.org/wiki/Main_Page"
    data = requests.get(url)
    soup = bs(data.text, "html.parser")
    # get the html tree from Wikipedia's main page

    data = []
    for item in soup.find_all('div', {"id": "mp-otd"}):
        for ul in item.find_all("ul", limit=1):
            for li in ul.find_all("li"):
                data.append(f"On this day in: {li.text}")

    return data


def splash_screen():
    """ displays a splash screen and "On this day" table from Wikipedia
    at the start of the program"""

    logo = """
     Welcome to:
     __          ___ _    _                _ _       
     \ \        / (_) |  (_)              | (_)      
      \ \  /\  / / _| | ___ _ __   ___  __| |_  __ _ 
       \ \/  \/ / | | |/ / | '_ \ / _ \/ _` | |/ _` |
        \  /\  /  | |   <| | |_) |  __/ (_| | | (_| |
         \/  \/   |_|_|\_\_| .__/ \___|\__,_|_|\__,_|
                           | |                  C.L.I.      
                           |_|                       
    """
    print(logo)

    today = on_this_day_wiki()
    for i in today:
        print(i)
    print("\nThe program can be stopped by CTRL^C key combination\n")


splash_screen()

SEARCH_FOR = str(input("\nWhat would you like to see on Wikipedia?\n>"))
# ask for input for the search term

TEXT = SEARCH_FOR.replace(" ", "_")
# where input is more than 1 word, it changes spaces to underscores

url = f"https://en.wikipedia.org/wiki/{TEXT}"
data = requests.get(url)
soup = bs(data.text, "html.parser")


# get the html tree from the page created with user input


def page_title_return():
    """returns the title of any page"""

    for h1 in soup.find_all("h1", {"id": "firstHeading"}):
        title = h1.text
        return title


def page_body_return():
    """ returns the content of any page """

    text_body = ""
    warning = False

    for main_div in soup.find_all("div", {"id": "mw-content-text"}):
        for div in main_div.find_all("div", {"class": "mw-parser-output"}):
            for p in div.find_all("p", {"class": ""}, limit=1):
                text_body = p.text  # returns body of an existing page as str

    for td in soup.find_all("div", {"id": "sisterproject"}):
        if SEARCH_FOR.capitalize() in f"Look for {SEARCH_FOR.capitalize()} on one of Wikipedia's sister projects":
            warning = True  # returns True if the page contains text for nonexistent entry

    if "may refer to" in text_body:
        for main_div in soup.find_all("div", {"id": "mw-content-text"}):
            for div in main_div.find_all("div", {"class": "mw-parser-output"}):
                for ul in div.find_all("ul"):
                    for li in ul.find_all("li", recursive=False):
                        if SEARCH_FOR.capitalize() in li.text:
                            print(f"* {li.text}")  # list of multiple occurrences for one term

    elif warning:  # test for no entry page
        return f"There are no articles for {SEARCH_FOR.capitalize()} on Wikipedia. Please rerun the program!"
    else:  # return paragraph of article page
        return text_body


def article_return():
    """ return article """
    print(f"Title:\t{page_title_return()}\n{page_body_return()}")


if __name__ == "__main__":
    article_return()
