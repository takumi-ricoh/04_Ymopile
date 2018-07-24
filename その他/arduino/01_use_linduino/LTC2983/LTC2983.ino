/*!



  LTC2983.ino:
  Generated Linduino code from the LTC2983 Demo Software.
  This code (plus the other code in this folder) is designed to be used by a Linduino,
  but can also be used to understand how to program the LTC2983.




  http://www.linear.com/product/LTC2983

  http://www.linear.com/product/LTC2983#demoboards

  $Revision: 1.6.2 $
  $Date: April 24, 2018 $
  Copyright (c) 2014, Linear Technology Corp.(LTC)
  All rights reserved.

  Redistribution and use in source and binary forms, with or without
  modification, are permitted provided that the following conditions are met:

  1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
  2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
  DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
  ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
  (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
  LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
  ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

  The views and conclusions contained in the software and documentation are those
  of the authors and should not be interpreted as representing official policies,
  either expressed or implied, of Linear Technology Corp.

  The Linear Technology Linduino is not affiliated with the official Arduino team.
  However, the Linduino is only possible because of the Arduino team's commitment
  to the open-source community.  Please, visit http://www.arduino.cc and
  http://store.arduino.cc , and consider a purchase that will help fund their
  ongoing work.
*/





#include <Arduino.h>
#include <stdint.h>
#include <stdbool.h>
#include "SPI.h"
#include "Wire.h"
#include "Linduino.h"
#include "LT_SPI.h"
#include "UserInterface.h"
#include "LT_I2C.h"
#include "QuikEval_EEPROM.h"
#include "stdio.h"
#include "math.h"

#include "LTC2983_configuration_constants.h"
#include "LTC2983_support_functions.h"
#include "LTC2983_table_coeffs.h"

#define CHIP_SELECT QUIKEVAL_CS  // Chip select pin

//--- Heimann Sensor(I2C)---
#define WAIT 100            //ms
#define SENSOR_NUM 24        //センサ数
#define SENSOR_BASEADR 0x5A //センサのアドレス
unsigned long previousMillis = millis();
unsigned long time;
//--- Heimann Sensor(I2C)---

// Function prototypes
void configure_channels();
void configure_global_parameters();


// -------------- Configure the LTC2983 -------------------------------
void setup()
{
  char demo_name[] = "DC2209";   // Demo Board Name stored in QuikEval EEPROM
  quikeval_I2C_init();          // Configure the EEPROM I2C port for 100kHz
  quikeval_SPI_init();          // Configure the spi port for 4MHz SCK
  quikeval_SPI_connect();       // Connect SPI to main data port
  pinMode(CHIP_SELECT, OUTPUT); // Configure chip select pin on Linduino

  Serial.begin(115200);         // Initialize the serial port to the PC

  //--- Heimann Sensor(I2C)---
  //I2Cスタート
  Wire.begin();
  //--- Heimann Sensor(I2C)---

  //  print_title();
  //  discover_demo_board(demo_name);

  configure_channels();
  configure_global_parameters();
}


void configure_channels()
{
  uint8_t channel_number;
  uint32_t channel_assignment_data;

  // ----- Channel 1: Assign Type E Thermocouple -----
  channel_assignment_data =
    SENSOR_TYPE__TYPE_E_THERMOCOUPLE |
    TC_COLD_JUNCTION_CH__2 |
    TC_SINGLE_ENDED |
    TC_OPEN_CKT_DETECT__YES |
    TC_OPEN_CKT_DETECT_CURRENT__10UA;
  assign_channel(CHIP_SELECT, 1, channel_assignment_data);
  // ----- Channel 2: Assign Off-Chip Diode -----
  channel_assignment_data =
    SENSOR_TYPE__OFF_CHIP_DIODE |
    DIODE_SINGLE_ENDED |
    DIODE_NUM_READINGS__2 |
    DIODE_AVERAGING_OFF |
    DIODE_CURRENT__20UA_80UA_160UA |
    (uint32_t) 0x100C49 << DIODE_IDEALITY_FACTOR_LSB;		// diode - ideality factor(eta): 1.00299930572509765625
  assign_channel(CHIP_SELECT, 2, channel_assignment_data);
  // ----- Channel 3: Assign Type E Thermocouple -----
  channel_assignment_data =
    SENSOR_TYPE__TYPE_E_THERMOCOUPLE |
    TC_COLD_JUNCTION_CH__4 |
    TC_SINGLE_ENDED |
    TC_OPEN_CKT_DETECT__YES |
    TC_OPEN_CKT_DETECT_CURRENT__10UA;
  assign_channel(CHIP_SELECT, 3, channel_assignment_data);
  // ----- Channel 4: Assign Off-Chip Diode -----
  channel_assignment_data =
    SENSOR_TYPE__OFF_CHIP_DIODE |
    DIODE_SINGLE_ENDED |
    DIODE_NUM_READINGS__2 |
    DIODE_AVERAGING_OFF |
    DIODE_CURRENT__20UA_80UA_160UA |
    (uint32_t) 0x100C49 << DIODE_IDEALITY_FACTOR_LSB;		// diode - ideality factor(eta): 1.00299930572509765625
  assign_channel(CHIP_SELECT, 4, channel_assignment_data);
  // ----- Channel 9: Assign Off-Chip Diode -----
  channel_assignment_data =
    SENSOR_TYPE__OFF_CHIP_DIODE |
    DIODE_SINGLE_ENDED |
    DIODE_NUM_READINGS__3 |
    DIODE_AVERAGING_OFF |
    DIODE_CURRENT__20UA_80UA_160UA |
    (uint32_t) 0x100C49 << DIODE_IDEALITY_FACTOR_LSB;		// diode - ideality factor(eta): 1.00299930572509765625
  assign_channel(CHIP_SELECT, 9, channel_assignment_data);

}

