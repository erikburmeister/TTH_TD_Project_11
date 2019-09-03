from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate

from rest_framework import status

from . import models
from . import views
from . import serializers

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
            status='l'
        )

    def test_register_user(self):
        factory = APIRequestFactory()
        factory.post(reverse('register-user'),
                     {'username': 'test_user',
                      'password': 'password'})
        test_user = User.objects.get(username='test_user')
        self.assertEqual(User.objects.count(), 1)
        self.assertTrue(test_user)

    def test_register_same_user(self):
        factory = APIRequestFactory()
        request = factory.post(reverse('register-user'),
                     {'username': 'test_user',
                      'password': 'password'})
        test_user = User.objects.get(username='test_user')
        view = views.UserRegisterView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(User.objects.count(), 1)
        self.assertTrue(test_user)

    def test_user_preferences(self):
        factory = APIRequestFactory()
        request = factory.get(reverse('preferences-update'))
        force_authenticate(request, user=self.test_user)
        view = views.UserPreferenceView.as_view()
        response = view(request)
        serializer = serializers.UserPrefSerializer(self.test_user_preferences)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_preferences_update(self):
        self.assertTrue(self.test_user_preferences.age, 'y')
        self.client.put(reverse('preferences-update'),
                        {'user': self.test_user,
                         'gender': 'm',
                         'age': 's',
                         'size': 's',})
        self.assertTrue(self.test_user_preferences.age, 's')

    def test_dog_undecided(self):
        factory = APIRequestFactory()
        user_dog = self.test_user_dog
        user_dog.status = 'u'
        user_dog.save()
        factory.get(reverse(
            'dogs-next', kwargs={'pk': 1, 'decision': 'undecided'}))
        self.assertEqual(models.Dog.objects.all().get(pk=1).name, 'Francesca')

    def test_dog_liked(self):
        factory = APIRequestFactory()
        user_dog = self.test_user_dog
        user_dog.status = 'l'
        user_dog.save()
        factory.get(reverse(
            'dogs-next', kwargs={'pk': 1, 'decision': 'liked'}))
        self.assertEqual(models.Dog.objects.all().get(pk=1).name, 'Francesca')

    def test_dog_disliked(self):
        factory = APIRequestFactory()
        user_dog = self.test_user_dog
        user_dog.status = 'd'
        user_dog.save()
        factory.get(reverse(
            'dogs-next', kwargs={'pk': 1, 'decision': 'disliked'}))
        self.assertEqual(models.Dog.objects.all().get(pk=1).name, 'Francesca')