from django.test  import TestCase, Client

from users.models      import User
from petsitters.models import Petsitter, PetsitterType, Type, PetsitterImage, Comment

class PetsitterListTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.maxDiff = None
        User.objects.bulk_create([
            User(
                id         = 1,
                name       = '유리한',
                kakao_id   = '111',
                nickname   = 'fjkhsfjkhsdfiouw',
            ),
            User(
                id         = 2,
                name       = '우리가',
                kakao_id   = '121',
                nickname   = 'dfjkhsfkjhsdf',
            ),
            User(
                id         = 3,
                name       = '박수쳐',
                kakao_id   = '123',
                nickname   = 'sakdhjkjf',
            )
            ]
        )

        Petsitter.objects.bulk_create([
            Petsitter(
                id              = 1,
                name            = '잘봐요',
                title           = '우리는 팻플래닛 대표',
                price           = 30000,
                grade           = '프로',
                count           = 0,
                information     = '누구보다 아이들을 잘 돌볼 수 있습니다.',
                address         = '서울시 강남구 논현동',
                longitude       = 34.123223,
                latitude        = 231.123111
            ),
            Petsitter(
                id              = 2,
                name            = '무비중',
                title           = '우리는 팻플래닛 대표',
                price           = 30000,
                grade           = '일반',
                count           = 0,
                information     = '누구보다 아이들을 잘 돌볼 수 있습니다.',
                address         = '서울시 강남구 논현동',
                longitude       = 34.123223,
                latitude        = 231.123111
            ),
            Petsitter(
                id              = 3,
                name            = '착실한',
                title           = '우리는 팻플래닛 대표',
                price           = 30000,
                grade           = '프로',
                count           = 0,
                information     = '누구보다 아이들을 잘 돌볼 수 있습니다.',
                address         = '서울시 강남구 논현동',
                longitude       = 34.123223,
                latitude        = 231.123111
            )]
        )

        Type.objects.bulk_create([
            Type(
                id   = 1,
                name = '마당 있음'
            ),

            Type(
                id   = 2,
                name = '픽업 가능'
            ),

            Type(
                id   = 3,
                name = '애완동물 없음'
            )]
        )

        PetsitterType.objects.bulk_create([
            PetsitterType(
                id           = 1,
                petsitter_id = 1,
                type_id      = 1
            ),
            PetsitterType(
                id           = 2,
                petsitter_id = 2,
                type_id      = 1
            ),
            PetsitterType(
                id           = 3,
                petsitter_id = 3,
                type_id      = 1
            )]
        )

        PetsitterImage.objects.bulk_create([
            PetsitterImage(
                id           = 1,
                petsitter_id = 1,
                image_url = ['https://github.com/nathanyoon1212/asds/blob/master/1-1.jpg?raw=true']
            ),
            PetsitterImage(
                id           = 2,
                petsitter_id = 2,
                image_url = ['https://github.com/nathanyoon1212/asds/blob/master/1-1.jpg?raw=true']
            ),
            PetsitterImage(
                id           = 3,
                petsitter_id = 3,
                image_url = ['https://github.com/nathanyoon1212/asds/blob/master/1-1.jpg?raw=true']
            )]
        )


        Comment.objects.bulk_create([
            Comment(
                id           = 1,
                content      = '감사합니다.',
                petsitter_id = 1,
                user_id      = 1
            ),
            Comment(
                id           = 2,
                content      = '감사합니다.',
                petsitter_id = 2,
                user_id      = 2
            ),
            Comment(
                id           = 3,
                content      = '감사합니다.',
                petsitter_id = 3,
                user_id      = 3
            )]
        )

    def tearDown(self):
        User.objects.all().delete()
        PetsitterType.objects.all().delete()
        Petsitter.objects.all().delete()
        Type.objects.all().delete()
        PetsitterImage.objects.all().delete()
        Comment.objects.all().delete()        

    def test_petsitter_list_view_get_method_success(self):    
        response = self.client.get('/petsitters/list')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),{ 
            "results": [
                {
                    "id"              : 1,
                    "title"           : '우리는 팻플래닛 대표',
                    "price"           : 30000,
                    "grade"           : '프로',
                    "type"            : ['마당 있음'],
                    "information"     : '누구보다 아이들을 잘 돌볼 수 있습니다.',
                    "address"         : '서울시 강남구 논현동',
                    "comment_count"   : 1,
                    "petsitter_image" : ["['https://github.com/nathanyoon1212/asds/blob/master/1-1.jpg?raw=true']"]                    
                },
                {
                    "id"              : 2,
                    "title"           : '우리는 팻플래닛 대표',
                    "price"           : 30000,
                    "grade"           : '일반',
                    "type"            : ['마당 있음'],
                    "information"     : '누구보다 아이들을 잘 돌볼 수 있습니다.',
                    "address"         : '서울시 강남구 논현동',
                    "comment_count"   : 1,
                    "petsitter_image" : ["['https://github.com/nathanyoon1212/asds/blob/master/1-1.jpg?raw=true']"]                  
                },
                {
                    "id"              : 3,
                    "title"           : '우리는 팻플래닛 대표',
                    "price"           : 30000,
                    "grade"           : '프로',
                    "type"            : ['마당 있음'],
                    "information"     : '누구보다 아이들을 잘 돌볼 수 있습니다.',
                    "address"         : '서울시 강남구 논현동',
                    "comment_count"   : 1,
                    "petsitter_image" : ["['https://github.com/nathanyoon1212/asds/blob/master/1-1.jpg?raw=true']"]                  
                }
            ]
        })

    def test_petsitter_list_view_get_method_all_filters_success(self):    
        response = self.client.get('/petsitters/list?sort_by=low_price&sort_by=many_comments&type_id=1&keyword=논현동')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "results": [
                {
                    "id"              : 1,
                    "title"           : '우리는 팻플래닛 대표',
                    "price"           : 30000,
                    "grade"           : '프로',
                    "type"            : ['마당 있음'],
                    "information"     : '누구보다 아이들을 잘 돌볼 수 있습니다.',
                    "address"         : '서울시 강남구 논현동',
                    "comment_count"   : 1,
                    "petsitter_image" : ["['https://github.com/nathanyoon1212/asds/blob/master/1-1.jpg?raw=true']"]                   
                },
                {
                    "id"              : 2,
                    "title"           : '우리는 팻플래닛 대표',
                    "price"           : 30000,
                    "grade"           : '일반',
                    "type"            : ['마당 있음'],
                    "information"     : '누구보다 아이들을 잘 돌볼 수 있습니다.',
                    "address"         : '서울시 강남구 논현동',
                    "comment_count"   : 1,
                    "petsitter_image" : ["['https://github.com/nathanyoon1212/asds/blob/master/1-1.jpg?raw=true']"]                 
                },
                {
                    "id"              : 3,
                    "title"           : '우리는 팻플래닛 대표',
                    "price"           : 30000,
                    "grade"           : '프로',
                    "type"            : ['마당 있음'],
                    "information"     : '누구보다 아이들을 잘 돌볼 수 있습니다.',
                    "address"         : '서울시 강남구 논현동',
                    "comment_count"   : 1,
                    "petsitter_image" : ["['https://github.com/nathanyoon1212/asds/blob/master/1-1.jpg?raw=true']"]                  
                }
            ]

        })

