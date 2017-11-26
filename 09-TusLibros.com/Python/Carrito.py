# coding=utf-8
from datetime import datetime, timedelta, date, time
from random import random

class Carrito:
	ERROR_ELEMENTO_FUERA_DEL_CATALOGO = "El producto agregado no pertenece al catalogo"
	ERROR_CANTIDAD_APARICIONES_NO_POSITIVO = "La cantidad de apariciones es menor o igual a 0"
	ERROR_CANTIDAD_APARICIONES_NO_ENTERA = "Como cantidad de apariciones se obtuvo numero no entero"
	ERROR_COMPORTAMIENTO_NO_MODELADO = "Se produjo una acción no contemplada."
	ERROR_CARRITO_VACIO = "Carrito Vacio"
	def __init__(self, unCatalogo):
		self._elementos = {}
		self._catalogo = unCatalogo
	def cantidadElementos(self):
		cantidadElementos = 0
		for clave in self._elementos:
			cantidadElementos += self._elementos[clave]
		return cantidadElementos
	def estaEnElCarrito(self, unElemento):
		if self.estaVacio() :
			raise Exception(self.ERROR_CARRITO_VACIO)
		return unElemento in self._elementos
	def cantidadDeAparciones(self, unElemento):
		return self._elementos[unElemento]
	def estaVacio(self):
		return len(self._elementos) == 0
	def dameCatalogo(self):
		return self._catalogo
	def dameProductos(self):
		res = self._elementos
		return res
	def agregarElemento(self, unElemento, cantidadDeAparicionesDeUnElemento):
		if isinstance(cantidadDeAparicionesDeUnElemento, float):
			raise Exception(self.ERROR_CANTIDAD_APARICIONES_NO_ENTERA)
		elif cantidadDeAparicionesDeUnElemento <= 0:
			raise Exception(self.ERROR_CANTIDAD_APARICIONES_NO_POSITIVO)
		elif unElemento in self._catalogo:
			if unElemento in self._elementos:
				self._elementos[unElemento] += cantidadDeAparicionesDeUnElemento
			else:
				self._elementos[unElemento] = cantidadDeAparicionesDeUnElemento
		elif not(unElemento in self._catalogo):
			raise Exception( self.ERROR_ELEMENTO_FUERA_DEL_CATALOGO )
		else:
			raise Exception( self.ERROR_PARAMENTRO_INVALIDO )
