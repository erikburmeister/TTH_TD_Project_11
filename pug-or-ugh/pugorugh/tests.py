from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate

from . import models
from . import views
from . import serializers
from .views import preferred_dog_age

# Create your tests here.
class ViewsTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.test_user = User.objects.create_user(
            username='test_user',
            email='test@email.com',
            password='password'
        )

        self.test_dog = models.Dog.objects.create(
            name="Francesca",
            image_filename="1.jpg",
            breed="Labrador",
            age=72,
            gender="f",
            size="l"
        )

        self.test_user_preferences = models.UserPref.objects.create(
            user=self.test_user,
            gender='m',
            age='y',
            size='s',
        )

        self.test_user_dog = models.UserDog.objects.create(
            user=self.test_user,
            dog=self.test_dog,
            status='u'
        )

    def test_preferred_dog_age(self):
        baby = preferred_dog_age('b')
        young = preferred_dog_age('y')
        adult = preferred_dog_age('a')
        senior = preferred_dog_age('s')
        self.assertEqual(baby, list(range(1,13)))
        self.assertEqual(young, list(range(13,25)))
        self.assertEqual(adult, list(range(24,61)))
        self.assertEqual(senior, list(range(60,121)))

    def test_register_user(self):
        self.client.post(reverse('register-user'),
                     {'username': 'test_user_2',
                      'password': 'password_2'})
        test_user_2 = User.objects.get(username='test_user_2')
        self.assertEqual(User.objects.count(), 2)
        self.assertTrue(test_user_2)

    def test_user_preferences(self):
        factory = APIRequestFactory()
        request = factory.get(reverse('preferences-update'))
        force_authenticate(request, user=self.test_user)
        view = views.UserPreferenceView.as_view()
        resp = view(request)
        serializer = serializers.UserPrefSerializer(self.test_user_preferences)
        self.assertEqual(resp.data, serializer.data)
        self.assertEqual(resp.status_code, 200)

    def test_user_preferences_update(self):
        factory = APIRequestFactory()
        request = factory.get(reverse('preferences-update'))
        force_authenticate(request, user=self.test_user)
        view = views.UserPreferenceView.as_view()
        resp = view(request)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, {'gender': 'm',
                                     'age': 'y',
                                     'size': 's'})
        request_2 = factory.put(reverse('preferences-update'),
                        {'gender': 'f',
                         'age': 's',
                         'size': 'l'})
        force_authenticate(request_2, user=self.test_user)
        resp_2 = view(request_2)
        self.assertEqual(resp_2.status_code, 200)
        self.assertEqual(resp_2.data, {'gender': 'f', 'age': 's', 'size': 'l'})

    def test_dog_update(self):
        factory = APIRequestFactory()
        request = factory.put(reverse('dogs-update',
                                      kwargs={'pk': 1, 'decision': 'liked'}))
        force_authenticate(request, user=self.test_user)
        view = views.ListDogsView.as_view()
        resp = view(request, pk='1', decision='liked')
        self.assertEqual(resp.status_code, 200)
