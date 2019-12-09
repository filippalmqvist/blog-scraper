from src.scrapers.abstract_scraper import make_soup, write_datafile
import re

WEBSITE = "https://feedback.minecraft.net/hc/en-us/sections/360002267532-Snapshot-Information-and-Changelogs"
BASE_SITE = "https://feedback.minecraft.net"
FILENAME = "../resources/data/minecraft_snap.txt"
MONTHS = {
    "january": "01",
    "february": "02",
    "march": "03",
    "april": "04",
    "may": "05",
    "june": "06",
    "july": "07",
    "august": "08",
    "september": "09",
    "october": "10",
    "november": "11",
    "december": "12"
}


def get_articles(articles, soup):
    while True:
        pagination = soup.find("li", {"class": "pagination-next"})
        posts = soup.find("ul", {"class": "article-list"})
        for post in posts.find_all("li"):
            articles.append(BASE_SITE + post.find("a").get("href"))

        if pagination is not None:
            soup = make_soup(BASE_SITE + pagination.find("a").get("href"))
        else:
            break
    return articles


def get_date(soup):
    date = None
    date_candidates = soup.find("div", {"class": "article-body"}).findChildren()

    for candidate in date_candidates:
        text = candidate.text.strip()
        words = re.split(r"\s+", text)

        if len(words) >= 3 and re.search(r"\d{1,2}", words[0]) and re.search(r"\d{4}", words[2]):
            if len(words[0]) == 1:
                words[0] = "0" + words[0]
            date = words[2] + MONTHS[words[1].lower()] + words[0]
            date = re.sub(r"\D", "", date)
            break

    return date


def scrape():
    soup = make_soup(WEBSITE)
    articles = []
    data = []

    # Get each individual entry
    articles = get_articles(articles, soup)

    # Get entry data
    for article in articles:
        blog_soup = make_soup(article)

        link = article
        date = get_date(blog_soup)
        title = blog_soup.find("h1", {"class": "article-title"}).text.strip()
        if date is None:
            continue

        data.append({"id": date, "title": title, "link": link})

    return write_datafile(data, FILENAME)