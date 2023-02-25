<h2 align="center">Simple Adafruit IO IoT Gateway w/ Virtual Serial Port</h2>

### For MacOS Users
```bash
brew install socat
pip3 install pyserial
```

```bash
socat -d -d pty,raw,echo=0 pty,raw,echo=0
```
Then copy the path of the first pty (e.g. /dev/ttys000) and paste it into the code (`controller.py`).

Echo the data to the serial console:
```bash
echo "sensor2:25" > /dev/ttys009
```
