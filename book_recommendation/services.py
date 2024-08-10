from . models import BookRecommendation, UserInteraction

class BookRecommendationService:
    
        @staticmethod
        def get_all_books():
            return BookRecommendation.objects.all()
    
        @staticmethod
        def get_book_by_id(book_id):
            return BookRecommendation.objects.get(id=book_id)
    
class UserInteractionService:  

    @staticmethod
    def get_all_interactions():
        return UserInteraction.objects.all()
    
    @staticmethod
    def filter_user_interactions_by_user_id(user_id):
        return UserInteraction.objects.filter(user_id=user_id)
    
    @staticmethod
    def filter_interaction_by_book_id_and_like(book_id, liked):
        return UserInteraction.objects.filter(book_id=book_id, liked=liked)

    @staticmethod
    def filter_interaction_by_user_id_and_book_id(user_id, book_id):
        return UserInteraction.objects.filter(user_id=user_id, book_id=book_id)
