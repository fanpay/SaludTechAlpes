import uuid
from saludtech.procesamiento.modulos.procesamiento.infraestructura.despachadores import Despachador
import saludtech.procesamiento.seedwork.presentacion.api as api
import json
from saludtech.procesamiento.modulos.procesamiento.aplicacion.servicios import ServicioAnonimizacion
from saludtech.procesamiento.modulos.procesamiento.aplicacion.dto import *
from saludtech.procesamiento.seedwork.dominio.excepciones import ExcepcionDominio

from flask import redirect, render_template, request, session, url_for
from flask import Response
from saludtech.procesamiento.modulos.procesamiento.aplicacion.mapeadores import MapeadorImagenDTOJson, MapeadorRespuestaImagenDTOJson, MapeadorImagen
from saludtech.procesamiento.modulos.procesamiento.aplicacion.comandos.iniciar_anonimizacion import IniciarAnonimizacion
from saludtech.procesamiento.modulos.procesamiento.aplicacion.queries.consultar_estado_proceso import ObtenerEstadoProceso
from saludtech.procesamiento.seedwork.aplicacion.comandos import ejecutar_commando
from saludtech.procesamiento.seedwork.aplicacion.queries import ejecutar_query

bp = api.crear_blueprint('anonimizacion', '/anonimizacion')

@bp.route('/crear-solicitud', methods=('POST',))
def iniciar_anonimizacion_asincrona():
    try:
        imagen_dict = request.json

        map_imagen = MapeadorImagenDTOJson()
        imagen_dto = map_imagen.externo_a_dto(imagen_dict)

        comando = IniciarAnonimizacion(
            id=imagen_dto.id,
            metadatos=imagen_dto.metadatos,
            nombre=imagen_dto.nombre,
            usuario=imagen_dto.usuario,
            id_solicitud=imagen_dto.id_solicitud,
            cedula=imagen_dto.cedula,
            configuracion=imagen_dto.configuracion,
            referencia_entrada=imagen_dto.referencia_entrada
        )
        
        despachador = Despachador()
        despachador.publicar_comando(comando, 'comandos-procesamiento7')

        
        return Response(imagen_dto.id_solicitud, status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')


@bp.route('/solicitudes/<usuario>', methods=('GET',))
def dar_reserva_usando_query(usuario=None):
    try:
        if id:
            query_resultado = ejecutar_query(ObtenerEstadoProceso(usuario))
            map_reserva = MapeadorRespuestaImagenDTOJson()
            
            resultado_serializable =[map_reserva.dto_a_externo(item) for item in query_resultado.resultado]
            
            return resultado_serializable
            #return Response(json.dumps(resultado_serializable), status=200, mimetype='application/json')
        else:
            return [{'message': 'GET!'}]
    
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')