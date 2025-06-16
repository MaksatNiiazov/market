from django.apps import apps
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from multiselectfield import MultiSelectField


class UserManager(BaseUserManager):
    def _create_user(self, username=None, email=None, password=None, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label,
            self.model._meta.object_name,
        )
        username = GlobalUserModel.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        if password:
            user.password = make_password(password)
        user.save(using=self._db)
        return user


class RoleType(models.TextChoices):
    DEFAULT = "DEFAULT", _("Customer")
    MERCHANT = "MERCHANT", _("Merchant")


class User(AbstractUser):
    avatar = models.CharField(
        max_length=500,
        blank=True,
        verbose_name=_("Avatar"),
    )
    roles = MultiSelectField(choices=RoleType.choices, default=RoleType.DEFAULT)
    sso_id = models.CharField(max_length=255, blank=True, null=True, unique=True)
    password = models.CharField(_("password"), max_length=128, blank=True, default="")
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
        ),
        validators=[AbstractUser.username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
        blank=True,
        null=True,
    )
    fio = models.CharField(max_length=400, null=True, blank=True)

    objects = UserManager()
