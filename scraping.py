import requests
from bs4 import BeautifulSoup
import csv
from pandas import DataFrame



articles_info = []

url = f"https://www.hespress.com/societe"

result = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

soup = BeautifulSoup(result.content, "lxml")

articles_container = soup.find("div", {"id": "main-page-content"})

all_articles = articles_container.find_all("div", {"class": "cover"})

print("len(all_articles) : " ,len(all_articles))
for article in all_articles :
    link_title = article.find("div", {"class" : "card-img-top"})
    link_title = link_title.find("a")
    article_title = link_title.attrs["title"]
    article_link = link_title.attrs["href"]

    result2 = requests.get(article_link, headers={'User-Agent': 'Mozilla/5.0'})
    soup2 = BeautifulSoup(result2.content, "lxml")
    article_content = soup2.find("div", {"class" : "article-content"}).text.strip()

    articles_info.append({
        "post_title": article_title,
        "post_content": article_content,
        "post_link": article_link
    })
DataFrame(articles_info).head()

# I can store the scraped data in a CSV file
columns = articles_info[0].keys()

with open("datasets\hespress-posts.csv", "w", encoding="utf-8-sig", newline="") as csv_file:
    dict_writer = csv.DictWriter(csv_file, columns)
    dict_writer.writeheader()
    dict_writer.writerows(articles_info)

    print("*"*50, "\n file created \n", "*"*50)

