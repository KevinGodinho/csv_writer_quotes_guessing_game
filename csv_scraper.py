import requests  # this is used to make call for data
from bs4 import BeautifulSoup  # this is used to parse data
from time import sleep  # slow requests to url's server (optional)
from csv import DictWriter

BASE_URL = 'http://quotes.toscrape.com'  # url we get html from


# function to scrape quotes
def scrape_quotes():

    url = '/page/1'  # specify page to loop through pages until None
    all_quotes = []  # list where data will be stored

    # while there are more pages to loop through
    while url:
        res = requests.get(f'{BASE_URL}{url}')  # call html from url
        soup = BeautifulSoup(res.text, 'html.parser')  # store html as text
        quotes = soup.find_all(class_='quote')  # get quotes in list

        # loop through & create list with desired data
        for quote in quotes:
            all_quotes.append({
                'text': quote.find(class_='text').get_text(),
                'author': quote.find(class_='author').get_text(),
                'bio-link': quote.find('a')['href']
            })

        next_btn = soup.find(class_='next')  # look for next page button
        # until there isn't one
        url = next_btn.find('a')['href'] if next_btn else None

        sleep(1)  # slows calls to server to not overload it (optional)
        print(all_quotes)
        return all_quotes  # return scraped quotes to be accessed outside function


# function to write quotes to csv file
def write_quotes(quotes):

    # open or create quotes.csv file
    with open('quotes.csv', 'w') as file:

        headers = ['text', 'author', 'bio-link']  # specify headers for file
        # begin DictWriter process
        csv_writer = DictWriter(file, fieldnames=headers)

        csv_writer.writeheader()  # write headers to file

        # loop through quotes and write them to file
        for quote in quotes:
            # already in dict format from all_quotes above
            csv_writer.writerow(quote)


quotes = scrape_quotes()  # call function and place quotes in global variable

write_quotes(quotes)  # call function to create csv file
