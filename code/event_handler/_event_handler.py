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
import zmq
import json
import threading
import traceback
import logging

context = zmq.Context()

logger = logging.getLogger("main.event_handler")


class Event:
    def __init__(self, topic, content):
        self.__topic: list[str] = topic
        self.__content = content

    @property
    def topic(self):
        return self.__topic

    @property
    def content(self):
        return self.__content
    
    def as_dict(self):
        return {"topic":self.__topic,"payload":self.__content}

    def match(self, spec):
        for index, entry in enumerate(spec):
            if self.__topic[index] != entry:
                return False

        return True

    def __str__(self):
        return f"<Message> [topic:{'/'.join(self.__topic)}, content: {self.__content}]"


class EventHandler:
    inst = None

    def __init__(self):
        self.__callbacks = []

    @classmethod
    def get_instance(cls) -> "EventHandler":
        if cls.inst is None:
            cls.inst = cls()
        return cls.inst

    # this is a decorator
    @classmethod
    def register(cls, topic_spec: str):
        def inner(callback):
            logger.info(f"registered {topic_spec} against {callback}")
            inst = cls.get_instance()
            inst.__register(callback, topic_spec.split("/"))
            return callback

        return inner

    def __register(self, callback, topic_spec: list[str]):
        self.__callbacks.append({"spec": topic_spec, "callback": callback})

    @classmethod
    def handle(cls, msg: Event) -> list[Event]:
        inst = cls.get_instance()
        all = []
        for entry in inst.__callbacks:
            if msg.match(entry["spec"]):
                out_msgs = entry["callback"](msg)
                all.extend(out_msgs)

        return all

class EventHandlerThread(threading.Thread):

    def __init__(self, zmq_config):
        super().__init__()
        zmq_in_conf = zmq_config["state_in"]
        self.zmq_in = context.socket(zmq_in_conf["type"])
        if zmq_in_conf["bind"]:
            self.zmq_in.bind(zmq_in_conf["address"])
        else:
            self.zmq_in.connect(zmq_in_conf["address"])

        zmq_out_conf = zmq_config["state_out"]
        self.zmq_out = context.socket(zmq_out_conf["type"])
        if zmq_out_conf["bind"]:
            self.zmq_out.bind(zmq_out_conf["address"])
        else:
            self.zmq_out.connect(zmq_out_conf["address"])

    def run(self):
        # listen for incoming events
        logger.debug("listening for inbound messages")
        while True:
            msg = self.zmq_in.recv()
            msg_json = json.loads(msg)
            logger.debug("StateModel got:", msg)
            try:
                topic_parts = msg_json["topic"].split("/")
                msg_payload = msg_json["payload"]
                message = Event(topic_parts, msg_payload)
                output_messages = EventHandler.handle(message)

                # send update(s)
                for msg in output_messages:
                    self.zmq_out.send_json(msg.as_dict())

            except Exception:
                logger.error(traceback.format_exc())


from django.conf import settings

def send_events(events: list[Event]):
    zmq_conf = settings.ZMQ_CONFIG["state_out"]
    socket = context.socket(zmq_conf["type"])
    socket.connect(zmq_conf["address"])

    for event in events:
        socket.send_json(event)
