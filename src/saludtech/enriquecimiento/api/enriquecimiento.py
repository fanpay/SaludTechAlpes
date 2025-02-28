import uuid
from saludtech.enriquecimiento.modulos.enriquecimineto.infraestructura.despachadores import Despachador
import saludtech.enriquecimiento.seedwork.presentacion.api as api
import json
from saludtech.enriquecimiento.modulos.enriquecimineto.aplicacion.servicios import ServicioAnonimizacion
from saludtech.enriquecimiento.modulos.enriquecimineto.aplicacion.dto import *
from saludtech.enriquecimiento.seedwork.dominio.excepciones import ExcepcionDominio

from flask import redirect, render_template, request, session, url_for
from flask import Response
from saludtech.enriquecimiento.modulos.enriquecimineto.aplicacion.mapeadores import MapeadorImagenAnonimizadaDTOJson, MapeadorRespuestaImagenAnonimizadaDTOJson, MapeadorImagenAnonimizada
from saludtech.enriquecimiento.modulos.enriquecimineto.aplicacion.comandos.iniciar_anonimizacion import IniciarAnonimizacion
from saludtech.enriquecimiento.modulos.enriquecimineto.aplicacion.queries.consultar_estado_proceso import ObtenerEstadoProceso
from saludtech.enriquecimiento.seedwork.aplicacion.comandos import ejecutar_commando
from saludtech.enriquecimiento.seedwork.aplicacion.queries import ejecutar_query

bp = api.crear_blueprint('enriquecimiento', '/enriquecimiento')

@bp.route('/enriquecimiento', methods=('POST',))
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

@bp.route('/enriquecimiento-comando', methods=('POST',))
def iniciar_anonimizacion_asincrona():
    try:
        imagen_dict = request.json

        map_imagen = MapeadorImagenAnonimizadaDTOJson()
        imagen_dto = map_imagen.externo_a_dto(imagen_dict)

        comando = IniciarAnonimizacion(
            id=str(uuid.uuid4()),
            metadatos=imagen_dto.metadatos,
            configuracion=imagen_dto.configuracion,
            referencia_entrada=imagen_dto.referencia_entrada
        )
        
        despachador = Despachador()
        despachador.publicar_comando(comando, 'comandos-anonimizacion9')

        
        return Response('{}', status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')


@bp.route('/estado-query/<id>', methods=('GET',))
def dar_reserva_usando_query(id=None):
    try:
        if id:
            query_resultado = ejecutar_query(ObtenerEstadoProceso(id))
            map_reserva = MapeadorRespuestaImagenAnonimizadaDTOJson()
            
            resultado_serializable = map_reserva.dto_a_externo(query_resultado.resultado)
            
            return resultado_serializable
            #return Response(json.dumps(resultado_serializable), status=200, mimetype='application/json')
        else:
            return [{'message': 'GET!'}]
    
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')