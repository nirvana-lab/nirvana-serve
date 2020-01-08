import jwt
from openapi.service.user import check_user_valid
from openapi.utils.exception_handle import DefalutError

JWT_SIGN = 'nirvana'

def generate_jwt_token(username, uid):

    paylaod = {
        'username': username,
        'uid': str(uid)
    }
    headers = {
        'typ': 'jwt',
        'alg': 'HS256'
    }
    jwt_token = jwt.encode(payload=paylaod, key=JWT_SIGN, algorithm='HS256', headers=headers).decode('utf-8')
    return jwt_token

def check_token(token):
    try:
        payload = jwt.decode(token, JWT_SIGN, True)
    except Exception:
        raise  DefalutError(title=f'token不合法', detail=f'token不合法', status=401, type='AuthError')
    user = payload.get('username')
    uid = payload.get('uid')
    if check_user_valid(user, uid):
        return user