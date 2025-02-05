import json
import os
from channels.generic.websocket import AsyncWebsocketConsumer

class JSONFileConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("json_updates_group", self.channel_name)
        await self.accept()
        await self.send_json_update()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("json_updates_group", self.channel_name)

    async def send_json_update(self, event=None):
        """Отправка обновленного JSON в WebSocket"""
        if os.path.exists('static/data/data.json'):
            with open('static/data/data.json', "r", encoding="utf-8") as file:
                try:
                    data = json.load(file)  # Загружаем данные из файла
                except json.JSONDecodeError:
                    return {"error": "Ошибка при чтении JSON файла"}
        text_data = json.dumps(event["data"]) if event else json.dumps(data)
        await self.send(text_data)