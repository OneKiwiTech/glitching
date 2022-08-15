from lite32bit import Lite32bit
from importlib import reload
import chipwhisperer.common.results.glitch as glitch
from tqdm.notebook import tqdm
import re
import struct

PLATFORM = ''

def main():
    lite = Lite32bit()
    lite.target.baud = 115200
    lite.get_scope_info()
    lite.get_target_info()
    lite.get_scope_setup()
    lite.reboot_flush()

    lite.scope.glitch.clk_src = 'clkgen'
    lite.scope.glitch.trigger_src = 'ext_single'
    lite.scope.glitch.repeat = 1
    lite.scope.glitch.output = "clock_xor"
    lite.scope.io.hs2 = "glitch"

    gc = glitch.GlitchController(groups=["success", "reset", "normal"], parameters=["width", "offset", "ext_offset"])
    #gc.display_stats()

    sample_size = 1
    gc.set_range("width", 2, 14)
    gc.set_range("offset", 0.4, 14)
    gc.set_range("ext_offset", 0, 41)
    step = 0.4
    gc.set_global_step(step)
    lite.scope.glitch.repeat = 1
    lite.reboot_flush()
    broken = False

    for glitch_settings in gc.glitch_values():
        lite.scope.glitch.offset = glitch_settings[1]
        lite.scope.glitch.width = glitch_settings[0]
        lite.scope.glitch.ext_offset = glitch_settings[2]
        for i in range(sample_size):
            if lite.scope.adc.state:
                # can detect crash here (fast) before timing out (slow)
                print("Trigger still high!")
                #gc.add("reset", (lite.scope.glitch.width, lite.scope.glitch.offset, lite.scope.glitch.ext_offset))
                #plt.plot(lwid, loff, 'xr', alpha=1)
                #fig.canvas.draw()

                #Device is slow to boot?
                lite.reboot_flush()

            lite.scope.arm()
            lite.target.simpleserial_write('p', bytearray([0]*5))

            ret = lite.scope.capture()


            if ret:
                print('Timeout - no trigger')
                #gc.add("reset", (lite.scope.glitch.width, lite.scope.glitch.offset, lite.scope.glitch.ext_offset))

                #Device is slow to boot?
                lite.reboot_flush()

            else:
                val = lite.target.simpleserial_read_witherrors('r', 1, glitch_timeout=10, timeout=50)#For loop check
                if val['valid'] is False:
                    print(val)
                    #gc.add("reset", (lite.scope.glitch.width, lite.scope.glitch.offset, lite.scope.glitch.ext_offset))
                    #plt.plot(scope.glitch.width, scope.glitch.offset, 'xr', alpha=1)
                    #fig.canvas.draw()
                else:

                    if val['payload'] == bytearray([1]): #for loop check
                        broken = True
                        #gc.add("success", (lite.scope.glitch.width, lite.scope.glitch.offset, lite.scope.glitch.ext_offset))
                        print(val['payload'])
                        print(lite.scope.glitch.width, lite.scope.glitch.offset, lite.scope.glitch.ext_offset)
                        print("🐙", end="")
                        break
                    else:
                        print('normal')
                        #gc.add("normal", (lite.scope.glitch.width, lite.scope.glitch.offset, lite.scope.glitch.ext_offset))
        if broken:
            break

if __name__ == "__main__":
    main()