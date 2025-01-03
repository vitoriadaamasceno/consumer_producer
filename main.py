from fastapi import FastAPI, Body, HTTPException
from pydantic import BaseModel
from typing import Annotated
from app.crawler.crawler import Crawler
import asyncio
import json

from app.producer import get_kafka_producer, send_to_topic

 
class Noticia(BaseModel):
    titulo: str
    data_publicacao: str | None = None
    url: str


app = FastAPI(title="API de Notícias")

@app.post("/noticias")
async def get_noticias(data_inicial: Annotated[str, Body()], data_final: Annotated[str, Body()]):
    crawler = Crawler(data_inicial, data_final)
    noticias = crawler.__main__()
    if noticias is None :
        raise HTTPException(status_code=404, detail="Nenhuma notícia encontrada, tente novamente")
    
    total_noticias = len(noticias)
    
    producer = await get_kafka_producer()
    for noticia in noticias:
        noticia = json.dumps(noticia, ensure_ascii=False, indent=4)
        await send_to_topic(producer,'noticias', noticia)

    await producer.stop()
    
    return {"total_noticias": total_noticias, "noticias": noticias}