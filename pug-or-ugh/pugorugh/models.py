from django.contrib.auth.models import User
from django.db import models

GENDER = (
    ('m', 'male'),
    ('f', 'female'),
    ('u', 'unknown'),
)
SIZE = (
    ('s', 'small'),
    ('m', 'medium'),
    ('l', 'large'),
    ('xl', 'extra large'),
    ('u', 'unknown'),
)
STATUS = (
    ('l', 'liked'),
    ('d', 'disliked'),
    ('u', 'undecided'),
)


class Dog(models.Model):
    name = models.CharField(max_length=255)
    image_filename = models.CharField(max_length=255)
    breed = models.CharField(max_length=255, default='')
    age = models.IntegerField(default=1)
    gender = models.CharField(max_length=1, choices=GENDER)
    size = models.CharField(max_length=2, choices=SIZE)

    def __str__(self):
        return """
        Name: {}, breed: {}, Age: {}
        Gender: {}, Size: {}
        """.format(self.name, self.breed, self.age,
                   self.gender, self.size)


class UserDog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="user")
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS)

    def __str__(self):
        return "User:{}, Status:{}, Dog:{}".format(
            self.user.username, self.status, self.dog.name)


class UserPref(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_pref')
    age = models.CharField(max_length=1, default='b,y,a,s')
    gender = models.CharField(max_length=1, default='m,f')
    size = models.CharField(max_length=2, default='s,m,l,xl')

    def __str__(self):
        return self.user.username
