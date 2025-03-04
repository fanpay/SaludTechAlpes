# Proyecto SaludTech de los Alpes 2025

Este repositorio contiene el código y la documentación del proyecto SaludTech de los Alpes 2025, desarrollado para el curso. El proyecto se centra en el diseño de la arquitectura para soportar la expansión global de la compañía, con un enfoque en escalabilidad y seguridad, especialmente en el mercado estadounidense y su cumplimiento con la ley HIPAA.

## Estructura del Proyecto

<details>

<summary>Click aquí para ver más detalle</summary>

``` bash
├── LICENSE
├── Lenguaje-obicuo # Carpeta con las imágenes del lenguaje ubicuo
├── README.md
├── collections # Carpeta con las colecciones de Postman
│   └── SALUDTECH.postman_collection.json
├── data # Carpeta temporal de Pulsar. Si ya existe, borrar antes de ejecutar por primera vez la aplicación
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
</details>

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

Tenga en cuenta que el sistema espera las siguientes variables de entorno:

```plaintext
POSTGRES_USER -> valor por defecto: postgres
POSTGRES_PASSWORD -> valor por defecto: postgres
POSTGRES_HOST -> valor por defecto: localhost
POSTGRES_PORT -> valor por defecto: 5432
POSTGRES_DB -> valor por defecto: transformacionesdb
BROKER_HOST -> valor por defecto: localhost
```

Si no se le especifican los valores, este asumirá los valores por defecto.

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

### Ejecución en máquina local (RECOMENDADO si la ejecución de los perfiles falla)

En algunas ocasiones, al tratar de conectarse los contenedores de Pulsar, se puede presentar el siguiente error:

> Pulsar error: TimeOut

Puede deberse a que Pulsar no ha iniciado correctamente debido a problemas con la carpeta `data` del mismo Pulsar que se crea en el directorio raíz del proyecto. Asegúrese de borrarla para evitar problemas.
> Más información: https://github.com/apache/bookkeeper/blob/405e72acf42bb1104296447ea8840d805094c787/bookkeeper-server/src/main/java/org/apache/bookkeeper/bookie/Cookie.java#L57-68


Por tal razón, se recomienda ejecutar la aplicación en su máquina local (luego de borrar la carpeta `data` anteriormente mencionada) y puede hacerlo de la siguiente manera:

- Ejecute el perfil de pulsar de docker-compose:
  
```bash
docker-compose --profile pulsar up
```

- Ejecute el perfil de la base de datos PostgreSQL de docker-compose:
  
```bash
docker-compose --profile transformaciones up
```
  
- Luego, Desde el directorio principal ejecute el siguiente comando para ejecutar la aplicación:

```bash
BROKER_HOST=localhost POSTGRES_USER=postgres POSTGRES_PASSWORD=postgres POSTGRES_DB=transformacionesdb POSTGRES_HOST=localhost POSTGRES_PORT=5432 flask --app src/saludtech/transformaciones/api --debug run
```

Si se realiza una ejecución manual, este dato debe cambiar en el archivo docker-compose.yml al siguiente:
```
- advertisedListeners=external:pulsar://127.0.0.1:6650
```

Asegúrate de pasarle las variables de entorno correctas.


## Comandos útiles

### Correr docker-compose usando profiles
```bash
docker-compose --profile <pulsar|transformaciones|saludtech-transformacion> up
```




# Entrega 1
<details>

<summary>Click aquí para ver más detalle</summary>

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

</details>

# Entrega 3

<details>

<summary>Click aquí para ver más detalle</summary>

## Escenarios de calidad 

https://uniandes-my.sharepoint.com/:p:/r/personal/f_orduz_uniandes_edu_co/_layouts/15/Doc.aspx?sourcedoc=%7B1AEF6370-BDD5-4D44-9DF2-764CEBDFDC07%7D&file=Entrega%20Semana%205.pptx&action=edit&mobileredirect=true&DefaultItemOpen=1&web=1

## Escenario de calidad a validar

Dado el contexto y las condiciones previas planteadas, se optó por validar el escenario de calidad #4 **Exposición de APIs externas de Salutech**, que que pertenece al atributo de  **Interoperabilidad**. La razón detrás de esta decisión radica en la necesidad crítica de comprender y gestionar de manera efectiva los estados del proceso de carga de datos a la plataforma, particularmente en lo que respecta a las fases iniciales de los procesos de transformación y enriquecimiento de datos.

La interoperabilidad es un componente esencial en la infraestructura tecnológica de cualquier sistema, la exposición de APIs externas de Salutech juega un papel clave, ya que permite la integración de fuentes de datos externas al ecosistema de la plataforma, o cualquier cliente, consumidor o desarrollador que pueda llegar a hacer uso de la plataforma.

## Diagrama de arquitectura de experimento

Para este ejercicio, se tomo unicamente la parte de transformacion del flujo. Ademas se creo un endpoint HTTP que se encargaria de publicar la informacion neceesaria para simular el inicio del proceso de transformacion. Este componente llamado publicador se agrego unicamente con fines de experimentacion, no hace parte del flujo de datos.

En este caso el servicio de transformacion recibe un comando de de inicio de proceso de transformacion, persiste la solicitud en la base de datos del servicio, expone un metodo GET que se utiliza para obtener el estado del proceso y por ultimo envia el comando al siguiente paso

![image](https://github.com/user-attachments/assets/d7b10c81-84db-4b3d-b14c-e8ee33e1bcfd)

</details>

# Entrega 4

Esto es un resumen de la entrega. El detalle asociado a los diferentes items, se justifican a lo largo del video de la entrega:


**Escenarios de calidad a validar:**

**Escenario 1:**
![Screenshot 2025-03-03 at 22 49 34](https://github.com/user-attachments/assets/01b5f2b1-f7d1-404d-b913-0d4df95acf4d)

**Escenario 2:**
![Screenshot 2025-03-03 at 22 49 42](https://github.com/user-attachments/assets/bf6a7e6d-302c-4bf8-9dfe-23e6d163af8f)

**Escenario 3:**
![Screenshot 2025-03-03 at 22 49 59](https://github.com/user-attachments/assets/2a2f1cd8-bc7d-4d6f-b069-6ce0fef1bcd2)


**Diagrama general de la arquitectura a validar (incluye detalle de mensajes para mayor claridad):**

![Arquitectura-entrega-4 drawio](https://github.com/user-attachments/assets/be43128f-3970-4b23-b80f-623fc6d685f9)


**Microservicios implementados (4 mínimo requeridos de acuerdo a las instrucciones del profesor + FrontEnd):**

- [BFF](https://github.com/fanpay/SaludTechAlpes/tree/main/src/bff_web)
- [Frontend](https://github.com/fanpay/SaludTechAlpes/tree/main/src/frontend)
- [MS Procesamiento](https://github.com/fanpay/SaludTechAlpes/tree/main/src/saludtech/procesamiento)
- [MS Transformaciones](https://github.com/fanpay/SaludTechAlpes/tree/main/src/saludtech/transformaciones)
- [MS Enriquecimiento](https://github.com/fanpay/SaludTechAlpes/tree/main/src/saludtech/enriquecimiento)

**Autenticación y autorización utilizada:**
- JWT + API Key

**Comunicación entre microservicios:**
- Asíncrona para eventos
- Síncrona para queries por medio de HTTP

**Modelo capa de datos utilizado:**
- CRUD

**Justificación bases de datos:**
- Modalidad usada: Híbrida:
- Ventajas en nuestro sistema:
  - Menos duplicidad de datos
  - Consultas eficientes
  - Simplicidad en la consistencia y transaccionalidad garantizando ACID
  - Menor cantidad de consultas cruzadas
  - Menos esfuerzo en la administración de base de datos
- Desventajas:
  - Incremento en el acoplamiento de los microservicios
  - La dificultad en la gobernanza de los datos
    
*Cabe aclarar que, en este caso; estamos haciendo es una agregación de los datos (aumentando la información en transformación). Esto no es un bloqueante sobre la base de datos así que el MS de transformación sería el que lleva la gobernanza sobre la base de datos y enriquecimiento únicamente va a complementar la información que hace transformación.*

**Plataforma de despliegue:**
- GCP

**URL de la aplicación:**
- http://34.71.215.107/login (atentos a instrucción del tutor para proveer el API Key)

**Video de la demostración:**
- https://drive.google.com/file/d/1IJuo8gYrqa_2waTIK6WnuAeU55IN6VQT/view?usp=sharing

**Tabla de distribución de responsabilidades:**

| **Responsable**          | **Microservicio**                          | **Actividad**                                                                                             |  
|--------------------------|--------------------------------------------|------------------------------------------------------------------------------------------------------------|  
| **Félix Orduz**          | **BFF + FrontEnd**                         | Integrar autenticación API Key/JWT en el frontend y validar tokens en el BFF (Backend for Frontend).     |  
| **Leonardo Bustamante**  | **Procesamiento**                          | Implementar pipelines de anonimización (enmascaramiento, tokenización) y garantizar trazabilidad.         |  
| **Esneider Velandia**    | **Enriquecimiento**                        | Añadir metadatos no sensibles a los datos anonimizados. |  
| **Fabián Payan**         | **Transformaciones**                       | Aplicar reglas de transformación de datos (ej. normalización, cifrado).   |  
| **Félix Orduz**          | **Despliegue GCP**                         | Configurar infraestructura en GCP para almacenamiento seguro de datos anonimizados. |  
| **Todos**                | **Ajustes, despliegue e integración**      | Realizar pruebas E2E de integración entre microservicios, ajustar políticas de acceso y desplegar en GCP. |  
