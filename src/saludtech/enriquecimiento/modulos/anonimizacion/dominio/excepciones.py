""" Excepciones del dominio de anonimizacion

En este archivo usted encontrará los Excepciones relacionadas
al dominio de anonimizacion

"""

from saludtech.enriquecimiento.seedwork.dominio.excepciones import ExcepcionFabrica

class TipoObjetoNoExisteEnDominioAnonimizacionExcepcion(ExcepcionFabrica):
    def __init__(self, mensaje='No existe una fábrica para el tipo solicitado en el módulo de anonimizacion'):
        self.__mensaje = mensaje
    def __str__(self):
        return str(self.__mensaje)