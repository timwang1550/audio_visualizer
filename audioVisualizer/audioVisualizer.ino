
// Fast LED library
#include <FastLED.h>

// LED strip constants
#define LED_COUNT 56 // 7 rows x 8 width
#define LED_HEIGHT 7
#define LED_WIDTH 8
#define LED_PIN 3

// LED and audio vectors
CRGB leds[LED_COUNT];
unsigned int AUDIO_BANDS[LED_WIDTH] = {0};

// LED enum for shifting
enum colors {
  
};

// Serial data variables
int dataCount = 0;

void setup() 
{
  // Serial startup
  Serial.begin(19200);
  while(!Serial); // loop forever if Serial fails 

  // LED setup
  FastLED.addLeds<NEOPIXEL, LED_PIN>(leds, LED_COUNT);
  FastLED.setBrightness(32); // quarter brightness
  
  CRGB colors[] = { CRGB::Red, CRGB::Orange, CRGB::Yellow, CRGB::Lime, 
    CRGB::LightSkyBlue, CRGB::RoyalBlue, CRGB::Purple, CRGB::Violet };

  // initalize starting colors
  for (int led = 0; led < LED_WIDTH; led++)
    leds[led] = colors[led];
    
  FastLED.show();
  delay(1000);
  // colorTest();
  
}


void loop()
{
  if (Serial.available()) // read when new data is updated
  {
    AUDIO_BANDS[dataCount++] = Serial.read();

    if (dataCount == LED_WIDTH) // once one a full array of data is filled
    {
      updateColor();
      dataCount = 0;  // reset counter
    }
  }
}


// update LED strips
void updateColor()
{
  // led strip positions bcoz too lazy to write a decent algorithm
  static int bands[LED_WIDTH][LED_HEIGHT] = {
    {0,15,16,31,32,47,48},
    {1,14,17,30,33,46,49},
    {2,13,18,29,34,45,50},
    {3,12,19,28,35,44,51},
    {4,11,20,27,36,43,52},
    {5,10,21,26,37,42,53},
    {6, 9,22,25,38,41,54},
    {7, 8,23,24,39,40,55}
  };

  // reset all bands to black aside from row 0
  for (int c = LED_WIDTH; c < LED_COUNT; c++)
    leds[c] = CRGB::Black;
  
  for (int band = 0; band < LED_WIDTH; band++)
  {
    unsigned int band_value = AUDIO_BANDS[band];
 
    // update height of band accordingly
    for (int h = 0; h < (band_value+1); h++)
    {
      // copy color of row 0
      leds[bands[band][h]] = leds[bands[band][0]];
    }
  }
  FastLED.show();
  Serial.print("\n");
  
}
