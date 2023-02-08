from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from users.managers import UserManager


class UserRoles:
    USER = "user"
    ADMIN = "admin"
    choices = (
        (USER, USER),
        (ADMIN, ADMIN),
    )


class User(AbstractBaseUser):
    # эта константа определяет поле для логина пользователя
    USERNAME_FIELD = 'email'

    # эта константа содержит список с полями,
    # которые необходимо заполнить при создании пользователя
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone', "role"]

    # для корректной работы нам также необходимо
    # переопределить менеджер модели пользователя
    objects = UserManager()

    first_name = models.CharField(
        max_length=100,
        verbose_name="Имя",
        help_text="Введите имя",
    )

    last_name = models.CharField(
        max_length=100,
        verbose_name="Фамилия",
        help_text="Введите фамилию",
    )

    email = models.EmailField(
        "email address",
        unique=True,
        help_text="Введите электронную почту",
    )

    phone = PhoneNumberField(
        verbose_name="Телефон",
        help_text="Введите телефон",

    )

    role = models.CharField(
        max_length=20,
        choices=UserRoles.choices,
        default=UserRoles.USER,
        verbose_name="Роль пользователя",
        help_text="Выберите роль пользователя",
    )

    is_active = models.BooleanField(
        verbose_name="Аккаунт активен",
        help_text="Укажите, активен ли аккаунт"
    )

    @property
    def is_superuser(self):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    @property
    def is_admin(self):
        return self.role == UserRoles.ADMIN

    @property
    def is_user(self):
        return self.role == UserRoles.USER

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["id"]
