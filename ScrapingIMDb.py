import re
from bs4 import BeautifulSoup
import pandas as pd
import requests
import psycopg2


# Connecting to our DataBase
db_host='localhost'
db_name='BdIMDb'
db_user='postgres'
db_password='qwerty321'
db_port='5432'
connection = psycopg2.connect(host=db_host, database=db_name, user=db_user, password=db_password)
cursor = connection.cursor()

# Check if there is a table. If not, then create a new one with these columns:
create_table_query = '''
    CREATE TABLE IF NOT EXISTS IMDb0(
        id SERIAL PRIMARY KEY,
        Title VARCHAR(255),
        Release_year INT,
        Genre VARCHAR(255),
        Runtime_min int,
        Rating float,
        Votes int
    )
'''
cursor.execute(create_table_query)

# Use headers to notify the website that we are not a robot
headers = {
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0"
}

# Create an empty list where we will put our data in later
movie_data = []

# Use for to scrape every page of the website
for page_num in range(1,77):
    url = f'https://www.imdb.com/list/ls503325184/?st_dt=&mode=detail&page={page_num}&ref_=ttls_vm_dtl&sort=list_order,asc'

    # Check the response of the URL to see if we will be able to scrape data using it
    response = requests.get(url, headers=headers)
    # print(response)

    # Using BeautifulSoup we extract the elements of HTML that have the data that we need
    soup = BeautifulSoup(response.content, 'html.parser')
    movie_elements = soup.find_all('div', class_='lister-item-content')

    # Using for we find the specific data that we need and clean it up
    for movie_element in movie_elements:
        # Using this command we look for data that we need from the scraped elements
        title = movie_element.find('h3', class_='lister-item-header').a.text.strip()
        year_text = movie_element.find('span', class_='lister-item-year').text.strip()
        # Using this command we remove unnecessary characters
        year_match = re.search(r'\d{4}', year_text)
        # Check to see if there is data to scrape if not we get the answer None
        year = int(year_match.group(0)) if year_match else None
        genre_text = movie_element.find('span', class_='genre')
        genre = genre_text.text.strip() if genre_text else None
        runtime_text = movie_element.find('span', class_='runtime')
        # Using strip() and replace() we remove unnecessary characters
        runtime = round(int(runtime_text.text.strip().replace(' min', '').replace(',', '')),0) if runtime_text else None
        rating_text = movie_element.find('div', class_='ipl-rating-star').find('span', class_='ipl-rating-star__rating')
        rating = round(float(rating_text.get_text(strip=True)), 1) if rating_text else None
        # Since this element does not have a specific class, we look for it using 'name' and 'data-value
        votes_text = movie_element.find('span', {'name': 'nv', 'data-value': True})
        votes = int(votes_text['data-value']) if votes_text else None

    # After extracting the data we put it all in our list that we created earlier
        movie_data.append({
            'Title': title,
            'Release year': year,
            'Genre': genre,
            'Runtime(min)': runtime,
            'Rating': rating,
            'Votes': votes
        })

    # Now we also insert the data in our DataBase to our table that we created earlier
        insert_query = '''
                                INSERT INTO IMDb0(Title, Release_year, Genre, Runtime_min, Rating, Votes)values(%s, 
                                %s, %s, %s, %s, %s)
                                '''
        cursor.execute(insert_query, (title, year, genre, runtime, rating, votes))
        connection.commit()

    # Using Pandas we create a DataFrame from our new list
    df = pd.DataFrame(movie_data)

    # Convert the floats to integers
    df['Release year'] = pd.to_numeric(df['Release year']).astype('Int64')
    df['Runtime(min)'] = pd.to_numeric(df['Runtime(min)']).astype('Int64')

    # Using Pandas to convert our DataFrame to a csv file
    df.to_csv('IMDb0.csv', index=False)