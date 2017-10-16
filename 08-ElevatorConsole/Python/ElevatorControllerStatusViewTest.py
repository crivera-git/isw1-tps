# -*- coding: utf-8 -*-
#
# Developed by 10Pines SRL
# License:
# This work is licensed under the
# Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/
# or send a letter to Creative Commons, 444 Castro Street, Suite 900, Mountain View,
# California, 94041, USA.
#
import unittest
from ElevatorController import ElevatorController

# El ElevatorControllerConsole va a observar lo que haga el elevatorController.
# Para hacer esto, el se debe "suscribir" a la lista de observadores.


# No se si esta es la idea del ejercicio: poder agregar consolas que tengan comportamientos particulares sin tener que tocar nada
# La idea es tener una consola generica y que cada consola en particular haga lo que quiera cuando 
#le lleguen las noticias de los cambios

class Consola:

    def visitCabinDoorClosingState(self,est):
        self.shouldBeImplementedBySubclass()
    def visitCabinDoorOpeningState(self,est):
        self.shouldBeImplementedBySubclass()
    def visitCabinDoorOpenedState(self,est):
        self.shouldBeImplementedBySubclass()
    def visitCabinDoorClosedState(self,est):
        self.shouldBeImplementedBySubclass()
    def visitCabinStoppedState(self,est):
        self.shouldBeImplementedBySubclass()
    def visitCabinMovingState(self,est):
        self.shouldBeImplementedBySubclass()

# Consola que a medida que le llegan los estados "los guarda en un log"
class ElevatorControllerConsole(Consola):
    def __init__(self,elevatorController):
        self._elevator = elevatorController
        elevatorController.suscribirALaMiListaDeModificaciones(self)
        # self._listeners = []
        self._mensajes = []
        # Me suscribo a los mensajes que envia elevatorController.
        # elevatorController.suscribirALaMiListaDeModificaciones(self)
    def visitCabinDoorClosingState(self,est):
        self._mensajes.append("Puerta Cerrandose")
    def visitCabinDoorOpeningState(self,est):
        self._mensajes.append("Puerta Abriendose")
    def visitCabinDoorOpenedState(self,est):
        self._mensajes.append("Puerta Abierta")
    def visitCabinDoorClosedState(self,est):
        self._mensajes.append("Puerta Cerrada")
    def visitCabinStoppedState(self,est):
        self._mensajes.append("Cabina Detenida")
    def visitCabinMovingState(self,est):
        self._mensajes.append("Cabina Moviendose")

    def lines(self):
        return self._mensajes

    # def nuevoEstado(self, objeto):
    #     self._mensajes.append(objeto)

class ElevatorControllerStatusView:
    def __init__(self,elevatorController):
        self._elevator = elevatorController
    def cabinStateFieldModel(self):
        return self._elevator.cabinState()
    def cabinDoorStateFieldModel(self):
        return self._elevator.doorState()

class ElevatorControllerViewTest(unittest.TestCase):

    def test01ElevatorControllerConsoleTracksDoorClosingState(self):
        elevatorController = ElevatorController()
        elevatorControllerConsole = ElevatorControllerConsole(elevatorController)

        elevatorController.goUpPushedFromFloor(1)

        lines = elevatorControllerConsole.lines()

        self.assertEquals(1,len(lines))
        self.assertEquals("Puerta Cerrandose",lines[0])

    def test02ElevatorControllerConsoleTracksCabinState(self):
        elevatorController = ElevatorController()
        elevatorControllerConsole = ElevatorControllerConsole(elevatorController)

        elevatorController.goUpPushedFromFloor(1)
        elevatorController.cabinDoorClosed()

        lines = elevatorControllerConsole.lines()

        self.assertEquals(3,len(lines))
        self.assertEquals("Puerta Cerrandose",lines[0])
        self.assertEquals("Puerta Cerrada",lines[1])
        self.assertEquals("Cabina Moviendose",lines[2])

    def test03ElevatorControllerConsoleTracksCabinAndDoorStateChanges(self):
        elevatorController = ElevatorController()
        elevatorControllerConsole = ElevatorControllerConsole(elevatorController)

        elevatorController.goUpPushedFromFloor(1)
        elevatorController.cabinDoorClosed()
        elevatorController.cabinOnFloor(1)

        lines = elevatorControllerConsole.lines()

        self.assertEquals(5,len(lines))
        self.assertEquals("Puerta Cerrandose",lines[0])
        self.assertEquals("Puerta Cerrada",lines[1])
        self.assertEquals("Cabina Moviendose",lines[2])
        self.assertEquals("Cabina Detenida",lines[3])
        self.assertEquals("Puerta Abriendose",lines[4])

    def test04ElevatorControllerCanHaveMoreThanOneView(self):
        elevatorController = ElevatorController()
        elevatorControllerConsole = ElevatorControllerConsole(elevatorController)
        elevatorControllerStatusView = ElevatorControllerStatusView(elevatorController)

        elevatorController.goUpPushedFromFloor(1)
        elevatorController.cabinDoorClosed()
        elevatorController.cabinOnFloor(1)

        lines = elevatorControllerConsole.lines()

        self.assertEquals(5,len(lines))
        self.assertEquals("Puerta Cerrandose",lines[0])
        self.assertEquals("Puerta Cerrada",lines[1])
        self.assertEquals("Cabina Moviendose",lines[2])
        self.assertEquals("Cabina Detenida",lines[3])
        self.assertEquals("Puerta Abriendose",lines[4])

        self.assertEquals("Stopped",elevatorControllerStatusView.cabinStateFieldModel())
        self.assertEquals("Opening",elevatorControllerStatusView.cabinDoorStateFieldModel())

if __name__ == "__main__":
    unittest.main()
