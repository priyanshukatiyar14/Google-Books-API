import requests, os
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import BookListSerializer, BookSearchSerializer
from rest_framework.permissions import IsAuthenticated


class BookListView(ListCreateAPIView):
    serializer_class=BookListSerializer
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        book_name = request.data.get('book_name')
        
        if not book_name:
            return Response({"error": "book_name is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        url = f"https://www.googleapis.com/books/v1/volumes?q=intitle:{book_name}&key={os.getenv('GOOGLE_API_KEY')}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()  
        except requests.exceptions.HTTPError as http_err:
            return Response({"error": str(http_err)}, status=response.status_code)
        except Exception as err:
            return Response({"error": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        try:
            items = response.json().get('items', [])
            books = []
            for item in items:
                volume_info = item.get('volumeInfo', {})
                book = {
                    "title": volume_info.get('title'),
                    "author": volume_info.get('authors', []),
                    "description": volume_info.get('description'),
                    "cover_image": volume_info.get('imageLinks', {}).get('thumbnail'),
                    "ratings": volume_info.get('averageRating')
                }
                books.append(book)
        except ValueError:
            return Response({"error": "Invalid JSON response"}, status=status.HTTP_502_BAD_GATEWAY)
        
        return Response(books, status=status.HTTP_200_OK)

class BookSearchView(ListCreateAPIView):
    serializer_class = BookSearchSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        keywords = request.data.get('keywords')
        authors = request.data.get('authors')
        categories = request.data.get('categories')

        if not keywords and not authors and not categories:
            return Response({"error": "At least one search parameter (keywords, authors, or categories) is required"}, status=status.HTTP_400_BAD_REQUEST)

        query = []
        if keywords:
            query.append(f'intitle:{keywords}')
        if authors:
            query.append(f'inauthor:{authors}')
        if categories:
            query.append(f'subject:{categories}')

        query_string = '+'.join(query)
        url = f"https://www.googleapis.com/books/v1/volumes?q={query_string}&key={os.getenv('GOOGLE_API_KEY')}"

        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
            return Response({"error": str(http_err)}, status=response.status_code)
        except Exception as err:
            return Response({"error": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            items = response.json().get('items', [])
            books = []
            for item in items:
                volume_info = item.get('volumeInfo', {})
                book = {
                    "title": volume_info.get('title'),
                    "author": volume_info.get('authors', []),
                    "description": volume_info.get('description'),
                    "cover_image": volume_info.get('imageLinks', {}).get('thumbnail'),
                    "ratings": volume_info.get('averageRating')
                }
                books.append(book)
        except ValueError:
            return Response({"error": "Invalid JSON response"}, status=status.HTTP_502_BAD_GATEWAY)

        return Response(books, status=status.HTTP_200_OK)