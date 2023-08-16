from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.utils import timezone


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=email,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        superuser = self.create_user(
            email=email,
            password=password,
        )
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.is_active = True
        superuser.save(using=self._db)
        return superuser


class User(AbstractUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    username = None
    nickname = models.CharField(default='', max_length=100, null=False, blank=True)
    email = models.EmailField(unique=True, max_length=255)
    profile_image = models.ImageField(upload_to='profile_image/', null=True, blank=True)

    last_second_login = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']

    def update_second_last_login(self):
        # 현재 last_login 값을 last_second_login으로 복사
        self.last_second_login = self.last_login
        # 현재 last_login 값을 현재 시간으로 업데이트
        self.last_login = timezone.now()
        self.save()

    objects = UserManager()

    def __str__(self):
        return self.email