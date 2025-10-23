import json
from translate import Translator
from channels.generic.websocket import AsyncWebsocketConsumer
from users.models.translate import Translate
from asgiref.sync import sync_to_async

class QuoteTranslateConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({
            "message": "Connected to Quotes Translator WebSocket"
        }))

    async def receive(self, text_data=None, bytes_data=None):
        user = self.scope.get("user")
        data = json.loads(text_data)
        quote = data.get("quote")
        target_lang = data.get("target_lang", "hi")

        translator = Translator(to_lang=target_lang)
        translated_text = translator.translate(quote)

        await sync_to_async(Translate.objects.create)(
            user=user,
            source_text=quote,
            target_language=target_lang,
            translated_text=translated_text
        )

        await self.send(text_data=json.dumps({
            "status": True,
            "user": user.full_name,
            "source_text": quote,
            "translated_text": translated_text
        }))

    async def disconnect(self, close_code):
        print("Disconnected successfully")

