import asyncio
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
from app.consumer.database import get_db_session, Noticia
from aiokafka import AIOKafkaConsumer
from sqlalchemy.orm import Session
import logging




async def add(db: Session, noticia: Noticia):
    noticia_db = Noticia(
        titulo=noticia['titulo'],
        data_publicacao=noticia['data_publicacao'],
        link=noticia['link']
    )
    db.add(noticia_db)
    await db.commit()
    await db.refresh(noticia_db)
    return True


KAFKA_BOOTSTRAP_SERVERS = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")

async def consume():
    consumer = AIOKafkaConsumer(
        'noticias',
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    )

    await consumer.start()

    try:
        logging.info("Consumer started")
        async for msg in consumer:
            try:
                noticia = json.loads(msg.value)
                print(noticia)
                async for db in get_db_session():
                    await add(db, noticia)
            except Exception as e:    
                logging.error(f"Error consuming message: {e}")
    finally:    
        await consumer.stop()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(consume())
    loop.run_forever()