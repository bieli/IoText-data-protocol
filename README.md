# IoText-data-protocol
Internet of Things data protocol - simplistic text and CSV-friendly IoT data protocol. Options: Schema-less, schema+versioning, building deltas for data values. Easy to re-use.

## Motivations
We can see a lot off complex protocols in IoT and IIoT world. Sometimes it's like overengineering for IoT hobby solutions.
This is text protocol with simple syntax, readable and self-explanaible rules.

## Rules
We have a few base facts about this new `IoText` data protocol:

1. This is `IoText data protocol`, not network or binary encrypted protocol, so we not expected super performance at start point.
2. We can use this `IoText data protocol` for every your solutions, when you need sending data from devices, e.g. Edge Devices to the cloud.
3. This `Text data protocol` we can encapsulate on top of other more perfect IoT protocols like MQTT, AMQP, and NATS.
4. We'he already documented and implemented all required classes and builders in Python programming language for you.
5. You can encode and decode messages with measurements - this is protocol dedicated for time-series near real-time data collecting (monitoring, IoT devices measurements, sharing physical sonds and sensors values from IIoT systems, industrial observability and much more).
6. It's still in development, so if you enjoy IoT things, you can put PR with updates/features.
7. This is already stable and tested data protocol on home automation (~70 measurements per second in LAN/WAN network).
8. This protocol have power to send one data row with 4096 metrics and one timestamp (UNIX time with miliseconds) + device name. All string values have no limits in length, but memory/RAM consumption is important in Edge Device and CPU time, too.

## Documentation
We have simple concept like CSV, comma separated data items.
One row have all metrics with one:
- timestamp (UNIX time with miliseconds, because it's universal, without timezones and other additional stuff)
- device_name (no limit in size - of course RAM/CPU have hard limits in devices!)

### Special chars (unexpected in device name and metrics names!)
 - `,` - comma separation of data items and metrics
 - `:` - data types and values separator
 - `|` - command types and command context separator
 - `=` - split data item char


### Message patterns

We have a few types of items possible inside message:
- <item_type>|<item_context> - e.g. t|3900237526042,d|device_name
- <item_type>|<metric_name>=<metric_type>:<metric_value> - e.g. m|current_battery=d:1.548


You can see reference implementation of item types in `ItemTypes` class  in `src/types` package. 

#### Exmaple message in IoT data protocol with one metric
```bash
t|3900237526042,d|device_name_001,m|val_water_level1=i:42
```
We can see informations like:
- data timestamp -> "3900237526042"
- device name -> "device_name_001"
- one metric named -> "val_water_level1" with -> "integer" value -> "42"

As you imagine, it's simple as possible ;-)

### Generic types

#### Item types
We have a few basic item types:
- `t` - timestamp UNIX milis item
- `d` - device name item
- `m` - metric item
- `h` - helth check

You can see reference implementation in `ItemTypes` class  in `src/types` package. 

#### Metric data types
We have a few basic data types:
- `i` - integer
- `d` - decimal (not float!)
- `b` - boolean
- `t` - text

You can see reference implementation in `MetricDataTypes` class  in `src/types` package.

### Codecs
We have a few basic data codecs:
- `MetricDataItemCodec` - decode/encode methods for full coding proces for data row
- `ItemCodec` - decode/encode methods for data row item
- `IoTextCodec` - decode/encode methods for data row items with Python data structures full support (you can use linters and debugging with no risks)

You can see reference implementation in `src/codecs` package.

### Examples
IoText protocol in `schema-less version` data row example:
```bash
t|3900237526042,d|device_name_001,m|val_water_001=i:1234,m|val_water_002=i:15,m|bulb_state=b:1,m|connector_state=b:0,m|temp_01=d:34.4,m|temp_02=d:36.4,m|temp_03=d:10.4,m|pwr=d:12.231,m|current=d:1.429,m|current_battery=d:1.548
```

#### Preparing message
You need two required informations:
- timestamp in UNIX milis
- device name
- all data metrics are optional, so it means, that you can use IoText protocol like ping - or health check - as well (we have dedicated `h` item type for helth check, too).


## TODO
 - [ ] - add validator for special chars
 - [ ] - add unit tests
 - [ ] - add fuzzing tests
 - [ ] - add limits/max. sizes for device name and metrics names
 - [ ] - add CRC16 from MODBUS protocol for serial communication checksum and any terminals usage
 - [ ] - add schema versioning, no need to repeat metrics names in all message (one schema in particular version can solve names by indexes in data protocol). More optimal version of protocol.
 - [ ] - add definition and examples of delta data sending (it's possibe in schema-less version as well, but maybe it will be good to have implementaion for that required in IoT systems typical optimisation scenario)
 - [ ] - examples, how encapsulate `IoText data protocol` on top od `MQTT IoT protocol`
