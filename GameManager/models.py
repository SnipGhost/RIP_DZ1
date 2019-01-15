from django.core import validators
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from GameManager.tools import modify_fields


@modify_fields(
    username={
        'verbose_name': 'Имя пользователя',
        'help_text': 'Уникальное имя - логин',
        'error_messages': {'unique': 'Данное имя уже занято'},
        # I am lazy to handle the remaining messages
        # TODO: Handle all error_messages
    },
)
class Profile(AbstractUser):

    AbstractUser._meta.get_field('username').validators = [
        validators.MinLengthValidator(2)]
    AbstractUser._meta.get_field('password').verbose_name = 'Пароль'

    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        default='avatars/default_avatar.png',
        verbose_name='Аватар'
    )
    description = models.CharField(
        max_length=255,
        verbose_name='О себе',
        blank=True,
        null=True
    )
    objects = UserManager()

    class Meta:
        db_table = 'users'
        verbose_name = _('Профиль пользователя')
        verbose_name_plural = _('Профили пользователей')


class Game(models.Model):
    name = models.CharField(max_length=80, verbose_name='Игра')
    description = models.TextField(max_length=4096, verbose_name='Описание')
    owner = models.ManyToManyField(Profile, verbose_name='Владелец')
    platform = models.IntegerField(choices=settings.PLATFORMS,
                                   null=True,
                                   verbose_name='Платформа')
    game_image = models.ImageField(upload_to='game_images/', blank=True, null=True,
                                   default='game_images/default_game_image.png',
                                   verbose_name='Изображение')

    class Meta:
        db_table = 'game'
        verbose_name = _('Игра')
        verbose_name_plural = _('Игры')
