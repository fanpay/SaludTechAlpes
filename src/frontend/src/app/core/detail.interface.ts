export interface Detail {
    error: string | null
    estado: string
    fecha_solicitud: Date
    fecha_ultima_actualizacion: Date
    id: string
    metadatos: Metadatos
    referencia_entrada: Referencia
    referencia_salida: string | null
    resultado: string | null
}

interface Metadatos {
    fecha_adquisicion: Date
    modalidad: string
    region: string
    resolucion: string
}

interface Referencia {
    llave_objeto: string
    nombre_bucket: string
    proveedor_almacenamiento: string
}


export interface Solicitud {
  error: string | null
  estado: string
  fecha_solicitud: Date
  fecha_ultima_actualizacion: Date
  id: string
  id_solicitud: string
  metadatos: Metadatos
  referencia_entrada: Referencia
  referencia_salida: string | null
  resultado: string | null
}
