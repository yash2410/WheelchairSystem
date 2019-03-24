// assign pin num
int bed = 9; //connects to pin No. 5 on CD4066
int gar = 10; //connects to pin No. 6 on CD4066
int bath = 11; //connects to pin No. 12 on CD4066
int kit = 12;//connects to pin No. 13 on CD4066

// duration for output
int time = 50;
char command;

void setup() {
  pinMode(bed, OUTPUT);
  pinMode(gar, OUTPUT);
  pinMode(bath, OUTPUT);
  pinMode(kit, OUTPUT);
  Serial.begin(9600);
  Serial.flush();
  digitalWrite(LED_BUILTIN, HIGH);
  Serial.println("[SETUP DONE]");

  Serial.println("1 : gar high\n2 : bed high\n3 : kit high\n4 : bath high\n");
  Serial.println("5 : gar low\n6 : bed low\n7 : kit low\n8 : bath low\n");
}

void loop() {
  while (Serial.available()) {
    command = Serial.read();
    Serial.println(command);
    switch (command) {
      case '1':
        digitalWrite(gar, HIGH);
        break;
      case '2':
        digitalWrite(bed, HIGH);
        break;
      case '3':
        digitalWrite(kit, HIGH);
        break;
      case '4':
        digitalWrite(bath, HIGH);
        break;
      case '5':
        digitalWrite(gar, LOW);
        break;
      case '6':
        digitalWrite(bed, LOW);
        break;
      case '7':
        digitalWrite(kit, LOW);
        break;
      case '8':
        digitalWrite(bath, LOW);
        break;
      default:
        reset();
        break;
    }
  }


}

void reset() {

  digitalWrite(LED_BUILTIN, HIGH);
  delay(1000);

}
