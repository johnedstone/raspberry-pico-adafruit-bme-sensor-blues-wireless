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
* see below 

### Purpose of this README
* Current date 24-Aug-2024
* to document what v1 (and v1.1) really is
* Currently, this version, v1 (and v1.1),
    * When it is not in motion, it report in every hour.  And sends the most recent track.qo 
    to the server and says it's best guess is gps, even if it is a stale gps file
    * When it is in motion it sends the track.qo file every 30 min
    * From below: `hub.set` `inbound` and `outbound` must be set to -1
* Triangulation is off 

### Verification
* This is the verification of the configuration

```
~ DeviceUID dev:x69623 (NOTE-WBNA-500) running firmware 5.1.1.16026

> {"req": "card.voltage"}
{
 "usb": true,
 "alert": true,
 "mode": "usb",
 "value": 4.875814610493385,
 "sync": true
}

> {"req": "card.location.mode"}
{
 "seconds": 1800,
 "mode": "periodic"
 }

> {"req": "hub.get"}
{
 "mode": "periodic",
 "host": "a.notefile.net",
 "product": "com.gmail.johnedstone:wbna_500.69623",
 "device": "dev:x69623"
}
> {"req": "card.location.track"}
{
 "start": true,
 "minutes": 60,
 "heartbeat": true,
 "sync": true
}
> {"req": "card.aux"}
{
 "mode": "track",
 "temperature": 25.46470193152229,
 "pressure": 99324.04928722812,
 "humidity": 57.77226570411907
}

> {"req": "card.triangulate"}
{"motion":1724545743}

```

### 24-Aug-2024 (later)
* upgraded to firmware: `6.2.5.16868`
* Note: lost functionality of {"req": "card.aux", "mode": "track"}
and had to restore notecard to it's original (see below)
* Redid JSONataExpression: `Route: USB on/off _health.qo` 

```
{
  "imei_string": $split(device, ":")[1],
  "uptime": "body: " & $replace($string(body), '\"', "'"),
  "latitude": $string($round(best_lat, 8)),
  "longitude": $string($round(best_lon, 8)),
  "best_location_type": best_location_type,
  "best_location_when": $fromMillis(best_location_when * 1000),
  "which_file": file,
  "when_captured_by_device": $fromMillis(when * 1000),
  "received_by_notehub": $fromMillis(received * 1000)
}
```

* Redid JSONataExpression: `Route: GPS Tracking _track.qo v2`

```
{
  "imei_string": $split(device, ":")[1],
  "uptime": "body: " &  $replace($string(body), '\"', "'"),
  "temperature": $string($round("temperature" in $keys(body) ? $lookup(body, "temperature"), 2)),
  "humidity": $string($round("humidity" in $keys(body) ? $lookup(body, "humidity"), 2)),
  "pressure": $string($round("pressure" in $keys(body) ? $lookup(body, "pressure"), 1)),
  "latitude": $string($round(best_lat, 8)),
  "longitude": $string($round(best_lon, 8)),
  "best_location_type": best_location_type,
  "best_location_when": $fromMillis(best_location_when * 1000),
  "which_file": file,
  "when_captured_by_device": $fromMillis(when * 1000),
  "received_by_notehub": $fromMillis(received * 1000)
}
```

### Resetting Card after firmware upgrade
```
> {"req": "card.restore", "delete": true}
{}

> {"req": "hub.set", "product": "com.gmail.xxxx", "mode": "periodic"}
{}

> {"req": "hub.sync"}
{}

> {"req": "hub.get"}
{"mode":"periodic","host":"a.notefile.net","product":"com.gmail.xxxx","device":"dev:xxxx69623"}

> {"req": "card.voltage", "usb": true, "alert": true, "sync": true}
{"usb":true,"alert":true,"mode":"usb","value":5.076108630173553,"calibration":0.35,"sync":true}

> {"req": "card.location.mode", "mode": "periodic", "seconds": 1800}
{"seconds":1800,"mode":"periodic"}

> {"req": "card.location.track", "start": true, "heartbeat": true, "hours": 1, "sync": true}
{"start":true,"hours":1,"heartbeat":true,"sync":true}

> {"req": "card.aux", "mode": "track"}
{"mode":"track","temperature":27.378273782463896,"pressure":99474.64740809557,"humidity":63.62531812004408}

> {"req": "card.aux"}
{"mode":"track","temperature":27.378273782463896,"pressure":99474.64740809557,"humidity":63.62531812004408}

```

<!--
# vim: ai et ts=4 sts=4 sw=4 nu
-->
