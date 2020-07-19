#include <IRremote.h>  //including infrared remote header file     
#define start_order 12495
#define feed_order 6375
#define stop_order 31365
#define noise     10  // Noise/hum/interference in mic signal
int RECV_PIN = 8; // the pin where you connect the output pin of IR sensor  
int MIC_PIN = 10;
int volume;
IRrecv reciever(RECV_PIN);     
decode_results output; 
    
void setup()     
{     
  Serial.begin(9600);     
  reciever.enableIRIn();
  pinMode(A0, INPUT);  
}

void loop()     
{ 
  volume = analogRead(A0);
  volume   = abs(volume - 512); // Center on zero
  volume   = (volume <= noise) ? 0 : (volume - noise);   
  delay(100);
  if(volume >= 90) {
    Serial.println("feedVoice");
  }
  
  if (reciever.decode(&output))// Returns 0 if no data ready, 1 if data ready.     
  {     
    unsigned int code = output.value;     
    switch(code) {
      case start_order:
         Serial.println("fly");
         break;
      case feed_order:
         Serial.println("feed");
         break;
      case stop_order:
         Serial.println("land");
         break;
    }
 
    reciever.resume(); // Restart the ISR state machine and Receive the next value     
  }
}
