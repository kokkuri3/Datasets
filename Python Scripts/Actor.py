import csv
import requests

# Replace 'YOUR_API_KEY' with your actual API key
API_KEY = 'f14c370921f887539a7a21ae5e833689'

# Define function to extract actors and movie IDs from movie credits
def extract_actors_and_movies(credits, movie_id):
    actors_and_movies = []
    for person in credits.get('cast', []):
        # Split the name into first name and last name
        name_parts = person['name'].split()
        first_name = name_parts[0] if name_parts else ''
        last_name = name_parts[-1] if len(name_parts) > 1 else ''

        # Extract the TMDB ID of the actor
        tmdb_id = person['id']

        # Append the first name, last name, TMDB ID, and movie ID to the list
        actors_and_movies.append({
            'first_name': first_name,
            'last_name': last_name,
            'tmdb_id': tmdb_id,
            'movie_id': movie_id,
        })
    return actors_and_movies

# List of endpoints for retrieving popular, top-rated, and upcoming movies
endpoints = [
    f'https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}&language=en-US&page=1',
    f'https://api.themoviedb.org/3/movie/top_rated?api_key={API_KEY}&language=en-US&page=1',
    f'https://api.themoviedb.org/3/movie/upcoming?api_key={API_KEY}&language=en-US&page=1'
]

# Open CSV file for writing
with open('actors.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['first_name', 'last_name', 'tmdb_id', 'movie_id']
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
                movie_id = movie['id']

                # Fetch credits data to get information about actors
                credits_url = f'https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={API_KEY}'
                credits_response = requests.get(credits_url)

                if credits_response.status_code == 200:
                    credits_data = credits_response.json()
                    actors_and_movies = extract_actors_and_movies(credits_data, movie_id)

                    # Write data to CSV file
                    writer.writerows(actors_and_movies)
                else:
                    # Print error message if request for credits was not successful
                    print('Error:', credits_response.status_code)
        else:
            # Print error message if request for movie data was not successful
            print('Error:', response.status_code)
