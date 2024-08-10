from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import BookListSerializer, BookSearchSerializer
from rest_framework.permissions import IsAuthenticated
from .google_books_integration import GoogleBooksAPI

class BookListView(CreateAPIView):
    serializer_class = BookListSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        book_name = request.data.get('book_name')
        
        if not book_name:
            return Response({"error": "book_name is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            items = GoogleBooksAPI.fetch_books(f"intitle:{book_name}")
            books = GoogleBooksAPI.extract_book_data(items)
        except ValueError as err:
            return Response({"error": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(books, status=status.HTTP_200_OK)

class BookSearchView(CreateAPIView):
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
        
        try:
            items = GoogleBooksAPI.fetch_books(query_string)
            books = GoogleBooksAPI.extract_book_data(items)
        except ValueError as err:
            return Response({"error": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(books, status=status.HTTP_200_OK)