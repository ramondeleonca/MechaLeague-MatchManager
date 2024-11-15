import launchpad_py
import time

lp = launchpad_py.LaunchpadMk2()
lp.Open()

print( " - Testing LedAllOn()" )
for i in [ 5, 21, 79, 3]:
    lp.LedAllOn( i )
    time.sleep(1)
lp.LedAllOn( 0 )

while True:
    # lp.ButtonFlush()
    # but = lp.ButtonStateRaw()
    but = lp.ButtonStateXY()
    print(but)
    time.sleep(0.1)