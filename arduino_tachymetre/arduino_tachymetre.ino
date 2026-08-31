const int SENSOR_PIN = 2;
const int LED_PIN = 8;

int lastSensorState = HIGH;

void setup() {
  pinMode(SENSOR_PIN, INPUT);
  pinMode(LED_PIN, OUTPUT);

  Serial.begin(9600);
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
