# bluetooth-ble-heartrate-sensor-poc

Using `bluepy` library to receive the heartrate notifications from a Suunto heartrate sensor device.

## Requirements

Install [bluepy](https://github.com/IanHarvey/bluepy) from source:

```
git clone https://github.com/IanHarvey/bluepy.git
cd bluepy
python setup.py build
sudo python setup.py install
```

## Running

Fetch the git repository

```
git clone https://github.com/amohar/bluetooth-ble-heartrate-sensor-poc.git
cd bluetooth-ble-heartrate-sensor-poc
./heartrate.py
```

There will be no initial output (it's a POC), after less than 30 seconds you should start getting the data.

```
0c:8c:dc:1c:XX:XX:  ❤ 71
0c:8c:dc:1c:XX:XX:  ❤ 70
0c:8c:dc:1c:XX:XX:  ❤ 69
0c:8c:dc:1c:XX:XX:  ❤ 68
```