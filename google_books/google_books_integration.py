import os
import requests


class GoogleBooksAPI:
    BASE_URL = "https://www.googleapis.com/books/v1/volumes"
    API_KEY = os.getenv('GOOGLE_API_KEY')

    @staticmethod
    def fetch_books(query):
        url = f"{GoogleBooksAPI.BASE_URL}?q={query}&key={GoogleBooksAPI.API_KEY}"
        with requests.Session() as session:
            try:
                response = session.get(url)
                response.raise_for_status()
                return response.json().get('items', [])
            except requests.exceptions.HTTPError as http_err:
                raise ValueError(f"HTTP error occurred: {http_err}")
            except Exception as err:
                raise ValueError(f"An error occurred: {err}")

    @staticmethod
    def extract_book_data(items):
        return [
            {
                "title": item.get('volumeInfo', {}).get('title'),
                "author": item.get('volumeInfo', {}).get('authors', []),
                "description": item.get('volumeInfo', {}).get('description'),
                "cover_image": item.get('volumeInfo', {}).get('imageLinks', {}).get('thumbnail'),
                "ratings": item.get('volumeInfo', {}).get('averageRating')
            }
            for item in items
        ]