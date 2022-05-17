import json, re

from json.decoder import JSONDecodeError

from django.views import View
from django.http  import JsonResponse, HttpResponse

from users.models      import User
from petsitters.models import Petsitter
from reviews.models    import Review

from users.decorator import log_in_decorator

class ReviewView(View):
    @log_in_decorator
    def post(self, request, petsitter_id):
        try:
            data = json.loads(request.body)
            user = request.user
            content = data.get('content', None)
            reviews  = Review.objects.filter(petsitter_id=petsitter_id)

            if not Petsitter.objects.filter(id=petsitter_id).exists():
                return JsonResponse({'message' : 'PETSITTER_DOES_NOT_EXIST'}, status=400)
            
            Review.objects.create(
                content           = content,
                review_image      = reviews.review_image_set.review_image_url,
                user_nickname     = user.nickname,
                petsitter_name    = petsitter_id.name,
                petsitter_address = petsitter_id.address,
                )

            return JsonResponse({'message':'CREATE_REVIEW'}, status=201)
        except JSONDecodeError:
            return JsonResponse({'message':'JSON_DECODE_ERROR'})

    def get(self, request, petsitter_id):
        if not Review.objects.filter(id=petsitter_id).exists():
            return JsonResponse({'message':'REVIEW_DOES_NOT_EXIST'}, status=400)

        review_list = [{
            'id'                : review.id,
            'content'           : review.content,
            'review_image'      : review.review_image_set.review_image_url,
            'user_nickname'     : User.objects.get(id=review.user.id).nickname, 
            'petsitter_name'    : Petsitter.objects.get(id=petsitter_id).name,
            'petsitter_address' : Petsitter.objects.get(id=petsitter_id).address
            } for review in Review.objects.filter(petsitter_id=petsitter_id)
            ]

    @log_in_decorator
    def delete(self, request, petsitter_id, review_id):
        user_id = request.user.id
        petsitter_id = petsitter_id

        if not Review.objects.filter(id=review_id, petsitter_id=petsitter_id, user_id=user_id).exists():
            return JsonResponse({'message':'REVIEW_DOES_NOT_EXIST'}, status=404)

        Review.objects.filter(id=review_id, petsitter_id=petsitter_id, user_id=user_id).first().delete()
        return JsonResponse({'message':'SUCCESS'}, status=204)