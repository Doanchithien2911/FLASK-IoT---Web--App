#include <WiFi.h>
#include <HTTPClient.h>
#include<ArduinoJson.h> 
#include<DHT.h>
const char* ssid = "YOUR WIFI";
const char* password =  "YOUR WIFI PASSWORD";
#define DHTPIN  4
#define DHTTYPE  DHT11
DHT dht(DHTPIN,DHTTYPE);
long long ngat=0;
int led = 2;
void setup() 
{
 
  Serial.begin(9600);
  dht.begin();
  WiFi.begin(ssid, password); 
 
  while (WiFi.status() != WL_CONNECTED) { //Check for the connection
    delay(1000);
    Serial.println("Connecting to WiFi..");
  }
 pinMode(led,OUTPUT);
 Serial.println(WiFi.localIP());
 Serial.println("Connected to the WiFi network");
 
}
 
void loop() 
{
 if(WiFi.status()== WL_CONNECTED)
 { 
  
   HTTPClient http1;
   HTTPClient http2;   
   
   http1.begin("http://"IP ADDRESS OF WIFI"/channel/452419/api/write/CDROUFJOVLUZHDREMBBB");  //Specify destination for HTTP request
   http1.addHeader("Content-Type", "application/json");           //Specify content-type header
   http2.begin("http://"IP ADDRESS OF WIFI"/channel/452419/api/get/led/CDROUFJOVLUZHDREMBBB");


    int httpCode2 = http2.GET();                        //Make the request

    if (httpCode2 > 0) 
    { //Check for the returning code

      String json1 = http2.getString();
      Serial.println(httpCode2);
      Serial.println(json1[2]);
      if(json1[2]=='1')
      {
        digitalWrite(led,HIGH);
      }
      else
      {
        digitalWrite(led,LOW);
      }
    }
    else 
    {
      Serial.println("Error on HTTP request");
    }

    http2.end(); //Free the resources

  float t = dht.readTemperature();
  float h = dht.readHumidity();
  Serial.println(t);
  Serial.println(h);
  DynamicJsonDocument data(2048);
  data["temp"]=t;
  data["humi"]=h;
  data["soil"]="";
  data["flow"]="";
  String json;
  serializeJson(data,json);
  

 if(millis()-2000>=ngat)
 {
   int httpResponseCode = http1.POST(json);   //Send the actual POST request
 
   if(httpResponseCode>0)
   {
 
    String response = http1.getString();                       //Get the response to the request
 
    Serial.println(httpResponseCode);   //Print return code
    Serial.println(response);           //Print request answer
 
   }
   else
   {
 
    Serial.print("Error on sending POST: ");
    Serial.println(httpResponseCode);
 
   }

   ngat=millis();
   http1.end(); 
  }
 
}
else
 {
    Serial.println("Error in WiFi connection");   
 
 }
}
