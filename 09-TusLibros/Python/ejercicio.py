import unittest

class Carrito:
	ERROR_LIBRO_FUERA_DEL_CATALOGO = "El libro agregado no pertenece al catalogo"
	def __init__(self, unCatalogo):
		self._elementos = {}
		self._catalogo = unCatalogo
	def cantidadElementos(self):
		return len(self._elementos)
	def agregarElemento(self, unElemento, cantidadDeUnElemento):
		if unElemento in self._catalogo:
			self._elementos[unElemento] += cantidadDeUnElemento
		else:
			raise Exception( self.ERROR_LIBRO_FUERA_DEL_CATALOGO )
	def estaEnElCarrito(self, unElemento):
		return unElemento in self._elementos
	def cantidadDeElementosComoEste(self, unElemento):
		return self._elementos.count(unElemento)
	def contenido(self):
		return self._elementos

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
		unCarrito.agregarElemento(unElemento)
		self.assertEquals( 1, unCarrito.cantidadElementos() )
		self.assertEquals( True, unCarrito.estaEnElCarrito(unElemento) )
	def test03AgregoUnLibroQueNoPerteneceAlCatalogo(self):
		unElemento = Libro()
		otroElemento = Libro()
		unCatalogo = [unElemento]
		unCarrito = Carrito(unCatalogo)
		try:
			unCarrito.agregarElemento(otroElemento)
			self.fail()
		except Exception as libroFueraCatalogo:
			self.assertEquals( Carrito.ERROR_LIBRO_FUERA_DEL_CATALOGO, libroFueraCatalogo.message )
	def test04AgregarMuchoElementosFunciona(self):  '''Este test pasaba desde el comienzo, por eso lo comentamos '''
		elemento1 = Libro()
		elemento2 = Libro()
		elemento3 = Libro()
		elemento4 = Libro()
		unCatalogo = [elemento1,elemento2,elemento3, elemento4]
		unCarrito = Carrito(unCatalogo)

		unCarrito.agregarElemento(elemento1)
		unCarrito.agregarElemento(elemento2)
		unCarrito.agregarElemento(elemento3)
		unCarrito.agregarElemento(elemento4)

		self.assertEquals( 4, unCarrito.cantidadElementos() )
		self.assertEquals( True, unCarrito.estaEnElCarrito(elemento1) )
		self.assertEquals( True, unCarrito.estaEnElCarrito(elemento2) )
		self.assertEquals( True, unCarrito.estaEnElCarrito(elemento3) )
		self.assertEquals( True, unCarrito.estaEnElCarrito(elemento4) )
	def test05AgregoVariosDelMismoLibroYSuCantidadDeAparicionesEsCorrecta(self):
		unElemento = Libro()
		unCatalogo = [unElemento]
		unCarrito = Carrito(unCatalogo)
		unCarrito.agregarElemento(unElemento)
		unCarrito.agregarElemento(unElemento)
		unCarrito.agregarElemento(unElemento)
		unCarrito.agregarElemento(unElemento)
		self.assertEquals( 4, unCarrito.cantidadElementos() )
		self.assertEquals( 4, unCarrito.cantidadDeElementosComoEste(unElemento) )










if __name__ == "__main__":
	unittest.main()
