import rpyc


class RpycServer(rpyc.Service):
    tray = None

    def __init__(self, tray):
        self.tray = tray

    def exposed_turn_on_eyetracker_capture(self):
        try:
            self.tray.start_tracking()
            print("eye tracker STARTED with rypc client call")
        except Exception as err:
            print("there was an error attempting to turn ON eye tracker")
            return {
                "success": False,
                "msg": err
            }

        return {
            "success": True,
            "msg": "eye tracker was successfully started"
        }

    def exposed_turn_off_eyetracker_capture(self):
        try:
            self.tray.stop_tracking()
            print("eye tracker STOPPED with rypc client call")
        except Exception as err:
            print("there was an error attempting to turn OFF eye tracker")
            return {
                "success": False,
                "msg": err
            }

        return {
            "success": True,
            "msg": "eye tracker was successfully stopped"
        }
