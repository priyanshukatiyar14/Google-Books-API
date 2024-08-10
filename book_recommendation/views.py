from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import BookRecommendationSerializer, UserInteractionPostSerializer
from .utils import get_user_from_token
from rest_framework.permissions import IsAuthenticated
from django.forms.models import model_to_dict
from .models import UserInteraction
from .services import BookRecommendationService, UserInteractionService


class BookRecommendationAPIViews(ListCreateAPIView):
    queryset = BookRecommendationService.get_all_books()
    serializer_class = BookRecommendationSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = get_user_from_token(request)
        request.data['submitted_by'] = user.id
        serializer = BookRecommendationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, *args, **kwargs):
        genre = request.query_params.get('genre')
        min_rating = request.query_params.get('min_rating')
        max_rating = request.query_params.get('max_rating')
        publication_date = request.query_params.get('publication_date')
        sort_by = request.query_params.get('sort_by', 'title') 

        queryset = self.get_queryset()

        if genre:
            queryset = queryset.filter(genre__icontains=genre)
        if min_rating:
            queryset = queryset.filter(rating__gte=min_rating)
        if max_rating:
            queryset = queryset.filter(rating__lte=max_rating)
        if publication_date:
            queryset = queryset.filter(publication_date=publication_date)

        queryset = queryset.order_by(sort_by).prefetch_related('userinteraction_set')

        recommended_books = BookRecommendationSerializer(queryset, many=True).data

        for book in recommended_books:
            book_id = book['id']
            interactions = UserInteractionService.filter_interaction_by_book_id_and_like(book_id,True).count()
            book['total_likes'] = interactions.filter(liked=True).count()
            book['comments'] = interactions.filter(comment__isnull=False).count()
            book['comment_list'] = list(interactions.filter(comment__isnull=False).values_list('comment', flat=True))

        return Response(recommended_books, status=status.HTTP_200_OK)
    
class BookRecommendationModifyAPIViews(RetrieveUpdateDestroyAPIView):
    queryset = BookRecommendationService.get_all_books()
    serializer_class = BookRecommendationSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

class UserInteractionAPIViews(ListCreateAPIView):
    serializer_class = UserInteractionPostSerializer
    queryset = UserInteractionService.get_all_interactions()
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = get_user_from_token(request)
        request.data['user'] = user.id

        if 'book_id' not in request.data:
            return Response({'error': 'book_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        book_id = request.data['book_id']

        existing_interaction = UserInteractionService.filter_interaction_by_user_id_and_book_id(user.id,book_id).first()

        if existing_interaction:
            if existing_interaction.liked == request.data['liked']:
                return Response({"error": "User interaction already exists"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                existing_interaction.liked = request.data['liked']
                existing_interaction.comment = request.data.get('comment', existing_interaction.comment)
                existing_interaction.save()
                interaction_dict = model_to_dict(existing_interaction)
                return Response(interaction_dict, status=status.HTTP_200_OK)

        request.data['book'] = BookRecommendationService.get_book_by_id(book_id)
        interaction_instance = UserInteraction(**request.data)
        interaction_instance.save()
        interaction_dict = model_to_dict(interaction_instance)
        return Response(interaction_dict, status=status.HTTP_201_CREATED)
    
    def get(self, request, *args, **kwargs):
        user = get_user_from_token(request)
        interactions = UserInteractionService.filter_user_interactions_by_user_id(user.id).values('book_id', 'liked', 'comment')
        return Response(list(interactions), status=status.HTTP_200_OK)

