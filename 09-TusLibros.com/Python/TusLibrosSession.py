# coding=utf-8

from datetime import datetime, timedelta, date, time
from random import random

from Carrito import *
from Cajero import *

class TusLibrosSession():
    ERROR_TIMEOUT = "Tiempo de inactividad excedido."

    def __init__(self, unNombreDeUsuario, unCarrito, unReloj):
        self._usuario = unNombreDeUsuario
        self._relojSession = unReloj
        self._horaUltimaOperacion = self._relojSession.now()
        self._carrito = unCarrito
    
    def validarHoraDeLaUltimaOperacion(self):
    	horaActual = self._relojSession.now()
        if (horaActual - self._horaUltimaOperacion) > timedelta(minutes=30):
			raise Exception(self.ERROR_TIMEOUT)
        else:
            self._horaUltimaOperacion = horaActual
    
    def listCart(self):
        return self._carrito.dameProductos()

    def addToCart(self, unElemento, unaCantidad):
        self.validarHoraDeLaUltimaOperacion()
        self._carrito.agregarElemento(unElemento, unaCantidad)
        
    def checkOutCart(self, cajero):
        self.validarHoraDeLaUltimaOperacion()
        return cajero.checkOut()

    def getCarrito(self):
        return self._carrito
    
