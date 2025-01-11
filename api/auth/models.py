from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UserManager(BaseUserManager):

	def create_user(self,name, email, password=None):

		if not email:

			raise ValueError('O usuário deve ter um endereço de email.')

		email = self.normalize_email(email)
		user = self.model(name=name, email=email)

		if password:

			user.set_password(password)

		user.full_clean()
		user.save(using=self._db)

		return user

	def create_superuser(self, name, email, password):

		user = self.create_user(name, email, password)
		user.is_superuser = True
		user.is_staff = True

		user.save(using=self._db)

		return user

class UserProfile(AbstractBaseUser, PermissionsMixin):

	name = models.CharField(max_length=255)
	email = models.EmailField(max_length=255, unique=True)

	first_name = models.CharField(max_length=30, blank=True, null=True)
	last_name = models.CharField(max_length=150, blank=True, null=True)

	full_name = models.CharField(max_length=255, blank=True, null=True)

	objects = UserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['name']

	is_active = models.BooleanField(default=True, verbose_name="Está ativo")
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)

	def __str__(self):

		return self.name
	
	def save(self, *args, **kwargs):

		self.full_name = f'{self.first_name} {self.last_name}'

		super().save(*args, **kwargs)

	class Meta:

		verbose_name = 'Usuário'