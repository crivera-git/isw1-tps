# coding=utf-8
import unittest
from datetime import datetime, timedelta

class Carrito:
	ERROR_ELEMENTO_FUERA_DEL_CATALOGO = "El producto agregado no pertenece al catalogo"
	ERROR_CANTIDAD_APARICIONES_NO_POSITIVO = "La cantidad de apariciones es menor o igual a 0"
	ERROR_CANTIDAD_APARICIONES_NO_ENTERA = "Como cantidad de apariciones se obtuvo numero no entero"
	ERROR_COMPORTAMIENTO_NO_MODELADO = "Se produjo una acción no contemplada."
	def __init__(self, unCatalogo):
		self._elementos = {}
		self._catalogo = unCatalogo
	def cantidadElementos(self):
		cantidadElementos = 0
		for clave in self._elementos:
			cantidadElementos += self._elementos[clave]
		return cantidadElementos
	def estaEnElCarrito(self, unElemento):
		return unElemento in self._elementos
	def cantidadDeAparciones(self, unElemento):
		return self._elementos[unElemento]
	def estaVacio(self):
		return len(self._elementos) == 0
	def dameCatalogo(self):
		return self._catalogo
	def dameProductos(self):
		return self._elementos
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

class Cajero:
	ERROR_CARRITO_VACIO = "El carrito provisto está vacio"
	ERROR_COMPORTAMIENTO_NO_MODELADO = "Se produjo una acción no contemplada."
	def __init__(self,catalogo):
		self._catalogoConPrecios = catalogo
		self._merchantProcesor = MerchanProcesor()
	def dameMerchantProcesor(self):
		return self._merchantProcesor
	def checkOut(self, carrito, tarjeta):
		if carrito.estaVacio():
			raise Exception( self.ERROR_CARRITO_VACIO )
		elif self.elCatalogoDelCarritoEsValido(carrito):
			self._merchantProcesor.validarTarjetaParaLaCompra(tarjeta)
			monto = self.calcularMontoDeLaCompra(carrito)
			self._merchantProcesor.cobrarAUnaTarjeta(tarjeta)
		else:
			raise Exception( self.ERROR_COMPORTAMIENTO_NO_MODELADO )
	def elCatalogoDelCarritoEsValido(self, carrito):
		respuesta = True
		for producto in carrito.dameCatalogo():
			respuesta = respuesta and (producto in self._catalogoConPrecios)
		return respuesta
	def calcularMontoDeLaCompra(self, carrito):
		monto = 0
		for producto in carrito.dameProductos():
			monto = monto + self._catalogoConPrecios[producto] * \
			carrito.cantidadDeAparciones(producto)
		return monto

class MerchanProcesor():
	ERROR_TARJETA_VENCIDA = "La tarjeta esta vencida."
	def __init__(self):
		pass
	def validarTarjetaParaLaCompra(self, tarjeta):
		if tarjeta.dameVecimiento() < datetime.today():
			raise Exception( self.ERROR_TARJETA_VENCIDA )
		else:
			return True
	def cobrarAUnaTarjeta(self, tarjeta):
		pass

class Tarjeta:
	ERROR_OBJETO_INVALIDO = "Los parámetros no son correctos."
	def __init__(self,expedicion,vencimiento):
		self._expedicion = expedicion
		self._vencimiento = vencimiento
		self.validarQueElObjetoSeaValido()
	def validarQueElObjetoSeaValido(self):
		if not self.guardaValidarObjeto():
			raise Exception( self.ERROR_OBJETO_INVALIDO )
	def guardaValidarObjeto(self):
		return isinstance(self._vencimiento, datetime) and \
		isinstance(self._expedicion, datetime) and \
		(self._vencimiento > self._expedicion)
	def dameVecimiento(self):
		return self._vencimiento

