# birds
Visualization &amp; Sonification of Bird Migration Data

Google Drive containing eBird data: https://drive.google.com/open?id=0B3WVhhpJA_yHOUpGWFZtdHVKODQ

`<bird-name>_pr.csv` column names:

 | date_time | COMMON NAME | OBSERVATION COUNT | LATITUDE | LONGITUDE | OBSERVATION DATE | time_deltas |
 | --------- | ------------| ----------------- | -------- | --------- | ---------------- | ----------- |
 |2011-01-02 09:00:00 | American Golden-Plover | 10 | -34.6841667 | -54.2768333 | 2011-01-02 | 118800 |
 
 *time_deltas is measured as seconds that have elapsed since 2011-01-01 00:00:00*


Vertex format:
151.2*-90.3*4&89.32*78.99*5&34.45*52.34*19

Individual sightings are separated by '&' so do `csv_file['VERTICES'][i].split('&')` or something to get list of sightings.
Each sighting is in format 46.43*23.43*8. Separated by '*'. First two things are latitude, then longitude, then observation count.

so `sighting_string.split('*')[0]` = latitude, `sighting_string.split('*')[1]` = longitude, `sighting_string.split('*')[2]` = # birds seen.
