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

from django.contrib import admin
from django.conf import settings
from django.urls import path,include
from django.shortcuts import redirect

def redirect_root(request):
    response = redirect('/admin')
    return response

urlpatterns = [
    path('',redirect_root),
    path('admin/', admin.site.urls),
]

for entry in settings.URL_ROUTING:
    urlpatterns.append(
        path(entry[0], include(entry[1]))
    )

if hasattr(settings,"ADMIN_HEADER"):
    admin.site.site_header = settings.ADMIN_HEADER 
if hasattr(settings, "ADMIN_TITLE"):
    admin.site.site_title = settings.ADMIN_TITLE

if hasattr(settings, "ADMIN_INDEX"):
    admin.site.index_title = settings.ADMIN_INDEX

from django.contrib.auth.models import Group
admin.site.unregister(Group)
