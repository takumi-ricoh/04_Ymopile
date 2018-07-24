#include <Wire.h>
#include <MsTimer2.h>

#define SENADR 0x5A //センサアドレス
#define WAIT1 100 //ms
#define WAIT2 20 //ms

unsigned long previousMillis;
unsigned long currentMillis;
unsigned long dt;

/*********************実行部****************************/
void setup() {

  //I2Cスタート
  Serial.begin(57600);
  Wire.begin();
  //同期信号出力ピン
  pinMode(8, OUTPUT);
  pinMode(9, OUTPUT);
  delay(100);

  previousMillis = millis(); //初期時刻
  digitalWrite(8, LOW); //一旦LOWにする
}

void loop() {
   digitalWrite(9, HIGH); //一旦LOWにする
  //時刻取得
  currentMillis = millis(); //現在の時刻
  //一定時間経過したら温度取得
  if ((currentMillis - previousMillis) > WAIT1) {
    previousMillis = currentMillis;//時刻リセット
    digitalWrite(8, HIGH); //立ち上がりエッジ
    double Vobj = readVobj();
    double Tobj = readTobj();
    double Tamb = readTamb();
    Serial.print(currentMillis); Serial.print(" "); Serial.print(Vobj);
    Serial.print(" "); Serial.print(Tobj); Serial.print(" "); Serial.println(Tamb);
  }
  else if ((currentMillis - previousMillis) > WAIT2) {
    digitalWrite(8, LOW); //LOWに戻す
  }
}
/***********************(参考：MsTimer2を使う場合)**************************/
void timeIntrp() {
  interrupts();
  double Vobj = readVobj();
  double Tobj = readTobj();
  double Tamb = readTamb();

  //時間
  digitalWrite(8, HIGH); //一旦highにする
  unsigned long currentMillis = millis();
  unsigned long dt = currentMillis - previousMillis;
  previousMillis = currentMillis;
  Serial.print(currentMillis); Serial.print(" "); Serial.print(Vobj);
  Serial.print(" "); Serial.print(Tobj); Serial.print(" "); Serial.println(Tamb);
  //Serial.println(dt);
  //Serial.println("-----------------------------------");
}

/****************************温度換算関数**************************/
//温度換算
double readVobj(void) {
  int16_t raw = read16_repeat(0x04);
  double Vobj;
  if (raw < 32768) {
    Vobj = raw * 0.02932;
  }
  else {
    Vobj = (raw - 32768) * (-0.02932);
  }
  return Vobj;
}

double readTobj(void) {
  int16_t raw = read16_repeat(0x07);
  double Tobj = raw * 0.02 - 273.15;
  return Tobj;
}

double readTamb(void) {
  int16_t raw = read16_repeat(0x06);
  double Tamb = raw * 0.02 - 273.15;
  return Tamb;
}

/************************** I2C 関数****************************/

uint16_t read16_repeat(uint8_t reg_adr) {
  uint16_t ret;

  Wire.beginTransmission(SENADR); // start transmission to device
  Wire.write(reg_adr); // sends register address to read from
  Wire.endTransmission(false); // end transmission

  Wire.requestFrom(SENADR, (uint8_t)3);// send data n-bytes read
  ret = Wire.read(); // receive DATA
  ret |= Wire.read() << 8;
  Wire.endTransmission(true);
  return ret;
}

uint16_t read16(uint8_t reg_adr) {
  uint16_t ret;

  Wire.beginTransmission(SENADR); // start transmission to device
  Wire.write(reg_adr); // sends register address to read from
  Wire.endTransmission(); // end transmission

  Wire.requestFrom(SENADR, (uint8_t)2);// send data n-bytes read
  ret = Wire.read(); // receive DATA
  ret <<= 8;
  ret |= Wire.read(); // receive DATA

  return ret;
}

void write16(uint8_t reg_adr, uint16_t d) {
  Wire.beginTransmission(SENADR); // start transmission to device
  Wire.write(reg_adr); // sends register address to read from
  Wire.write(d >> 8); // write data
  Wire.write(d);  // write data
  Wire.endTransmission(); // end transmission
}
