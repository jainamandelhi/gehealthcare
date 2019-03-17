# Third Party Stuff
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.postgres.fields import CIEmailField
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

# gehealthcare Stuff
from gehealthcare.base.models import UUIDModel


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email: str, password: str, is_staff: bool, is_superuser: bool, **extra_fields):
        """Creates and saves a User with the given email and password.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email: str, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email: str, password: str, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)


class User(AbstractBaseUser, UUIDModel, PermissionsMixin):
    first_name = models.CharField(_('First Name'), max_length=120, blank=True)
    last_name = models.CharField(_('Last Name'), max_length=120, blank=True)
    # https://docs.djangoproject.com/en/1.11/ref/contrib/postgres/fields/#citext-fields
    email = CIEmailField(_('email address'), unique=True, db_index=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text='Designates whether the user can log into this admin site.')

    is_active = models.BooleanField('active', default=True,
                                    help_text='Designates whether this user should be treated as '
                                              'active. Unselect this instead of deleting accounts.')
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    hadm_id = models.CharField(_('hadm_id'), max_length=10, null=True, blank=True)
    admittime = models.DateTimeField(_('admittime'), null=True, blank=True)
    dischtime = models.DateTimeField(_('dischtime'), null=True, blank=True)
    deathtime = models.DateTimeField(_('deathtime'), null=True, blank=True)
    admission_type = models.CharField(_('admission_type'), null=True, blank=True, max_length=30)
    admission_location = models.TextField(_('admission_location'), null=True, blank=True)
    discharge_location = models.TextField(_('discharge_location'), null=True, blank=True)
    insurance = models.CharField(_('insurance'), null=True, blank=True, max_length=100)
    language = models.CharField(_('language'), null=True, blank=True, max_length=100)
    religion = models.CharField(_('religion'), null=True, blank=True, max_length=100)
    martial_status = models.CharField(_('martial_status'), null=True, blank=True, max_length=100)
    ethnicity = models.CharField(_('ethnicity'), null=True, blank=True, max_length=150)
    diagnosis = models.CharField(_('diagnosis'), null=True, blank=True, max_length=250)
    state = models.CharField(_('state'), null=True, blank=True, max_length=150)
    district = models.CharField(_('district'), null=True, blank=True, max_length=150)
    statement = models.TextField(_('statement'), null=True, blank=True)

    USERNAME_FIELD = 'email'
    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ('-date_joined', )

    def __str__(self):
        return str(self.id)

    def get_full_name(self) -> str:
        """Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '{} {}'.format(self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self) -> str:
        """Returns the short name for the user.
        """
        return self.first_name.strip()
