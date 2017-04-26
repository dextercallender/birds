import ddf.minim.*;
import ddf.minim.analysis.*;
import ddf.minim.effects.*;
import ddf.minim.signals.*;
import ddf.minim.spi.*;
import ddf.minim.ugens.*;

Table table;
TableRow row;

float time = 0.0;

String[] dates;
String[] times;
float[] latitudes;
float[] longitudes;
float[] temps;
int[] observation_size;
int rowCount;

/* for temperature color mapping */
float minTemp;
float maxTemp;
int colMax = 0xffff0000;
int colMed = 0xff00ff00;
int colMin = 0xff0000ff;
int curCol;

PFont f;

// Sonification

Minim minim;
AudioOutput out;
Oscil wave;

// Visualization

PImage bg;

void setup(){
  size(1536,768,P3D);
  background(255);
  table = loadTable("final4.csv","header, csv");
  rowCount = table.getRowCount();
  dates = new String[rowCount];
  times = new String[rowCount];
  latitudes = new float[rowCount];
  longitudes = new float[rowCount];
  temps = new float[rowCount];
  observation_size = new int[rowCount];
  
  f = createFont("Arial", 16, true);
  
  for(int i=0; i < table.getRowCount(); i++){
    row = table.getRow(i);
    latitudes[i] = row.getFloat("LATITUDE");
    longitudes[i] = row.getFloat("LONGITUDE");
    dates[i] = row.getString("OBSERVATION_DATETIME");
    times[i] = row.getString("time_deltas");
    temps[i] = row.getFloat("temperature");
    observation_size[i] = row.getInt("OBSERVATION COUNT");
  } 
  
  minim = new Minim(this);
  
  minTemp = min(temps);
  maxTemp = max(temps);
  
  // use the getLineOut method of the Minim object to get an AudioOutput object
  out = minim.getLineOut();
 
  // create a sine wave Oscil, set to 440 Hz, at 0.5 amplitude
  wave = new Oscil( 440, 0.5f, Waves.SINE );
  
  // patch the Oscil to the output
  wave.patch( out );
  
  bg = loadImage("world-map.jpg");
  
}

int ex = 0;

void draw(){
  background(bg);
  time += 0.5;
  
  if( ex == rowCount -1 ){
    exit();
  }
  
  textFont(f, 16);
  
  //float x = map(latitudes[ex], 36.0, 37.0, 0.0, float(width));   
  //float y = map(longitudes[ex], -122.0, -121.0, 0.0, float(height));
  float x = ((float(width)/360.0) * (180 + longitudes[ex]));
  float y = ((float(height)/180.0) * (90 - latitudes[ex]));
  int size = Math.max(observation_size[ex], 10);
  
  // temperature mapping for dot color
  float mappedTemp = map(temps[ex], minTemp, maxTemp, 0, 1);
  if (mappedTemp == 0) {
    curCol = 0xff808080;      // grey
  } else if (mappedTemp < 0.5) {
    curCol = lerpColor(colMin, colMed, 2*mappedTemp);      // blue to green
  } else {
    curCol = lerpColor(colMed, colMax, 2*(mappedTemp-0.5));      // green to red
  }
  fill(curCol);
  ellipse( x, y, size, size);


  fill(255, 0,0);
  text(dates[ex], 25, 25);
  
  ex +=1;
  
  wave.setAmplitude(map(x, 0, width, 1, 0) );
  wave.setFrequency(map(y, 0, height, 110, 880) );
}

float dateTimeToFloat(){
  return 0;
}

// calculate the centroid over a set span of time