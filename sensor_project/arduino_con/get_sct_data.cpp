/*
 * =====================================================================================
 *
 *       Filename:  db_SCT.cpp
 *
 *    Description:  Collect current information from the CT sensor based on ARDUINO uno
 *                  board and send the data to bluehost database
 *
 *        Created:  05/27/2014 03:11:03 PM
 *       Compiler:  g++ 4.7.0
 *
 * =====================================================================================
 */

#include "EmonLib.h"
EnergyMonitor emon1;

void setup(){
    
    Serial.begin(9600); 
    emonl.cirrent(1, 111.1);  // Current: input pin, calibration
}


void loop(){
    
    double Irms = emon1.calcIrms(1480);   // Calculate Irms only

    Serial.print(Irms * 230.0);           // Apparent power
    Serial.print(" ");                     
    Serial.println(Irms);                 // Irms

}
