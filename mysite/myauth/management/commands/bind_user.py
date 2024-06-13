from django.contrib.auth.models import User, Group, Permission
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.get(pk=5)
        group, created = Group.objects.get_or_create(
            name='profile_manager'
        )
        permission_profile = Permission.objects.get(
            codename='view_profile'
        )

        permissions_logentry = Permission.objects.get(
            codename='view_logentry'
        )

        group.permissions.add(permission_profile) #добавление разрешения в группу
        user.groups.add(group) #добавления пользователя к группе
        user.user_permissions.add(permissions_logentry) #добавление разрешения пользователю

        group.save()
        user.save()


