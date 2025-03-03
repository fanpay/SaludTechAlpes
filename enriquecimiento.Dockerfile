FROM python:3.10
ENV PYTHONUNBUFFERED 1
EXPOSE 5000/tcp

# Instalar libpq-dev para tener libpq versión 10 o superior
RUN apt-get update && apt-get install -y libpq-dev

COPY requirements.txt ./

# Actualizar pip, forzar una versión de setuptools compatible y actualizar wheel
RUN pip install --upgrade --no-cache-dir "pip<24.1" "setuptools<66.0.0" wheel

RUN pip install --no-cache-dir -r requirements.txt

# Forzar la compilación de psycopg2 versión 2.9.9
RUN pip install --no-binary :all: psycopg2==2.9.9

COPY . .

CMD [ "flask", "--app", "./src/saludtech/enriquecimiento/api", "run", "--host=0.0.0.0"]
