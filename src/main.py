import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

SOURCE_URL = "https://cnbc.com/"

def bs_request(query=None):
    url_path = SOURCE_URL + query if query else SOURCE_URL
    response = requests.get(url_path)
    if response.status_code==200:
        soup = BeautifulSoup(response.text, "html.parser")
        news = soup.find_all('div', class_='Card-standardBreakerCard')
    else: 
        print('Unable to Access the Link')                
    return news

def scraper(articles):
    titles = []
    urls = []
    paragraphs = []
    dates = []
    categories = []
    for article in articles:
        try:
            url = article.find('a').get('href')
            content = article.find('div', class_='Card-textContent')
            title = content.find('div', class_='Card-titleContainer').text
            urls.append(url)
            titles.append(title)
        except:
            pass

    for u in urls:
        response = requests.get(u)
        if response.status_code==200:
            soup = BeautifulSoup(response.text, "html.parser")
            try: 
                article = soup.find('div', class_='ArticleBody-articleBody')
                texts = article.find_all('p')
                paragraph = ''
                for t in texts:
                    paragraph += '\n' + t.text
                paragraphs.append(paragraph)
            except:
                paragraphs.append('NaN')
            try:
                category = soup.find('a', class_='ArticleHeader-eyebrow').text
                categories.append(category)            
            except:
                categories.append('NaN')
            try:
                time = soup.find('time').text.split(', ')[1]
                dates.append(time)
            except:
                dates.append('NaN')
    news = {"title": titles, "url" : urls, "category": categories, "date": dates, "content": paragraphs}
    data = pd.DataFrame(news)
    output_dir = '../output'
    data.to_csv(os.path.join(output_dir, 'news_data.csv'), index=False)
    return data

def main():
    news = bs_request('business')
    data = scraper(news)
    print(data)

if __name__ == "__main__":
    main()