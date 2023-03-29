#############
# LIBRARIES #
#############

import os

import requests
from selenium import webdriver
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

from bs4 import BeautifulSoup as bs
import time
import bs4.element
from urllib.parse import urljoin

# Chrome driver

import pandas as pd
import string


#####################################################
# Function to scrape the content of the KIM website #
#####################################################

def get_movie_info(letter):
    movie_info_list = []
    movie_description_list = []
    URI = f'https://kids-in-mind.com/{letter}.htm'
    response = requests.get(URI)
    # print(response.status_code)
    if response:
        print('Success')
        # Getting the list of all movies --contained in class="et_pb_text_inner" in <a> tag
        # First find the class="et_pb_text_inner"
        movies = [] # all hrefs
        soup = bs(response.content, 'html.parser').find_all('div', class_="et_pb_text_inner")
        movie_by_title = soup[2]
        movie_by_title = movie_by_title.find_all('a')
        movie_by_title_href = [movie['href'] for movie in movie_by_title]
        movie_title = [movie.text for movie in movie_by_title]
        # print(movie_title)
        # Creating the URL for each movie
        movie_by_title_url = [urljoin(URI, movie) for movie in movie_by_title_href]
        # print(movie_by_title_url)
        # Opening each movie page and scraping the content
        for movie in movie_by_title_url:
            # print(movie)
            movie_page = requests.get(movie)
            # print(movie_page)
            # print(movie_page.status_code)
            print(f'Getting info for {movie}')
            soup = bs(movie_page.content, 'html.parser').find_all('div', class_="et_pb_text_inner")
            try:
                movie_info = soup[1].find('p').text
                # print(movie_info)
                movie_info_list.append(movie_info)
                # print(movie_title)
                movie_description = soup[2].find('p').text
                # print(movie_description)
                movie_description_list.append(movie_description)
                time.sleep(1)
                # movie_info_dict['movie_title'] = movie_title
                # movie_info_dict['movie_info'] = movie_info
                
            except:
                pass
    movies_df = pd.DataFrame(list(zip(movie_info_list, movie_description_list)), columns =['movie_info', 'movie_description'])
    movies_df[['movie_title', 'movie_year', 'movie_rating', 'KIM_ratings']] = movies_df.movie_info.str.split("|", expand=True)
    movies_df['KIM_ratings'] = movies_df['KIM_ratings'].str.strip('- ')
    movies_df[['sex_nudity', 'violence_gore', 'language']] = movies_df.KIM_ratings.str.split(".", expand=True)
    movies_df = movies_df[['movie_title', 'movie_year', 'movie_rating', 'sex_nudity', 'violence_gore', 'language', 'movie_description']]
    
    return movies_df

