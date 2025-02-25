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
TODO
