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
from django.utils.module_loading import autodiscover_modules


class EventHandlerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "event_handler"

    def ready(self):
        autodiscover_modules("event_handler")
