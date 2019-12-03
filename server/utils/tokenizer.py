# TODO: Make this a secure key and in a enviroment variable
_SECRET_KEY = "holakase"

from itsdangerous import (
    TimedJSONWebSignatureSerializer as Serializer,
    BadSignature,
    SignatureExpired,
)

# TODO: Change expiration time when in production
def generate_auth_token(user_id, expiration=600000):
    s = Serializer(_SECRET_KEY, expires_in=expiration)
    return s.dumps({"id": user_id})


def verify_auth_token(token):
    s = Serializer(_SECRET_KEY)
    try:
        user = s.loads(token)
    except SignatureExpired:
        print("[!] Invalid token: SignatureExpired")
        raise SignatureExpired  # valid token, but expired
    except BadSignature:
        print("[!] Invalid token: BadSignature")
        raise BadSignature  # invalid token
    return user
