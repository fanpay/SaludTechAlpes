# Proyecto SaludTech de los Alpes 2025

Este repositorio contiene el código y la documentación del proyecto SaludTech de los Alpes 2025, desarrollado para el curso. El proyecto se centra en el diseño de la arquitectura para soportar la expansión global de la compañía, con un enfoque en escalabilidad y seguridad, especialmente en el mercado estadounidense y su cumplimiento con la ley HIPAA.

## Estructura del Proyecto

``` bash
├── LICENSE
├── Lenguaje-obicuo # Carpeta con las imágenes del lenguaje ubicuo
├── README.md
├── collections # Carpeta con las colecciones de Postman
│   └── SALUDTECH.postman_collection.json
├── docker-compose.yml # Archivo de configuración de Docker Compose
├── docs
│   └── entrega1 # Carpeta con los archivos de la entrega 1
│       ├── AS-IS
│       ├── README.md
│       └── TO-BE
├── pyproject.toml # Archivo de configuración de Poetry
├── requirements.txt # Archivo con las dependencias del proyecto
├── src # Carpeta con el código fuente
│   ├── README.md
│   └── saludtech
│       └── transformaciones # Carpeta con los archivos del microservicio de transformación
│           ├── api # Carpeta con los archivos de la API
│           │   └── anonimizacion.py
│           ├── config # Carpeta con los archivos de configuración
│           │   ├── db.py
│           │   └── uow.py
│           ├── modulos # Carpeta con los archivos de los módulos
│           │   └── anonimizacion  # Carpeta con los archivos del módulo de anonimización
│           │       ├── aplicacion # Carpeta con los archivos de la aplicación
│           │       │   ├── comandos # Carpeta con los archivos de comandos
│           │       │   │   ├── base.py
│           │       │   │   ├── cancelar_anonimizacion.py
│           │       │   │   ├── completar_anonimizacion.py
│           │       │   │   ├── iniciar_anonimizacion.py
│           │       │   │   └── reintentar_anonimizacion.py
│           │       │   ├── dto.py
│           │       │   ├── handlers.py
│           │       │   ├── mapeadores.py
│           │       │   ├── queries # Carpeta con los archivos de queries
│           │       │   │   ├── base.py
│           │       │   │   ├── consultar_estado_proceso.py
│           │       │   │   └── obtener_errores.py
│           │       │   └── servicios.py
│           │       ├── dominio # Carpeta con los archivos del dominio
│           │       │   ├── entidades.py
│           │       │   ├── eventos.py
│           │       │   ├── excepciones.py
│           │       │   ├── fabricas.py
│           │       │   ├── mixins.py
│           │       │   ├── objetos_valor.py
│           │       │   ├── reglas.py
│           │       │   ├── repositorios.py
│           │       │   └── servicios.py
│           │       └── infraestructura # Carpeta con los archivos de infraestructura
│           │           ├── consumidores.py
│           │           ├── despachadores.py
│           │           ├── dto.py
│           │           ├── excepciones.py
│           │           ├── fabricas.py
│           │           ├── mapeadores.py
│           │           ├── repositorios.py
│           │           └── schema # Carpeta con los archivos de schema
│           │               └── v1 # Carpeta con los archivos de la versión 1
│           │                   ├── comandos.py
│           │                   └── eventos.py
│           └── seedwork # Carpeta con los archivos de seedwork
│               ├── aplicacion # Carpeta con los archivos de la aplicación
│               │   ├── comandos.py
│               │   ├── dto.py
│               │   ├── handlers.py
│               │   ├── queries.py
│               │   └── servicios.py
│               ├── dominio # Carpeta con los archivos del dominio
│               │   ├── entidades.py
│               │   ├── eventos.py
│               │   ├── excepciones.py
│               │   ├── fabricas.py
│               │   ├── mixins.py
│               │   ├── objetos_valor.py
│               │   ├── reglas.py
│               │   ├── repositorios.py
│               │   └── servicios.py
│               ├── infraestructura # Carpeta con los archivos de infraestructura
│               │   ├── despachadores.py
│               │   ├── schema # Carpeta con los archivos de schema
│               │   │   └── v1 # Carpeta con los archivos de la versión 1
│               │   │       ├── comandos.py
│               │   │       ├── eventos.py
│               │   │       └── mensajes.py
│               │   ├── uow.py
│               │   └── utils.py
│               └── presentacion # Carpeta con los archivos de presentación
│                   └── api.py
├── src-gen # Carpeta con los diagramas generados por Context Mapper
├── tests # Carpeta con los tests
└── transformacion.Dockerfile # Dockerfile para el microservicio de transformación
```

## SaludTech
### Ejecutar Aplicación

Desde el directorio principal ejecute el siguiente comando.

```bash
flask --app src/saludtech/transformaciones/api run
```

