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

class Observer:
    def __init__(self,sujeto):
        sujeto.registrarObservador(self)
    def update(self,state):
        self.shouldBeImplementedBySubclass()
class ElevatorControllerObserver(Observer):
    def update(self,state):
        state.accept(self)
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


class ElevatorControllerConsole(ElevatorControllerObserver):
    def __init__(self,elevatorController):
        Observer.__init__(self,elevatorController)
        self._mensajes = []
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

class ElevatorControllerStatusView(ElevatorControllerObserver):

    def visitCabinDoorClosingState(self,est):
        self._cabinDoorState = "Closing"
    def visitCabinDoorOpeningState(self,est):
        self._cabinDoorState = "Opening"
    def visitCabinDoorOpenedState(self,est):
        self._cabinDoorState = "Opened"
    def visitCabinDoorClosedState(self,est):
        self._cabinDoorState = "Closed"
    def visitCabinStoppedState(self,est):
        self._cabinState = "Stopped"
    def visitCabinMovingState(self,est):
        self._cabinState = "Moving"
    def cabinStateFieldModel(self):
        return self._cabinState
    def cabinDoorStateFieldModel(self):
        return self._cabinDoorState
    

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
