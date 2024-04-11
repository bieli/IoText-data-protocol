[![codecov](https://codecov.io/gh/bieli/IoText-data-protocol/branch/main/graph/badge.svg?token=L8FFQNPQXI)](https://codecov.io/gh/bieli/IoText-data-protocol)


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
- `h` - health check
- `c` - CRC-16 (from MODBUS control sum) for all combined IoText payload as string

You can see reference implementation in `ItemTypes` class  in `src/types` package. 

#### Metric data types
We have a few basic data types:
- `i` - integer
- `d` - decimal (not float!)
- `b` - boolean
- `t` - text
- `I` - list of integers
- `D` - list of decimals (not float!)
- `B` - list of booleans
- `T` - list of texts (base64 encoded with UTF-8, removed and auto-restored padding at the end - conflict with "=" protocol separator)

You can see reference implementation in `MetricDataTypes` class  in `src/types` package.

### Codecs
We have a few basic data codecs:
- `MetricDataItemCodec` - decode/encode methods for full coding proces for data row
- `ItemCodec` - decode/encode methods for data row item
- `IoTextCodec` - decode/encode methods for data row items with Python data structures full support (you can use linters and debugging with no risks)

You can see reference implementation in `src/codecs` package.

### How to prepare IoText message
You need two required informations:
- timestamp in UNIX millis
- device name
- all data metrics are optional, so it means, that you can use IoText protocol like ping - or health check - as well (we have dedicated `h` item type for helth check, too).
- CRC item it's optional sum control method (using CRC-16 MODBUS implementation)

### Examples

#### IoText message with generic values

IoText protocol in `schema-less version` data row example:
```bash
t|3900237526042,d|device_name_001,m|val_water_001=i:1234,m|val_water_002=i:15,m|bulb_state=b:1,m|connector_state=b:0,m|temp_01=d:34.4,m|temp_02=d:36.4,m|temp_03=d:10.4,m|pwr=d:12.231,m|current=d:1.429,m|current_battery=d:1.548
```
and after de-serialization to Python data structures we can see:
```bash
[
  Item(kind='t', name='3900237526042', metric=None),
  Item(kind='d', name='device_name_001', metric=None),
  Item(kind='m', name='val_water_001', metric=MetricDataItem(data_type='i', value=1234)),
  Item(kind='m', name='val_water_002', metric=MetricDataItem(data_type='i', value=15)),
  Item(kind='m', name='bulb_state', metric=MetricDataItem(data_type='b', value=True)),
  Item(kind='m', name='connector_state', metric=MetricDataItem(data_type='b', value=False)),
  Item(kind='m', name='temp_01', metric=MetricDataItem(data_type='d', value=Decimal('34.4'))),
  Item(kind='m', name='temp_02', metric=MetricDataItem(data_type='d', value=Decimal('36.4'))),
  Item(kind='m', name='temp_03', metric=MetricDataItem(data_type='d', value=Decimal('10.4'))),
  Item(kind='m', name='pwr', metric=MetricDataItem(data_type='d', value=Decimal('12.231'))),
  Item(kind='m', name='current', metric=MetricDataItem(data_type='d', value=Decimal('1.429'))),
  Item(kind='m', name='current_battery', metric=MetricDataItem(data_type='d', value=Decimal('1.548')))]
```

#### IoText message with lists of values

IoText protocol in `schema-less version` data row example with lists values:
```bash
t|3900237526142,d|device_name_002,m|ints_list=I:+1-22+333333,m|bools_list=B:0111,m|decimals_list=D:-123.456+1234567890.98765+999.8,m|texts_list=T:Wyd8JywgJzphYmMnLCAnISFAJywgJ3h5MHonLCAnMWFiYywnXQ
```
and after de-serialization to Python data structures with lists values we can see:
```bash
[
    Item(kind=ItemTypes.TIMESTAMP_MILIS, name="3900237526142", metric=None),
    Item(kind=ItemTypes.DEVICE_ID, name="device_name_002", metric=None),
    Item(
        kind=ItemTypes.METRIC_ITEM,
        name="ints_list",
        metric=MetricDataItem(data_type=MetricDataTypes.INTEGERS_LIST, value=[1, -22, 333333]),
    ),
    Item(
        kind=ItemTypes.METRIC_ITEM,
        name="bools_list",
        metric=MetricDataItem(data_type=MetricDataTypes.BOOLS_LIST, value=[False, True, True, True]),
    ),
    Item(
        kind=ItemTypes.METRIC_ITEM,
        name="decimals_list",
        metric=MetricDataItem(data_type=MetricDataTypes.DECIMALS_LIST, value=[-123.456, 1234567890.98765, 999.8]),
    ),
    Item(
        kind=ItemTypes.METRIC_ITEM,
        name="texts_list",
        metric=MetricDataItem(data_type=MetricDataTypes.TEXTS_LIST, value=['|', ':abc', '!!@', 'xy0z', '1abc,']),
    ),
]
```

#### IoText message with CRC16 sum control item

IoText protocol in `schema-less version` data row example:
```bash
t|123123123123,d|device_one,m|value=d:123.321,c|4C5A
```
and after de-serialization to Python data structures we can see:
```bash
[
    Item(kind=ItemTypes.TIMESTAMP_MILIS, name="123123123123", metric=None),
    Item(kind=ItemTypes.DEVICE_ID, name="device_one", metric=None),
    Item(
        kind=ItemTypes.METRIC_ITEM,
        name="value",
        metric=MetricDataItem(data_type=MetricDataTypes.DECIMAL, value=Decimal('123.321')),
    ),
    Item(
        kind=ItemTypes.CRC,
        name="4C5A",
        metric=None
    )
]
```

#### IoText message to/from JSON format (for backward compatibility with other APIs and subsystems)

You can use below methods from IoText Python API:
- `iotext_data_struct = IoTextItemDataBuilder.from_json(iotext_msg_as_json)`
- `builder = IoTextItemDataBuilder(...)`
  - `builder.add_measure(...)`
  - `builder.to_json()`

IoText message as JSON row example:
```bash
[{"t": "3900237526042"}, {"d": "DEV_NAME_002"}, {"m": "battery_level", "v": 12.07, "t": "d"}, {"m": "open_door", "v": "1", "t": "b"}, {"m": "open_window", "v": "0", "t": "b"}, {"m": "counter_01", "v": 1234, "t": "i"}, {"m": "ints_list", "v": "-12+13-14", "t": "I"}, {"c": "9838"}]
```
and after de-serialization from JSON format to IoText's Python data structure:
```bash
[
            Item(kind=ItemTypes.TIMESTAMP_MILIS, name="3900237526042", metric=None),
            Item(kind=ItemTypes.DEVICE_ID, name="DEV_NAME_002", metric=None),
            Item(
                kind=ItemTypes.METRIC_ITEM,
                name="battery_level",
                metric=MetricDataItem(
                    data_type=MetricDataTypes.DECIMAL,
                    value=Decimal("12.07"),
                ),
            ),
            Item(
                kind=ItemTypes.METRIC_ITEM,
                name="open_door",
                metric=MetricDataItem(data_type=MetricDataTypes.BOOL, value=True),
            ),
            Item(
                kind=ItemTypes.METRIC_ITEM,
                name="open_window",
                metric=MetricDataItem(data_type=MetricDataTypes.BOOL, value=False),
            ),
            Item(
                kind=ItemTypes.METRIC_ITEM,
                name="counter_01",
                metric=MetricDataItem(data_type=MetricDataTypes.INTEGER, value=1234),
            ),
            Item(
                kind=ItemTypes.METRIC_ITEM,
                name="ints_list",
                metric=MetricDataItem(
                    data_type=MetricDataTypes.INTEGERS_LIST,
                    value=[-12, 13, -14],
                ),
            ),
            Item(
                kind=ItemTypes.CRC,
                name="9838",
                metric=None,
            ),
        ]
```


## How to use this library?

### Use class IoTextCodec for decode and encode data messages 
```python

from src.codecs.iot_ext_codec import IoTextCodec

MSG_1_EXAMPLE = '''t|3900237526042,d|device_name_001,m|val_water_001=i:1234,m|val_water_002=i:15,m|bulb_state=b:1,m|connector_state=b:0,m|temp_01=d:34.4,m|temp_02=d:36.4,m|temp_03=d:10.4,m|pwr=d:12.231,m|current=d:1.429,m|current_battery=d:1.548'''

item = IoTextCodec.decode(MSG_1_EXAMPLE)
print('decoded_msg:', item)

item_encoded_str = IoTextCodec.encode(item)
print('encoded_msg   :', item_encoded_str)

assert item_encoded_str == MSG_1_EXAMPLE
```

### Use class IoTextItemDataBuilder to build message with simple builder
```python
from src.builders.iot_ext_item_data_builder import  IoTextItemDataBuilder

EXPECTED_MSG = '''t|3900237526042,d|DEV_NAME_002,m|battery_level=d:12.07,m|open_door=b:1,m|open_window=b:0,m|counter_01=i:1234'''

builder = IoTextItemDataBuilder(3900237526042, 'DEV_NAME_002', add_crc16=False)
builder.add_measure('battery_level', 12.07)
builder.add_measure('open_door', True)
builder.add_measure('open_window', False)
builder.add_measure('counter_01', 1234)

built_msg = str(builder)

print("built_msg: ", built_msg)

assert EXPECTED_MSG == built_msg
```

## How to install library
```bash
$ pip install git+https://github.com/bieli/IoText-data-protocol@main#egg=IoText-data-protocol

## test in REPL
$ python3
Python 3.8.10 (default, Nov 22 2023, 10:22:35)
...
>>> from src.builders.iot_ext_item_data_builder import IoTextItemDataBuilder
>>> b = IoTextItemDataBuilder(123, 'D1')
>>> b
<src.builders.iot_ext_item_data_builder.IoTextItemDataBuilder object at 0x7f9ebbc1d550>
>>> str(b)
't|123,d|D1'
```

## Code coverage graph

[![codecov-graph](https://codecov.io/gh/bieli/IoText-data-protocol/branch/main/graphs/tree.svg?token=L8FFQNPQXI)](https://codecov.io/gh/bieli/IoText-data-protocol)

## TODO
 - [x] FIX bug in add_measure(...) for BOOL type values!?
 - [x] add CRC16 from MODBUS protocol for serial communication checksum and any terminals usage
 - [x] add CI/CD pipeline on github based on Github Actions
 - [x] update unit tests
 - [ ] add validator for special chars
 - [ ] add fuzzing tests (discovery limits in values/metrics sizes and check performance issues on SBC devices like RaspberryPi and ESP32)
 - [ ] add limits/max. sizes for device name and metrics names
 - [ ] add setup.py file and publish package for PIP + release on github
 - [ ] add schema versioning, no need to repeat metrics names in all message (one schema in particular version can solve names by indexes in data protocol). More optimal version of protocol.
 - [ ] add definition and examples of delta data sending (it's possible in schema-less version as well, but maybe it will be good to have implementation for that required in IoT systems typical optimisation scenario)
 - [ ] examples, how encapsulate `IoText data protocol` on top od `MQTT IoT protocol`
