
import json, uuid

from datetime         import datetime, timedelta
from django.db.models import Q
from django.db        import transaction
from django.http      import JsonResponse
from django.views     import View

from petsitters.models import Petsitter
from bookings.models   import Booking

from users.decorator import log_in_decorator

class BookingView(View):
    @log_in_decorator
    def post(self, request, petsitter_id):
            data          = json.loads(request.body)
            checkin_date  = datetime.strptime(data['checkin_date'],'%Y-%m-%d')
            checkout_date = datetime.strptime(data['checkout_date'],'%Y-%m-%d')
            
            if checkin_date < datetime.today() :
                return JsonResponse({'message' : 'NO_WAY_TO_BOOK_BEFORE_TODAY'}, status=400)
            
            if checkout_date < checkin_date :
                return JsonResponse({'message' : 'INVALID_BOOKING_DATE'}, status=400)
            
            #이미 예약된 조건 
            q = Q() 
            q |= Q(check_in__range  = [checkin_date,checkout_date-timedelta(days=1)])
            q |= Q(check_out__range = [checkin_date+timedelta(days=1),checkout_date])

            #이미 예약이 되서 불가능한 예약 리스트
            #booked_list = Booking.objects.filter(q)
            
            if Booking.objects.filter(q, petsitter_id = petsitter_id, user=request.user).exists():
                return JsonResponse({'message' : 'DOUBLE_BOOKED_FOR_THE_DAY'}, status=400)

            petsitter = Petsitter.objects.get(id=petsitter_id)

            with transaction.atomic():
            
            booking = Booking.objects.create(
                booking_code  = str(uuid.uuid4()),
                checkin_date  = checkin_date,
                checkout_date = checkout_date,
                user_id       = request.user,
                petsitter     = petsitter
                #booking_status_id = 1  ?
            )

            for i in range(int((checkin_date-checkin_date)))

            #if date not in petsitter.petsitter_schedule

            return JsonResponse({'message': 'SUCCESS'}, status=201)
