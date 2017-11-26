# coding=utf-8

from datetime import datetime, timedelta, date, time
from random import random

from Carrito import *

class Cajero:
	ERROR_CARRITO_VACIO = "El carrito provisto está vacio"
	ERROR_COMPORTAMIENTO_NO_MODELADO = "Se produjo una acción no contemplada."
	ERROR_TARJETA_VENCIDA = "La tarjeta esta vencida."

	def __init__(self,idUsuario, merchantProcesor, carrito, tarjeta, fecha):
		self._merchantProcesor = merchantProcesor
		self._carrito = carrito
		self.ValidarElCarritoNoEsVacio()
		self._tarjeta = tarjeta
		self.validarTarjetaParaLaVenta(self._tarjeta, fecha)
		self._fecha = fecha
		self._usuario = idUsuario

	def checkOut(self):
		monto = self.calcularMontoDeLaCompra(self._carrito)
		mpMessage = self._merchantProcesor.cobrarAUnaTarjeta(self._tarjeta, monto)
		return Sale(self.crearTransaccionID(), self, monto)
		
	def calcularMontoDeLaCompra(self, carrito):
		monto = 0
		for producto in carrito.dameProductos():
			monto = monto + carrito.dameCatalogo()[producto] * \
            carrito.cantidadDeAparciones(producto)
		if isinstance(monto, int):
			monto = float(monto)
		monto = round(monto, 2)
		return monto

	def validarTarjetaParaLaVenta(self, tarjeta, fechaDeHoy):
		if tarjeta.estaVencida(fechaDeHoy):
			raise Exception(self.ERROR_TARJETA_VENCIDA)

	def crearTransaccionID(self):
		return random()

	def ValidarElCarritoNoEsVacio(self):
		if self._carrito.estaVacio():
			raise Exception(self.ERROR_CARRITO_VACIO)
	
	def getUsuario(self):
		return self._usuario

	def getCarrito(self):
		return self._carrito


class Sale():
    	def __init__(self, IdVenta, Cajero, MontoVenta):
		self._IdVenta = IdVenta
		self._cajero = Cajero
		self._MontoVenta = MontoVenta

	def getIdVenta(self):
		return self._IdVenta

	def getTotal(self):
    		return self._MontoVenta

	def getCajero(self):
		return self._cajero

	def getIdVenta(self):
		return self._IdVenta


'''Cara interna'''
class MPSimulator():
	ERROR_TARJETA_VENCIDA = "La tarjeta esta vencida."
	ERROR_TARJETA_ROBADA = "Tarjeta Robada"
	ERROR_TARJETA_SIN_CREDITO = "Tarjeta Sin Credito"
	ERROR_COMPORTAMIENTO_NO_MODELADO = "Se produjo una acción no contemplada."
	''' Esto es lo más facil que podemos hacer sin tener que hacer toda la
	logica de un portfolio. Porque una tarjeta tiene que preguntar el saldo
	de la cuenta... Como hacemos tdd queremos hacer lo más sencillo que pase
	los tests y como además no nos piden que modelemos el comportamiento de
	la logica bancaria con esto alcanza.
	Otro test que no hacemos es que el simulator verifique que la tarjeta este
	vencida ya que lo verificamos nosotros. Somos conscientes que en la vida
	real el banco lo valida igual.'''

	def __init__(self, tarjetasRobadas, tarjetasSinSaldos):
		self._robadas = tarjetasRobadas
		self._sinSaldo = tarjetasSinSaldos

	def cobrarAUnaTarjeta(self, tarjeta, monto):
		numeroTarjeta = tarjeta.numero()
		if numeroTarjeta in self._robadas:
			raise Exception(self.ERROR_TARJETA_ROBADA)
		elif numeroTarjeta in self._sinSaldo:
			raise Exception(self.ERROR_TARJETA_SIN_CREDITO)


'''cara externa'''
class MPtoHTTP():
	def cobrarAUnaTarjeta(self, tarjeta, monto):
		toMPasHTTP(tarjeta.nombre, tar)
