#include <SoftwareSerial.h>
#include <MP3Player_KT403A.h>

SoftwareSerial mp3(14,15);

//릴레이1번 힌트실, 복도EM, UV, 창문T5
int ledWhite1 = 51;
int ledWhite2 = 49;
int ledRed = 47;
int ledWindow = 4;
int ledUV = 5;

//릴레이2번 칠판3개, 딱
int emBbik = 53;
int emDdak = 29;

//릴레이3번 삑 흰등2개 빨간불
int emBokdo = 6;
int ledHint = 7;

//마그네틱센서
int mag1 = 8;
int mag11 = 9;
int mag12 = 10;
int mag2 = 11;
int mag3 = 16;
int mag4 = 17;

//체크용 변수
bool pass1 = true;
bool pass2 = true;
bool pass3 = true;
bool pass4 = true;
bool pass5 = true;

void setup() 
{

pinMode(mag1, INPUT_PULLUP);    // 책, 파레트, 옷 센서
pinMode(mag11, INPUT_PULLUP);
pinMode(mag12, INPUT_PULLUP);

pinMode(mag3, INPUT_PULLUP);    // 지우개 센서 
pinMode(mag4, INPUT_PULLUP);    // 구두 센서

pinMode(mag2, INPUT_PULLUP);    // 투표 센서 입력

pinMode(ledWhite1, OUTPUT);
pinMode(ledWhite2, OUTPUT);
pinMode(ledRed, OUTPUT);
pinMode(ledHint, OUTPUT);
pinMode(ledWindow, OUTPUT);
pinMode(ledUV, OUTPUT);


digitalWrite(ledWhite1, LOW);
digitalWrite(ledWhite2, LOW);
digitalWrite(ledRed, HIGH);
digitalWrite(ledHint, HIGH);
digitalWrite(ledWindow, HIGH);
digitalWrite(ledUV, HIGH);


pinMode(emBbik, OUTPUT);
pinMode(emBokdo, OUTPUT);
pinMode(emDdak, OUTPUT);
digitalWrite(emBbik, LOW);
digitalWrite(emBokdo, LOW);
digitalWrite(emDdak, LOW);


delay(1500);



mp3.begin(9600);
Serial.begin(9600);


Serial.println("mp3 device setting");
SelectPlayerDevice(0x02);
SetVolume(0x19);

//mp3 first song playing
SpecifyMusicPlay(0, 1);
Serial.println("start");
}





void loop() {
  // put your main code here, to run repeatedly:


int a = digitalRead(mag1); int a1 = digitalRead(mag11); int a2 = digitalRead(mag12);
Serial.print("책, 파레트, 옷 센서 입력 : ");
Serial.print(a); Serial.print(a1); Serial.println(a2);

int b = digitalRead(mag3);
Serial.print("지우개 센서 입력 : ");
Serial.println(b);

int c = digitalRead(mag4);
Serial.print("구두 센서 입력 : ");
Serial.println(c);

int d = digitalRead(A7);
Serial.print("카세트 센서 전압 : ");
Serial.println(d);

int e = digitalRead(mag2);
Serial.print("투표 센서 입력 : ");
Serial.println(e);
delay(1000);

if (a && a1 && a2 && pass1)
{
  pass1 = 0;
  FirstCode();
}

if (!b && !pass1 && pass2)
{
  pass2 = 0;
  SecondCode();
  }

if (!c && !pass1 && !pass2 && pass3)
{
  pass3 = 0;
  ThirdCode();
}

if (d && !pass1 && !pass2 && !pass3 && pass4)
{
  pass4 = 0;
  FourthCode();
}
if (e && !pass1 && !pass2 && !pass3 && !pass4 && pass5)
{
  pass5 = 0;
  FifthCode();
  delay(300000);
}
}

  

void FirstCode()
{
  Serial.println("First Action");
  PlayNext();
  blinkLED(ledWhite1, ledWhite2);

  //웃는소리
  PlayNext();
  //SpecifyMusicPlay(0, 0x02);
  delay(25000);
  digitalWrite(ledRed, LOW);
  //삑
  digitalWrite(emBbik, HIGH);

  //BGM
  PlayNext();
  
  //SpecifyMusicPlay(0, 0x03);
}

