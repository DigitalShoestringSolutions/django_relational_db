"""
This file is part of the django_relational_db service module.

Copyright (C) 2025 Shoestring and University of Cambridge

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from django.apps import AppConfig
from django.db.models.signals import post_migrate


class DefaultAdminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'default_admin'

    def ready(self):
        post_migrate.connect(create_default_admin,sender=self)


def create_default_admin(sender, **kwargs):
    from django.contrib.auth import get_user_model
    import os
    User = get_user_model()

    try:
        User.objects.get(username="admin")
        exists = True
    except User.DoesNotExist:
        exists = False

    if not exists:
        try:
            from setup import intial_admin_pw_file
            password = open(intial_admin_pw_file,"r").read()
            if password:
                User.objects.create_superuser('admin','',password)
                print("INFO: Created default admin user")
                with open(intial_admin_pw_file,"w") as f:
                    f.write("")
            else:
                print("ERROR: default admin not created - password blank")   
        except:
            print("WARNING: default admin not created - may already exist")
