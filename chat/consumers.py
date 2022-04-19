import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.shortcuts import redirect
import asyncio
from .models import RoomMember
from asgiref.sync import sync_to_async
from django.http.response import JsonResponse

@sync_to_async
def get_all_rooms(roomname):
    print("roomname++++++++++++++",roomname)
    try:
        d = RoomMember.objects.get(room_name = roomname)
        print("d############",d)
        return True
    except:
        print("Inside exceptin at line number 16")
        return JsonResponse(
            {
                "message": "room name not exists"
            }
        )

class ChatConsumer(AsyncWebsocketConsumer):
    # async def get_all_rooms(self):
    #     try:
    #         d = RoomMember.objects.get(room_name = self.room_group_name)
    #         print("d############",d)
    #         return True
    #     except:
    #         return redirect("not-able-to-join/")

    async def connect(self): 
        await self.accept()
        

    async def disconnect(self, close_code):
        
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        print('Disconnected!')
        

    # Receive message from WebSocket
    async def receive(self, text_data):
        receive_dict = json.loads(text_data)
        print("receive_dict",receive_dict)
        peer_username = receive_dict['peer']
        action = receive_dict['action']
        message = receive_dict['message']
        try:
            roomname = receive_dict['roomname']
            print("roomname",roomname)
            self.room_group_name =roomname
        except:
            roomname = ""
            print("roomname not found")
        

            
            # return render(request,'chat/main.html',{'error':f'Room Doesn\'t Exists with name - '+roomname})

        # print('unanswered_offers: ', self.unanswered_offers)

        print('Message received: ', message)

        print('peer_username: ', peer_username)
        print('action: ', action)
        print('self.channel_name: ', self.channel_name)
        await self.channel_layer.group_add(
            roomname,
            self.channel_name
        )
        if(action == 'new-offer') or (action =='new-answer'):
            # in case its a new offer or answer
            # send it to the new peer or initial offerer respectively

            receiver_channel_name = receive_dict['message']['receiver_channel_name']

            print('Sending to ', receiver_channel_name)

            # set new receiver as the current sender
            receive_dict['message']['receiver_channel_name'] = self.channel_name

            await self.channel_layer.send(
                receiver_channel_name,
                {
                    'type': 'send.sdp',
                    'receive_dict': receive_dict,
                }
            )

            return

        # set new receiver as the current sender
        # so that some messages can be sent
        # to this channel specifically
        receive_dict['message']['receiver_channel_name'] = self.channel_name

        # send to all peers
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send.sdp',
                'receive_dict': receive_dict,
            }
        )

    async def send_sdp(self, event):
        receive_dict = event['receive_dict']

        this_peer = receive_dict['peer']
        action = receive_dict['action']
        message = receive_dict['message']
        
        roomname = self.room_group_name
        data = await get_all_rooms(roomname)
        if data==True:
            res = {
            'peer': this_peer,
            'action': action,
            'message': message,
            }
        else:
            message['error'] = True
            res = {
            'peer': this_peer,
            'action': action,
            'message': message,
            }
            
        await self.send(text_data=json.dumps(res))