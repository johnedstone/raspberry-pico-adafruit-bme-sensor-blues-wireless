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
Note: setting the heartbeat to 1 hour, and the periodic to 1800 (30 min) seems to give a consistent 1 hour heartbeat.
As opposed to setting the heartbeat to 12 hours, and the periodic to 1800, which then seemed to skip the heartbeat.  This was,
perhaps, due to the occassional unexplained periodic reporting, in which case the heartbeat didn't report in at the 12 hour mark.
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

### Another example without using `heartbeat`
See this link, [https://discuss.blues.io/t/any-reason-not-to-use-card-location-track-just-to-get-heartbeat/1006/8](https://discuss.blues.io/t/any-reason-not-to-use-card-location-track-just-to-get-heartbeat/1006/8)
for this idea:
> You can do that, but if you don’t need the GPS/GNSS location you can achieve the same thing by using {"req":"hub.set","inbound":mins}, where min is how often you want the Notecard to check in with Notehub. When the sync occurs you’ll see a `_session.qo` event come through in Notehub.

_Note: put code here for this example, turning off GPS_

### References
* [JSONata Examples](https://blues.io/blog/10-jsonata-examples/)
* [JSONata Docs](https://docs.jsonata.org/overview)
* [Notecard essential requests](https://dev.blues.io/notecard/notecard-walkthrough/essential-requests/)
* [Monitoring USB connect/disconnect](https://dev.blues.io/api-reference/notecard-api/card-requests/#card-voltage)
* [Earlier example](https://www.hackster.io/rob-lauer/cellular-enabled-power-outage-detector-w-sms-notifications-181408)
