<h1 align="center"> Virtual Serial Ports using socat on macOS</h1>

```bash
brew install socat
pip3 install pyserial
```

```bash
socat -d -d pty,raw,echo=0 pty,raw,echo=0
```
