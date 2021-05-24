import rpyc

proxy = rpyc.connect('localhost', 33333, config={'allow_public_attrs': True})

result = proxy.root.turn_off_eyetracker_capture('C:\\Users\\PC\Desktop\\tests\\test.json')
# result = proxy.root.turn_on_eyetracker_capture()
print("result:", result)