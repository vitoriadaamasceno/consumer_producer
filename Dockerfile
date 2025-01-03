FROM python:3.11.6

#instalar pacotes de localidade
RUN apt-get update && apt-get install -y locales \
    && echo "pt_BR.UTF-8 UTF-8" > /etc/locale.gen \
    && locale-gen pt_BR.UTF-8 \
    && update-locale LANG=pt_BR.UTF-8

#definir a localidade padrão
ENV LANG pt_BR.UTF-8
ENV LANGUAGE pt_BR:pt
ENV LC_ALL pt_BR.UTF-8

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
# instalar o watchdog para monitorar alterações nos arquivos
RUN pip install --no-cache-dir watchdog[watchmedo] 

COPY . .