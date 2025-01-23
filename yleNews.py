from bs4 import BeautifulSoup
import requests

def getNews():

    url = 'https://feeds.yle.fi/uutiset/v1/recent.rss?publisherIds=YLE_UUTISET'

    headlines = requests.get(url)

    soup = BeautifulSoup(headlines.content, features='html.parser')

    items = soup.find_all('item')

    newsArticles = []

    for i in items:

        title = i.find('title').text
        description = i.find('description').text
        link = i.find('link').text
        article = {'title': title, 'description': description, 'link': link}
        newsArticles.append(article)

    return newsArticles[0:5]
