# coding=utf-8
import unittest

class Carrito:
	ERROR_ELEMENTO_FUERA_DEL_CATALOGO = "El producto agregado no pertenece al catalogo"
	ERROR_CANTIDAD_APARICIONES_NO_POSITIVO = "La cantidad de apariciones es menor o igual a 0"
	ERROR_CANTIDAD_APARICIONES_NO_ENTERA = "Como cantidad de apariciones se obtuvo numero no entero"
	ERROR_PARAMENTRO_INVALIDO = "Uno o más parametros invalidos"
	def __init__(self, unCatalogo):
		self._elementos = []
		self._catalogo = unCatalogo
	def cantidadElementos(self):
		return len(self._elementos)
	def estaEnElCarrito(self, unElemento):
		return unElemento in self._elementos
	def cantidadDeElementosComoEste(self, unElemento):
		return self._elementos.count(unElemento)
	def estaVacio(self):
		return len(self._elementos) == 0
	def agregarElemento(self, unElemento, cantidadDeAparicionesDeUnElemento):
		if isinstance(cantidadDeAparicionesDeUnElemento, float):
			raise Exception(self.ERROR_CANTIDAD_APARICIONES_NO_ENTERA)
		elif cantidadDeAparicionesDeUnElemento <= 0:
			raise Exception(self.ERROR_CANTIDAD_APARICIONES_NO_POSITIVO)
		elif unElemento in self._catalogo:
			for i in range(cantidadDeAparicionesDeUnElemento):
				self._elementos.append(unElemento)
		elif not(unElemento in self._catalogo):
			raise Exception( self.ERROR_ELEMENTO_FUERA_DEL_CATALOGO )
		else:
			raise Exception( self.ERROR_PARAMENTRO_INVALIDO )

class Cajero:
	ERROR_CARRITO_VACIO = "El carrito provisto está vacio"
	def __init__(self,catalogo):
		self._catalogoConPrecios = catalogo
	def checkOut(self, carrito):
		if carrito.estaVacio():
			raise Exception( self.ERROR_CARRITO_VACIO )

class Tarjeta:
	def __init__(self):
		pass

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
	'''Este test pasaba desde el comienzo, por eso lo comentamos '''
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
		self.assertEquals( 10, unCarrito.cantidadDeElementosComoEste(unElemento) )
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
		try:
			unCajero.checkOut(unCarrito)
			self.fail()
		except Exception as carritoVacio:
			self.assertEquals( unCajero.ERROR_CARRITO_VACIO, carritoVacio.message )
	def test09ElCatalogoDeElCajeroTieneTodosLosProductosQueTieneElCatalogoDelCarrito(self):
		unCatalogo = ["Producto1","Producto2","Producto3"]
		unCarrito = Carrito(unCatalogo)
		unCatalogoConPrecios = {"Producto1": 1.3,"Producto2": 2,"Producto3":4}
		unCajero = Cajero(unCatalogoConPrecios)







if __name__ == "__main__":
	unittest.main()
