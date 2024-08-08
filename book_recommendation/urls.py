from django.urls import path
from . views import *

urlpatterns = [
    path('recommend/', BookRecommendationAPIViews.as_view(), name='book_recommendation'),
    path('recommend/<uuid:pk>/', BookRecommendationModifyAPIViews.as_view(), name='book_recommendation_detail'),
    path('interactions/', UserInteractionAPIViews.as_view(), name='user_interactions'),
]