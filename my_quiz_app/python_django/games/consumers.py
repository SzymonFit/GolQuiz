import json
from channels.generic.websocket import AsyncWebsocketConsumer
import logging

logger = logging.getLogger(__name__)

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.game_id = self.scope['url_route']['kwargs']['game_id']
        self.game_group_name = f'game_{self.game_id}'

        # Dołącz do pokoju
        await self.channel_layer.group_add(
            self.game_group_name,
            self.channel_name
        )

        await self.accept()
        logger.info(f"Połączono WebSocket dla gry {self.game_id}")

    async def disconnect(self, close_code):
        # Opuść pokój
        await self.channel_layer.group_discard(
            self.game_group_name,
            self.channel_name
        )
        logger.info(f"Rozłączono WebSocket dla gry {self.game_id}")

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']

        logger.info(f"Otrzymano wiadomość: {message}")

        await self.channel_layer.group_send(
            self.game_group_name,
            {
                'type': 'game_message',
                'message': message
            }
        )

    async def game_message(self, event):
        message = event['message']

        logger.info(f"Wysłano wiadomość: {message}")

        await self.send(text_data=json.dumps({
            'message': message
        }))
