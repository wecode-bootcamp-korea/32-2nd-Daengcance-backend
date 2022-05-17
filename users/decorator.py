import jwt

from django.http import JsonResponse
from daengcance.settings import ALGORITHM, SECRET_KEY
from users.models import User

def log_in_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization')
            payload      = jwt.decode(access_token, SECRET_KEY, algorithms=ALGORITHM)
            request.user = User.objects.get(id=payload['id'])

            return func(self, request, *args, **kwargs)

        except User.DoesNotExist:
            return JsonResponse({'message' : 'invalid_user'}, status=401)
        except jwt.InvalidSignatureError:
            return JsonResponse({'message' : 'invalid_signature'}, status=401)
        except jwt.DecodeError:
            return JsonResponse({'message' : 'invalid_payload'}, status=401)

    return wrapper