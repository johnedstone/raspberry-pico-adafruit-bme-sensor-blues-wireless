### Using the notecarrier/notecard alone, without a MCU, to monitor power on/off

### Setup for Monitoring USB Powere with LiPo Battary attached
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

### JSONata
* [JSONata Exerciser](https://try.jsonata.org/)
* Unsetting integers: set to -1
* Unsetting strings: set to "-"

Example for routing the `_health.qo` file.
```
{"imei_string": $split(device, ":")[1],"start_time":0, "uptime": $fromMillis(when * 1000) & ", " & $lookup(body, "text")}
```

### Adding Reporting Latitude and Longitude to Power Management
```
> {
  "req": "hub.set",
  "mode": "minimum"
}

> {
  "req": "card.location.mode",
  "mode": "periodic",
  "seconds": 1800
}

> {
  "req": "card.location.track",
  "start": true,
  "heartbeat": true,
  "sync": true,
  "hours": 1
}
```
And adding, the example for routing the `_track.qo` file.  
*Note: it looks like whenver the USB power is changed, _track.qo is fired,
so perhaps following the _health.qo is not necessary if one is following the _track.qo*
```
{"imei_string": $split(device, ":")[1],"start_time":0,
"uptime": $fromMillis(when * 1000) & ", " &
"event: " & $lookup(body, "status") & ", " &
"location_type: " & best_location_type & ", " &
"latitude: " &
$round(best_lat, 8) & ", longitude: " & $round(best_lon, 8),
"latitude": $string($round(best_lat, 8)),
"longitude": $string($round(best_lon, 8))
}
```

#### References
* [JSONata Examples](https://blues.io/blog/10-jsonata-examples/)
* [JSONata Docs](https://docs.jsonata.org/overview)
* [Notecard essential requests](https://dev.blues.io/notecard/notecard-walkthrough/essential-requests/)
* [Monitoring USB connect/disconnect](https://dev.blues.io/api-reference/notecard-api/card-requests/#card-voltage)
* [Earlier example](https://www.hackster.io/rob-lauer/cellular-enabled-power-outage-detector-w-sms-notifications-181408)
