import Queue
import unittest
from collections import deque
class ElevatorController:
    ''' COLABORADORES INTERNOS '''
    def __init__(self):
        self._idle = True
        self._cabina_detenida = True
        self._cabina_puerta_abierta = True
        self._cabina_puerta_abriendo = False
        self._cabina_puerta_cerrada = False
        self._cabina_puerta_cerrando = False
        self._esperando_por_personas = False
        self._piso_de_cabina = 0
        self._llamados = deque()

    ''' METODOS DE CLASE '''

    ''' GETTERS '''
    def isIdle(self):
        return self._idle
    def isCabinStopped(self):
        return self._cabina_detenida
    def isCabinDoorOpened(self):
        return self._cabina_puerta_abierta
    def cabinFloorNumber(self):
        return self._piso_de_cabina
    def isWorking(self):
        return not self._idle
    def isCabinMoving(self):
        return (not self._cabina_detenida)
    def isCabinDoorOpening(self):
        return self._cabina_puerta_abriendo
    def isCabinDoorClosing(self):
        return self._cabina_puerta_cerrando
    def isCabinDoorClosed(self):
        return self._cabina_puerta_cerrada
    def isCabinDoorOpening(self):
        return self._cabina_puerta_abriendo
    def isCabinWaitingForPeople(self):
        return self._cabina_puerta_abierta

    ''' METODOS VERDADEROS '''
    def empezar_a_cerrar_puerta(self):
        self._cabina_puerta_abierta = False
        self._cabina_puerta_abriendo = False
        self._cabina_puerta_cerrando = True
        self._cabina_puerta_cerrada = False
    def cabinDoorClosed(self):
        if self._idle:
            raise ElevatorEmergency("Sensor de puerta desincronizado")
        if self._cabina_puerta_cerrada:
            raise ElevatorEmergency("Sensor de puerta desincronizado")
        if self._cabina_puerta_abriendo:
            raise ElevatorEmergency("Sensor de puerta desincronizado")
        self.empezar_a_cerrar_puerta()
        self._cabina_puerta_cerrando = False
        self._cabina_puerta_cerrada = True
        self._cabina_detenida = False
    def goUpPushedFromFloor(self, numero_de_piso):
        self._llamados.append(numero_de_piso)
        self._idle = False
        self._cabina_detenida = True
        self.empezar_a_cerrar_puerta()
    def cabinOnFloor(self,numero_de_piso):
        if len(self._llamados)==1:
            if self.isCabinStopped():
                raise ElevatorEmergency("Sensor de cabina desincronizado")
        if numero_de_piso!=self._piso_de_cabina+1:
            raise ElevatorEmergency("Sensor de cabina desincronizado")

        piso = self._llamados.popleft()
        self._piso_de_cabina = piso
    	self._cabina_detenida = True
    	self._cabina_puerta_abierta = False
    	self._cabina_puerta_abriendo = True
    	self._cabina_puerta_cerrada = False
    def cabinDoorOpened(self):
    	self._cabina_puerta_abierta = True
    	self._cabina_puerta_abriendo = False
    	if len(self._llamados)==0:
            self._idle = True
    def empezar_a_abrir_puerta(self):
   		self._cabina_puerta_abierta = False
   		self._cabina_puerta_cerrada = False
   		self._cabina_puerta_cerrando = False
   		self._cabina_puerta_abriendo = True
    def openCabinDoor(self):
        if self.isWorking():
            self.empezar_a_abrir_puerta()
            self._cabina_puerta_abriendo = True
            self._cabina_puerta_abierta = True
            self._cabina_puerta_cerrada = True
    def waitForPeopleTimedOut(self):
        self._cabina_puerta_cerrando = True
    def closeCabinDoor(self):
        self._cabina_puerta_cerrando = True

class ElevatorEmergency(Exception):
    def __init__(self,mensaje):
        self.message = mensaje
        