#include <Servo.h>

Servo myservo, myservo1, myservo2;

int PWM = 3, INA = 4, INB = 5, EN = 6; 

String op = "";
bool entComp = false;
int v0 = 0, v1 = 25, v2 = 50, v3 = 75, v = 100;
int i = 105;    
int alpha = 100;
void setup() {
  Serial.begin(9600);
  
  pinMode(PWM, OUTPUT);
  pinMode(INA, OUTPUT);
  pinMode(INB, OUTPUT);
  pinMode(EN, OUTPUT);
  myservo.attach(9);
  myservo1.attach(10); 
  myservo2.attach(11); 
}

void loop() {

  
  if(entComp){
    
    if(op == "adelante\n"){
      adelante(v);
    }
    if(op == "atras\n"){
      atras(v);
    }
    if(op == "izq\n"){
      myservo.write(i-alpha);
      abre();
    }
    if(op == "centro\n"){
      paro();
      myservo.write(i);
      cierra();
    }
    if(op == "der\n"){
      myservo.write(i+alpha);
      abre();
    }
    if(op == "CenArr\n"){
      myservo.write(i);
      adelante(v);
    }
    if(op == "CenAba\n"){
      myservo.write(i);
      atras(v);
    }

    if(op == "Buscar\n"){
      myservo.write(i+alpha);
      abre();
      adelante(v);
    }
    
  op = "";
  entComp = false;
  }
}

void adelante(uint8_t vel){
  int velocidad;
  velocidad = map(vel, 0, 100, 0, 255);
  analogWrite(PWM, velocidad);
  digitalWrite(EN, HIGH);
  digitalWrite(EN, HIGH);
  digitalWrite(INA, HIGH);
  digitalWrite(INB, LOW);
}
void atras(uint8_t vel){
  int velocidad;
  velocidad = map(vel, 0, 100, 0, 255);
  analogWrite(PWM, velocidad);
  digitalWrite(EN, HIGH);
  digitalWrite(INA, LOW);
  digitalWrite(INB, HIGH);
}
void paro(){
  analogWrite(PWM, 0);
  digitalWrite(EN, LOW);
  digitalWrite(INA, LOW);
  digitalWrite(INB, LOW);
}
void abre(){
  myservo1.write(90);
  myservo2.write(180);
}
void cierra(){
  myservo1.write(180);
  myservo2.write(90);
}

void serialEvent(){
  while(Serial.available()){
    char inChar = (char)Serial.read();
    op += inChar;
    if(inChar =='\n'){
      entComp = true;
    }
  }
}
