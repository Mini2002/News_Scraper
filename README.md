# News_Scraper
It is a script which scrapes headlines from BBC news.

# Features
- Scrapes Unique Headlines from BBC news.
- Saves the data to mysql database.
- Has 4 columns Headlines, time of scraping, text count and word count.
- Used schedule library to auto run the script every 12 hours.

# Tech Stacks
- Python3
- BeautifulSoup
- Requests
- MySQl

# Data pipeline
- Extract->transform->load(mysql database)