Siempre puede ejecutarlo en modo DEBUG:

```bash
flask --app src/saludtech/transformaciones/api --debug run
```

### Ejecutar Aplicación con Docker


## Docker-compose

Para desplegar toda la arquitectura en un solo comando, usamos `docker-compose`. Para ello, desde el directorio principal, ejecute el siguiente comando:

```bash
docker-compose --profile transformaciones --profile saludtech-transformacion --profile pulsar up
```

En caso de querer desplegar dicha topología en el background puede usar el parametro `-d`.

```bash
docker-compose --profile transformaciones --profile saludtech-transformacion --profile pulsar up -d
```

Si desea detener el ambiente ejecute:

```bash
docker-compose stop
```

### RECOMENDADO: Ejecución en máquina local (si la ejecución de los perfiles falla)

En algunas ocasiones, al tratar de conectarse los contenedores de Pulsar, se puede presentar el siguiente error:

> Pulsar error: TimeOut

Por tal razón, se recomienda ejecutar la aplicación en su máquina local y puede hacerlo de la siguiente manera:

- Ejecute el perfil de pulsar de docker-compose:
  
```bash
docker-compose --profile pulsar up
```
  
- Luego, Desde el directorio principal ejecute el siguiente comando para ejecutar la aplicación:

```bash
flask --app src/saludtech/transformaciones/api --debug run
```


## Comandos útiles

### Correr docker-compose usando profiles
```bash
docker-compose --profile <pulsar|transformaciones|saludtech-transformacion> up
```




# Entrega 1
Los diagramas AS-IS y TO-BE se encuentran en la carpeta `src-gen`.  Estos diagramas fueron generados utilizando Context Mapper a partir de los archivos `.cml` ubicados en `docs/entrega1/`.

1. **Abra los archivos `.cml` (saludtechdemo-entrega1-as-is.cml y saludtechdemo-entrega1-to-be.cml) con Context Mapper.**

2. **Context Mapper generará automáticamente los diagramas en formato PNG.  Estos se guardan en `src-gen`.**

## Estructura del C&oacute;digo

El código fuente principal se encuentra en la carpeta `src/saludtech`.

### Las imágenes del lenguaje ubicuo se encuentran en el directorio: `./Lenguaje-obicuo`:

**Imagen de dominio y subdominios de AS-IS**
- `./Lenguaje-obicuo/Dominio y subdominios AS-IS.png`

**Imagen de dominio y subdominios de TO-BE**
- `./Lenguaje-obicuo/Dominio y subdominios TO - BE.png`

**Imagen de lenguaje obicuo AS-IS**
- `./Lenguaje-obicuo/Lenguaje ubicuo AS-IS.png`

**Imagen de lenguaje obicuo TO-BE**
- `./Lenguaje-obicuo/Dominio y subdominios TO - BE.png`

# Entrega 2

## Escenarios de calidad 

https://uniandes-my.sharepoint.com/:p:/r/personal/f_orduz_uniandes_edu_co/_layouts/15/Doc.aspx?sourcedoc=%7B1AEF6370-BDD5-4D44-9DF2-764CEBDFDC07%7D&file=Entrega%20Semana%205.pptx&action=edit&mobileredirect=true&DefaultItemOpen=1&web=1

## Escenario de calidad a validar

Dado el contexto y las condiciones previas planteadas, se optó por validar el escenario de calidad #4 **Exposición de APIs externas de Salutech**, que que pertenece al atributo de  **Interoperabilidad**. La razón detrás de esta decisión radica en la necesidad crítica de comprender y gestionar de manera efectiva los estados del proceso de carga de datos a la plataforma, particularmente en lo que respecta a las fases iniciales de los procesos de transformación y enriquecimiento de datos.

La interoperabilidad es un componente esencial en la infraestructura tecnológica de cualquier sistema, la exposición de APIs externas de Salutech juega un papel clave, ya que permite la integración de fuentes de datos externas al ecosistema de la plataforma, o cualquier cliente, consumidor o desarrollador que pueda llegar a hacer uso de la plataforma.

## Diagrama de arquitectura de experimento

Para este ejercicio, se tomo unicamente la parte de transformacion del flujo. Ademas se creo un endpoint HTTP que se encargaria de publicar la informacion neceesaria para simular el inicio del proceso de transformacion. Este componente llamado publicador se agrego unicamente con fines de experimentacion, no hace parte del flujo de datos.

En este caso el servicio de transformacion recibe un comando de de inicio de proceso de transformacion, persiste la solicitud en la base de datos del servicio, expone un metodo GET que se utiliza para obtener el estado del proceso y por ultimo envia el comando al siguiente paso

![image](https://github.com/user-attachments/assets/d7b10c81-84db-4b3d-b14c-e8ee33e1bcfd)

