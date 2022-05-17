from datetime import timedelta
from django.http      import JsonResponse
from django.db.models import Q, Count
from django.views     import View

from petsitters.models import Petsitter, Type, PetsitterImage
from bookings.models   import Booking 

class PetsitterListView(View):
    def get(self, request):
        sort_by   = request.GET.get('sort_by')
        check_in  = request.GET.get('check_in', None)
        check_out = request.GET.get('check_out', None)
        keyword   = request.GET.get('keyword', "")
        type_id   = request.GET.get('type_id', None)
        offset    = int(request.GET.get('offset', 0))
        limit     = int(request.GET.get('limit', 10))

        sorting_options = {
            "low_price"      : "price", 
            "many_comments"  : "-comment_count"        
        }

        if check_in or check_out:
            return JsonResponse({"message" : "Ivalid Input"}, status=400)
        # 이미 예약된 조건
        q_booking = Q(checkout_data__range=[check_in+timedelta(days=1), check_out]) | \
                    Q(checkin_date__range=[check_in, check_out-timedelta(days=1)])
        # 이미 예약이 되서 불가능한 예약 리스트
        booked_list = Booking.objects.filter(q_booking)

        q = Q()

        if type_id :
            q &= Q(types__id = type_id)

        if keyword:
            q &= Q(address__icontains = keyword)
        
        petsitters = Petsitter.objects\
                              .annotate(comment_count = Count('comment__id'))\
                              .exclude(booking__in=booked_list)\
                              .filter(q)\
                              .order_by(sorting_options.get(sort_by, "id"))[offset : offset+limit]

        results = [{           
            "id"              : petsitter.id, 
            "titile"          : petsitter.title,
            "price"           : int(petsitter.price),
            "grade"           : petsitter.grade,
            "type"            : [type.name for type in petsitter.type.all()],
            "information"     : petsitter.information,
            "address"         : petsitter.address,
            "petsitter_image" : [petsitter_image.petsitter_image_url for petsitter_image in petsitter.petsitterimage_set.all()]
        } for petsitter in petsitters]
        return JsonResponse({"result" : results}, status=200)

class PetsitterDetailView(View):
    def get(self, request, petsitter_id):
        try:
            petsitter = Petsitter.objects.get(id=petsitter_id)

            result    = {
                "id"              : petsitter.id, 
                "name"            : petsitter.name,
                "titile"          : petsitter.title,
                "price"           : int(petsitter.price),
                "grade"           : petsitter.grade,
                "count"           : petsitter.count,
                "type"            : [type.name for type in petsitter.type.all()],
                "information"     : petsitter.information,
                "address"         : petsitter.address,
                "longitude"       : float(petsitter.longitude),
                "latitude"        : float(petsitter.latitude),
                "petsitter_image" : [petsitterimage.petsitter_image_url for petsitterimage in petsitter.petsitterimage_set.all()]
            }
            return JsonResponse({"message" : result}, status=200)

        except petsitter.DoesNotExist:
            return JsonResponse({"message" : "PETSITTER DOES NOT EXIST"}, status=404)
        
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)