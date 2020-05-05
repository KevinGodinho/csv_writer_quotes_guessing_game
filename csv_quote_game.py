import requests  # this is used to make call for data
from bs4 import BeautifulSoup  # this is used to parse data
from random import choice  # randomly select item from data structure
from csv import DictReader

BASE_URL = 'http://quotes.toscrape.com'  # url we get html from


def read_quotes(filename):

    with open(filename, 'r') as file:
        csv_reader = DictReader(file)
        return list(csv_reader)


# function to start quote guessing game
def start_game(quotes):

    quote = choice(quotes)  # select a random quote
    remaining_guesses = 4  # track guesses so game isn't eternal
    guess = ''  # store user's guess

    print('Here\'s a quote: ')  # start output to user
    print(quote['text'])  # display test of quote to user
    print(quote['author'])

    # while user has not guessed the correct author
    while guess.lower() != quote['author'].lower() and remaining_guesses > 0:
        # prompt user input
        guess = input(
            f'Who said this quote? Guesses remaining: {remaining_guesses}\n')
        remaining_guesses -= 1  # decrement remaining guesses to end game eventually

        # end game if answer is corred
        if guess.lower() == quote['author'].lower():
            print('YOUR ANSWER IS CORRECT!')
            break

        # provide hints if answer is incorrect until no more remaining guesses
        if remaining_guesses == 3:
            # call data for quote being used
            res = requests.get(f'{BASE_URL}{quote["bio-link"]}')
            soup = BeautifulSoup(res.text, 'html.parser')  # parse html
            # get birth date of author
            birth_date = soup.find(class_='author-born-date').get_text()
            # get birth place of author
            birth_place = soup.find(class_='author-born-location').get_text()
            # display hint
            print(
                f'Here\'s a hint: The author was born on {birth_date} {birth_place}.')
        elif remaining_guesses == 2:
            # next hint
            print(
                f'Here\'s a hint: The author\'s first name starts with: {quote["author"][0]}')
        elif remaining_guesses == 1:
            # get first character of author's last name
            last_initial = quote['author'].split(' ')
            # last hint
            print(
                f'Here\'s a hint: The author\'s last name starts with: {last_initial[1][0]}')
        else:
            # you lose
            print(
                f'Sorry you ran out of guesses. The answer was {quote["author"]}')

    replay = ''  # store user's answer of restarting game
    yes = ('yes', 'y')  # store valid yes options
    no = ('no', 'n')  # store valid no options

    # while user input is invalid, prompt user to play again
    while replay.lower() not in yes and replay.lower() not in no:
        # prompt user to play again
        replay = input('Would you like to play again? (y/n)? ')

    # restart game if yes, end game if no
    if replay.lower() in yes:
        start_game(quotes)  # call function to restart game
    else:
        print('OK, GOODBYE!')  # end game


quotes = read_quotes('quotes.csv')

start_game(quotes)  # call function to intiate game and pass in scraped quotes
