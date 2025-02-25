# Proyecto SaludTech de los Alpes 2025

Este repositorio contiene el código y la documentación del proyecto SaludTech de los Alpes 2025, desarrollado para el curso. El proyecto se centra en el diseño de la arquitectura para soportar la expansión global de la compañía, con un enfoque en escalabilidad y seguridad, especialmente en el mercado estadounidense y su cumplimiento con la ley HIPAA.

## Estructura del Proyecto

``` bash
├── README.md              # Este archivo, con las instrucciones de uso
├── docs                   # Documentación del proyecto
│   └── entrega1           # Artefactos de la entrega 1
│       ├── saludtechdemo-entrega1-as-is.cml    # Modelo AS-IS en Context Mapper
│       └── saludtechdemo-entrega1-to-be.cml    # Modelo TO-BE en Context Mapper
├── pyproject.toml          # Archivo de configuración de Python
├── requirements.txt        # Dependencias del proyecto
├── src-gen                # Artefactos generados (diagramas, etc.)
│   ├── saludtechdemo-entrega1-as-is_ContextMap.png   # Diagrama AS-IS
│   └── saludtechdemo-entrega1-to-be_ContextMap.png   # Diagrama TO-BE
├── .gitpod.yml # indica a Gitpod cómo preparar y compilar un proyecto
├── .gitpod.Dockerfile
```

# Entrega 1
Los diagramas AS-IS y TO-BE se encuentran en la carpeta `src-gen`.  Estos diagramas fueron generados utilizando Context Mapper a partir de los archivos `.cml` ubicados en `docs/entrega1/`.

1. **Abra los archivos `.cml` (saludtechdemo-entrega1-as-is.cml y saludtechdemo-entrega1-to-be.cml) con Context Mapper.**

2. **Context Mapper generará automáticamente los diagramas en formato PNG.  Estos se guardan en `src-gen`.**

### Estructura del Código

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

