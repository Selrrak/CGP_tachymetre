import math
import threading
import time
from dataclasses import dataclass

import serial
import serial.tools.list_ports

BAUD_RATE = 115200
IDENTIFICATION_COMMAND = b"WHO_ARE_YOU?\n"
EXPECTED_RESPONSE = "ID:TACHYMETRE_UNO_V1"
MARKS_PER_TURN = 4
RADIUS_M = 0.25


def find_arduino():
    for port in serial.tools.list_ports.comports():
        try:
            with serial.Serial(port.device, BAUD_RATE, timeout=0.1) as ser:
                time.sleep(2)
                ser.reset_input_buffer()
                ser.write(IDENTIFICATION_COMMAND)
                deadline = time.monotonic() + 1.0
                buffer = ""

                while time.monotonic() < deadline:
                    if ser.in_waiting:
                        c = ser.read().decode(errors="ignore")

                        if c == "\n":
                            response = buffer.strip()

                            if response == EXPECTED_RESPONSE:
                                return port.device

                            buffer = ""
                        else:
                            buffer += c

        except (serial.SerialException, UnicodeDecodeError):
            pass

    return None


def measurements(stop_event=None):
    if stop_event is None:
        stop_event = threading.Event()

    arduino_port = find_arduino()

    if arduino_port is None:
        raise RuntimeError("Arduino not detected")

    print(f"Arduino found on {arduino_port}")

    with serial.Serial(arduino_port, BAUD_RATE, timeout=0.1) as ser:
        intervals = []

        while not stop_event.is_set():
            line = ser.readline().decode("utf-8").strip()

            if not line.startswith("INTERVAL:"):
                continue

            value = line.split(":", 1)[1]
            interval_us = int(value)
            intervals.append(interval_us)

            if len(intervals) == MARKS_PER_TURN:
                yield compute_values(intervals)
                intervals.clear()


def compute_values(intervals) -> Measurement:
    average_interval_us = sum(intervals) / len(intervals)
    rps = 1_000_000 / (MARKS_PER_TURN * average_interval_us)
    rpm = rps * 60
    angular_velocity = 2 * math.pi * rps
    centrip_accel = (angular_velocity**2) * RADIUS_M
    centrip_g = centrip_accel / 9.81

    return Measurement(
        average_interval_us=average_interval_us,
        rps=round(rps, 2),
        rpm=round(rpm, 2),
        angular_velocity=round(angular_velocity, 2),
        centripetal_accel=round(centrip_accel, 2),
        centripetal_g=round(centrip_g, 2),
    )


@dataclass
class Measurement:
    average_interval_us: float
    rps: float
    rpm: float
    angular_velocity: float
    centripetal_accel: float
    centripetal_g: float
