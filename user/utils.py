import jwt

from django.http import JsonResponse
from wiso.settings import SECRET_KEY
from .models import User


def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization', None)
            payload = jwt.decode(access_token, SECRET_KEY, algorithm='HS256')
            user = User.objects.get(id=payload["id"])
            request.user = user
        except jwt.DecodeError:
            return JsonResponse({'message': 'INVALID_TOKEN'}, status=401)
        except User.DoesNotExist:
            return JsonResponse({'message': 'INVALID_USER'}, status=400)
        except TypeError:
            return JsonResponse({'message': 'INVALID_VALUE'}, status=400)
        except KeyError:
            return JsonResponse({'message': 'INVALID'}, status=400)
        return func(self, request, *args, **kwargs)

    return wrapper