void SecondCode()
{
  Serial.println("Second Action");

  digitalWrite(ledRed, HIGH);
  delay(1000);
  
  PlayNext();
  delay(17000);

  digitalWrite(ledWindow, LOW);
  delay(100);
  
  digitalWrite(ledWindow, HIGH);
  delay(100);
  
  digitalWrite(ledWindow, LOW);
  delay(100);
  
  digitalWrite(ledWindow, HIGH);
  delay(1000);

    digitalWrite(ledWindow, LOW);
  delay(100);
  
  digitalWrite(ledWindow, HIGH);
  delay(100);
    digitalWrite(ledWindow, LOW);
  delay(100);
  
  digitalWrite(ledWindow, HIGH);
  delay(2000);  
    
  digitalWrite(ledWindow, LOW);

 PlayNext();

}

void ThirdCode()
{
  Serial.println("Third Action");
  digitalWrite(ledWindow, HIGH);
  
  PlayNext();
  delay(33000);

  digitalWrite(emBokdo, HIGH);
  delay(2000);

  PlayNext();
}

void FourthCode()
{
  Serial.println("쉐이킹");
  digitalWrite(ledRed, LOW);
  delay(300);
  digitalWrite(ledRed, HIGH);
  delay(300);
    digitalWrite(ledRed, LOW);
  delay(300);
  digitalWrite(ledRed, HIGH);
  delay(300);
    digitalWrite(ledRed, LOW);
  delay(300);
  digitalWrite(ledRed, HIGH);
  delay(300);
    digitalWrite(ledRed, LOW);
  delay(300);
  digitalWrite(ledRed, HIGH);
  delay(300);
    digitalWrite(ledRed, LOW);
  delay(300);
  digitalWrite(ledRed, HIGH);
  delay(300);
    digitalWrite(ledRed, LOW);
  delay(300);
  digitalWrite(ledRed, HIGH);
  delay(300);
    digitalWrite(ledRed, LOW);
  delay(300);
  digitalWrite(ledRed, HIGH);
  delay(300);
    digitalWrite(ledRed, LOW);
 
  PlayNext();

  delay(25000);

  digitalWrite(emDdak, HIGH);
  
  
  delay(3000);

  PlayNext();
}

void FifthCode()
{
  digitalWrite(ledRed, HIGH);
  Serial.println("UV & 힌트실 연락");
  delay(5000);
  PlayNext();
  digitalWrite(ledUV, LOW);
  
  delay(3000);
  
  digitalWrite(ledHint, LOW);
}


void blinkLED(int led1, int led2)
{
  Serial.println("Blink");
  digitalWrite(led1, HIGH);
  digitalWrite(led2, HIGH);
  delay(200);
  digitalWrite(led1, LOW);
  digitalWrite(led2, LOW);
  delay(2000);
  digitalWrite(led1, HIGH);
  delay(1500);
  digitalWrite(led1, LOW);
  digitalWrite(led2, LOW);
  delay(3000);
  digitalWrite(led2, HIGH);
  digitalWrite(led1, HIGH);
  delay(200);
  digitalWrite(led2, LOW);
  delay(200);
  digitalWrite(led2, HIGH);
  delay(200);
  digitalWrite(led2, LOW);
  delay(200);
  digitalWrite(led1, LOW);
  digitalWrite(led2, HIGH);
  delay(200);
  digitalWrite(led2, LOW);
  delay(200);
  digitalWrite(led2, HIGH);
  delay(200);
  digitalWrite(led1, HIGH);
  digitalWrite(led2, LOW);
  delay(200);
  digitalWrite(led2, HIGH);
  delay(1000);
  digitalWrite(led1, LOW);
  delay(800);
  digitalWrite(led2, LOW);
  delay(200);
    digitalWrite(led1, LOW);
  digitalWrite(led2, HIGH);
  delay(200);
  digitalWrite(led2, LOW);
  delay(200);
  digitalWrite(led2, HIGH);
  delay(200);
  digitalWrite(led1, HIGH);
  digitalWrite(led2, LOW);
  delay(200);
  digitalWrite(led2, HIGH);
  delay(1000);
  digitalWrite(led1, LOW);
  delay(800);
  digitalWrite(led2, LOW);
  delay(200);
  
  digitalWrite(led1, HIGH);
  digitalWrite(led2, HIGH);
  delay(5000);
  digitalWrite(ledRed, LOW);
}
