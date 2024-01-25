from bs4 import BeautifulSoup
import requests
import re


url = 'https://www.imdb.com/list/ls093350982/'

r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')

# Get Netflix Movie Blocks
# //div[@class='lister-item mode-detail']
movies = soup.find_all(
    name='div',
    attrs={
        'class': 'lister-item mode-detail'
    }
)


print('# of movies Find:', len(movies))
for i, movie in enumerate(movies):
    # Find title
    title_element = movie.find('h3').a
    print(i, title_element.text, title_element['href'])

    # Find published year
    year = movie.find(
        'span', attrs={'class': 'lister-item-year text-muted unbold'}).text
    print('\t', 'year:', year)

    # Find vote and gross
    votes_and_gross = movie.find_all(
        'span',
        attrs={'name': 'nv', 'data-value': re.compile('\d+')}
    )
    if len(votes_and_gross) == 2:
        num_of_votes, num_of_gross = votes_and_gross[0]['data-value'], votes_and_gross[1]['data-value']
    else:
        num_of_votes, num_of_gross = votes_and_gross[0]['data-value'], -1

    print('\t', num_of_votes, num_of_gross)
    print()
