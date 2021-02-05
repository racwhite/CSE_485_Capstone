import sys
import time
import threading

threads = []

def myfunc(i):
    print("sleeping 2 sec from thread {}".format(i))
    #time.sleep(.01)
    # raise SystemExit()
    print("finished sleeping from thread {}".format(i))

for i in range(10):
    t = threading.Thread(name='sleep', target=myfunc, args=(i,))
    t.start()

for t in threads:
    t.join()

print("End of main thread")