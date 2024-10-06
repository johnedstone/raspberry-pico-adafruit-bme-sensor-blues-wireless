### Monitor power on/off
* Using the Notecarrier A and a Notecard alone __without__ a microcontroller,
e.g. Raspberryp Pi Pico or Adafruit RP2040 Feather,  to monitor power on/off

### Purpose of this README
* New version, 2.0 for device UID x69623
* Notecarrier A (firmware: `6.2.5.16868`) and NOTE-WBNA-500 and BME280 sensor (Adafruit) and [0.3 Watt 3.3 Volt Solar Power System](https://voltaicsystems.com/Solar-System-Lithium-Ion-Capacitor)
* Attempting to avoid `insufficient power supply penalty box`. See this [post](https://discuss.blues.com/t/restarted-because-insufficient-battery-current-available-for-power-on-360-min-safety-delay-completed/2349)

### References
* https://dev.blues.io/guides-and-tutorials/notecard-guides/asset-tracking/
* https://dev.blues.io/notecard/notecard-walkthrough/low-power-design/#customizing-voltage-variable-behaviors

### Changes
* 06-Oct-2024: Changed the following. So `low` is now > 3.2 and < 3.6, and `dead` is < 3.2
```
{"req": "card.voltage", "usb": true, "alert": true, "mode": "usb:4.6;high:3.8;normal:3.6;low:3.4;dead:3.2"}
```
to
```
{"req": "card.voltage", "usb": true, "alert": true, "mode": "usb:4.6;high:3.8;normal:3.6;low:3.2;dead:0"}
```
and changed the following so that GPS will work in `low` period
```
{"req": "card.location.mode", "mode": "periodic", "vseconds": "usb:1800;high:1800;normal:1800;low:0;dead:0"}
```
to
```
{"req": "card.location.mode", "mode": "periodic", "vseconds": "usb:1800;high:1800;normal:1800;low:1800;dead:0"}
```
and changed the following so that the device will sync outbound during the `low` period
```
{"req": "hub.set", "mode": "periodic", "voutbound": "usb:60;high:60;normal:60;low:0;dead:0"}
```
to
```
{"req": "hub.set","mode": "periodic", "voutbound": "usb:60;high:60;normal:60;low:60;dead:0"}
```

### Configure
```
{"req": "card.restore", "delete": true}
{"req": "hub.set", "product": "your-productuid", "mode": "periodic", "voutbound": "usb:60;high:60;normal:60;low:0;dead:0", "vinbound": "usb:1440;high:1440;normal:1440;low:0;dead:0"}
{"req": "hub.sync"}
{"req": "card.triangulate", "mode": "-"}
{"req": "card.voltage", "usb": true, "alert": true, "mode": "usb:4.6;high:3.8;normal:3.6;low:3.2;dead:0"}
{"req": "card.location.mode", "mode": "periodic", "vseconds": "usb:1800;high:1800;normal:1800;low:1800;dead:0"}
{"req": "card.location.track", "start": true, "heartbeat": true, "hours": 1}
{"req": "card.aux", "mode": "track"}
```


### [JSONataExpression](https://try.jsonata.org/): `Route: USB on/off _health.qo` 
* Added voltage 01-Oct-2024

```
{
  "imei_string": $split(device, ":")[1],
  "uptime": "body: " &  $substring($replace($string(body), '\"', "'"), 0, 185),
  "latitude": $string($round(best_lat, 8)),
  "longitude": $string($round(best_lon, 8)),
  "best_location_type": best_location_type,
  "best_location_when": $fromMillis(best_location_when * 1000),
  "which_file": file,
  "when_captured_by_device": $fromMillis(when * 1000),
  "received_by_notehub": $fromMillis(received * 1000),
  "voltage": $string("voltage" in $keys(body) ? $lookup(body, "voltage"))
}
```

### JSONataExpression: `Route: GPS Tracking _track.qo v2`
* Added voltage 01-Oct-2024

```
{
  "imei_string": $split(device, ":")[1],
  "uptime": "body: " &  $substring($replace($string(body), '\"', "'"), 0, 185),
  "temperature": $string($round("temperature" in $keys(body) ? $lookup(body, "temperature"), 2)),
  "humidity": $string($round("humidity" in $keys(body) ? $lookup(body, "humidity"), 2)),
  "pressure": $string($round("pressure" in $keys(body) ? $lookup(body, "pressure"), 1)),
  "latitude": $string($round(best_lat, 8)),
  "longitude": $string($round(best_lon, 8)),
  "best_location_type": best_location_type,
  "best_location_when": $fromMillis(best_location_when * 1000),
  "which_file": file,
  "when_captured_by_device": $fromMillis(when * 1000),
  "received_by_notehub": $fromMillis(received * 1000),
  "voltage": $string("voltage" in $keys(body) ? $lookup(body, "voltage"))
}
```

<!--
# vim: ai et ts=4 sts=4 sw=4 nu
-->