class DetailTest(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.client = Client()
        User.objects.bulk_create([
            User(
                id         = 1,
                name       = '유리한',
                kakao_id   = '111',
                nickname   = 'fjkhsfjkhsdfiouw',
            ),
            User(
                id         = 2,
                name       = '우리가',
                kakao_id   = '121',
                nickname   = 'dfjkhsfkjhsdf',
            ),
            User(
                id         = 3,
                name       = '박수쳐',
                kakao_id   = '123',
                nickname   = 'sakdhjkjf',
            )
            ]
        )

        Petsitter.objects.bulk_create([
            Petsitter(
                id              = 1,
                name            = '잘봐요',
                title           = '우리는 팻플래닛 대표',
                price           = 30000,
                grade           = '프로',
                count           = 0,
                information     = '누구보다 아이들을 잘 돌볼 수 있습니다.',
                address         = '서울시 강남구 논현동',
                longitude       = 34.123223,
                latitude        = 231.123111
            ),
            Petsitter(
                id              = 2,
                name            = '무비중',
                title           = '우리는 팻플래닛 대표',
                price           = 30000,
                grade           = '일반',
                count           = 0,
                information     = '누구보다 아이들을 잘 돌볼 수 있습니다.',
                address         = '서울시 강남구 논현동',
                longitude       = 34.123223,
                latitude        = 231.123111
            ),
            Petsitter(
                id              = 3,
                name            = '착실한',
                title           = '우리는 팻플래닛 대표',
                price           = 30000,
                grade           = '프로',
                count           = 0,
                information     = '누구보다 아이들을 잘 돌볼 수 있습니다.',
                address         = '서울시 강남구 논현동',
                longitude       = 34.123223,
                latitude        = 231.123111
            )]
        )

        Type.objects.bulk_create([
            Type(
                id   = 1,
                name = '마당 있음'
            ),

            Type(
                id   = 2,
                name = '픽업 가능'
            ),

            Type(
                id   = 3,
                name = '애완동물 없음'
            )]
        )

        PetsitterType.objects.bulk_create([
            PetsitterType(
                id           = 1,
                petsitter_id = 1,
                type_id      = 1
            ),
            PetsitterType(
                id           = 2,
                petsitter_id = 2,
                type_id      = 1
            ),
            PetsitterType(
                id           = 3,
                petsitter_id = 3,
                type_id      = 1
            )]
        )

        PetsitterImage.objects.bulk_create([
            PetsitterImage(
                id           = 1,
                petsitter_id = 1,
                image_url = ['https://github.com/nathanyoon1212/asds/blob/master/1-1.jpg?raw=true']
            ),
            PetsitterImage(
                id           = 2,
                petsitter_id = 2,
                image_url = ['https://github.com/nathanyoon1212/asds/blob/master/1-1.jpg?raw=true']
            ),
            PetsitterImage(
                id           = 3,
                petsitter_id = 3,
                image_url = ['https://github.com/nathanyoon1212/asds/blob/master/1-1.jpg?raw=true']
            )]
        )


        Comment.objects.bulk_create([
            Comment(
                id           = 1,
                content      = '감사합니다.',
                petsitter_id = 1,
                user_id      = 1
            ),
            Comment(
                id           = 2,
                content      = '감사합니다.',
                petsitter_id = 2,
                user_id      = 2
            ),
            Comment(
                id           = 3,
                content      = '감사합니다.',
                petsitter_id = 3,
                user_id      = 3
            )]
        )

    def tearDown(self):
        User.objects.all().delete()
        PetsitterType.objects.all().delete()
        Petsitter.objects.all().delete()
        Type.objects.all().delete()
        PetsitterImage.objects.all().delete()
        Comment.objects.all().delete()


    def test_success_petsitter_detail_view_get_method(self):
        response = self.client.get('/petsitters/detail/1')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'result': {
                    "id"              : 1,
                    "name"            : '잘봐요',
                    "title"           : '우리는 팻플래닛 대표',
                    "price"           : 30000,
                    "grade"           : '프로',
                    "count"           : 0,
                    "type"            : ['마당 있음'],
                    "information"     : '누구보다 아이들을 잘 돌볼 수 있습니다.',
                    "address"         : '서울시 강남구 논현동',
                    "longitude"       : 34.123223,
                    "latitude"        : 231.123111,
                    "petsitter_image" : ["['https://github.com/nathanyoon1212/asds/blob/master/1-1.jpg?raw=true']"], 
                    }                 
                }
            )