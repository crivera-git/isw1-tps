import unittest
from collections import defaultdict

class Carrito:
	ERROR_LIBRO_FUERA_DEL_CATALOGO = "El libro agregado no pertenece al catalogo"
	def __init__(self, unCatalogo):
		self._elementos = defaultdict(int)
		self._catalogo = unCatalogo

	def cantidadElementos(self):
		return sum(self._elementos.values())

	def agregarElemento(self, unElemento, cantidadDeAparicionesDeUnElemento):
		if unElemento in self._catalogo:
			self._elementos[unElemento] += cantidadDeAparicionesDeUnElemento
		else:
			raise Exception( self.ERROR_LIBRO_FUERA_DEL_CATALOGO )
	def estaEnElCarrito(self, unElemento):
		return unElemento in self._elementos
	def cantidadDeElementosComoEste(self, unElemento):
		return self._elementos[unElemento]

class Libro:
	def __init__(self):
		pass

class testXX(unittest.TestCase):
	def test01CuandoCreoElCarritoEsteEstaVacio(self):
		unCatalogo = []
		unCarrito = Carrito(unCatalogo)
		self.assertEquals( 0, unCarrito.cantidadElementos() )
	def test02AgregoUnLibroAUnCarritoVacioYSoloContieneAEsteLibro(self):
		unElemento = Libro()
		unCatalogo = [unElemento]
		unCarrito = Carrito(unCatalogo)
		unCarrito.agregarElemento(unElemento, 1)
		self.assertEquals( 1, unCarrito.cantidadElementos() )
		self.assertEquals( True, unCarrito.estaEnElCarrito(unElemento) )
	def test03AgregoUnLibroQueNoPerteneceAlCatalogo(self):
		unElemento = Libro()
		otroElemento = Libro()
		unCatalogo = [unElemento]
		unCarrito = Carrito(unCatalogo)
		try:
			unCarrito.agregarElemento(otroElemento,1)
			self.fail()
		except Exception as libroFueraCatalogo:
			self.assertEquals( Carrito.ERROR_LIBRO_FUERA_DEL_CATALOGO, libroFueraCatalogo.message )
			self.assertEquals( 0, unCarrito.cantidadElementos())
	'''Este test pasaba desde el comienzo, por eso lo comentamos '''
	def test04AgregarMuchoElementosFunciona(self):
		elemento1 = Libro()
		elemento2 = Libro()
		elemento3 = Libro()
		elemento4 = Libro()
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
		unElemento = Libro()
		unCatalogo = [unElemento]
		unCarrito = Carrito(unCatalogo)
		unCarrito.agregarElemento(unElemento,1)
		unCarrito.agregarElemento(unElemento,5)
		unCarrito.agregarElemento(unElemento,1)
		unCarrito.agregarElemento(unElemento,3)
		self.assertEquals( 10, unCarrito.cantidadElementos() )
		self.assertEquals( 10, unCarrito.cantidadDeElementosComoEste(unElemento) )










if __name__ == "__main__":
	unittest.main()
