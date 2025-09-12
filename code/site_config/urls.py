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
from django.urls import path,include
from django.shortcuts import redirect

def redirect_root(request):
    response = redirect('/admin')
    return response

urlpatterns = [
    path('',redirect_root),
    path('admin/', admin.site.urls),
    path('state/', include('state.urls')),
    path('events/',include('state.event_urls')),
]

admin.site.site_header = "Location Tracking Admin"
admin.site.site_title = "Location Tracking Admin Portal"
admin.site.index_title = "Welcome to Location Tracking Administration Portal"

from django.contrib.auth.models import Group
admin.site.unregister(Group)
