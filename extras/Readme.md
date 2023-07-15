### Using the notecarrier/notecard alone, without a MCU, to monitor power on/off
### Setup
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

Example of a REST API, routing `_health.qo`
```
{"imei_string": $split(device, ":")[1],"start_time":0, "uptime": $fromMillis(when * 1000) & ": " & $lookup(body, "text")}
```

#### References
* [Notecard essential requests](https://dev.blues.io/notecard/notecard-walkthrough/essential-requests/)
* [Monitoring USB connect/disconnect](https://dev.blues.io/api-reference/notecard-api/card-requests/#card-voltage)
* [Earlier example](https://www.hackster.io/rob-lauer/cellular-enabled-power-outage-detector-w-sms-notifications-181408)
