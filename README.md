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
