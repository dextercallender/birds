Table table;
TableRow row;

float time = 0.0;

String[] dates;
String[] times;
float[] latitudes;
float[] longitudes;

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