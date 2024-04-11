import csv
import requests

# Replace 'YOUR_API_KEY' with your actual API key
API_KEY = 'f14c370921f887539a7a21ae5e833689'
WATCHMODE_API_KEY = 'IBmIzjjq0A0QgCv9nb27hIgvyMjSSaC304R8L74T'

# List of endpoints for retrieving popular, top-rated, and upcoming movies
endpoints = [
    f'https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}&language=en-US&page=1',
    f'https://api.themoviedb.org/3/movie/top_rated?api_key={API_KEY}&language=en-US&page=1',
    f'https://api.themoviedb.org/3/movie/upcoming?api_key={API_KEY}&language=en-US&page=1'
]

# Open a file for writing CSV data
with open("movies.csv", "w", newline='', encoding="utf-8") as csvfile:
    fieldnames = ['tmdb_id', 'imdb_id', 'title', 'description', 'content_rating_id', 'rating', 'release_year', 'watchmode_id', 'num_reviews', 'aka', 'language']
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
                title = movie['title']
                description = movie['overview']
                release_year = int(movie['release_date'].split('-')[0]) if movie['release_date'] else None
                rating = movie['vote_average']
                language = movie['original_language']  # Extracting language
                # Add dummy values for other fields as they are not provided by the API
                imdb_id = f'tt{tmdb_id}'  # Assuming tmdb_id as imdb_id
                content_rating_id = 1  # Assuming unique content rating id for each movie
                watchmode_id = 0  # Placeholder for watchmode_id
                num_reviews = movie.get('vote_count', 0)  # Number of reviews
                aka = movie.get('original_title', '')  # Alternate title
                
                # Fetch watchmode data to get watchmode_id
                watchmode_url = f'https://api.watchmode.com/v1/title/movie/imdb_id/{imdb_id}/sources/free?apiKey={WATCHMODE_API_KEY}'
                watchmode_response = requests.get(watchmode_url)
                
                if watchmode_response.status_code == 200:
                    watchmode_data = watchmode_response.json()
                    if watchmode_data and 'title_id' in watchmode_data:
                        watchmode_id = watchmode_data['title_id']
                
                # Write movie data to CSV
                writer.writerow({
                    'tmdb_id': tmdb_id,
                    'imdb_id': imdb_id,
                    'title': title,
                    'description': description,
                    'content_rating_id': content_rating_id,
                    'rating': rating,
                    'release_year': release_year,
                    'watchmode_id': watchmode_id,
                    'num_reviews': num_reviews,
                    'aka': aka,
                    'language': language  # Adding language to the CSV row
                })
        else:
            # Print error message if request was not successful
            print('Error:', response.status_code)
