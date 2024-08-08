from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

def decode_access_token(access_token):
    payload = AccessToken(access_token).payload
    return payload