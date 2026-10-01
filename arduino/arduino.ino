constexpr size_t SENSOR_PIN = 2;
constexpr size_t LED_PIN = 8;
constexpr size_t COMMAND_SIZE = 32;
constexpr unsigned long MIN_PULSE_INTERVAL_US = 225000;

volatile unsigned long lastDetection = 0;
volatile unsigned long interval = 0;
volatile bool newDetection = false;

char command[COMMAND_SIZE];
size_t commandIndex = 0;

void sensorPulse() {
  unsigned long now = micros();

  if (lastDetection == 0) {
    lastDetection = now;
    return;
  }
  unsigned long elapsed = now - lastDetection;

  // filtrer les detections successives trop rapides
  if (elapsed >= MIN_PULSE_INTERVAL_US) {
    interval = elapsed;
    newDetection = true;
    lastDetection = now;
  }
}

void setup() {
  Serial.begin(115200);

  pinMode(SENSOR_PIN, INPUT);
  pinMode(LED_PIN, OUTPUT);

  attachInterrupt(
    digitalPinToInterrupt(SENSOR_PIN),
    sensorPulse,
    RISING);
}

void loop() {

  // Permet à l'arduino de s'identifier auprès du script python
  while (Serial.available()) {
    char c = Serial.read();

    if (c == '\n') {
      command[commandIndex] = '\0';

      if (strcmp(command, "WHO_ARE_YOU?") == 0) {
        Serial.println("ID:TACHYMETRE_UNO_V1");
      }

      commandIndex = 0;

    } else if (commandIndex < COMMAND_SIZE - 1) {
      command[commandIndex++] = c;
    }
  }

  // Prise de mesure
  if (newDetection) {
    noInterrupts();
    unsigned long measuredInterval = interval;
    newDetection = false;
    interrupts();

    Serial.print("INTERVAL:");
    Serial.println(measuredInterval);
  }

  // LED mirrors sensor state
  digitalWrite(LED_PIN, digitalRead(SENSOR_PIN));
}
