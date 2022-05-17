from django.http                  import JsonResponse
from django.db.models             import Q, Count
from django.views                 import View
from petsitters.models            import Petsitter, Type, PetsitterImage
from bookings.models              import Booking 

class PetsitterListView(View):
    def get(self, request):
        sort_by      = request.GET.get('sort_by', 'price')
        check_in     = request.GET.get('check_in', "2022-01-01")
        check_out    = request.GET.get('check_out', "2022-12-31")
        keyword      = request.GET.get('keyword', "")

        type_id      = request.GET.get('type_id', None)

        offset       = int(request.GET.get('offset', 0))
        limit        = int(request.GET.get('limit', 10))

        sorting_options = {
            "low_price"      : "price", 
            "many_comments"  : "-comment_count"        
        }


        # Booking_period  = Booking.objecs.filter(
        #     check_in_gte  = check_in,
        #     check_out_lte = check_out
        # )
        # available_petsitter_list = set(available_petsitter.petsitter_id for available_petsitter in Booking_period)[offset : offset + limit]

        q = Q()

        if type_id :
            q &= Q(type__in = type_id)

        if keyword:
            q &= Q(address__icontains = keyword)
        
        # q &= Q(id__in = available_petsitter_list)
        
        petsitters = Petsitter.objects.filter(q)\
                                            .order_by(sorting_options.get(sort_by, "price")).annotate(comment_count = Count('comment__id')).all()[offset : offset+limit]

        results = [{           
            "id"               : petsitter.id, 
            "titile"           : petsitter.title,
            "price"            : int(petsitter.price),
            "grade"            : petsitter.grade,
            "type"             : [type.name for type in petsitter.type.all()],
            "information"      : petsitter.information,
            "address"          : petsitter.address,
            "petsitter_image"  : [petsitterimage.petsitter_image_url for petsitterimage in petsitter.petsitterimage_set.all()]
        } for petsitter in petsitters]
        return JsonResponse({"result" : results}, status=200)

class PetsitterDetailView(View):
    def get(self,petsitter_id):
        try:
            petsitter = Petsitter.objects.get(id=petsitter_id)

            result    = {
                "id"               : petsitter.id, 
                "name"             : petsitter.name,
                "titile"           : petsitter.title,
                "price"            : int(petsitter.price),
                "grade"            : petsitter.grade,
                "count"            : petsitter.count,
                "type"             : [type.name for type in petsitter.type.all()],
                "information"      : petsitter.information,
                "address"          : petsitter.address,
                "longitude"        : float(petsitter.longitude),
                "latitude"         : float(petsitter.latitude),
                "petsitter_image"  : [petsitterimage.petsitter_image_url for petsitterimage in petsitter.petsitterimage_set.all()]
            }
            return JsonResponse({"message" : result}, status=200)

        except petsitter.DoesNotExist:
            return JsonResponse({"message" : "PETSITTER DOES NOT EXIST"}, status=404)
        
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)