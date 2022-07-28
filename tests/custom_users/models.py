from django.contrib.auth.base_user import AbstractBaseUser


class NoSuperUser(AbstractBaseUser):
    pass
