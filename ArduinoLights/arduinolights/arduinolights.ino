#include "FastLED.h"

#define NUM_LEDS 300
#define DATA_PIN 3
#define updateLEDS 5

CRGB leds[NUM_LEDS];

int incomingByte = 0;

struct color{
  int r;
  int g;
  int b;
};
typedef struct color Color;

color mainColor;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  FastLED.addLeds<NEOPIXEL, DATA_PIN>(leds, NUM_LEDS);
  for(int i = 0; i < NUM_LEDS; i++){
      leds[i] = CRGB(0, 0, 0);
  }
  FastLED.show();
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available() > 0){
    incomingByte = Serial.read();

    Serial.println(incomingByte);
  }
  for(int i = NUM_LEDS - 1; i >= updateLEDS; i--){
    leds[i] = leds[i-updateLEDS];
  }
/*
  //Christmas Mode
  if(incomingByte == 49){
    mainColor.r = 150;
    mainColor.g = 0;
    mainColor.b = 0;
  }else if(incomingByte == 50){
    mainColor.r = 0;
    mainColor.g = 150;
    mainColor.b = 0;
  }else if(incomingByte == 51){
    mainColor.r = 150;
    mainColor.g = 150;
    mainColor.b = 150;
  }else if(incomingByte == 52){
    mainColor.r = 150;
    mainColor.g = 150;
    mainColor.b = 0;
  }else if(incomingByte == 53){
    mainColor.r = 200;
    mainColor.g = 0;
    mainColor.b = 0;
  }else if(incomingByte == 54){
    mainColor.r = 0;
    mainColor.g = 200;
    mainColor.b = 0;
  }else if(incomingByte == 55){
    mainColor.r = 200;
    mainColor.g = 200;
    mainColor.b = 200;
  }else if(incomingByte == 56){
    mainColor.r = 200;
    mainColor.g = 200;
    mainColor.b = 0;
  }else if(incomingByte == 57){
    mainColor.r = 255;
    mainColor.g = 0;
    mainColor.b = 0;
  }else if(incomingByte == 58){
    mainColor.r = 0;
    mainColor.g = 255;
    mainColor.b = 0;
  }else if(incomingByte == 59){
    mainColor.r = 255;
    mainColor.g = 255;
    mainColor.b = 0;
  }else if(incomingByte == 60){
    mainColor.r = 255;
    mainColor.g = 255;
    mainColor.b = 255;
  }

*/
  //Normal Mode
  
   if(incomingByte == 49){
    mainColor.r = 255;
    mainColor.g = 0;
    mainColor.b = 0;
  }else if(incomingByte == 50){
    mainColor.r = 255;
    mainColor.g = 0;
    mainColor.b = 128;
  }else if(incomingByte == 51){
    mainColor.r = 255;
    mainColor.g = 0;
    mainColor.b = 255;
  }else if(incomingByte == 52){
    mainColor.r = 128;
    mainColor.g = 0;
    mainColor.b = 255;
  }else if(incomingByte == 53){
    mainColor.r = 0;
    mainColor.g = 0;
    mainColor.b = 255;
  }else if(incomingByte == 54){
    mainColor.r = 0;
    mainColor.g = 128;
    mainColor.b = 255;
  }else if(incomingByte == 55){
    mainColor.r = 0;
    mainColor.g = 255;
    mainColor.b = 255;
  }else if(incomingByte == 56){
    mainColor.r = 0;
    mainColor.g = 128;
    mainColor.b = 0;
  }else if(incomingByte == 57){
    mainColor.r = 0;
    mainColor.g = 255;
    mainColor.b = 0;
  }else if(incomingByte == 58){
    mainColor.r = 128;
    mainColor.g = 255;
    mainColor.b = 0;
  }else if(incomingByte == 59){
    mainColor.r = 255;
    mainColor.g = 255;
    mainColor.b = 0;
  }else if(incomingByte == 60){
    mainColor.r = 255;
    mainColor.g = 128;
    mainColor.b = 0;
  }
   
  for(int i = 0; i < updateLEDS; i++){
    leds[i] = CRGB(mainColor.r, mainColor.g, mainColor.b);
  }
  FastLED.show();

}


