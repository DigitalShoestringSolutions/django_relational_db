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
import os
from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application
import django
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "site_config.settings")

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
    }
)

import event_handler
import shoestring_wrapper.wrapper


# shoestring_wrapper.wrapper.Wrapper.start({'zmq_config':zmq_config})
shoestring_wrapper.wrapper.MQTTServiceWrapper(
    settings.MQTT, settings.ZMQ_CONFIG
).start()
event_handler_thread = event_handler.EventHandlerThread(settings.ZMQ_CONFIG).start()

