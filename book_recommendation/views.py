from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import BookRecommendationSerializer, UserInteractionPostSerializer
from . models import BookRecommendation, UserInteraction
from .utils import decode_access_token
from user.models import Users
from rest_framework.permissions import IsAuthenticated
from django.forms.models import model_to_dict

class BookRecommendationAPIViews(ListCreateAPIView):
    queryset = BookRecommendation.objects.all()
    serializer_class = BookRecommendationSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        
        payload=decode_access_token(request.headers['Authorization'].split(' ')[1])
        request.data['submitted_by']=payload['user_id']
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

        queryset = queryset.order_by(sort_by)

        recommended_books = BookRecommendationSerializer(queryset, many=True).data

        for book in recommended_books:
            book['total_likes'] = UserInteraction.objects.filter(book_id=book['id'], liked=True).count()
            book['comments'] = UserInteraction.objects.filter(book_id=book['id'], comment__isnull=False).count()
            book['comment_list'] = [interaction['comment'] for interaction in UserInteraction.objects.filter(book_id=book['id'], comment__isnull=False).values('comment')]

        return Response(recommended_books, status=status.HTTP_200_OK)
    
class BookRecommendationModifyAPIViews(RetrieveUpdateDestroyAPIView):
    queryset = BookRecommendation.objects.all()
    serializer_class = BookRecommendationSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
    
    
class UserInteractionAPIViews(ListCreateAPIView):
    serializer_class = UserInteractionPostSerializer
    queryset=UserInteraction.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        payload = decode_access_token(request.headers['Authorization'].split(' ')[1])
        user_id = payload['user_id']
        request.data['user'] = Users.objects.get(id=user_id)

        if 'book_id' not in request.data:
            return Response({'error': 'book_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        book_id = request.data['book_id']

        existing_interaction = UserInteraction.objects.filter(book_id=book_id, user_id=user_id).first()

        if existing_interaction:
            if existing_interaction.liked == request.data['liked']:
                return Response({"error": "User interaction already exists"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                existing_interaction.liked = request.data['liked']
                existing_interaction.comment = request.data.get('comment', existing_interaction.comment)
                existing_interaction.save()
                interaction_dict = model_to_dict(existing_interaction)
                return Response(interaction_dict, status=status.HTTP_200_OK)

        request.data['book'] = BookRecommendation.objects.get(id=book_id)
        interaction_instance = UserInteraction(**request.data)
        interaction_instance.save()
        interaction_dict = model_to_dict(interaction_instance)
        return Response(interaction_dict, status=status.HTTP_201_CREATED)
    
    def get(self, request, *args, **kwargs):
        payload=decode_access_token(request.headers['Authorization'].split(' ')[1])
        user_id=payload['user_id']
        interactions=UserInteraction.objects.filter(user_id=user_id).values('book_id', 'liked', 'comment')
        return Response(list(interactions), status=status.HTTP_200_OK)


