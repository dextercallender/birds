import ddf.minim.*;
import ddf.minim.analysis.*;
import ddf.minim.effects.*;
import ddf.minim.signals.*;
import ddf.minim.spi.*;
import ddf.minim.ugens.*;

Table table;
Table city_temps;
TableRow row;

float time = 0.0;

String[] dates;
float[] latitudes;
float[] longitudes;
float[] temperatures;
int rowCount;
int tempCount;

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
int dayIterator;
int traceLength;
float[] prevLatitudes;
float[] prevLongitudes;
color[] prevTemperatures;
String[] polygons;
float[] city_xs;
float[] city_ys;

float[][] city_temperatures;

/* projecting coordinates into the XY space */
float getX(int w, float lon) {
  float res = ((float(w)/360.0) * (180 + lon));
  println("getX: " + str(res));
  return res;
}
float getY(int h, float lat) {
  return ((float(h)/180.0) * (90 - lat));
}

void setup() {
  size(1536, 769, P3D);
  background(255);
  table = loadTable("purplesandpiper.csv", "header, csv");
  city_temps = loadTable("city_temps.csv", "header, csv");
  
  rowCount = table.getRowCount();
  tempCount = city_temps.getRowCount();
  dates = new String[rowCount];
  latitudes = new float[rowCount];
  longitudes = new float[rowCount];
  temperatures = new float[rowCount];
  traceLength = 10;
  prevLatitudes = new float[traceLength];
  prevLongitudes = new float[traceLength];
  prevTemperatures = new color[traceLength];
  polygons = new String[rowCount];
  
  city_temperatures = new float[8][tempCount];
  
  //these are hard coded indices
  //vancouver, anchorage, nyc, albuquerque, mex_city, brasilia, buenos_aires, cape_horn
  city_xs = new float[8];
  city_ys = new float[8];
  float[] city_lats = {49.28, 61.21, 40.7, 35.08, 19.43, -15.79, -34.6, -54.93};
  float[] city_lons = {-123.12, -149.9, -74.0, -106.6, -99.13, -47.88, -58.38, -67.61};
  
  for (int i=0; i < 8; i++) {
    city_ys[i] = getY(height, city_lats[i]);
    city_xs[i] = getX(width, city_lons[i]);
  }
  
  // this is fucking terrible
  for(int j=0; j < tempCount; j++) {
    row = city_temps.getRow(j);
    city_temperatures[0][j] = row.getFloat("vancouver");
    city_temperatures[1][j] = row.getFloat("anchorage");
    city_temperatures[2][j] = row.getFloat("nyc");
    city_temperatures[3][j] = row.getFloat("albuquerque");
    city_temperatures[4][j] = row.getFloat("mexico_city");
    city_temperatures[5][j] = row.getFloat("brasilia");
    city_temperatures[6][j] = row.getFloat("buenos_aires");
    city_temperatures[7][j] = row.getFloat("cape_horn");
  }
  

  for (int i=0; i < table.getRowCount(); i++) {
    row = table.getRow(i);
    dates[i] = row.getString("OBSERVATION_DATE");
    latitudes[i] = row.getFloat("AVG LAT");
    longitudes[i] = row.getFloat("AVG LON");
    temperatures[i] = row.getFloat("TEMPERATURE");
    polygons[i] = row.getString("VERTICES");
  } 

  minim = new Minim(this);
  // use the getLineOut method of the Minim object to get an AudioOutput object
  out = minim.getLineOut();
  // create a sine wave Oscil, set to 440 Hz, at 0.5 amplitude
  wave = new Oscil( 440, 0.5f, Waves.SINE );
  // patch the Oscil to the output
  //wave.patch( out );

  bg = loadImage("darkmap.jpg");
  dayIterator = 0;
  frameRate(8);
}

color temp_to_color(float temp) {
  return lerpColor( color(155, 222, 232), color(255, 102, 26), temp);
}

