# coding=utf-8
import unittest
from datetime import datetime, timedelta, date, time
from random import random


class Sale:
	def __init__(self,IdVenta,Cajero,MontoVenta):
		self._IdVenta = IdVenta
		self._cajero = Cajero
		self._MontoVenta = MontoVenta
	def getIdVenta(self):
		return self._IdVenta
	def getTotal(self):
		return self._MontoVenta
	def getCajero(self):
		return self._cajero


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

class Cajero:
	ERROR_CARRITO_VACIO = "El carrito provisto está vacio"
	ERROR_COMPORTAMIENTO_NO_MODELADO = "Se produjo una acción no contemplada."
	ERROR_TARJETA_VENCIDA = "La tarjeta esta vencida."
	def __init__(self,merchantProcesor):
		self._merchantProcesor = merchantProcesor
	def dameUltimoCarrito(self):
		return self._salesBook[len(self._salesBook)-1]
	def validarTarjetaParaLaCompra(self, tarjeta, fechaDeHoy):
		if tarjeta.estaVencida(fechaDeHoy):
			raise Exception( self.ERROR_TARJETA_VENCIDA )
	# def cobrarAUnaTarjeta(self,tarjeta,fecha):
	# 	pass
	def creartransaccionID(self):
		return random()
	def checkOut(self, carrito, tarjeta, unaFecha):
		if carrito.estaVacio():
			raise Exception( self.ERROR_CARRITO_VACIO )
		elif not carrito.estaVacio():
			self.validarTarjetaParaLaCompra(tarjeta, unaFecha)
			monto = self.calcularMontoDeLaCompra(carrito)
			if isinstance(monto, int):
				monto = float(monto)
			monto = round( monto, 2)
			mpMessage = self._merchantProcesor.cobrarAUnaTarjeta(tarjeta,monto)
			venta = Sale(random(),self,monto)
			#self._salesBook.append(venta)
			return venta
		else:
			raise Exception( self.ERROR_COMPORTAMIENTO_NO_MODELADO )
	def calcularMontoDeLaCompra(self, carrito):
		monto = 0
		for producto in carrito.dameProductos():
			monto = monto + carrito.dameCatalogo()[producto] * \
			carrito.cantidadDeAparciones(producto)
		return monto

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
	def __init__(self,tarjetasRobadas, tarjetasSinSaldos):
		self._robadas = tarjetasRobadas
		self._sinSaldo = tarjetasSinSaldos
	def cobrarAUnaTarjeta(self, tarjeta, monto):
		numeroTarjeta = tarjeta.numero()
		if numeroTarjeta in self._robadas:
			raise Exception( self.ERROR_TARJETA_ROBADA )
		elif numeroTarjeta in self._sinSaldo:
			raise Exception( self.ERROR_TARJETA_SIN_CREDITO )

'''cara externa'''
class MPtoHTTP():
	def cobrarAUnaTarjeta(self, tarjeta, monto):
		toMPasHTTP(tarjeta.nombre, tar)

