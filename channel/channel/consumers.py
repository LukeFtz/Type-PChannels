from email import message
import json
import string
import secrets
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

def make_token():
        alphabet = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(secrets.choice(alphabet) for i in range(8))
        return password

class Consumers(WebsocketConsumer):
    
    def connect(self):
        
        self.room_group_name = 'typep'
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
    
    def receive(self, text_data):
        data = json.loads(text_data)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'communication',
                'data':data
            }
        )
    
    def communication(self, event):
        data = event['data']
        print(data)
        if (data["func"]=="GEN_TOKEN"):
            token = make_token()
            token_data = json.dumps({
                "func":"TOKEN",
                "token":token
            })
            self.send(text_data=token_data)
        elif (data["func"]=="DEF_OVEN"):
            data_to_send=json.dumps({"func":"OVEN_SETTED", "token": "$Xip%meT"})
            self.send(text_data=data_to_send)
        elif data["func"]=="STRT_HEAT":
            data_to_send=json.dumps({"func":"OVEN_HEATING", "token": "$Xip%meT"})
            self.send(text_data=data_to_send)
        elif data["func"]=="SEND_VAL":
            data_to_send=json.dumps({"func":"OVEN_TEMP", "val":150, "token": "$Xip%meT"})
            self.send(text_data=data_to_send)
        elif data["func"]=="SEND_COMPLETE":
            data_to_send=json.dumps({"func":"HEAT_COMPLETE", "token": "$Xip%meT"})
            self.send(text_data=data_to_send)
        # else:
        #     self.send(text_data=json.dumps(data))
        

    def disconnect(self, close_code):
        # Called when the socket closes
        self.close()
        