void draw() {
  background(bg);
  //background(0);
  stroke(255);
  strokeWeight(2);
  line(0,height/2,width,height/2);
  float amt = (temperatures[dayIterator]-266.09) / (306.85-266.09); // (current_temp - min_temp) / (max_temp - min_temp) 
  color tempColor = lerpColor( color(155, 222, 232), color(255, 102, 26), amt);

  if ( dayIterator == rowCount-1 ) {
    exit();
  }

  float x = ((float(width)/360.0) * (180 + longitudes[dayIterator]));
  float y = ((float(height)/180.0) * (90 - latitudes[dayIterator]));

  // centroid
  stroke(0);
  fill(255, 0, 0);
  ellipse( x, y, 15, 15);
  
  // polygon
  fill(tempColor);
  String verticesString = polygons[dayIterator];
  float[] vertices = parseVerticesString(verticesString);
  
  fill(255,0,0);
  beginShape();
  for(int i=0;i<vertices.length;i+=2){
    vertex(((float(width)/360.0) * (180 + vertices[i+1])), ((float(height)/180.0) * (90 - vertices[i])));
  }
  endShape(CLOSE);

  //temperature
  noStroke();
  fill(tempColor);
  ellipse(x, y, 50, 50);

  // sonification
  wave.setAmplitude(map(x,0, width,1,0));
  wave.setFrequency(map(y,0, height,110,880));

  // textual information
  fill(255);
  textSize(20);
  text(dates[dayIterator], 40, height-70);
  
  //draw on these cities
  //VANCOUVER
  textSize(14);
  fill(temp_to_color(city_temperatures[0][dayIterator]));
  text("VANCOUVER", city_xs[0], city_ys[0]);
  //ANCHORAGE
  fill(temp_to_color(city_temperatures[1][dayIterator]));
  text("ANCHORAGE", city_xs[1], city_ys[1]);
  fill(temp_to_color(city_temperatures[2][dayIterator]));
  text("NYC", city_xs[2], city_ys[2]);
  
  fill(temp_to_color(city_temperatures[3][dayIterator]));
  text("ALBUQUERUQE", city_xs[3], city_ys[3]);
  fill(temp_to_color(city_temperatures[4][dayIterator]));
  text("MEXICO CITY", city_xs[4], city_ys[4]);
  fill(temp_to_color(city_temperatures[5][dayIterator]));
  text("BRASILIA", city_xs[5], city_ys[5]);
  fill(temp_to_color(city_temperatures[6][dayIterator]));
  text("BUENOS AIRES", city_xs[6], city_ys[6]);
  fill(temp_to_color(city_temperatures[7][dayIterator]));
  text("CAPE HORN", city_xs[7], city_ys[7]);

  // past traces
  if ( dayIterator > traceLength ) {
    for (int i=0;i<traceLength;i++) {
      prevLatitudes[i] = ((float(width)/360.0) * (180 + longitudes[dayIterator - i-1]));
      prevLongitudes[i] = ((float(height)/180.0) * (90 - latitudes[dayIterator - i-1]));
      amt = (temperatures[dayIterator-i-1]-266.09) / (306.85-266.09);
      prevTemperatures[i] = lerpColor(color(155, 222, 232), color(255, 102, 26), amt);
    }
    for (int i=0; i<traceLength; i++) {
      
      //trace
      fill( 255, 255 -(i*20));
      stroke( 255, 255 -(i*20));
      ellipse(prevLatitudes[i], prevLongitudes[i], 12-i*2, 12-i*2);
      
      //temperature
      fill(prevTemperatures[i]);
      noStroke();
      ellipse(prevLatitudes[i], prevLongitudes[i], 30-i*2, 30-i*2);
      
      if ( i < traceLength - 1 ) {
        stroke(255);
        strokeWeight(2);
        line(prevLatitudes[i], prevLongitudes[i], prevLatitudes[i+1], prevLongitudes[i+1]);
      }
      
    }
  }
  dayIterator +=1;
}

float[] parseVerticesString(String vertexString){
  /* returns an array of consecutive latitude and longtidue values */
  String[] vertices = split(vertexString,"&");
  float[] result = new float[vertices.length * 2];
  for(int i=0;i<vertices.length;i++){
    String[] values = split(vertices[i],"*");
    result[i*2] = float(values[0]);
    result[(i*2)+1] = float(values[1]);
  }
  return result;
}

// max & min temps
// white_rumped_sandpiper_pr_temps_nodup_clusteredfinal     ( 266.09, 306.85 )