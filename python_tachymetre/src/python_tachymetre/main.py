import sys

from PySide6.QtCore import QObject, QThread, Signal
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from serial_listener import measurements
from tachymeter import Tachymeter


class SerialWorker(QObject):
    measurementReceived = Signal(object)

    def run(self):
        for measurement in measurements():
            self.measurementReceived.emit(measurement)


app = QGuiApplication(sys.argv)

tachymeter = Tachymeter()

worker = SerialWorker()
thread = QThread()

worker.moveToThread(thread)

worker.measurementReceived.connect(tachymeter.update)

thread.started.connect(worker.run)

thread.start()

engine = QQmlApplicationEngine()

engine.rootContext().setContextProperty(
    "tachymeter",
    tachymeter,
)

engine.load("Main.qml")

if not engine.rootObjects():
    sys.exit(-1)

exit_code = app.exec()

thread.quit()
thread.wait()

sys.exit(exit_code)
