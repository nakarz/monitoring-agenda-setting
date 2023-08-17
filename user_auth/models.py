from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

ROLES_CHOICES = (
    ('admin', 'Admin'),
    ('petugas_monitor', 'Petugas Monitor'),
    ('petugas_agenda_setting', 'Petugas Agenda Setting'),
)
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=255)
    nip = models.CharField(max_length=50, unique=True)
    roles = models.CharField(max_length=50, choices=ROLES_CHOICES)
    email = models.EmailField(unique=True)

    groups_related_name = 'user_auth_user_groups'
    user_permissions_related_name = 'user_auth_user_permissions'

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name=groups_related_name,
        related_query_name='user_auth_user',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name=user_permissions_related_name,
        related_query_name='user_auth_user',
    )

    def __str__(self):
        return self.full_name