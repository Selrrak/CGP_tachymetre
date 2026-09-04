from PySide6.QtCore import Property, QObject, Signal, Slot

from tachymetre.serial_listener import Measurement, measurements


class Tachymeter(QObject):
    rpmChanged = Signal()
    rpsChanged = Signal()
    angularVelocityChanged = Signal()
    centripetalAccelChanged = Signal()
    centripetalGChanged = Signal()

    def __init__(self):
        super().__init__()

        self._rpm = 0.0
        self._rps = 0.0
        self._angular_velocity = 0.0
        self._centripetal_accel = 0.0
        self._centripetal_g = 0.0

    @Property(float, notify=rpmChanged)
    def rpm(self):
        return self._rpm

    @Property(float, notify=rpsChanged)
    def rps(self):
        return self._rps

    @Property(float, notify=angularVelocityChanged)
    def angular_velocity(self):
        return self._angular_velocity

    @Property(float, notify=centripetalAccelChanged)
    def centripetal_accel(self):
        return self._centripetal_accel

    @Property(float, notify=centripetalGChanged)
    def centripetal_g(self):
        return self._centripetal_g

    def update(self, measurement: Measurement):
        self._rpm = measurement.rpm
        self._rps = measurement.rps
        self._angular_velocity = measurement.angular_velocity
        self._centripetal_accel = measurement.centripetal_accel
        self._centripetal_g = measurement.centripetal_g

        self.rpmChanged.emit()
        self.rpsChanged.emit()
        self.angularVelocityChanged.emit()
        self.centripetalAccelChanged.emit()
        self.centripetalGChanged.emit()
