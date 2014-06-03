#include <iostream>
#include <fstream>
#include <ofstream>

using namespace std;

#include "EmonLib.h"                   // Include Emon Library
EnergyMonitor emon1;                   // Create an instance

void setup()
{  
  Serial.begin(9600);
  
  emon1.current(1, 111.1);             // Current: input pin, calibration.
}

void loop()
{
  double Irms = emon1.calcIrms(1480);  // Calculate Irms only
  double power = Irms * 230.0;
  
  Serial.print(power);	       // Apparent power
  Serial.print(" ");
  Serial.println(Irms);		       // Irms
  
  ofstream myfile("test.txt");
  if(!myfile.isopen()){
     Serial.print("Error in opening file!");
     return;
  }
  
  myfile << power << "," << Irms << "\n";
  myfile.close();  
}