void configure_global_parameters()
{
  // -- Set global parameters
  transfer_byte(CHIP_SELECT, WRITE_TO_RAM, 0xF0, TEMP_UNIT__C |
                REJECTION__50_60_HZ);
  // -- Set any extra delay between conversions (in this case, 0*100us)
  transfer_byte(CHIP_SELECT, WRITE_TO_RAM, 0xFF, 0);
}

//--- Heimann Sensor(I2C)---

/*** 温度換算関数 ***/
double readTobj( uint8_t sen_adr ) {
  int16_t raw = read16_repeat( 0x07, sen_adr );
  double Tobj = raw * 0.02 - 273.15;
  if ( Tobj < 0 ) Tobj = 0;
  return Tobj;
}

/*** I2C 関数 ***/
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
//--- Heimann Sensor(I2C)---

// -------------- Run the LTC2983 -------------------------------------

void loop()
{
  ////////////////////////////////
  // タイムスタンプ
  ////////////////////////////////
  time = millis();


  ////////////////////////////////
  // Heimann Sensor (I2C）
  ////////////////////////////////

  unsigned int i;
  unsigned long currentMillis = millis();
  unsigned long dt = currentMillis - previousMillis;
  if (dt > WAIT) {
    previousMillis = currentMillis;
    Serial.print(time);
    Serial.print( "," );

    ////////////////////////////////
    // Thrmocoiple (SPi)
    ////////////////////////////////
    //measure_channel(CHIP_SELECT, 1, TEMPERATURE);      // Ch 1: Type E Thermocouple
    //  measure_channel(CHIP_SELECT, 2, TEMPERATURE);      // Ch 2: Off-Chip Diode
    //measure_channel(CHIP_SELECT, 3, TEMPERATURE);      // Ch 3: Type E Thermocouple
    //  measure_channel(CHIP_SELECT, 4, TEMPERATURE);      // Ch 4: Off-Chip Diode
    //  measure_channel(CHIP_SELECT, 9, TEMPERATURE);      // Ch 9: Off-Chip Diode

    //疑似信号
    Serial.print(random(100, 200));
    Serial.print( "," );
    Serial.print(random(100, 200));
    Serial.print( "," );

    for ( i = 0; i < SENSOR_NUM; i++ ) {          // 全部のセンサの測定値を順次読み出す
      double Tobj = random(100, 200); //readTobj( SENSOR_BASEADR + i );
      double Tamb = random(100, 200); //Tobj; //ひとまず
      //if( Tobj > 0.0 ) {                          // 接続されているセンサの結果だけ出力（接続されていないセンサからの戻り値は0[deg]）
      Serial.print( i );                    // 結果を出力する
      Serial.print( ":" );                    // 結果を出力する
      Serial.print( Tobj );                    // 結果を出力する
      Serial.print( ":" );                    // 結果を出力する
      Serial.print( Tamb );                    // 結果を出力する
      Serial.print(",");                       // 区切り文字を出力する
      //}
    }
    Serial.println();
  }
  //  Serial.println();
}
