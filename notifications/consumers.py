from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync
import urllib.parse as parse

class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        info = parse.parse_qs(self.scope['query_string'].decode('utf8'))
        self.currency = info['currency'][0]
        self.value = float(info['value'][0])
        self.group_name = 'currencies_notifications'
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )


    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    def receive(self, text_data):
        message = text_data

        self.send(text_data=json.dumps({
            'message': message
        }))

    def currency_update(self, event):
        print(self.value, event['value'])
        if event['value'] <= self.value:
            self.send(text_data=json.dumps({
                'message': f'A moeda {event["currency"]} agora vale {event["value"]}!'
            })) 