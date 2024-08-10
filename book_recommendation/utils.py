from rest_framework_simplejwt.tokens import AccessToken
from user.services import UsersService

def decode_access_token(access_token):
    payload = AccessToken(access_token).payload
    return payload

def get_user_from_token(request):
    token = request.headers['Authorization'].split(' ')[1]
    payload = decode_access_token(token)
    return UsersService.get_user_by_id(payload['user_id'])