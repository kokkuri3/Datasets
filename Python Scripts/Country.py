import requests
import csv

# Replace 'YOUR_API_KEY' with your actual API key
API_KEY = 'f14c370921f887539a7a21ae5e833689'

# Function to fetch data from TMDB API with pagination
def fetch_data(url_template, max_pages):
    data = []
    for page in range(1, max_pages + 1):
        url = url_template.format(API_KEY=API_KEY, page=page)
        response = requests.get(url)
        if response.status_code == 200:
            data += response.json().get('results', [])
        else:
            print(f'Error fetching data from URL: {url}')
    return data

# Function to extract countries from actor details
def extract_actor_countries(actor_id):
    countries = []
    actor_details_url = f'https://api.themoviedb.org/3/person/{actor_id}?api_key={API_KEY}'
    response = requests.get(actor_details_url)
    if response.status_code == 200:
        actor_details = response.json()
        place_of_birth = actor_details.get('place_of_birth', '')
        if place_of_birth:
            # Extract only the country from the place_of_birth field
            country = place_of_birth.split(",")[-1].strip()
            countries.append(country)
    return countries

# List of endpoints for retrieving popular, top-rated, and upcoming movies
endpoints = [
    f'https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}&language=en-US&page=1',
    f'https://api.themoviedb.org/3/movie/top_rated?api_key={API_KEY}&language=en-US&page=1',
    f'https://api.themoviedb.org/3/movie/upcoming?api_key={API_KEY}&language=en-US&page=1'
]

# Open CSV file for writing movie-country and actor-country associations
with open('countries.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['tmdb_id', 'country']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Send GET requests to the API endpoints
    for endpoint in endpoints:
        response = requests.get(endpoint)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Extract movie data from the response
            movie_data = response.json()['results']

            # Iterate over the movies
            for movie in movie_data:
                # Extract relevant information for each movie
                tmdb_id = movie['id']
                
                # Extract countries associated with the movie
                countries = extract_actor_countries(tmdb_id)

                # Write data to CSV file
                for country in countries:
                    writer.writerow({'tmdb_id': tmdb_id, 'country': country})
        else:
            # Print error message if request for movie data was not successful
            print('Error:', response.status_code)

    # Send GET request to retrieve popular actors
    popular_actors_url = f'https://api.themoviedb.org/3/person/popular?api_key={API_KEY}&language=en-US&page=1'
    response = requests.get(popular_actors_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Extract actor data from the response
        actor_data = response.json()['results']

        # Iterate over the actors
        for actor in actor_data:
            # Extract relevant information for each actor
            tmdb_id = actor['id']
            
            # Extract countries associated with the actor
            countries = extract_actor_countries(tmdb_id)

            # Write data to CSV file
            for country in countries:
                writer.writerow({'tmdb_id': tmdb_id, 'country': country})
    else:
        # Print error message if request for actor data was not successful
        print('Error:', response.status_code)
