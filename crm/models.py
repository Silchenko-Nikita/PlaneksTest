import os
import random
import string

from django.conf.global_settings import LANGUAGES
from django.contrib.auth.models import User, Group
from django.db import models
from django.db.models.signals import post_save, pre_save, post_init
from django.urls import reverse

from common.consts import OBJECT_STATUS_ACTIVE
from common.models import BasicModel


User._meta.get_field('email')._unique = True
User._meta.get_field('username')._unique = False


def get_email(self):
    return self.email


User.add_to_class("__str__", get_email)


class UserProfile(BasicModel):
    AVATAR_PATH = os.path.join('crm', 'avatars')
    DEFAULT_AVATAR = os.path.join(AVATAR_PATH, 'default.png')

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', unique=True, verbose_name="Пользователь")
    birthday = models.DateField(blank=True, null=True, verbose_name="День рождения")
    language = models.CharField(max_length=7, choices=LANGUAGES, default='ru', verbose_name="Язык")
    avatar = models.ImageField(verbose_name='Аватар', upload_to=AVATAR_PATH, default=DEFAULT_AVATAR)

    def get_absolute_url(self):
        return reverse('guest-profile', kwargs={'pk': self.user.id})

    def save(self, **kwargs):
        self.user._original_groups = self.user.groups
        self.user._original_profile = self.user.profile
        return super().save(**kwargs)

    def __str__(self):
        return str(self.user.email) + " профиль"

    class Meta:
        db_table = 'user_profile'
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Group.objects.get_or_create(name='User')
        Group.objects.get_or_create(name='Editor')
        Group.objects.get_or_create(name='Admin')

        instance.groups.add(Group.objects.get(name='User'))
        UserProfile.objects.create(user=instance)


def user_pre_save(sender, instance, **kwargs):
    letters = string.ascii_lowercase
    instance.username = ''.join(random.choice(letters) for i in range(20))


def user_post_save(sender, instance, **kwargs):
    if instance.profile.previous_status == instance.profile.status:
        instance.profile.save()


def user_profile_post_init(sender, instance, **kwargs):
    instance.previous_status = instance.status if instance.pk is not None else False


def user_profile_post_save(sender, instance, **kwargs):
    if instance.previous_status == OBJECT_STATUS_ACTIVE and not instance.status == OBJECT_STATUS_ACTIVE:
        instance.user.is_active = False
        instance.user.save()
    if not instance.previous_status == OBJECT_STATUS_ACTIVE and instance.status == OBJECT_STATUS_ACTIVE:
        instance.user.is_active = True
        instance.user.save()


post_save.connect(create_user_profile, sender=User)
post_save.connect(user_post_save, sender=User)
pre_save.connect(user_pre_save, sender=User)

post_save.connect(user_profile_post_save, sender=UserProfile)
post_init.connect(user_profile_post_init, sender=UserProfile)
