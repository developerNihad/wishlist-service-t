import aio_pika
import json
from app.config import settings
from app.events.event_models import WishlistEvent
from typing import Optional

class EventPublisher:
    def __init__(self):
        self.connection: Optional[aio_pika.Connection] = None
        self.channel: Optional[aio_pika.Channel] = None
    
    async def connect(self):
        """RabbitMQ bağlantısını kur"""
        self.connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
        self.channel = await self.connection.channel()
        
        # Exchange'i declare et
        await self.channel.declare_exchange(
            "wishlist_events",
            aio_pika.ExchangeType.TOPIC,
            durable=True
        )
    
    async def publish_wishlist_event(self, event: WishlistEvent):
        """Wishlist event'ini yayınla"""
        if not self.channel:
            await self.connect()
            
        message_body = json.dumps(event.model_dump()).encode()
        
        message = aio_pika.Message(
            body=message_body,
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT
        )
        
        await self.channel.default_exchange.publish(
            message,
            routing_key=event.event_type.value
        )
    
    async def close(self):
        """Bağlantıyı kapat"""
        if self.connection:
            await self.connection.close()

# Global publisher instance
event_publisher = EventPublisher()