//
// Heiman Thrmopile Test Program
//    2018/03/22
//
//   複数のセンサの検出温度（Tobj）を表示
//　 センサのアドレスは、0x5Aからインクリメント
//
//   センサには、0x5Aからアドレスを振っておくこと。
//   1chあたりの測定時間は、1.2[ms]。24個読むのには約30[ms]要する。
//   センサのデータ更新時間が100[ms]のため、同じセンサを読み出すのは100[ms]以上経過後にする処理を入れてある。
//   どのセンサの出力値かわかるように、データの前にセンサ番号を追加。

#include <Wire.h>

#define WAIT 300            //Wait時間（同一センサを読む時の間隔が、100[ms]以上になるようにする）
#define SENSOR_NUM 24       //センサ数
#define SENSOR_BASEADR 0x5A //センサのベースアドレス

unsigned long previousMillis = millis();
unsigned long time;

/**************/
/*** 実行部 ***/
/**************/
void setup() {
  //I2Cスタート
  Serial.begin(115200);    // ターミナルソフトのボーレートは115200に指定すること
  Wire.begin();
  //  pinMode(8, OUTPUT);
  delay(200);
}

void loop() {
  unsigned int i;
  unsigned long currentMillis = millis();
  unsigned long dt = currentMillis - previousMillis;
  if (dt > WAIT) {        //一つ目のセンサを読むタイミングが、前回測定時より間隔が、WAIT[ms]以上になら測定開始
    previousMillis = currentMillis;

    time = millis();

    //時刻の表示
    Serial.print(time);
    Serial.print( "," );

    //ダミー熱電対データ
    Serial.print("0,0,");

    for ( i = 0; i < SENSOR_NUM; i++ ) {          
      // 全部のセンサの測定値を順次読み出す
      double Tobj = readTobj( SENSOR_BASEADR + i );
      double Tamb = readTamb( SENSOR_BASEADR + i );

      if( Tobj > 0.0 ) {                          // 接続されているセンサの結果だけ出力（接続されていないセンサからの戻り値は0[deg]）
        Serial.print( i );                   // 結果を出力する
        Serial.print( ":" );                     // 結果を出力する
        Serial.print( Tobj );                    // 結果を出力する
        Serial.print( ":" );                     // 結果を出力する
        Serial.print( Tamb );                    // 結果を出力する
        Serial.print(",");                       // 区切り文字を出力する
      }     
    }
  Serial.println();                              // 改行を出力する
  }
}

/********************/
/*** 温度換算関数 ***/
/********************/
double readTobj( uint8_t sen_adr ) {
  int16_t raw = read16_repeat( 0x07, sen_adr );
  double Tobj = raw * 0.02 - 273.15;
  if ( Tobj < 0 ) Tobj = 0;
  return Tobj;
}

double readTamb( uint8_t sen_adr ) {
  int16_t raw = read16_repeat( 0x06, sen_adr );
  double Tobj = raw * 0.02 - 273.15;
  if ( Tobj < 0 ) Tobj = 0;
  return Tobj;
}

/****************/
/*** I2C 関数 ***/
/****************/
uint16_t read16_repeat( uint8_t reg_adr, uint8_t sen_adr ) {
  uint16_t ret;

  Wire.beginTransmission( sen_adr ); // start transmission to device
  Wire.write( reg_adr ); // sends register address to read from
  Wire.endTransmission( false ); // end transmission

  Wire.requestFrom( sen_adr, (uint8_t)3);// send data n-bytes read
  ret = Wire.read(); // receive DATA
  ret |= Wire.read() << 8;
  Wire.endTransmission( true );
  return ret;
}
