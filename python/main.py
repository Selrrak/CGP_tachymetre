import signal
import sys
import threading

from PySide6.QtCore import QObject, QThread, Signal
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

from src.serial_listener import measurements
from src.tachymeter import Tachymeter


class SerialWorker(QObject):
    measurementReceived = Signal(object)

    def __init__(self, stop_event):
        super().__init__()
        self.stop_event = stop_event

    def run(self):
        try:
            for measurement in measurements(self.stop_event):
                if self.stop_event.is_set():
                    break

                self.measurementReceived.emit(measurement)

        except Exception as e:
            print(f"Serial worker error: {e}")

        print("Serial worker stopped")


app = QGuiApplication(sys.argv)

stop_event = threading.Event()

tachymeter = Tachymeter()

worker = SerialWorker(stop_event)
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


def handle_sigint(signum, frame):
    print("\nStopping...")
    stop_event.set()
    app.quit()


signal.signal(signal.SIGINT, handle_sigint)

exit_code = app.exec()

# Tell the serial worker to stop
stop_event.set()

# Wait for SerialWorker.run() to return
thread.quit()
thread.wait()

sys.exit(exit_code)
