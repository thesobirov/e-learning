from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.apps import apps

User = get_user_model()


class Command(BaseCommand):
    help = 'Creates user roles, groups, and assigns permissions'

    def handle(self, *args, **kwargs):

        superuser_group, _ = Group.objects.get_or_create(name='Superuser')
        teacher_group, _ = Group.objects.get_or_create(name='Teacher')
        user_group, _ = Group.objects.get_or_create(name='User')

        catalog_model = apps.get_model('quiz', 'Catalog')
        test_model = apps.get_model('quiz', 'Test')

        superuser_permissions = Permission.objects.filter(content_type__app_label='quiz')
        superuser_group.permissions.set(superuser_permissions)

        teacher_permissions = Permission.objects.filter(
            content_type=ContentType.objects.get_for_model(test_model),
            codename__in=['add_test', 'change_test', 'delete_test']
        )
        teacher_group.permissions.set(teacher_permissions)

        user_permissions = Permission.objects.filter(
            content_type=ContentType.objects.get_for_model(test_model),
            codename='view_test'
        )
        user_group.permissions.set(user_permissions)

        if not User.objects.filter(username='superuser').exists():
            superuser = User.objects.create_superuser('superuser', 'superuser@example.com', 'password')
            superuser.groups.add(superuser_group)
            self.stdout.write(self.style.SUCCESS('Superuser created and added to Superuser group'))

        if not User.objects.filter(username='teacher').exists():
            teacher = User.objects.create_user('teacher', 'teacher@example.com', 'password')
            teacher.groups.add(teacher_group)
            self.stdout.write(self.style.SUCCESS('Teacher created and added to Teacher group'))

        if not User.objects.filter(username='user').exists():
            normal_user = User.objects.create_user('user', 'user@example.com', 'password')
            normal_user.groups.add(user_group)
            self.stdout.write(self.style.SUCCESS('Normal user created and added to User group'))

        self.stdout.write(self.style.SUCCESS('Groups, permissions, and users set up successfully'))
