# coding=utf-8

from datetime import datetime, timedelta, date, time
from random import random

from VentasPorCliente import *
from TusLibrosSession import *
from Carrito import *
from Cajero import *

'''cara interna de rest'''
class SistemMisLibros:
	ERROR_USUARIO_INEXISTENTE = "El usuario no existe."
	ERROR_CLAVE_INVALIDA = "La clave no es correcta."
	ERROR_ID_INEXISTENTE = "La id no existe."
	ERROR_TIMEOUT = "Tiempo de inactividad excedido."

	def __init__(self, Usuarios, unCatalogo, merchantProcesor, reloj):
		self._usuarios = Usuarios  # diccionario usuario : contraseña
		self._comprasPorUsuario = {}
		for usuario in self._usuarios:
		 	self._comprasPorUsuario[usuario] = []
		# diccionario idCarrito : (usuarioAlQuePertenece,carrito, horaUltimaOperación)
		#self._carritos = {}
		self._sessions = {}
		self._catalogo = unCatalogo
		self._merchantProcesor = merchantProcesor
		self._reloj = reloj
		self._salesBook = []

	def createCart(self, unUsuario, unaClave):
		self.validarUsuario(unUsuario, unaClave)
		IDNueva = self.crearId()
		unaSession = TusLibrosSession(unUsuario, Carrito(self._catalogo), self._reloj)
		self._sessions[IDNueva] = unaSession
		return IDNueva

	def listCart(self, unId):
	   	return self.getSession(unId).listCart()
	
	def addToCart(self, unUsuario, unElemento, unaCantidad):
		self.getSession(unUsuario).addToCart(unElemento, unaCantidad)
		
	def checkOutCart(self, idUsuario, nroTarjeta, fechaVencimientoTarjeta, nombreTarjeta):
		session = self.getSession(idUsuario)
		tarjeta = Tarjeta(fechaVencimientoTarjeta, nroTarjeta, nombreTarjeta)
		fecha = self.fechaDeHoy()
		carrito = session.getCarrito()
		venta = session.checkOutCart(Cajero(idUsuario,self._merchantProcesor, carrito,\
		tarjeta, fecha))
		self._salesBook.append(venta)
		return venta.getIdVenta()

	def listPurchases(self, unUsuario, unaClave):
		self.validarUsuario(unUsuario, unaClave)
		ventasDelCliente = []
		for sale in self._salesBook:
			if(sale.getCajero().getUsuario() == unUsuario):
				ventasDelCliente.append(sale.getCajero().getCarrito())
		return VentasPorCliente(ventasDelCliente, self._catalogo)

	def crearId(self):
		return random()

	def getSession(self, unUsuario):
		if not(unUsuario in self._sessions):
			raise Exception(self.ERROR_ID_INEXISTENTE)
		return self._sessions[unUsuario]
	
	def validarUsuario(self, unUsuario, unaClave):
		if not(unUsuario in self._usuarios):
			raise Exception(self.ERROR_USUARIO_INEXISTENTE)
		else:
			if self._usuarios[unUsuario] != unaClave:
				raise Exception(self.ERROR_CLAVE_INVALIDA)

	def fechaDeHoy(self):
    		fecha = date.today()
		fechaNuestroModelo = FechaMMAA(fecha.month, fecha.year)
		return fechaNuestroModelo


class Tarjeta:
    	ERROR_OBJETO_INVALIDO = "Los parámetros no son correctos."
	def __init__(self,vencimiento,numero,nombre):
    		self._vencimiento = vencimiento
		self._numero = numero
		self._nombre = nombre
		self.validarQueElObjetoSeaValido()
	def validarQueElObjetoSeaValido(self):
    		if not ( (16 == len(str(self._numero))) and isinstance(self._nombre, str) ):
    			raise Exception( self.ERROR_OBJETO_INVALIDO )
	def estaVencida(self, fechaDeHoy):
    		return self._vencimiento.esMenor(fechaDeHoy)
	def numero(self):
		return self._numero


class FechaMMAA:
	def __init__(self, mes, anio):
		self._mes = mes
		self._anio = anio
	def dameMes(self):
		return self._mes
	def dameAnio(self):
		return self._anio
	def esMenor(self, other):
		respuesta = self._anio < other.dameAnio()
		if self._anio == other.dameAnio():
			respuesta = self._mes < other.dameMes()
		return respuesta


class Reloj():
		def __init__(self):
			self._fechaInicial = datetime.now()
			self._fechaConTiempoAgregado = datetime.now()

		def now(self):
			tiempoActual = datetime.now()
			tiempoAgregado = self._fechaConTiempoAgregado - self._fechaInicial
			return tiempoActual + tiempoAgregado

		def agregarTiempo(self):
    			self._fechaConTiempoAgregado = self._fechaConTiempoAgregado + \
				timedelta(minutes=32)