class testXX(unittest.TestCase):
	def test01CuandoCreoElCarritoEsteEstaVacio(self):
		unCatalogo = []
		unCarrito = Carrito(unCatalogo)
		self.assertTrue( unCarrito.estaVacio() )
	def test02AgregoUnLibroAUnCarritoVacioYSoloContieneAEsteLibro(self):
		unElemento = "unProducto"
		unCatalogo = [unElemento]
		unCarrito = Carrito(unCatalogo)
		unCarrito.agregarElemento(unElemento, 1)
		self.assertEquals( 1, unCarrito.cantidadElementos() )
		self.assertEquals( True, unCarrito.estaEnElCarrito(unElemento) )
	def test03AgregoUnLibroQueNoPerteneceAlCatalogo(self):
		unElemento = 1
		otroElemento = 2
		unCatalogo = [unElemento]
		unCarrito = Carrito(unCatalogo)
		try:
			unCarrito.agregarElemento(otroElemento,1)
			self.fail()
		except Exception as libroFueraCatalogo:
			self.assertEquals( Carrito.ERROR_ELEMENTO_FUERA_DEL_CATALOGO, libroFueraCatalogo.message )
			self.assertEquals( 0, unCarrito.cantidadElementos())
	''' testing'''
	def test04AgregarMuchoElementosFunciona(self):
		elemento1 = 1
		elemento2 = 12
		elemento3 = 13
		elemento4 = 14
		unCatalogo = [elemento1,elemento2,elemento3, elemento4]
		unCarrito = Carrito(unCatalogo)

		unCarrito.agregarElemento(elemento1,1)
		unCarrito.agregarElemento(elemento2,1)
		unCarrito.agregarElemento(elemento3,1)
		unCarrito.agregarElemento(elemento4,1)

		self.assertEquals( 4, unCarrito.cantidadElementos() )
		self.assertEquals( True, unCarrito.estaEnElCarrito(elemento1) )
		self.assertEquals( True, unCarrito.estaEnElCarrito(elemento2) )
		self.assertEquals( True, unCarrito.estaEnElCarrito(elemento3) )
		self.assertEquals( True, unCarrito.estaEnElCarrito(elemento4) )
	def test05AgregoVariosDelMismoLibroYSuCantidadDeAparicionesEsCorrecta(self):
		unElemento = 1
		unCatalogo = [unElemento]
		unCarrito = Carrito(unCatalogo)
		unCarrito.agregarElemento(unElemento,1)
		unCarrito.agregarElemento(unElemento,5)
		unCarrito.agregarElemento(unElemento,1)
		unCarrito.agregarElemento(unElemento,3)
		self.assertEquals( 10, unCarrito.cantidadElementos() )
		self.assertEquals( 10, unCarrito.cantidadDeAparciones(unElemento) )
	def test06NoPuedoAgregarCantidadNoPositivaDeProductos(self):
			unElemento = 1
			unCatalogo = [unElemento]
			unCarrito = Carrito(unCatalogo)
			try:
				unCarrito.agregarElemento(unElemento,-5)
				self.fail()
			except Exception as apariconesInvalidas:
				self.assertEquals( Carrito.ERROR_CANTIDAD_APARICIONES_NO_POSITIVO, apariconesInvalidas.message )
				self.assertEquals( 0, unCarrito.cantidadElementos())
	def test07NoPuedoAgregarCantidadNoEnteraDeProductos(self):
		unElemento = 1
		unCatalogo = [unElemento]
		unCarrito = Carrito(unCatalogo)
		try:
			unCarrito.agregarElemento(unElemento,1.5)
			self.fail()
		except Exception as apariconesInvalidas:
			self.assertEquals( Carrito.ERROR_CANTIDAD_APARICIONES_NO_ENTERA, apariconesInvalidas.message )
			self.assertEquals( 0, unCarrito.cantidadElementos())
	'''----------------------------Fin test carrito--------------------------'''
	def test08NoPodemosCobrarAUnCarritoVacio(self):
		unCatalogo = []
		unCarrito = Carrito(unCatalogo)
		unCatalogoConPrecios = {}
		unCajero = Cajero(unCatalogoConPrecios)
		expedicion = datetime.today() - timedelta(days=40)
		vencimiento = datetime.today() - timedelta(days=10)
		tarjeta = Tarjeta(expedicion,vencimiento)
		try:
			unCajero.checkOut(unCarrito,tarjeta)
			self.fail()
		except Exception as carritoVacio:
			self.assertEquals( unCajero.ERROR_CARRITO_VACIO, carritoVacio.message )
	def test09ElCatalogoDeElCajeroTieneTodosLosProductosQueTieneElCatalogoDelCarrito(self):
		unCatalogo = ["Producto1",2,"Producto3"]
		unCarrito = Carrito(unCatalogo)
		unCatalogoConPrecios = {"Producto1": 1.3, 2: 2,"Producto3":4,5 :2}
		unCajero = Cajero(unCatalogoConPrecios)
		self.assertTrue( unCajero.elCatalogoDelCarritoEsValido(unCarrito) )
	def test10ElMontoDeUnCarritoConUnProductoEsCorrecto(self):
		unCatalogo = ["Producto1",2,"Producto3"]
		unCarrito = Carrito(unCatalogo)
		unCatalogoConPrecios = {"Producto1": 10, 2: 2,"Producto3":4,5 :2}
		unCajero = Cajero(unCatalogoConPrecios)

		unCarrito.agregarElemento("Producto1", 1)#count 10

		self.assertEquals( 10, unCajero.calcularMontoDeLaCompra(unCarrito) )
	'''testing. Nos dimos cuenta que este test no necesariamente debería ser
	testing si nosotros hubiésemos implementado el metodo calcularMontoDeLaCompra
	de una manera más sencilla como por ejemplo solo tomar un elemento. Lo tendremos
	en cuenta para los siguientes tests.'''
	''' De todos modos no le encontramos el sentido de "mal" un algoritmo que es
	sencillo solo para seguir el modelo de TDD. Cuál es el por qué de esto?'''
	def test11ElMontoDeUnCarritoConMuchosElementosYMuchasAparciones(self):
		unCatalogo = ["Producto1",2,"Producto3"]
		unCarrito = Carrito(unCatalogo)
		unCatalogoConPrecios = {"Producto1": 10, 2: 2,"Producto3":4,5 :2}
		unCajero = Cajero(unCatalogoConPrecios)

		unCarrito.agregarElemento("Producto1", 5)#count 50
		unCarrito.agregarElemento(2,5)#count 60
		unCarrito.agregarElemento("Producto3", 10)#count 100

		self.assertEquals( 100, unCajero.calcularMontoDeLaCompra(unCarrito) )
	''' Como hacer para testear la creación de objetos invalidos en python'''
	def test12NoSePuedeCrearTarjetaInvalida(self):
		pass
		# try:
		# 	expedicion = datetime.today() - timedelta(days=40)
		# 	vencimiento = datetime.today() - timedelta(days=50)
		# 	unaTarjeta = Tarjeta(expedicion,vencimiento)
		# 	self.fail()
		# except Exception as tarjetaInvalida:
		# 	self.assertEquals( unaTarjeta.ERROR_OBJETO_INVALIDO, tarjetaInvalida.message )
	def test13NoSePuedeComprarConUnaTarjetaVencida(self):
		unCatalogo = ["Producto1",2,"Producto3"]
		unCarrito = Carrito(unCatalogo)
		unCatalogoConPrecios = {"Producto1": 10, 2: 2,"Producto3":4,5 :2}
		unCajero = Cajero(unCatalogoConPrecios)
		expedicion = datetime.today() - timedelta(days=40)
		vencimiento = datetime.today() - timedelta(days=10)
		unaTarjeta = Tarjeta(expedicion,vencimiento)

		unCarrito.agregarElemento("Producto1",2)
		try:
			unCajero.checkOut(unCarrito, unaTarjeta)
			self.fail()
		except Exception as tarjetaVencida:
			self.assertEquals( unCajero.dameMerchantProcesor().ERROR_TARJETA_VENCIDA,\
			tarjetaVencida.message )



if __name__ == "__main__":
	unittest.main()
