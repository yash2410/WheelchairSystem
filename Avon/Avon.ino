// assign pin num
int bed = 4; //connects to pin No. 5 on CD4066
int gar = 5; //connects to pin No. 6 on CD4066
int bath = 6; //connects to pin No. 12 on CD4066
int kit = 7;//connects to pin No. 13 on CD4066

// duration for output
char command;

void setup() {
  pinMode(bed,OUTPUT);
  pinMode(gar, OUTPUT);
  pinMode(bath, OUTPUT);
  pinMode(kit, OUTPUT);

  Serial.begin(9600);
  Serial.flush();
  Serial.println("[SETUP DONE]");

}

void loop() {
  while (Serial.available()) {
    command = Serial.read();
    if (command == '1') {

      digitalWrite(gar, HIGH);
      Serial.println("command : " + String(command));
    } else if (command == '2') {

      digitalWrite(bed, HIGH);
      Serial.println("command : " + String(command));
    } else if (command == '3') {

      digitalWrite(kit, HIGH);
      Serial.println("command : " + String(command));
    } else if (command == '4') {

      digitalWrite(bath, HIGH);
      Serial.println("command : " + String(command));
    } else if (command == '5') {

      digitalWrite(gar, LOW);
      Serial.println("command : " + String(command));
    } else if (command == '6') {

      digitalWrite(bed, LOW);
      Serial.println("command : " + String(command));
    } else if (command == '7') {

      digitalWrite(kit, LOW);
      Serial.println("command : " + String(command));
    } else if (command == '8') {

      digitalWrite(bath, LOW);
      Serial.println("command : " + String(command));
    } else {

      Serial.println("command didnt match");
    }

  }
}


void reset() {
  delay(1000);
  Serial.println("Reset");
}
