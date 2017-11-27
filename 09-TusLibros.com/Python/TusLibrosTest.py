# coding=utf-8
import unittest

from TusLibrosRest import *

class testXX(unittest.TestCase):

	def testCuandoCreoElCarritoEsteEstaVacio(self):
		unCatalogo = []
		unCarrito = Carrito(unCatalogo)
		self.assertTrue(unCarrito.estaVacio())
	def testCarritoNoEstaVacioCuandoSeLeAgregaProducto(self):
		unElemento = "unProducto"
		unCatalogo = [unElemento]
		unCarrito = Carrito(unCatalogo)
		unCarrito.agregarElemento(unElemento, 1)
		self.assertFalse(unCarrito.estaVacio())

	def testAgregoUnLibroAUnCarritoVacioYSoloContieneAEsteLibro(self):
		unElemento = "unProducto"
		unCatalogo = [unElemento]
		unCarrito = Carrito(unCatalogo)
		unCarrito.agregarElemento(unElemento, 1)
		self.assertEquals(1, unCarrito.cantidadElementos())
		self.assertEquals(True, unCarrito.estaEnElCarrito(unElemento))

	def testAgregoUnLibroQueNoPerteneceAlCatalogo(self):
		unElemento = 1
		otroElemento = 2
		unCatalogo = [unElemento]
		unCarrito = Carrito(unCatalogo)
		try:
			unCarrito.agregarElemento(otroElemento, 1)
			self.fail()
		except Exception as libroFueraCatalogo:
			self.assertEquals(Carrito.ERROR_ELEMENTO_FUERA_DEL_CATALOGO,
			                  libroFueraCatalogo.message)
			self.assertEquals(0, unCarrito.cantidadElementos())
	''' testing'''

	def testAgregarMuchoElementosFunciona(self):
		elemento1 = 1
		elemento2 = 12
		elemento3 = 13
		elemento4 = 14
		unCatalogo = [elemento1, elemento2, elemento3, elemento4]
		unCarrito = Carrito(unCatalogo)

		unCarrito.agregarElemento(elemento1, 1)
		unCarrito.agregarElemento(elemento2, 1)
		unCarrito.agregarElemento(elemento3, 1)
		unCarrito.agregarElemento(elemento4, 1)

		self.assertEquals(4, unCarrito.cantidadElementos())
		self.assertEquals(True, unCarrito.estaEnElCarrito(elemento1))
		self.assertEquals(True, unCarrito.estaEnElCarrito(elemento2))
		self.assertEquals(True, unCarrito.estaEnElCarrito(elemento3))
		self.assertEquals(True, unCarrito.estaEnElCarrito(elemento4))

	def testAgregoVariosDelMismoLibroYSuCantidadDeAparicionesEsCorrecta(self):
		unElemento = 1
		unCatalogo = [unElemento]
		unCarrito = Carrito(unCatalogo)
		unCarrito.agregarElemento(unElemento, 1)
		unCarrito.agregarElemento(unElemento, 5)
		unCarrito.agregarElemento(unElemento, 1)
		unCarrito.agregarElemento(unElemento, 3)
		self.assertEquals(10, unCarrito.cantidadElementos())
		self.assertEquals(10, unCarrito.cantidadDeAparciones(unElemento))

	def testNoPuedoAgregarCantidadNoPositivaDeProductos(self):
			unElemento = 1
			unCatalogo = [unElemento]
			unCarrito = Carrito(unCatalogo)
			try:
				unCarrito.agregarElemento(unElemento, -5)
				self.fail()
			except Exception as apariconesInvalidas:
				self.assertEquals(
					Carrito.ERROR_CANTIDAD_APARICIONES_NO_POSITIVO, apariconesInvalidas.message)
				self.assertEquals(0, unCarrito.cantidadElementos())

	def testNoPuedoAgregarCantidadNoEnteraDeProductos(self):
		unElemento = 1
		unCatalogo = [unElemento]
		unCarrito = Carrito(unCatalogo)
		try:
			unCarrito.agregarElemento(unElemento, 1.5)
			self.fail()
		except Exception as apariconesInvalidas:
			self.assertEquals(
				Carrito.ERROR_CANTIDAD_APARICIONES_NO_ENTERA, apariconesInvalidas.message)
			self.assertEquals(0, unCarrito.cantidadElementos())
	'''----------------------------Fin test carrito--------------------------'''

	# def testNoPodemosCrearUnCajeroConCarritoVacio(self):
	# 	unCatalogo = {}
	# 	unCarrito = Carrito(unCatalogo)
	# 	tarjetasRobadas = []
	# 	tarjetaSinCredito = []
	# 	mpSimulator = MPSimulator(tarjetasRobadas, tarjetaSinCredito)
	# 	mpSimulator = MPSimulator(tarjetasRobadas, tarjetaSinCredito)
	# 	vencimiento = FechaMMAA(8, 2017)
	# 	unaFecha = FechaMMAA(10, 2017)
	# 	nombre = "Juan Perez"
	# 	tarjeta = Tarjeta(vencimiento, 5400000000000001, nombre)
	# 	idUsuario = "1234"
	# 	try:
	# 		# unCajero.checkOut(unCarrito, tarjeta, unaFecha)
	# 		unCajero = Cajero(idUsuario, mpSimulator, unCarrito, tarjeta, unaFecha)
	# 		self.fail()
	# 	except Exception as carritoVacio:
	# 		self.assertEquals(unCajero.ERROR_CARRITO_VACIO, carritoVacio.message)

	def testElMontoDeUnCarritoConUnProductoEsCorrecto(self):
		unCatalogo = {"Producto1": 10, 2: 2, "Producto3": 4, 5: 2}
		unCarrito = Carrito(unCatalogo)
		tarjetasRobadas = []
		tarjetaSinCredito = []
		mpSimulator = MPSimulator(tarjetasRobadas, tarjetaSinCredito)
		vencimiento = FechaMMAA(8, 2017)
		unaFecha = FechaMMAA(7, 2017)
		nombre = "Juan Perez"
		tarjeta = Tarjeta(vencimiento, 5400000000000001, nombre)
		idUsuario = "1234"
		unCarrito.agregarElemento("Producto1", 1)  # count 10
		unCajero = Cajero(idUsuario, mpSimulator, unCarrito, tarjeta, unaFecha)


		self.assertEquals(10, unCajero.calcularMontoDeLaCompra(unCarrito))
	'''testing.
	Nos dimos cuenta que este test no necesariamente debería ser
	testing si nosotros hubiésemos implementado el metodo calcularMontoDeLaCompra
	de una manera más sencilla como por ejemplo solo tomar un elemento. Lo tendremos
	en cuenta para los siguientes tests.'''
	''' De todos modos no le encontramos el sentido de "mal" un algoritmo que es
	sencillo solo para seguir el modelo de TDD. Cuál es el por qué de esto?'''

	def testElMontoDeUnCarritoConMuchosElementosYMuchasAparcionesEsCorrecto(self):
		unId = "user1"
		unaClave = "user1"
		nuestrosUsuarios = {}
		unCatalogo = {"Producto1": 10, 2: 2, "Producto3": 4, 5: 2}
		unCarrito = Carrito(unCatalogo)
		tarjetasRobadas = []
		tarjetaSinCredito = []
		mpSimulator = MPSimulator(tarjetasRobadas, tarjetaSinCredito)
		vencimiento = FechaMMAA(12, 2017)
		unaFecha = FechaMMAA(10, 2017)
		nombre = "Juan Perez"
		tarjeta = Tarjeta(vencimiento, 5400000000000001, nombre)
		unCarrito.agregarElemento("Producto1", 5)  # count 50
		unCarrito.agregarElemento(2, 5)  # count 60
		unCarrito.agregarElemento("Producto3", 10)  # count 100
		unCajero = Cajero(unId, mpSimulator, unCarrito, tarjeta, unaFecha)

		

		self.assertEquals(100, unCajero.calcularMontoDeLaCompra(unCarrito))

	def testNoSePuedeCrearTarjetaInvalidaNombre(self):
		try:
			vencimiento = FechaMMAA(10, 2017)
			nombre = 123
			Tarjeta(vencimiento, 5400000000000001, nombre)
			self.fail()
		except Exception as tarjetaInvalida:
			self.assertEquals("Los parámetros no son correctos.",tarjetaInvalida.message)

	def testNoSePuedeCrearTarjetaInvalidaNumero(self):
		try:
			vencimiento = FechaMMAA(10, 2017)
			nombre = "Juan Perez"
			Tarjeta(vencimiento, 5400, nombre)
			self.fail()
		except Exception as tarjetaInvalida:
			self.assertEquals("Los parámetros no son correctos.",
			                  tarjetaInvalida.message)
	''' En este test el que se fija que la tarjeta este vencida es el cajero.
	Si la consulta del cajero falla entonces levanta una exepción y se corta la
	ejecución al esta no estar handleada.'''

	# def testNoSePuedeComprarConUnaTarjetaVencida(self):
	# 	unCatalogo = {"Producto1": 10, 2: 2, "Producto3": 4, 5: 2}
	# 	unCarrito = Carrito(unCatalogo)
	# 	tarjetasRobadas = []
	# 	tarjetaSinCredito = []
	# 	mpSimulator = MPSimulator(tarjetasRobadas, tarjetaSinCredito)
	# 	vencimiento = FechaMMAA(8, 2017)
	# 	unaFecha = FechaMMAA(10, 2017)
	# 	nombre = "Juan Perez"
	# 	idUsuario = "1234"
	# 	tarjeta = Tarjeta(vencimiento, 5400000000000001, nombre)
	# 	unCarrito.agregarElemento("Producto1", 2)

	# 	try:
	# 		#unCajero.checkOut(unCarrito, unaTarjeta, unaFecha)
	# 		unCajero = Cajero(idUsuario, mpSimulator, unCarrito, tarjeta, unaFecha)
	# 		self.fail()
	# 	except Exception as tarjetaVencida:
	# 		self.assertEquals(unCajero.ERROR_TARJETA_VENCIDA, tarjetaVencida.message)
	# 		# self.assertEquals( len(unCajero.dameSalesBook()),0)

	'''-------------------------fin test cajero------------------------------'''

	def testNoSePuedeComprarConTarjetaRobada(self):
		unCatalogo = {"Producto1": 10, 2: 2, "Producto3": 4, 5: 2}
		unCarrito = Carrito(unCatalogo)
		tarjetasRobadas = [5400000000000001]
		tarjetaSinCredito = []
		mpSimulator = MPSimulator(tarjetasRobadas, tarjetaSinCredito)
		vencimiento = FechaMMAA(8, 2017)
		unaFecha = FechaMMAA(10, 2016)
		nombre = "Juan Perez"
		unaTarjetaRobada = Tarjeta(vencimiento, 5400000000000001, nombre)
		idUsuario = "1234"
		unCarrito.agregarElemento("Producto1", 2)
		unCajero = Cajero(idUsuario, mpSimulator, unCarrito, unaTarjetaRobada, unaFecha)
		try:
			unCajero.checkOut()
			self.fail()
		except Exception as tarjetaRobada:
			self.assertEquals("Tarjeta Robada",
                            tarjetaRobada.message)

	def testNoSePuedeComprarConTarjetaSinCredito(self):
		unCatalogo = {"Producto1": 10, 2: 2, "Producto3": 4, 5: 2}
		unCarrito = Carrito(unCatalogo)
		tarjetasRobadas = []
		tarjetaSinCredito = [5400000000000002]
		mpSimulator = MPSimulator(tarjetasRobadas, tarjetaSinCredito)
		vencimiento = FechaMMAA(8, 2017)
		unaFecha = FechaMMAA(10, 2016)
		nombre = "Juan Perez"
		unaTarjetaSinCredito = Tarjeta(vencimiento, 5400000000000002, nombre)
		idUsuario = "1234"
		unCarrito.agregarElemento("Producto1", 2)
		unCajero = Cajero(idUsuario, mpSimulator, unCarrito, unaTarjetaSinCredito, unaFecha)

		try:
			unCajero.checkOut()
			self.fail()
		except Exception as tarjetaSinCredito:
			self.assertEquals("Tarjeta Sin Credito",tarjetaSinCredito.message)

	'''------------------fin test Merchant Processor ------------------------'''

	def testNoPuedoCrearUnCarritoAUnUsuarioInvalido(self):
		unId = "user1"
		unaClave = "user1"
		nuestrosUsuarios = {}
		unCatalogo = {"Producto1": 10, 2: 2, "Producto3": 4, 5: 2}
		tarjetasRobadas = []
		tarjetaSinCredito = []
		mpSimulator = MPSimulator(tarjetasRobadas, tarjetaSinCredito)
		reloj = Reloj()
		sistema = SistemMisLibros(nuestrosUsuarios, unCatalogo, mpSimulator, reloj)
		try:
			sistema.createCart(unId, unaClave)
			self.fail()
		except Exception as usuarioInexistente:
			self.assertEquals(usuarioInexistente.message,
                            sistema.ERROR_USUARIO_INEXISTENTE)

	def testLaClaveDelUsuarioNoEsCorrecta(self):
		unId = "user1"
		unaClave = "user1"
		nuestrosUsuarios = {"user1": "user2"}
		unCatalogo = {"Producto1": 10, 2: 2, "Producto3": 4, 5: 2}
		tarjetasRobadas = []
		tarjetaSinCredito = []
		mpSimulator = MPSimulator(tarjetasRobadas, tarjetaSinCredito)
		reloj = Reloj()
		sistema = SistemMisLibros(nuestrosUsuarios, unCatalogo, mpSimulator, reloj)
		try:
			sistema.createCart(unId, unaClave)
			self.fail()
		except Exception as claveInvalida:
			self.assertEquals(claveInvalida.message,
                            sistema.ERROR_CLAVE_INVALIDA)

	def testListCartDeUnCarritoInexistenteFalla(self):
		unId = "user1"
		unaClave = "user1"
		nuestrosUsuarios = {"user1": "user1"}
		unCatalogo = {"Producto1": 10, 2: 2, "Producto3": 4, 5: 2}
		tarjetasRobadas = []
		tarjetaSinCredito = []
		mpSimulator = MPSimulator(tarjetasRobadas, tarjetaSinCredito)
		reloj = Reloj()
		sistema = SistemMisLibros(nuestrosUsuarios, unCatalogo, mpSimulator, reloj)
		IdInvalida = 123
		try:
			sistema.listCart(IdInvalida)
			self.fail()
		except Exception as carritoInexistente:
			self.assertEquals(carritoInexistente.message,
                            sistema.ERROR_ID_INEXISTENTE)

	def testListCartDeUnNuevoCarritoValidoEsUnCarritoVacio(self):
		unId = "user1"
		unaClave = "user1"
		nuestrosUsuarios = {"user1": "user1"}
		unCatalogo = {"Producto1": 10, 2: 2, "Producto3": 4, 5: 2}
		tarjetasRobadas = []
		tarjetaSinCredito = []
		mpSimulator = MPSimulator(tarjetasRobadas, tarjetaSinCredito)
		reloj = Reloj()
		sistema = SistemMisLibros(nuestrosUsuarios, unCatalogo, mpSimulator, reloj)
		IdDeUnCarrito = sistema.createCart(unId, unaClave)

		self.assertEquals(sistema.listCart(IdDeUnCarrito), {})

	def testNoSePuedeHacerListCartDeUnCarritoVencido(self):
		unId = "user1"
		unaClave = "user1"
		nuestrosUsuarios = {"user1": "user1"}
		unCatalogo = {"Producto1": 10, 2: 2, "Producto3": 4, 5: 2}
		tarjetasRobadas = []
		tarjetaSinCredito = []
		mpSimulator = MPSimulator(tarjetasRobadas, tarjetaSinCredito)
		reloj = Reloj()
		sistema = SistemMisLibros(nuestrosUsuarios, unCatalogo, mpSimulator, reloj)
		unaSession = sistema.createCart(unId, unaClave)
		unElemento = "Producto1"
		sistema.addToCart(unaSession, unElemento, 1)
		reloj.agregarTiempo()
		numeroTarjeta = 5400000000000002
		vencimiento = FechaMMAA(8, 2018)
		nombre = "Juan Perez"
		try:
			sistema.checkOutCart(unaSession, unId, numeroTarjeta, vencimiento, nombre)
			self.fail()
		except Exception as carritoVencido:
			self.assertEquals(carritoVencido.message, sistema.ERROR_TIMEOUT)

	def testAgregarUnElementoAUnCarritoYElElementoSeAgrega(self):
		unId = "user1"
		unaClave = "user1"
		nuestrosUsuarios = {"user1": "user1"}
		unCatalogo = {"Producto1": 10, 2: 2, "Producto3": 4, 5: 2}
		tarjetasRobadas = []
		tarjetaSinCredito = []
		mpSimulator = MPSimulator(tarjetasRobadas, tarjetaSinCredito)
		reloj = Reloj()
		sistema = SistemMisLibros(nuestrosUsuarios, unCatalogo, mpSimulator, reloj)
		IdDeNuevoCarrito = sistema.createCart(unId, unaClave)
		unElemento = "Producto1"
		sistema.addToCart(IdDeNuevoCarrito, unElemento, 1)
		compra = {unElemento: 1}
		self.assertEquals(sistema.listCart(IdDeNuevoCarrito), compra)
	def testAgregarMasDeUnElementoAlCarritoYLosElementosSeAgregan(self):
		unId = "user1"
		unaClave = "user1"
		nuestrosUsuarios = {"user1": "user1"}
		unCatalogo = {"Producto1": 10, 2: 2, "Producto3": 4, 5: 2}
		tarjetasRobadas = []
		tarjetaSinCredito = []
		mpSimulator = MPSimulator(tarjetasRobadas, tarjetaSinCredito)
		reloj = Reloj()
		sistema = SistemMisLibros(nuestrosUsuarios, unCatalogo, mpSimulator, reloj)
		IdDeNuevoCarrito = sistema.createCart(unId, unaClave)
		unElemento = "Producto1"
		otroElemento = "Producto3"
		sistema.addToCart(IdDeNuevoCarrito, unElemento, 1)
		sistema.addToCart(IdDeNuevoCarrito, otroElemento, 2)
		compra = {unElemento: 1,otroElemento: 2}
		self.assertEquals(sistema.listCart(IdDeNuevoCarrito), compra)


	def testAddToCartDeUnCarritoInexistente(self):
		unId = "user1"
		unaClave = "user1"
		nuestrosUsuarios = {"user1": "user1"}
		unCatalogo = {"Producto1": 10, 2: 2, "Producto3": 4, 5: 2}
		tarjetasRobadas = []
		tarjetaSinCredito = []
		mpSimulator = MPSimulator(tarjetasRobadas, tarjetaSinCredito)
		reloj = Reloj()
		sistema = SistemMisLibros(nuestrosUsuarios, unCatalogo, mpSimulator, reloj)
		IdInvalida = 123
		unElemento = "Producto1"

		try:
			sistema.addToCart(IdInvalida, unElemento, 1)
			self.fail()
		except Exception as carritoInexistente:
			self.assertEquals(carritoInexistente.message,
                            sistema.ERROR_ID_INEXISTENTE)

	def testNoSePuedeHacerAddToCartDeUnCarritoVencido(self):
		unId = "user1"
		unaClave = "user1"
		nuestrosUsuarios = {"user1": "user1"}
		unCatalogo = {"Producto1": 10, 2: 2, "Producto3": 4, 5: 2}
		tarjetasRobadas = []
		tarjetaSinCredito = []
		mpSimulator = MPSimulator(tarjetasRobadas, tarjetaSinCredito)
		reloj = Reloj()
		sistema = SistemMisLibros(nuestrosUsuarios, unCatalogo, mpSimulator, reloj)
		IdDeUnCarrito = sistema.createCart(unId, unaClave)
		unElemento = "Producto1"
		sistema.addToCart(IdDeUnCarrito, unElemento, 1)
		reloj.agregarTiempo()

		try:
			sistema.addToCart(IdDeUnCarrito, unElemento, 1)
			self.fail()
		except Exception as carritoVencido:
			self.assertEquals(carritoVencido.message,
                            sistema.ERROR_TIMEOUT)

	def testListPurchasesDeUnCienteInexistenteFalla(self):
		unId = "user2"
		unaClave = "user1"
		nuestrosUsuarios = {"user1": "user1"}
		unCatalogo = {"Producto1": 10, 2: 2, "Producto3": 4, 5: 2}
		tarjetasRobadas = []
		tarjetaSinCredito = []
		mpSimulator = MPSimulator(tarjetasRobadas, tarjetaSinCredito)
		reloj = Reloj()
		sistema = SistemMisLibros(nuestrosUsuarios, unCatalogo, mpSimulator, reloj)
		IdInvalida = 123
		unElemento = "Producto1"

		try:
			sistema.listPurchases(unId, unaClave)
			self.fail()
		except Exception as usuarioInexistente:
			self.assertEquals(usuarioInexistente.message,
                            sistema.ERROR_USUARIO_INEXISTENTE)

	def testListPurchasesDeUnaClaveErroneaFalla(self):
		unId = "user2"
		unaClave = "user2"
		nuestrosUsuarios = {"user2": "user1"}
		unCatalogo = {"Producto1": 10, 2: 2, "Producto3": 4, 5: 2}
		tarjetasRobadas = []
		tarjetaSinCredito = []
		mpSimulator = MPSimulator(tarjetasRobadas, tarjetaSinCredito)
		reloj = Reloj()
		sistema = SistemMisLibros(nuestrosUsuarios, unCatalogo, mpSimulator, reloj)
		IdInvalida = 123
		unElemento = "Producto1"

		try:
			sistema.listPurchases(unId, unaClave)
			self.fail()
		except Exception as claveErronea:
			self.assertEquals(claveErronea.message,
                            sistema.ERROR_CLAVE_INVALIDA)

	def testListPurchasesDeUnUsuarioQueNotieneComprasEstaVacia(self):
		unId = "user2"
		unaClave = "user1"
		nuestrosUsuarios = {"user2": "user1"}
		unCatalogo = {"Producto1": 10, 2: 2, "Producto3": 4, 5: 2}
		tarjetasRobadas = []
		tarjetaSinCredito = []
		mpSimulator = MPSimulator(tarjetasRobadas, tarjetaSinCredito)
		reloj = Reloj()
		sistema = SistemMisLibros(nuestrosUsuarios, unCatalogo, mpSimulator, reloj)
		IdDeUnCarrito = sistema.createCart(unId, unaClave)
		self.assertEquals(0, sistema.listPurchases(unId, unaClave).getTotalVentasCantidad())
		self.assertEquals(0, sistema.listPurchases(unId, unaClave).calcularMontoTotal())


	def testListPurchasesDeUnUsuarioQueTieneUnaCompraEsCorrecto(self):

		unId = "user1"
		unaClave = "user1"
		nuestrosUsuarios = {"user1": "user1"}
		unCatalogo = {"Producto1": 10, 2: 2, "Producto3": 4, 5: 2}
		tarjetasRobadas = []
		tarjetaSinCredito = []
		mpSimulator = MPSimulator(tarjetasRobadas, tarjetaSinCredito)
		reloj = Reloj()
		sistema = SistemMisLibros(nuestrosUsuarios, unCatalogo, mpSimulator, reloj)
		unaSession = sistema.createCart(unId, unaClave)
		unElemento = "Producto1"
		sistema.addToCart(unaSession, unElemento, 1)

		numeroTarjeta = 5400000000000002
		vencimiento = FechaMMAA(8, 2018)
		nombre = "Juan Perez"

		sistema.checkOutCart(unaSession,unId, numeroTarjeta, vencimiento, nombre)
		self.assertEquals(1, sistema.listPurchases(unId, unaClave).getTotalVentasCantidad())
		self.assertEquals(1, sistema.listPurchases(unId, unaClave).getVentasDeProducto(unElemento))

	def testListPurchasesDeUnUsuarioQueTieneMasDeUnaCompraEsCorrecto(self):
		unId = "user1"
		unaClave = "user1"
		nuestrosUsuarios = {"user1": "user1"}
		unCatalogo = {"Producto1": 10, "Producto2": 2, "Producto3": 4, 5: 2}
		tarjetasRobadas = []
		tarjetaSinCredito = []
		mpSimulator = MPSimulator(tarjetasRobadas, tarjetaSinCredito)
		reloj = Reloj()
		sistema = SistemMisLibros(nuestrosUsuarios, unCatalogo, mpSimulator, reloj)
		unaSession = sistema.createCart(unId, unaClave)
		unElemento = "Producto1"
		sistema.addToCart(unaSession, unElemento, 1)

		numeroTarjeta = 5400000000000002
		vencimiento = FechaMMAA(8, 2018)
		nombre = "Juan Perez"

		sistema.checkOutCart(unaSession,unId, numeroTarjeta, vencimiento, nombre)
		
		otraSession = sistema.createCart(unId, unaClave)
		otroElemento = "Producto2"
		sistema.addToCart(otraSession, otroElemento, 2)
		sistema.checkOutCart(otraSession,unId, numeroTarjeta, vencimiento, nombre)
		
		self.assertEquals(3, sistema.listPurchases(unId, unaClave).getTotalVentasCantidad())

	def testNoSePuedeHacerCheckOutDeUnCarritoQueNoExiste(self):
		unId = "user1"
		unaClave = "user1"
		nuestrosUsuarios = {"user1": "user1"}
		unCatalogo = {"Producto1": 10, 2: 2, "Producto3": 4, 5: 2}
		tarjetasRobadas = []
		tarjetaSinCredito = []
		mpSimulator = MPSimulator(tarjetasRobadas, tarjetaSinCredito)
		reloj = Reloj()
		sistema = SistemMisLibros(nuestrosUsuarios, unCatalogo, mpSimulator, reloj)
		IdDeUnCarrito = sistema.createCart(unId, unaClave)
		unElemento = "Producto1"
		sistema.addToCart(IdDeUnCarrito, unElemento, 1)

		idInexitente = 123
		numeroTarjeta = 5400000000000002
		vencimiento = FechaMMAA(8, 2017)
		nombre = "Juan Perez"

		ComprasDelUsuarioViejas = sistema.listPurchases(unId,unaClave).getTotalVentasCantidad()
		try:
			sistema.checkOutCart(idInexitente,unId, numeroTarjeta, vencimiento, nombre)
			self.fail()
		except Exception as carritoInexistente:
			self.assertEquals(carritoInexistente.message, sistema.ERROR_ID_INEXISTENTE)
			ComprasDelUsuarioNuevas = sistema.listPurchases(unId,unaClave).getTotalVentasCantidad()
			self.assertEquals(ComprasDelUsuarioNuevas, ComprasDelUsuarioViejas)

	def testHacerCheckOutAumentaLasComprasDelUsuario(self):
		unId = "user1"
		unaClave = "user1"
		nuestrosUsuarios = {"user1": "user1"}
		unCatalogo = {"Producto1": 10, 2: 2, "Producto3": 4, 5: 2}
		tarjetasRobadas = []
		tarjetaSinCredito = []
		mpSimulator = MPSimulator(tarjetasRobadas, tarjetaSinCredito)
		reloj = Reloj()
		sistema = SistemMisLibros(nuestrosUsuarios, unCatalogo, mpSimulator, reloj)
		idSession = sistema.createCart(unId, unaClave)
		unElemento = "Producto1"
		sistema.addToCart(idSession, unElemento, 1)

		numeroTarjeta = 5400000000000002
		vencimiento = FechaMMAA(8, 2018)
		nombre = "Juan Perez"

		ComprasDelUsuarioViejas = sistema.listPurchases(unId,unaClave).getTotalVentasCantidad()
		sistema.checkOutCart(idSession,unId, numeroTarjeta, vencimiento, nombre)
		ComprasDelUsuarioNuevas = sistema.listPurchases(unId,unaClave).getTotalVentasCantidad()

		self.assertEquals(ComprasDelUsuarioNuevas, ComprasDelUsuarioViejas + 1)

	def testNoSePuedeHacerCheckOutDeUnCarritoVencido(self):
		unId = "user1"
		unaClave = "user1"
		nuestrosUsuarios = {"user1": "user1"}
		unCatalogo = {"Producto1": 10, 2: 2, "Producto3": 4, 5: 2}
		tarjetasRobadas = []
		tarjetaSinCredito = []
		mpSimulator = MPSimulator(tarjetasRobadas, tarjetaSinCredito)
		reloj = Reloj()
		sistema = SistemMisLibros(nuestrosUsuarios, unCatalogo, mpSimulator, reloj)
		unaSession = sistema.createCart(unId, unaClave)
		unElemento = "Producto1"
		sistema.addToCart(unaSession, unElemento, 1)

		numeroTarjeta = 5400000000000002
		vencimiento = FechaMMAA(8, 2018)
		nombre = "Juan Perez"
		reloj.agregarTiempo()
		ComprasDelUsuarioViejas = sistema.listPurchases(unId,unaClave).getTotalVentasCantidad()
		try:
			sistema.checkOutCart(unaSession,unId, numeroTarjeta, vencimiento, nombre)
			self.fail()
		except Exception as carritoVencido:
			self.assertEquals(carritoVencido.message, sistema.ERROR_TIMEOUT)
			ComprasDelUsuarioNuevas = sistema.listPurchases(unId,unaClave).getTotalVentasCantidad()
			self.assertEquals(ComprasDelUsuarioNuevas, ComprasDelUsuarioViejas)


if __name__ == "__main__":
	unittest.main()
