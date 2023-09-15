from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class AbstractTime(models.Model):
    """ For Every Database Table """

    created_at = models.DateTimeField("Created Date", auto_now_add=True)
    updated_at = models.DateTimeField("Updated Date", auto_now=True)

    class Meta:
        abstract = True

class Master_Config(AbstractTime):
    label =  models.CharField(max_length=200)
    parent_id = models.ForeignKey('self', on_delete=models.CASCADE, related_name="acb")

    class Meta:
        abstract = False



class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.

        param:
            emai (str): Email ID of user
            password (str): password of user
        return:
            user (MyUserManager): user object
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(email=self.normalize_email(email))

        user.user_type = extra_fields.get("user_type")
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email and password.
        param:
            emai (str): Email ID of user
            password (str): password of user
        return:
            user (MyUserManager): user object
        """
        user = self.create_user(email, password=password, user_type="super_user")
        user.user_type = "super_user"
        user.is_admin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser, AbstractTime):
    """
    Create Account on Database, Account Model
    """

    email = models.EmailField(
        "Email Address", max_length=255, unique=True, null=False, blank=False
    )
    user_type = models.ForeignKey(
        "Master_Config", on_delete=models.CASCADE, related_name="abc")
    is_active = models.BooleanField(default=True, null=False, blank=False)
    is_admin = models.BooleanField(default=False, null=False, blank=False)

    objects = MyUserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return str(self.email)

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        # Simplest possible answer: All admins are staff
        return self.is_admin