'''cara interna de rest'''
class SistemMisLibros:
	ERROR_USUARIO_INEXISTENTE = "El usuario no existe."
	ERROR_CLAVE_INVALIDA = 	"La clave no es correcta."
	ERROR_ID_INEXISTENTE = "La id no existe."
	ERROR_COMPORTAMIENTO_NO_MODELADO = "Se produjo una acción no contemplada."
	ERROR_TIMEOUT = "Tiempo de inactividad excedido."

	def __init__(self, Usuarios, unCatalogo, merchantProcesor,reloj):
		self._usuarios = Usuarios # diccionario usuario : contraseña
		self._comprasPorUsuario = {}
		for usuario in self._usuarios:
		 	self._comprasPorUsuario[usuario] = []
		self._carritos = {} # diccionario idCarrito : (usuarioAlQuePertenece,carrito, horaUltimaOperación)
		self._catalogo = unCatalogo
		self._cajero = Cajero(merchantProcesor)
		self._reloj = reloj
		self._salesBook = []
	def dameCuantasComprasHizoElUsuario(self,unUsuario): 
		if len(self._comprasPorUsuario[unUsuario]) == 0:
			return 0
		return len(self._comprasPorUsuario[unUsuario])
	def dameComprasDelUsuario(self,unUsuario):
		return self._comprasPorUsuario[unUsuario]
	def crearId(self):
		return random()
	def createCart(self, unUsuario, unaClave):
		self.validarUsuario(unUsuario, unaClave)
		IDNueva = self.crearId()
		horaOperacion = self._reloj.now()
		tuplaUsuarioCarrito = [unUsuario, Carrito(self._catalogo), horaOperacion]
		
		self._carritos[IDNueva] = tuplaUsuarioCarrito
		return IDNueva
	def validarUsuario(self, unUsuario, unaClave):
		if not( unUsuario in self._usuarios):
			raise Exception( self.ERROR_USUARIO_INEXISTENTE )
		else:
			if self._usuarios[unUsuario] != unaClave:
				raise Exception( self.ERROR_CLAVE_INVALIDA )
	def validarHoraDeLaUltimaOperacion(self, idCarrito):
		horaActual = self._reloj.now()
		if (horaActual - self._carritos[idCarrito][2]) > timedelta(minutes=30):
			raise Exception( self.ERROR_TIMEOUT )
		else:
			self._carritos[idCarrito][2] = horaActual
	def listCart(self, unId):
		if not(unId in self._carritos):
			raise Exception( self.ERROR_ID_INEXISTENTE )
		else:
			self.validarHoraDeLaUltimaOperacion(unId)
			return self._carritos[unId][1].dameProductos()
	def addToCart(self,unId,unElemento,unaCantidad):
		if not(unId in self._carritos):
			raise Exception(self.ERROR_ID_INEXISTENTE)
		elif unId in self._carritos:
			self.validarHoraDeLaUltimaOperacion(unId)
			self._carritos[unId][1].agregarElemento(unElemento,unaCantidad)
		else:
			raise Exception(self.ERROR_COMPORTAMIENTO_NO_MODELADO)
	def checkOutCart(self,idCarrito,nroTarjeta,fechaVencimientoTarjeta,nombreTarjeta):
		
		if not(idCarrito in self._carritos):
			raise Exception(self.ERROR_ID_INEXISTENTE)
		elif idCarrito in self._carritos:
			self.validarHoraDeLaUltimaOperacion(idCarrito)
			tarjeta = Tarjeta(fechaVencimientoTarjeta,nroTarjeta,nombreTarjeta)
			fecha = date.today()
			fechaNuestroModelo = FechaMMAA(fecha.month,fecha.year)
			carrito = self._carritos[idCarrito][1]
			transaccionID = self._cajero.checkOut(carrito,tarjeta,fechaNuestroModelo)
			''' Para este momento nosotros sabemos que la compra ya se realizo
			porque sino ya hubiera saltado la exepcion '''
			usuarioQueCompro = self._carritos[idCarrito][0]
			self._comprasPorUsuario[usuarioQueCompro].append(carrito.dameProductos()) 
			return transaccionID
	def listPurchases(self,unUsuario,unaClave):
		self.validarUsuario(unUsuario,unaClave)
		return self._comprasPorUsuario[unUsuario]
	
#class SistemMisLibrosSession:
#    def __init__(self, )





'''cara externa de rest'''
class HTTPtoSistem():
	''' Los que handlean las exepciones son las caras externas ya que pasan
	codigos de error hacia afuera'''


class Reloj():
		def __init__(self):
			self._fechaInicial = datetime.now()
			self._fechaConTiempoAgregado = datetime.now()
		def now(self):
			tiempoActual = datetime.now()
			tiempoAgregado = self._fechaConTiempoAgregado - self._fechaInicial
			return tiempoActual + tiempoAgregado
		def agregarTiempo(self):
			self._fechaConTiempoAgregado = self._fechaConTiempoAgregado + timedelta(minutes=32)



