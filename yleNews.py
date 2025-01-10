from bs4 import BeautifulSoup
import requests

def getNews():

    url = 'https://feeds.yle.fi/uutiset/v1/majorHeadlines/YLE_UUTISET.rss'

    headlines = requests.get(url)

    soup = BeautifulSoup(headlines.text, 'html')

    item = soup.find_all('item')

    newsArticles = []

    for i in item:
        title = i.find('title').text
        link = i.find('link').text
        desc = i.find('description').text

        article = [title, link, desc]

    newsArticles.append(article)

    return newsArticles[0:5]