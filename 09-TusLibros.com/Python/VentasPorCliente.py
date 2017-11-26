# coding=utf-8

from datetime import datetime, timedelta, date, time
from random import random

from Carrito import *
from Cajero import *


class VentasPorCliente():
    def __init__(self, ventasDelCliente, catalogo):
        self._catalogo = catalogo
        self._ventasPorProducto = {}
        self.inicializarVentas()
        self.agruparVentas(ventasDelCliente)

    def inicializarVentas(self):
        for producto in self._catalogo:
            self._ventasPorProducto[producto] = 0

    def agruparVentas(self, ventasPorCliente):
        for carrito in ventasPorCliente:
            for producto in carrito:
                self._ventasPorProducto[producto] += carrito[producto]
     
    def getVentasDeProducto(self, unProducto):
        return self._ventasPorProducto[unProducto]
    
    def getTotalVentasCantidad(self):
        totalVentas = 0
        for producto in self._ventasPorProducto:
            totalVentas += self.getVentasDeProducto(producto)
        return totalVentas
    
    def calcularMontoTotal(self):
        monto = 0
        for producto in self._ventasPorProducto:
            monto += self._catalogo[producto] * self.getVentasDeProducto(producto)
        return monto
    
    def hayVentas(self):
        return self.getTotalVentasCantidad() != 0