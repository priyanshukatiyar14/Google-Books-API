from rest_framework import serializers


class BookListSerializer(serializers.Serializer):
    book_name = serializers.CharField(max_length=100)

class BookSearchSerializer(serializers.Serializer):
    keywords = serializers.CharField(max_length=100, required=False)
    authors = serializers.CharField(max_length=100, required=False)
    categories = serializers.CharField(max_length=100, required=False)