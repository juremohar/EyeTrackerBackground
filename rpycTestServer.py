import rpyc
from rpyc import ThreadedServer

# To je samo example serverja, za ta del bo poskrbel moj program,
# tole ti zgolj pofejka obanšanje trackerja, tako, da boš lahko preizkusila svoj del

class RpycServer(rpyc.Service):
    def exposed_turn_on_eyetracker_capture(self):
        print("started eye tracker")
        return {
            "success": True,
            "msg": "eye tracker was successfully started"
        }

    def exposed_turn_off_eyetracker_capture(self, location=None):
        print("stopped eye tracker - ", location)

        return {
            "success": True,
            "msg": "eye tracker was successfully stopped"
        }


t = ThreadedServer(RpycServer, port=33333)
t.start()
