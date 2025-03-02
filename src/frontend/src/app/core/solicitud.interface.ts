export interface Solicitud {
  usuario: string;
  nombre_paciente: string;
  cedula: string;
  descripcion: string;
  metadatos: Metadatos;
  configuracion: Configuracion;
  referencia_entrada: Referencia;
}

interface Metadatos {
  modalidad: string;
  region: string;
  resolucion: Resolucion;
  fecha_adquisicion: Date;
}

interface Resolucion {
  alto: number;
  ancho: number;
  dpi: number;
}

interface Configuracion {
  nivel_anonimizacion: number;
  formato_salida: string;
  ajustes_contraste: AjustesContraste;
  algoritmo: string;
}

interface AjustesContraste {
  brillo: number;
  contraste: number;
}

interface Referencia {
  llave_objeto: string;
  nombre_bucket: string;
  proveedor_almacenamiento: string;
}
