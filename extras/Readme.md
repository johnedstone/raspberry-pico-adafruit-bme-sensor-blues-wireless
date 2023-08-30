### Monitor power on/off
* Using the notecarrier/notecard alone without a microcontroller,
e.g. Raspberryp Pi Pico or Adafruit RP2040 Feather,  to monitor power on/off

### Setup for Monitoring USB Power with LiPo Battary attached
```
~ Connected to serial
~ DeviceUID dev:xxxxxx (NOTE-WBNA-500) running firmware 4.4.1.4015700

> {"req": "card.restore", "delete": true}
> > {"req": "hub.set", "product": "your.product.UID", "mode": "periodic"}
{}
> {"req": "hub.sync"}
> {"req": "card.voltage", "usb": true, "alert": true, "sync": true}
{
 "usb": true,
 "alert": true,
 "hours": 15,
 "mode": "usb",
 "value": 5.069422002230467,
 "vmin": 4.92,
 "vmax": 5.07,
 "vavg": 5.06,
 "sync": true
}
```

##### Unsetting the notecard
* Unsetting integers: set to -1
* Unsetting strings: set to "-"

#### JSONata Expression
File: `_health.qo`  
* [JSONata Exerciser](https://try.jsonata.org/)

```
{
  "imei_string": $split(device, ":")[1],"start_time":0,
  "uptime": $fromMillis(when * 1000) & ", file: " & file & ", why: " &
  $lookup(body, "text") & ", " &
    "location(" & best_location_type & "): " &
    $round(best_lat, 8) & "," & $round(best_lon, 8) & ", " &
    "voltage: " & $round("voltage" in $keys(body) ? $lookup(body, "voltage"):0, 2) ,
  "latitude": $string($round(best_lat, 8)),
  "longitude": $string($round(best_lon, 8))
}
```

### Adding Reporting Latitude and Longitude
* Turning on GPS
* Reference: [dev.blues.io Time and Location Requests](https://dev.blues.io/notecard/notecard-walkthrough/time-and-location-requests/#working-with-gps-on-the-notecard)
```
> {"req": "card.location.mode", "mode": "periodic", "seconds": 3600}
{
 "seconds": 3600,
 "mode": "periodic"
}

> {"req": "card.location"}
{
 "status": "GPS inactive {gps-inactive}",
 "mode": "periodic"
}

> {"req": "card.location"}
{
 "status": "GPS inactive {gps-inactive} {gps}",
 "mode": "periodic",
 "lat": 39.88019205,
 "lon": -86.0825915166667,
 "dop": 1.5,
 "time": 1690981627
}
```

### Turning on hourly checkin
_To disable and use tracking (preferred), see the next section_
```
> {"req": "hub.set", "inbound": 60, "mode": "periodic"}
{}
```

#### JSONata Expression
File: `_session.qo`
```
{
  "imei_string": $split(device, ":")[1],"start_time":0,
  "uptime": $fromMillis(when * 1000) & ", " &
    "why: " & $lookup(body, "why") & ", " &
    "location(" & best_location_type & "): " &
    $round(best_lat, 8) & "," & $round(best_lon, 8) & ", " &
    "voltage: " & $round(voltage, 2) ,
  "latitude": $string($round(best_lat, 8)),
  "longitude": $string($round(best_lon, 8))
}
```

### Turning off hourly checks, turn on GPS tracking
* _Note: turn off JSONata expression for `_session.qo` above_
* including [BME280 sensor](https://dev.blues.io/notecard/notecard-walkthrough/advanced-notecard-configuration/#working-with-the-notecard-aux-pins)

```
> {"req": "hub.get"}
{
 "mode": "periodic",
 "host": "a.notefile.net",
 "product": "com.gmail.johnedstone:wbna_500.69623",
 "device": "dev:868050040069623",
 "inbound": 60
}
> {"req": "hub.set", "inbound": -1}
{}
> {"req": "hub.get"}
{
 "mode": "periodic",
 "host": "a.notefile.net",
 "product": "com.gmail.johnedstone:wbna_500.69623",
 "device": "dev:868050040069623"
}
> {"req": "card.location.mode", "mode": "periodic", "seconds": 1800}
{
 "seconds": 1800,
 "mode": "periodic"
}
> {"req": "card.location.track", "start": true, "heartbeat": true, "hours": 1, "sync": true}
{
 "start": true,
 "minutes": 60,
 "heartbeat": true,
 "sync": true
}
> {"req": "card.aux", "mode": "track"}
{
 "mode": "track",
 "temperature": 24.694623746435973,
 "pressure": 99327.93271799856,
 "humidity": 64.3365592121199
}
```

#### JSONata Expression
File: `_track.qo`
```
{
  "imei_string": $split(device, ":")[1],
  "start_time": 0,
  "uptime": $fromMillis(when * 1000) & ", file: " & file &
    ", where_when: " & $fromMillis(where_when * 1000) &
    ", " & "location(" & best_location_type & "): " &
    $round(where_lat, 8) & "," & $round(where_lon, 8) & ", " &
    $round($lookup(body, "temperature"), 1) & "C/" &
    $round("humidity" in $keys(body) ? $lookup(body, "humidity"):0.0, 1) & "%RH, " &
    "voltage: " & $round($lookup(body, "voltage"), 2),
  "latitude": $string($round(where_lat, 8)),
  "longitude": $string($round(where_lon, 8)),
  "temperature": $string($round($lookup(body, "temperature"), 2)),
  "humidity": $string($round("humidity" in $keys(body) ? $lookup(body, "humidity"):0.0, 2))
}
```

### References
* [JSONata Examples](https://blues.io/blog/10-jsonata-examples/)
* [JSONata Docs](https://docs.jsonata.org/overview)
* [JSONata Exerciser](https://try.jsonata.org/)
* [Notecard essential requests](https://dev.blues.io/notecard/notecard-walkthrough/essential-requests/)
* [Monitoring USB connect/disconnect](https://dev.blues.io/api-reference/notecard-api/card-requests/#card-voltage)
* [Earlier example](https://www.hackster.io/rob-lauer/cellular-enabled-power-outage-detector-w-sms-notifications-181408)

<!--
# vim: ai et ts=4 sts=4 sw=4 nu
-->
