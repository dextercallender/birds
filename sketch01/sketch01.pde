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

Minim minim;
AudioOutput out;
Oscil wave;

void setup(){
  size(1920,1080,P3D);
  background(255);
  table = loadTable("bird_sampleset.csv","header, csv");
  int rowCount = table.getRowCount();
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
  
}

int ex = 0;

void draw(){
  background(frameCount % 255);
  time += 0.5;
  
  float x = map(latitudes[ex], 36.0, 37.0, 0.0, float(width));   
  float y = map(longitudes[ex], -122.0, -121.0, 0.0, float(height));
  ellipse( x, y, 20, 20);
  
  ex +=1;
  
}

float dateTimeToFloat(){
  return 0;
}



// calculate the centroid over a set span of time