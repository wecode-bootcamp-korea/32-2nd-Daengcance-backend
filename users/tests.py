import jwt

from django.test         import TestCase, Client
from django.conf         import settings

from unittest.mock       import patch
from users.models        import User
from django.conf         import settings

class KakaoSignTest(TestCase):
    def setUp(self):
        User.objects.create(
            id       = 1,
            name     = '지수',
            kakao_id = 1234567890,
            email    = 'gsoosuu@gmail.com'
        )

    def tearDown(self):
        User.objects.all().delete()

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
            },
            'email': 'gsoosuu@gmail.com'
        }
    }

        mocked_kakao_user_info.return_value = MockedResponse()
    
        headers = {'Authorization':'FAKE_access_token'}
        response = client.post('/users/login/kakao', **headers)

        access_token = jwt.encode({'id':1}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'SUCCESS', 'access_token': access_token, 'nickname':'지수'})

    @patch('users.views.requests.get')
    def test_kakao_signup_success(self, mocked_kakao_user_info):
        client = Client()

        class MockedResponse:
            def json(self):
                return {
                    'id': 123456789,
                    'properties': {
                        'nickname': '현정'
                    },
                    'kakao_account': {
                        'profile': {
                            'nickname':'현정',
                        },
                        'email' : 'gsoosuu@gmail.com'
                    }
                }

        mocked_kakao_user_info.return_value = MockedResponse()

        headers  = {'Authorization': 'FAKE_access_token'}
        response = client.post('/users/login/kakao', **headers)

        access_token = jwt.encode({'id':2}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message' : 'SUCCESS', 'access_token' : access_token, 'nickname': '현정'})
