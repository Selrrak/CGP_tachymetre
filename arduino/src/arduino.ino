constexpr size_t SENSOR_PIN = 2;
constexpr size_t LED_PIN = 8;
constexpr size_t COMMAND_SIZE = 32;

int lastSensorState = HIGH;
char command[COMMAND_SIZE];
size_t commandIndex = 0;
unsigned long lastDetection = 0;

void setup() {
  Serial.begin(115200);
  pinMode(SENSOR_PIN, INPUT);
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  while (Serial.available()) {
    char c = Serial.read();

    if (c == '\n') {
      //listen to the serial port and id the board to a script asking "who are you"
      command[commandIndex] = '\0';

      if (strcmp(command, "WHO_ARE_YOU?") == 0) {
        Serial.println("ID:TACHYMETRE_UNO_V1");
      }

      commandIndex = 0;
    } else if (commandIndex < COMMAND_SIZE - 1) {
      command[commandIndex++] = c;
    }
  }
  // Read the sensor
  int sensorState = digitalRead(SENSOR_PIN);

  digitalWrite(LED_PIN, sensorState);

  if (sensorState == HIGH && lastSensorState == LOW) {
    unsigned long now = micros();

    if (lastDetection != 0) {
      unsigned long interval = now - lastDetection;

      Serial.print("INTERVAL:");
      Serial.println(interval);
    }

    lastDetection = now;
  }
  lastSensorState = sensorState;
  delay(10);
}
