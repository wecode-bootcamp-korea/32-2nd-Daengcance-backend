from os import access
import jwt

from django.test import TestCase, Client
from django.conf import settings

from unittest.mock import patch
from users.models  import User
from django.conf   import settings

class KakaoSignTest(TestCase):
    def setUp(self):
        User.objects.create(
            id       = 1,
            kakao_id = #여기채워 ,
            nickname = '지수',
            email    = 'gsoosuu@gmail.com'
        )

    def tearDown(self):
        User.objects.all().delete

    @patch('users.views.requests.get')
    def test_kakao_signin_success(self, mocked_kakao_user_info):
        client = Client()

        class MockedResponse:
            def json(self):
                return {
        'id' : 1234567890,
        'properties' : {
            'nickname': '지수'
        },
        'kakao_account': {
            'profile': {
                'nickname': '지수',
                'email': 'gsoosuu@gmail.com',
            }
        }
    }

        mocked_kakao_user_info.return_value = MockedResponse()
    
        headers = {'Authorization':'FAKE_access_token'}
        response = client.get('/users/kakao', **headers)
    
        user_id = jwt.decode(response.json()['access_token'], settings.SECRET_KEY, settings.ALGORITHM)
    
        access_token = jwt.encode({'id':user_id['id']}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'REGISTERED_USER', 'access_token': access_token})

        @patch('users.views.requests.get')
        def test_kakao_signup_success(self, mocked_kakao_user_info):
            client = Client()

            class MockedResponse:
                def json(self):
                    return {
            'id': 121212121,
            'properties': {
                'nickname': '현정',
                'email': 'gsoosuu@gmail.com'
            }
        }

        mocked_kakao_user_info.return_value = MockedResponse()

        headers = {'Authorization': 'FAKE_access_token'}
        response = client.get('/users/kakao', **headers)

        user_id = jwt.decode(response.json()['access_token'], settings.SECRET_KEY, settings.ALGORITHM)
        access_token = jwt.encode({'id':user_id['id']}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'message': 'NEW_USER', 'access_token': access_token})