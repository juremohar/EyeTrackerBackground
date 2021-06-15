EyeTrackerBackground


To build EyeTrackerBackground
- pyinstaller main.spec
- pyinstaller --onefile --noconsole main.spec


To build EyeTrackerCalibration
- pyinstaller calibrationWindow.spec
- pyinstaller --onefile --noconsole calibrationWindow.spec


For other project to use this app this is possible by python libraray called rpyc.

config:
- host: "localhost"
- port: 33333


Simple client example:
```
import rpyc

proxy = rpyc.connect('localhost', 33333, config={'allow_public_attrs': True})

# turn on eyetracker
result = proxy.root.turn_on_eyetracker_capture()

# turn off eyetracker
result = proxy.root.turn_off_eyetracker_capture()

```

Response is in following format:

```

{
    "success": True,
    "msg": "eye tracker was successfully started"
}

{
    "success": False,
    "msg": "eye tracker was not found"
}
```