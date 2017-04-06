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
int rowCount;

// Sonification

Minim minim;
AudioOutput out;
Oscil wave;

// Visualization

PImage bg;

void setup(){
  size(1536,768,P3D);
  background(255);
  table = loadTable("ebd_pursan_201101_201601_relFeb-2017.csv","header, csv");
  rowCount = table.getRowCount();
  dates = new String[rowCount];
  times = new String[rowCount];
  latitudes = new float[rowCount];
  longitudes = new float[rowCount];
  
  for(int i=0; i < table.getRowCount(); i++){
    row = table.getRow(i);
    latitudes[i] = row.getFloat("LATITUDE");
    longitudes[i] = row.getFloat("LONGITUDE");
    dates[i] = row.getString("OBSERVATION DATE");
    times[i] = row.getString("TIME OBSERVATIONS STARTED");
  } 
  
  minim = new Minim(this);
  
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
  
  //float x = map(latitudes[ex], 36.0, 37.0, 0.0, float(width));   
  //float y = map(longitudes[ex], -122.0, -121.0, 0.0, float(height));
  float x = ((float(width)/360.0) * (180 + longitudes[ex]));
  float y = ((float(height)/180.0) * (90 - latitudes[ex]));
  
  fill(255,0,0);
  ellipse( x, y, 12, 12);
  
  ex +=1;
  
  wave.setAmplitude(map(x, 0, width, 1, 0) );
  wave.setFrequency(map(y, 0, height, 110, 880) );
}

float dateTimeToFloat(){
  return 0;
}

// calculate the centroid over a set span of time