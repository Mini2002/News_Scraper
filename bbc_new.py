import requests
import bs4
import pandas as pd
import mysql.connector
import schedule
import time
from dotenv import load_dotenv
import os
load_dotenv() 

def scrape_news():
    # Extract
    try:
        url = requests.get('https://www.bbc.com/news')
    except requests.exceptions.RequestException as e:
        print(f'Hold on looks like we are no able to fetch the url {e}')
        return

    soup = bs4.BeautifulSoup(url.text,'lxml')

    headlines = []

    for i in soup.select('[data-testid="card-headline"]'):
        headlines.append(i.text.strip())

    df = pd.DataFrame({
        'headline': headlines,
        'scraped_at': pd.Timestamp.now()
    })


    # Tranform
    df = df[df['headline'].str.len() >10]
    df['headline_length'] = df['headline'].str.len()
    df = df.dropna()
    df = df.drop_duplicates(subset=['headline'],keep='first')
    df['word_count'] = df['headline'].str.split().str.len()

    # load
    # df.to_csv('headlines.csv',index=False)

    connection = mysql.connector.connect(
        host='localhost',
        user = 'root',
        password = os.getenv("DB_PASSWORD"),
        database = 'news_db'
    )
    cursor = connection.cursor()

    create_table = """ 
    Create Table if not exists Headlines (
    id INT AUTO_INCREMENT PRIMARY KEY,
    headline VARCHAR(500),
    scraped_at DATETIME,
    headline_length INT,
    word_count INT
    )
    """

    cursor.execute(create_table)

    for i, row in df.iterrows():
        insert_query = """
        INSERT INTO headlines (headline,scraped_at,headline_length,word_count)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(insert_query,(row['headline'],row['scraped_at'],row['headline_length'],row['word_count']))

    connection.commit()
    connection.close()

    print(f"Inserted {len(df)} headlines into database!")

schedule.every().day.at("09:00").do(scrape_news)
schedule.every(12).hours.do(scrape_news)

while True:
    schedule.run_pending()
    time.sleep(60)