class testXX(unittest.TestCase):
	

	def testCuandoCreoElCarritoEsteEstaVacio(self):
		unCatalogo = []
		unCarrito = Carrito(unCatalogo)
		self.assertTrue( unCarrito.estaVacio() )
	def testAgregoUnLibroAUnCarritoVacioYSoloContieneAEsteLibro(self):
		unElemento = "unProducto"
		unCatalogo = [unElemento]
		unCarrito = Carrito(unCatalogo)
		unCarrito.agregarElemento(unElemento, 1)
		self.assertEquals( 1, unCarrito.cantidadElementos() )
		self.assertEquals( True, unCarrito.estaEnElCarrito(unElemento) )
	def testAgregoUnLibroQueNoPerteneceAlCatalogo(self):
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
	def testAgregarMuchoElementosFunciona(self):
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
	def testAgregoVariosDelMismoLibroYSuCantidadDeAparicionesEsCorrecta(self):
		unElemento = 1
		unCatalogo = [unElemento]
		unCarrito = Carrito(unCatalogo)
		unCarrito.agregarElemento(unElemento,1)
		unCarrito.agregarElemento(unElemento,5)
		unCarrito.agregarElemento(unElemento,1)
		unCarrito.agregarElemento(unElemento,3)
		self.assertEquals( 10, unCarrito.cantidadElementos() )
		self.assertEquals( 10, unCarrito.cantidadDeAparciones(unElemento) )
	def testNoPuedoAgregarCantidadNoPositivaDeProductos(self):
			unElemento = 1
			unCatalogo = [unElemento]
			unCarrito = Carrito(unCatalogo)
			try:
				unCarrito.agregarElemento(unElemento,-5)
				self.fail()
			except Exception as apariconesInvalidas:
				self.assertEquals( Carrito.ERROR_CANTIDAD_APARICIONES_NO_POSITIVO, apariconesInvalidas.message )
				self.assertEquals( 0, unCarrito.cantidadElementos())
	def testNoPuedoAgregarCantidadNoEnteraDeProductos(self):
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
	def testNoPodemosCobrarAUnCarritoVacio(self):
		unCatalogo = {}
		unCarrito = Carrito(unCatalogo)
		tarjetasRobadas = []
		tarjetaSinCredito = []
		mpSimulator = MPSimulator(tarjetasRobadas,tarjetaSinCredito)
		unCajero = Cajero(mpSimulator)
		vencimiento = FechaMMAA(8, 2017)
		unaFecha = FechaMMAA(10, 2017)
		nombre = "Juan Perez"
		tarjeta = Tarjeta(vencimiento,5400000000000001, nombre)

		try:
			unCajero.checkOut(unCarrito,tarjeta,unaFecha)
			self.fail()
		except Exception as carritoVacio:
			self.assertEquals( unCajero.ERROR_CARRITO_VACIO, carritoVacio.message )
	def testElMontoDeUnCarritoConUnProductoEsCorrecto(self):
		unCatalogo = {"Producto1": 10, 2: 2,"Producto3":4,5 :2}
		unCarrito = Carrito(unCatalogo)
		tarjetasRobadas = []
		tarjetaSinCredito = []
		mpSimulator = MPSimulator(tarjetasRobadas,tarjetaSinCredito)
		unCajero = Cajero(mpSimulator)

		unCarrito.agregarElemento("Producto1", 1)#count 10

		self.assertEquals( 10, unCajero.calcularMontoDeLaCompra(unCarrito) )
	'''testing.
	Nos dimos cuenta que este test no necesariamente debería ser
	testing si nosotros hubiésemos implementado el metodo calcularMontoDeLaCompra
	de una manera más sencilla como por ejemplo solo tomar un elemento. Lo tendremos
	en cuenta para los siguientes tests.'''
	''' De todos modos no le encontramos el sentido de "mal" un algoritmo que es
	sencillo solo para seguir el modelo de TDD. Cuál es el por qué de esto?'''
	def testElMontoDeUnCarritoConMuchosElementosYMuchasAparcionesEsCorrecto(self):
		unCatalogo = {"Producto1": 10, 2: 2,"Producto3":4,5 :2}
		unCarrito = Carrito(unCatalogo)
		tarjetasRobadas = []
		tarjetaSinCredito = []
		mpSimulator = MPSimulator(tarjetasRobadas,tarjetaSinCredito)
		unCajero = Cajero(mpSimulator)

		unCarrito.agregarElemento("Producto1", 5)#count 50
		unCarrito.agregarElemento(2,5)#count 60
		unCarrito.agregarElemento("Producto3", 10)#count 100

		self.assertEquals( 100, unCajero.calcularMontoDeLaCompra(unCarrito) )
	def testNoSePuedeCrearTarjetaInvalidaNombre(self):
		try:
			vencimiento = FechaMMAA(10, 2017)
			nombre = 123
			Tarjeta(vencimiento, 5400000000000001,nombre)
			self.fail()
		except Exception as tarjetaInvalida:
			self.assertEquals( "Los parámetros no son correctos." , tarjetaInvalida.message )
	def testNoSePuedeCrearTarjetaInvalidaNumero(self):
		try:
			vencimiento = FechaMMAA(10, 2017)
			nombre = "Juan Perez"
			Tarjeta(vencimiento, 5400,nombre)
			self.fail()
		except Exception as tarjetaInvalida:
			self.assertEquals( "Los parámetros no son correctos." , tarjetaInvalida.message )
	''' En este test el que se fija que la tarjeta este vencida es el cajero.
	Si la consulta del cajero falla entonces levanta una exepción y se corta la
	ejecución al esta no estar handleada.'''
	def testNoSePuedeComprarConUnaTarjetaVencida(self):
		unCatalogo = {"Producto1": 10, 2: 2,"Producto3":4,5 :2}
		unCarrito = Carrito(unCatalogo)
		tarjetasRobadas = []
		tarjetaSinCredito = []
		mpSimulator = MPSimulator(tarjetasRobadas,tarjetaSinCredito)
		unCajero = Cajero(mpSimulator)
		vencimiento = FechaMMAA(8, 2017)
		unaFecha = FechaMMAA(10, 2017)
		nombre = "Juan Perez"
		unaTarjeta = Tarjeta(vencimiento,5400000000000001,nombre)

		unCarrito.agregarElemento("Producto1",2)
		try:
			unCajero.checkOut(unCarrito, unaTarjeta, unaFecha)
			self.fail()
		except Exception as tarjetaVencida:
			self.assertEquals( unCajero.ERROR_TARJETA_VENCIDA,\
			tarjetaVencida.message )
			# self.assertEquals( len(unCajero.dameSalesBook()),0)

	'''-------------------------fin test cajero------------------------------'''

	def testNoSePuedeComprarConTarjetaRobada(self):
		unCatalogo = {"Producto1": 10, 2: 2,"Producto3":4,5 :2}
		unCarrito = Carrito(unCatalogo)
		tarjetasRobadas = [5400000000000001]
		tarjetaSinCredito = []
		mpSimulator = MPSimulator(tarjetasRobadas,tarjetaSinCredito)
		unCajero = Cajero(mpSimulator)
		vencimiento = FechaMMAA(8, 2017)
		unaFecha = FechaMMAA(10, 2016)
		nombre = "Juan Perez"
		unaTarjetaRobada = Tarjeta(vencimiento,5400000000000001,nombre)
		unCarrito.agregarElemento("Producto1",2)
		try:
			unCajero.checkOut(unCarrito, unaTarjetaRobada, unaFecha)
			self.fail()
		except Exception as tarjetaRobada:
			self.assertEquals( "Tarjeta Robada",\
			tarjetaRobada.message )
	def testNoSePuedeComprarConTarjetaSinCredito(self):
		unCatalogo = {"Producto1": 10, 2: 2,"Producto3":4,5 :2}
		unCarrito = Carrito(unCatalogo)
		tarjetasRobadas = []
		tarjetaSinCredito = [5400000000000002]
		mpSimulator = MPSimulator(tarjetasRobadas,tarjetaSinCredito)
		unCajero = Cajero(mpSimulator)
		vencimiento = FechaMMAA(8, 2017)
		unaFecha = FechaMMAA(10, 2016)
		nombre = "Juan Perez"
		unaTarjetaSinCredito = Tarjeta(vencimiento,5400000000000002,nombre)


		unCarrito.agregarElemento("Producto1",2)
		try:
			unCajero.checkOut(unCarrito,unaTarjetaSinCredito,unaFecha)
			self.fail()
		except Exception as tarjetaSinCredito:
			self.assertEquals( "Tarjeta Sin Credito",\
			tarjetaSinCredito.message )

	'''------------------fin test Merchant Processor ------------------------'''

	def testNoPuedoCrearUnCarritoAUnUsuarioInvalido(self):
		unId = "user1"
		unaClave = "user1"
		nuestrosUsuarios = {}
		unCatalogo = {"Producto1": 10, 2: 2,"Producto3":4,5 :2}
		tarjetasRobadas = []
		tarjetaSinCredito = []
		mpSimulator = MPSimulator(tarjetasRobadas,tarjetaSinCredito)
		reloj = Reloj()
		sistema = SistemMisLibros(nuestrosUsuarios,unCatalogo,mpSimulator,reloj)
		try:
			sistema.createCart(unId, unaClave)
			self.fail()
		except Exception as usuarioInexistente:
			self.assertEquals( usuarioInexistente.message, \
			sistema.ERROR_USUARIO_INEXISTENTE )
	def testLaClaveDelUsuarioNoEsCorrecta(self):
		unId = "user1"
		unaClave = "user1"
		nuestrosUsuarios = {"user1":"user2"}
		unCatalogo = {"Producto1": 10, 2: 2,"Producto3":4,5 :2}
		tarjetasRobadas = []
		tarjetaSinCredito = []
		mpSimulator = MPSimulator(tarjetasRobadas,tarjetaSinCredito)
		reloj = Reloj()
		sistema = SistemMisLibros(nuestrosUsuarios,unCatalogo,mpSimulator,reloj)
		try:
			sistema.createCart(unId, unaClave)
			self.fail()
		except Exception as claveInvalida:
			self.assertEquals( claveInvalida.message, \
			sistema.ERROR_CLAVE_INVALIDA )
	def testListCartDeUnCarritoInexistenteFalla(self):
		unId = "user1"
		unaClave = "user1"
		nuestrosUsuarios = {"user1":"user1"}
		unCatalogo = {"Producto1": 10, 2: 2,"Producto3":4,5 :2}
		tarjetasRobadas = []
		tarjetaSinCredito = []
		mpSimulator = MPSimulator(tarjetasRobadas,tarjetaSinCredito)
		reloj = Reloj()
		sistema = SistemMisLibros(nuestrosUsuarios,unCatalogo,mpSimulator,reloj)
		IdInvalida = 123
		try:
			sistema.listCart(IdInvalida)
			self.fail()
		except Exception as carritoInexistente:
			self.assertEquals( carritoInexistente.message, \
			sistema.ERROR_ID_INEXISTENTE )
	def testListCartDeUnNuevoCarritoValidoEsUnCarritoVacio(self):
		unId = "user1"
		unaClave = "user1"
		nuestrosUsuarios = {"user1":"user1"}
		unCatalogo = {"Producto1": 10, 2: 2,"Producto3":4,5 :2}
		tarjetasRobadas = []
		tarjetaSinCredito = []
		mpSimulator = MPSimulator(tarjetasRobadas,tarjetaSinCredito)
		reloj = Reloj()
		sistema = SistemMisLibros(nuestrosUsuarios,unCatalogo,mpSimulator,reloj)
		IdDeUnCarrito = sistema.createCart(unId, unaClave)

		self.assertEquals( sistema.listCart(IdDeUnCarrito), {} )
	def testNoSePuedeHacerListCartDeUnCarritoVencido(self):
		unId = "user1"
		unaClave = "user1"
		nuestrosUsuarios = {"user1":"user1"}
		unCatalogo = {"Producto1": 10, 2: 2,"Producto3":4,5 :2}
		tarjetasRobadas = []
		tarjetaSinCredito = []
		mpSimulator = MPSimulator(tarjetasRobadas,tarjetaSinCredito)
		reloj = Reloj()
		sistema = SistemMisLibros(nuestrosUsuarios,unCatalogo,mpSimulator,reloj)
		IdDeUnCarrito = sistema.createCart(unId, unaClave)
		unElemento = "Producto1"
		sistema.addToCart(IdDeUnCarrito,unElemento,1)
		reloj.agregarTiempo()

		try:
			sistema.listCart(IdDeUnCarrito)
			self.fail()
		except Exception as carritoVencido:
			self.assertEquals( carritoVencido.message, \
			sistema.ERROR_TIMEOUT )
	def testAgregarUnElementoAUnCarritoYElElementoSeAgrega(self):
		unId = "user1"
		unaClave = "user1"
		nuestrosUsuarios = {"user1":"user1"}
		unCatalogo = {"Producto1": 10, 2: 2,"Producto3":4,5 :2}
		tarjetasRobadas = []
		tarjetaSinCredito = []
		mpSimulator = MPSimulator(tarjetasRobadas,tarjetaSinCredito)
		reloj = Reloj()
		sistema = SistemMisLibros(nuestrosUsuarios,unCatalogo,mpSimulator,reloj)
		IdDeUnCarrito = sistema.createCart(unId, unaClave)
		unElemento = "Producto1"
		sistema.addToCart(IdDeUnCarrito,unElemento,1)
		compra = {unElemento:1}
		self.assertEquals(sistema.listCart(IdDeUnCarrito),compra )
	def testAddToCartDeUnCarritoInexistente(self):
		unId = "user1"
		unaClave = "user1"
		nuestrosUsuarios = {"user1":"user1"}
		unCatalogo = {"Producto1": 10, 2: 2,"Producto3":4,5 :2}
		tarjetasRobadas = []
		tarjetaSinCredito = []
		mpSimulator = MPSimulator(tarjetasRobadas,tarjetaSinCredito)
		reloj = Reloj()
		sistema = SistemMisLibros(nuestrosUsuarios,unCatalogo,mpSimulator,reloj)
		IdInvalida = 123
		unElemento = "Producto1"

		try:
			sistema.addToCart(IdInvalida,unElemento,1)
			self.fail()
		except Exception as carritoInexistente:
			self.assertEquals( carritoInexistente.message, \
			sistema.ERROR_ID_INEXISTENTE )
	def testNoSePuedeHacerAddToCartDeUnCarritoVencido(self):
		unId = "user1"
		unaClave = "user1"
		nuestrosUsuarios = {"user1":"user1"}
		unCatalogo = {"Producto1": 10, 2: 2,"Producto3":4,5 :2}
		tarjetasRobadas = []
		tarjetaSinCredito = []
		mpSimulator = MPSimulator(tarjetasRobadas,tarjetaSinCredito)
		reloj = Reloj()
		sistema = SistemMisLibros(nuestrosUsuarios,unCatalogo,mpSimulator,reloj)
		IdDeUnCarrito = sistema.createCart(unId, unaClave)
		unElemento = "Producto1"
		sistema.addToCart(IdDeUnCarrito,unElemento,1)
		reloj.agregarTiempo()

		try:
			sistema.addToCart(IdDeUnCarrito,unElemento,1)
			self.fail()
		except Exception as carritoVencido:
			self.assertEquals( carritoVencido.message, \
			sistema.ERROR_TIMEOUT )
	def testListPurchasesDeUnCienteInexistenteFalla(self):
		unId = "user2"
		unaClave = "user1"
		nuestrosUsuarios = {"user1":"user1"}
		unCatalogo = {"Producto1": 10, 2: 2,"Producto3":4,5 :2}
		tarjetasRobadas = []
		tarjetaSinCredito = []
		mpSimulator = MPSimulator(tarjetasRobadas,tarjetaSinCredito)
		reloj = Reloj()
		sistema = SistemMisLibros(nuestrosUsuarios,unCatalogo,mpSimulator,reloj)
		IdInvalida = 123
		unElemento = "Producto1"

		try:
			sistema.listPurchases(unId, unaClave)
			self.fail()
		except Exception as usuarioInexistente:
			self.assertEquals( usuarioInexistente.message, \
			sistema.ERROR_USUARIO_INEXISTENTE )
	def testListPurchasesDeUnaClaveErroneaFalla(self):
		unId = "user2"
		unaClave = "user2"
		nuestrosUsuarios = {"user2":"user1"}
		unCatalogo = {"Producto1": 10, 2: 2,"Producto3":4,5 :2}
		tarjetasRobadas = []
		tarjetaSinCredito = []
		mpSimulator = MPSimulator(tarjetasRobadas,tarjetaSinCredito)
		reloj = Reloj()
		sistema = SistemMisLibros(nuestrosUsuarios,unCatalogo,mpSimulator,reloj)
		IdInvalida = 123
		unElemento = "Producto1"

		try:
			sistema.listPurchases(unId, unaClave)
			self.fail()
		except Exception as claveErronea:
			self.assertEquals( claveErronea.message, \
			sistema.ERROR_CLAVE_INVALIDA )
	def testListPurchasesDeUnUsuarioQueNotieneComprasEstaVacia(self):
		unId = "user2"
		unaClave = "user1"
		nuestrosUsuarios = {"user2":"user1"}
		unCatalogo = {"Producto1": 10, 2: 2,"Producto3":4,5 :2}
		tarjetasRobadas = []
		tarjetaSinCredito = []
		mpSimulator = MPSimulator(tarjetasRobadas,tarjetaSinCredito)
		reloj = Reloj()
		sistema = SistemMisLibros(nuestrosUsuarios,unCatalogo,mpSimulator,reloj)
		IdDeUnCarrito = sistema.createCart(unId, unaClave)
		self.assertEquals( [], sistema.listPurchases(unId, unaClave) )


	def testListPurchasesDeUnUsuarioQueTieneUnaCompraEsCorrecto(self):
		
		unId = "user1"
		unaClave = "user1"
		nuestrosUsuarios = {"user1":"user1"}
		unCatalogo = {"Producto1": 10, 2: 2,"Producto3":4,5 :2}
		tarjetasRobadas = []
		tarjetaSinCredito = []
		mpSimulator = MPSimulator(tarjetasRobadas,tarjetaSinCredito)
		reloj = Reloj()
		sistema = SistemMisLibros(nuestrosUsuarios,unCatalogo,mpSimulator,reloj)
		IdDeUnCarrito = sistema.createCart(unId, unaClave)
		unElemento = "Producto1"
		sistema.addToCart(IdDeUnCarrito,unElemento,1)

		numeroTarjeta= 5400000000000002
		vencimiento = FechaMMAA(8, 2018)
		nombre = "Juan Perez"

		sistema.checkOutCart(IdDeUnCarrito,numeroTarjeta,vencimiento,nombre)
		venta = {unElemento:1}
		ventas = [venta]
		self.assertEquals( ventas, sistema.listPurchases(unId,unaClave) )

	def testListPurchasesDeUnUsuarioQueTieneMasDeUnaCompraEsCorrecto(self):
		unId = "user1"
		unaClave = "user1"
		nuestrosUsuarios = {"user1":"user1"}
		unCatalogo = {"Producto1": 10, "Producto2": 2,"Producto3":4,5 :2}
		tarjetasRobadas = []
		tarjetaSinCredito = []
		mpSimulator = MPSimulator(tarjetasRobadas,tarjetaSinCredito)
		reloj = Reloj()
		sistema = SistemMisLibros(nuestrosUsuarios,unCatalogo,mpSimulator,reloj)
		IdDeUnCarrito = sistema.createCart(unId, unaClave)
		unElemento = "Producto1"
		sistema.addToCart(IdDeUnCarrito,unElemento,1)

		numeroTarjeta= 5400000000000002
		vencimiento = FechaMMAA(8, 2018)
		nombre = "Juan Perez"

		sistema.checkOutCart(IdDeUnCarrito,numeroTarjeta,vencimiento,nombre)
		venta1 = {unElemento:1}
		IdOtroCarrito = sistema.createCart(unId, unaClave)
		otroElemento = "Producto2"
		sistema.addToCart(IdOtroCarrito,otroElemento,2)
		sistema.checkOutCart(IdOtroCarrito,numeroTarjeta,vencimiento,nombre)
		venta2 = {otroElemento:2}

		ventas = [venta1,venta2]


		self.assertEquals( ventas, sistema.listPurchases(unId,unaClave) )





	def testNoSePuedeHacerCheckOutDeUnCarritoQueNoExiste(self):
		unId = "user1"
		unaClave = "user1"
		nuestrosUsuarios = {"user1":"user1"}
		unCatalogo = {"Producto1": 10, 2: 2,"Producto3":4,5 :2}
		tarjetasRobadas = []
		tarjetaSinCredito = []
		mpSimulator = MPSimulator(tarjetasRobadas,tarjetaSinCredito)
		reloj = Reloj()
		sistema = SistemMisLibros(nuestrosUsuarios,unCatalogo,mpSimulator,reloj)
		IdDeUnCarrito = sistema.createCart(unId, unaClave)
		unElemento = "Producto1"
		sistema.addToCart(IdDeUnCarrito,unElemento,1)

		idInexitente = 123
		numeroTarjeta=5400000000000002
		vencimiento = FechaMMAA(8, 2017)
		nombre = "Juan Perez"

		ComprasDelUsuarioViejas = sistema.dameCuantasComprasHizoElUsuario(unId)
		try:
			sistema.checkOutCart(idInexitente,numeroTarjeta,vencimiento,nombre)
			self.fail()
		except Exception as carritoInexistente:
			self.assertEquals( carritoInexistente.message, \
			sistema.ERROR_ID_INEXISTENTE )
			ComprasDelUsuarioNuevas = sistema.dameCuantasComprasHizoElUsuario(unId)
			self.assertEquals(ComprasDelUsuarioNuevas,ComprasDelUsuarioViejas)
	def testHacerCheckOutAumentaLasComprasDelUsuario(self):
		unId = "user1"
		unaClave = "user1"
		nuestrosUsuarios = {"user1":"user1"}
		unCatalogo = {"Producto1": 10, 2: 2,"Producto3":4,5 :2}
		tarjetasRobadas = []
		tarjetaSinCredito = []
		mpSimulator = MPSimulator(tarjetasRobadas,tarjetaSinCredito)
		reloj = Reloj()
		sistema = SistemMisLibros(nuestrosUsuarios,unCatalogo,mpSimulator,reloj)
		IdDeUnCarrito = sistema.createCart(unId, unaClave)
		unElemento = "Producto1"
		sistema.addToCart(IdDeUnCarrito,unElemento,1)

		numeroTarjeta= 5400000000000002
		vencimiento = FechaMMAA(8, 2018)
		nombre = "Juan Perez"

		ComprasDelUsuarioViejas = sistema.dameCuantasComprasHizoElUsuario(unId)
		sistema.checkOutCart(IdDeUnCarrito,numeroTarjeta,vencimiento,nombre)
		ComprasDelUsuarioNuevas = sistema.dameCuantasComprasHizoElUsuario(unId)

		self.assertEquals(ComprasDelUsuarioNuevas, ComprasDelUsuarioViejas+1)
	def testNoSePuedeHacerCheckOutDeUnCarritoVencido(self):
		unId = "user1"
		unaClave = "user1"
		nuestrosUsuarios = {"user1":"user1"}
		unCatalogo = {"Producto1": 10, 2: 2,"Producto3":4,5 :2}
		tarjetasRobadas = []
		tarjetaSinCredito = []
		mpSimulator = MPSimulator(tarjetasRobadas,tarjetaSinCredito)
		reloj = Reloj()
		sistema = SistemMisLibros(nuestrosUsuarios,unCatalogo,mpSimulator,reloj)
		IdDeUnCarrito = sistema.createCart(unId, unaClave)
		unElemento = "Producto1"
		sistema.addToCart(IdDeUnCarrito,unElemento,1)

		numeroTarjeta= 5400000000000002
		vencimiento = FechaMMAA(8, 2018)
		nombre = "Juan Perez"
		reloj.agregarTiempo()
		ComprasDelUsuarioViejas = sistema.dameCuantasComprasHizoElUsuario(unId)
		try:
			sistema.checkOutCart(IdDeUnCarrito,numeroTarjeta,vencimiento,nombre)
			self.fail()
		except Exception as carritoVencido:
			self.assertEquals( carritoVencido.message, \
			sistema.ERROR_TIMEOUT )
			ComprasDelUsuarioNuevas = sistema.dameCuantasComprasHizoElUsuario(unId)
			self.assertEquals(ComprasDelUsuarioNuevas,ComprasDelUsuarioViejas)


if __name__ == "__main__":
	unittest.main()
