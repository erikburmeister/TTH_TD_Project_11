from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import generics
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView

from . import models
from . import serializers


def preferred_dog_age(preferred_age):
    preferred_age_groups = []
    b = [b for b in range(1, 13)]
    y = [y for y in range(13, 25)]
    a = [a for a in range(24, 61)]
    s = [s for s in range(60, 121)]

    if 'b' in preferred_age:
        preferred_age_groups.extend(b)
    if 'y' in preferred_age:
        preferred_age_groups.extend(y)
    if 'a' in preferred_age:
        preferred_age_groups.extend(a)
    if 's' in preferred_age:
        preferred_age_groups.extend(s)

    return preferred_age_groups


class UserRegisterView(CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    model = get_user_model()
    serializer_class = serializers.UserSerializer


class UserPreferenceView(generics.RetrieveUpdateAPIView):
    queryset = models.UserPref.objects.all()
    serializer_class = serializers.UserPrefSerializer

    def get_object(self, *args, **kwargs):
        try:
            user_preferences = self.get_queryset().get(
                user_id=self.request.user.pk)
        except ObjectDoesNotExist:
            user_preferences = self.get_queryset().create(
                user_id=self.request.user.pk)
        return user_preferences

    def put(self, request, *args, **kwargs):
        user_preferences = self.get_queryset().get(
            user_id=self.request.user)

        if request.method == 'PUT':
            data = request.data
            user_preferences.age = data.get('age')
            user_preferences.gender = data.get('gender')
            user_preferences.size = data.get('size')
            user_preferences.save()
        serializer = serializers.UserPrefSerializer(
            user_preferences)
        return Response(serializer.data)


class ListDogsView(generics.RetrieveUpdateAPIView):
    queryset = models.Dog.objects.all()
    serializer_class = serializers.DogSerializer

    def get_object(self):
        response = self.kwargs.get('decision')
        pk = self.kwargs.get('pk')

        user_preferences = models.UserPref.objects.get(
            user=self.request.user)
        age = user_preferences.age.split(",")
        gender = user_preferences.gender.split(",")
        size = user_preferences.size.split(",")

        if response == 'undecided':
            user_dog = models.UserDog.objects.filter(
                user=self.request.user).exists()

            if not user_dog:
                dogs = models.Dog.objects.all()

                for dog in dogs:
                    models.UserDog.objects.create(
                        user=self.request.user,
                        dog=dog,
                        status="u")

            undecided = models.Dog.objects.filter(
                age__in=preferred_dog_age(age),
                gender__in=gender,
                size__in=size,
                userdog__user=self.request.user,
                userdog__status='u',
            )

            if undecided:
                try:
                    undecided_dogs = undecided.filter(
                        id__gt=pk)[:1].get()
                except ObjectDoesNotExist:
                    undecided_dogs = undecided.first()
                return undecided_dogs
            else:
                return status.HTTP_404_NOT_FOUND

        elif response == 'liked':
            liked = models.Dog.objects.filter(
                age__in=preferred_dog_age(age),
                gender__in=gender,
                size__in=size,
                userdog__user=self.request.user,
                userdog__status='l',
            )

            if liked:
                try:
                    liked_dogs = liked.filter(
                        id__gt=pk)[:1].get()
                except ObjectDoesNotExist:
                    liked_dogs = liked.first()
                return liked_dogs
            else:
                return status.HTTP_404_NOT_FOUND

        elif response == 'disliked':
            disliked = models.Dog.objects.filter(
                age__in=preferred_dog_age(age),
                gender__in=gender,
                size__in=size,
                userdog__user=self.request.user,
                userdog__status='d',
            )

            if disliked:
                try:
                    disliked_dogs = disliked.filter(
                        id__gt=pk)[:1].get()
                except ObjectDoesNotExist:
                    disliked_dogs = disliked.first()
                return disliked_dogs
            else:
                return status.HTTP_404_NOT_FOUND


    def put(self, request, *args, **kwargs):
        response = self.kwargs.get('decision')
        pk = self.kwargs.get('pk')
        dog_instance = self.get_queryset().get(id=pk)

        try:
            user_dog = models.UserDog.objects.get(
                user=self.request.user, dog=dog_instance)
        except ObjectDoesNotExist:
            user_dog = models.UserDog.objects.create(
                user=self.request.user, dog=dog_instance)
        else:
            user_dog.status = response[0]
            user_dog.save()

        dog = serializers.DogSerializer(dog_instance)
        return Response(dog.data)
