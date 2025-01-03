import os
from aiokafka import AIOKafkaProducer
import asyncio


async def get_kafka_producer():
    KAFKA_BOOTSTRAP_SERVERS = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092") #obtém o endereço do servidor Kafka do arquivo .env
    ''' 
    Essa função cria um produtor Kafka que será utilizado para enviar mensagens para o tópico do Kafka.
    '''
    producer = AIOKafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    )
    await producer.start()
    return producer

async def send_to_topic(producer, topic, data):
    ''' 
    Essa função envia mensagens para o tópico do Kafka.
    '''
    try:
        await producer.send_and_wait(topic, data.encode()) #send to wait é um método que envia a mensagem e aguarda a confirmação de que a mensagem foi enviada com sucesso
    except Exception as e:
        print('Erro ao enviar mensagem para o Kafka', e)