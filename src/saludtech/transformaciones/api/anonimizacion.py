from saludtech.transformaciones.modulos.anonimizacion.infraestructura.despachadores import Despachador
import saludtech.transformaciones.seedwork.presentacion.api as api
import json
from saludtech.transformaciones.modulos.anonimizacion.aplicacion.servicios import ServicioAnonimizacion
from saludtech.transformaciones.modulos.anonimizacion.aplicacion.dto import ReservaDTO
from saludtech.transformaciones.seedwork.dominio.excepciones import ExcepcionDominio

from flask import redirect, render_template, request, session, url_for
from flask import Response
from saludtech.transformaciones.modulos.anonimizacion.aplicacion.mapeadores import MetadatosImagenDTO, ResultadoProcesamientoDTO, ReferenciaAlmacenamientoDTO, MapeadorImagenAnonimizadaDTOJson, ConfiguracionAnonimizacionDTO
from saludtech.transformaciones.modulos.anonimizacion.aplicacion.comandos.iniciar_anonimizacion import IniciarAnonimizacion
from saludtech.transformaciones.modulos.anonimizacion.aplicacion.queries.consultar_estado_proceso import ObtenerEstadoProceso
from saludtech.transformaciones.seedwork.aplicacion.comandos import ejecutar_commando
from saludtech.transformaciones.seedwork.aplicacion.queries import ejecutar_query

bp = api.crear_blueprint('anonimizacion', '/anonimizacion')

@bp.route('/iniciar', methods=('POST',))
def iniciar_anonimizacion():
    try:
        imagen_dict = request.json

        map_imagen = MapeadorImagenAnonimizadaDTOJson()
        imagen_dto = map_imagen.externo_a_dto(imagen_dict)

        servicio = ServicioAnonimizacion()
        dto_final = servicio.iniciar_anonimizacion(imagen_dto)

        return map_imagen.dto_a_externo(dto_final)
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')

@bp.route('/iniciar-comando', methods=('POST',))
def iniciar_anonimizacion_asincrona():
    try:
        imagen_dict = request.json

        map_imagen = MapeadorImagenAnonimizadaDTOJson()
        imagen_dto = map_imagen.externo_a_dto(imagen_dict)

        comando = IniciarAnonimizacion(
            id=imagen_dto.id,
            metadatos=imagen_dto.metadatos,
            configuracion=imagen_dto.configuracion,
            referencia_entrada=imagen_dto.referencia_entrada
        )
        
        despachador = Despachador()
        despachador.publicar_comando(comando, 'comandos-anonimizacion')

        
        return Response('{}', status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')


@bp.route('/estado/<id>', methods=('GET',))
def dar_reserva_usando_query(id=None):
    try:
        if id:
            query_resultado = ejecutar_query(ObtenerEstadoProceso(id))
            map_reserva = MapeadorImagenAnonimizadaDTOJson()
            
            return map_reserva.dto_a_externo(query_resultado.resultado)
        else:
            return [{'message': 'GET!'}]
    
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')