#### JSON config for devices with just Notecard and Notecarrier (and BME280)
* x69623 reports gps for best location
* x71767 does not reports gps for best location, as there is no heartbeat.  That is, 
with a heartbeat, if the device is not moved, but there is a gps file, then it
"knows" it's a gps "best location".  See x69623 v2 Readme.md
