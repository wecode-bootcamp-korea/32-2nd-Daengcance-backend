import json

from django.views import View
from django.http  import JsonResponse, HttpResponse

from users.models      import User
from petsitters.models import Petsitter
from reviews.models    import Review
from users.decorator   import log_in_decorator

class ReviewView(View):
    @log_in_decorator
    def post(self, request):
        try:
            data         = json.loads(request.body)
            user         = request.user
            content      = data.get('content', None)
            petsitter_id = data["petsitter_id"]

            if not Petsitter.objects.filter(id=petsitter_id).exists():
                return JsonResponse({'message' : 'PETSITTER_DOES_NOT_EXIST'}, status=400)
            
            Petsitter = Petsitter.objects.get(id=petsitter_id)

            Review.objects.create(
                content           = content,
                user_nickname     = user.nickname,
                petsitter_name    = Petsitter.name,
                petsitter_address = Petsitter.address,
            )

            return JsonResponse({'message':'CREATE_REVIEW'}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'message':'JSON_DECODE_ERROR'})

    def get(self, request, petsitter_id):
        if not Petsitter.objects.filter(id=petsitter_id).exists():
            return JsonResponse({'message':'PETSITTER_DOES_NOT_EXIST'}, status=404)

        review_list = [{
            'id'                : review.id,
            'content'           : review.content,
            'review_image'      : review.review_image_set.review_image_url,
            'user_nickname'     : review.user.nickname, 
            'petsitter_name'    : review.petsitter.name,
            'petsitter_address' : review.petsitter.address
            } for review in Review.objects.filter(petsitter_id=petsitter_id)
        ]
        return JsonResponse({'result' : review_list}, status=200)

    @log_in_decorator
    def delete(self, request, petsitter_id, review_id):
        user = request.user

        if not Review.objects.filter(id=review_id, petsitter_id=petsitter_id, user=user).exists():
            return JsonResponse({'message':'REVIEW_DOES_NOT_EXIST'}, status=404)

        Review.objects.get(id=review_id, petsitter_id=petsitter_id, user=user).delete()
        return JsonResponse({'message':'SUCCESS'}, status=204)