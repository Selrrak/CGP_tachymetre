constexpr size_t SENSOR_PIN = 2;
constexpr size_t LED_PIN = 8;
constexpr size_t COMMAND_SIZE = 32;

int lastSensorState = HIGH;
char command[COMMAND_SIZE];
size_t commandIndex = 0;

void setup() {
  while (Serial.available()) {
    char c = Serial.read();

    if (c == '\n') {
      command[commandIndex] = '\0';

      if (strcmp(command, "WHO_ARE_YOU?") == 0) {
        Serial.println("TACHYMETRE_UNO_V1");
      }

      commandIndex = 0;
    } else if (commandIndex < COMMAND_SIZE - 1) {
      command[commandIndex++] = c;
    }
  }
  pinMode(SENSOR_PIN, INPUT);
  pinMode(LED_PIN, OUTPUT);

  Serial.begin(115200);
}

void loop() {
  int sensorState = digitalRead(SENSOR_PIN);

  digitalWrite(LED_PIN, sensorState);

  if (sensorState != lastSensorState) {
    if (sensorState == HIGH) {
      Serial.println("Object detected");
    } else {
      Serial.println("No object");
    }

    lastSensorState = sensorState;
  }

  delay(10);
}
