from django.http                  import JsonResponse
from django.db.models             import Q, Count
from django.views                 import View
from petsitters.models            import Petsitter, Type
from bookings.models              import Booking 

class PetsitterListView(View):
    def get(self, request):
        sort_by      = request.GET.get('sort_by', 'price')
        check_in     = request.GET.get('check_in', "2022-01-01")
        check_out    = request.GET.get('check_out', "2022-12-31")
        keyword      = request.GET.get('keyword', "")

        pick_up      = request.GET.get('pick_up', None)
        another_pet  = request.GET.get('another_pet', None)
        yard         = request.GET.get('yard', None)

        offset       = int(request.GET.get('offset', 0))
        limit        = int(request.GET.get('limit', 10))

        sorting_options = {
            "low_price" : "price"
        }

        # Booking_period  = Booking.objecs.filter(
        #     check_in_gte  = check_in,
        #     check_out_lte = check_out
        # )
        # available_petsitter_list = set(available_petsitter.petsitter_id for available_petsitter in Booking_period)[offset : offset + limit]

        q = Q()

        if another_pet:
            q &= Q(another_pet = another_pet)
        
        if pick_up:
            q &= Q(pick_up = pick_up)

        if yard:
            q &= Q(yard = yard)

        if keyword:
            q &= Q(pettisitter_address__icontains = keyword)
        
        # q &= Q(id__in = available_petsitter_list)
        
        petsitters = Petsitter.objects.annotate(comment_count = Count('comment__id')).all()\
                                                    .filter(q).order_by(sorting_options.get(sort_by, "price"))[offset : offset+limit]

        results = [{           
            "id"               : petsitter.id, 
            "titile"           : petsitter.title,
            "price"            : int(petsitter.price),
            "grade"            : petsitter.grade,
            "type"             : [{
                "type_id"      : petsitter.type.id,
                "type_name"    : petsitter.type.name,
                } for petsitter_type in petsitters.types.all()],
            "information"      : petsitter.information,
            "address"          : petsitter.address,
            "petsitter_image"  : [image.petsitter_image_url for image in petsitters.petsitter_images.all()]
        } for petsitter in petsitters]
        return JsonResponse({"result" : results}, status=200)

class PetsitterDetailView(View):
    def get(self, request,petsitter_id):
        try:
            petsitter = Petsitter.objects.get(id__in=petsitter_id)

            result    = {
                "id"               : petsitter.id, 
                "name"             : petsitter.name,
                "titile"           : petsitter.title,
                "price"            : int(petsitter.price),
                "grade"            : petsitter.grade,
                "count"            : petsitter.count,
                "type"             : [{
                    "type_id"      : petsitter.type.id,
                    "type_name"    : petsitter.type.name,
                    } for petsitter_type in petsitter.type.all()],
                "information"      : petsitter.information,
                "address"          : petsitter.address,
                "longitude"        : float(petsitter.longitude),
                "latitude"         : float(petsitter.latitude),
                "petsitter_image"  : [image.petsitter_image_url for image in petsitter.petsitter_images.all()]
            }
            return JsonResponse({"message" : result}, status=200)

        except petsitter.DoesNotExist:
            return JsonResponse({"message" : "PETSITTER DOES NOT EXIST"}, status=404)
        
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)