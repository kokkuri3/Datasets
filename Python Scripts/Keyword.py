import requests
import csv

# Replace 'YOUR_API_KEY' with your actual API key
API_KEY = 'f14c370921f887539a7a21ae5e833689'

# Function to fetch movie keywords
def fetch_movie_keywords(movie_id):
    keywords_url = f'https://api.themoviedb.org/3/movie/{movie_id}/keywords?api_key={API_KEY}'
    response = requests.get(keywords_url)
    if response.status_code == 200:
        keywords_data = response.json().get('keywords', [])
        keywords = [keyword['name'] for keyword in keywords_data]
        return keywords
    else:
        print(f'Error fetching keywords for movie with ID {movie_id}')
        return []

# List of endpoints for retrieving popular, top-rated, and upcoming movies
endpoints = [
    f'https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}&language=en-US&page=1',
    f'https://api.themoviedb.org/3/movie/top_rated?api_key={API_KEY}&language=en-US&page=1',
    f'https://api.themoviedb.org/3/movie/upcoming?api_key={API_KEY}&language=en-US&page=1'
]

# Open CSV file for writing movie-keyword associations
with open('keywords.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['tmdb_id', 'keyword']
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
                
                # Fetch keywords associated with the movie
                keywords = fetch_movie_keywords(tmdb_id)

                # Write data to CSV file
                for keyword in keywords:
                    writer.writerow({'tmdb_id': tmdb_id, 'keyword': keyword})
        else:
            # Print error message if request for movie data was not successful
            print('Error:', response.status_code)
