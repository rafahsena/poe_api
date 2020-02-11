from channels.generic.websocket import WebsocketConsumer
import json
import urllib.parse as parse

class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        batata = parse.parse_qs(self.scope['query_string'].decode('utf8'))
        print(batata)

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        message = text_data

        self.send(text_data=json.dumps({
            'message': message
        }))