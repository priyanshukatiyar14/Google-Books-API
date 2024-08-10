from . models import Users

class UsersService:

    @staticmethod
    def get_user_by_email(email):
        return Users.objects.filter(email=email).first()
    
    @staticmethod
    def get_user_by_id(user_id):
        return Users.objects.get(id=user_id)
    
    @staticmethod
    def get_all_users():
        return Users.objects.all()