from django.contrib.auth.base_user import AbstractBaseUser


class NoSuperuser(AbstractBaseUser):
    pass


class NoStaff(AbstractBaseUser):
    pass
