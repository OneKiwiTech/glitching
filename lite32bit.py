import time
import numpy
import chipwhisperer as cw

class Lite32bit:
    def __init__(self):
        self.scope = cw.scope(name='Lite')
        self.scope.default_setup()
        target_type = self.get_target_type()
        self.target = cw.target(self.scope, target_type)
        print("INFO: Found ChipWhisperer 😍")

    def get_target_type(self):
        try:
            if SS_VER == "SS_VER_2_1":
                target_type = cw.targets.SimpleSerial2
            elif SS_VER == "SS_VER_2_0":
                raise OSError("SS_VER_2_0 is deprecated. Use SS_VER_2_1")
            else:
                target_type = cw.targets.SimpleSerial
        except:
            SS_VER="SS_VER_1_1"
            target_type = cw.targets.SimpleSerial
        return target_type

    def get_scope_info(self):
        print('name: %s' %self.scope.get_name())
        print('fw_version: %s' %self.scope.fw_version_str)
        print('latest_fw: %s' %self.scope.latest_fw_str)
        print('usb serial number: %s' %self.scope.sn)
        print('serial ports:')
        for serial in self.scope.get_serial_ports():
            print('    %s' %serial)
        print('feature list:')
        for i, feature in enumerate(self.scope.feature_list(), 1):
            print('    %02d: %s' %(i, feature))
    
    def setup_scope(self):
        self.scope.glitch.trigger_src = 'continuous'
        self.scope.glitch.clk_src = 'clkgen'
        self.scope.glitch.width = 48.8
        self.scope.glitch.offset = 0
        self.scope.io.glitch_hp = True
        self.scope.io.glitch_lp = True

    def get_scope_setup(self):
        print('scope.glitch:')
        print(self.scope.glitch)
        print('scope.clock:')
        print(self.scope.clock)
        print('scope.io:')
        print(self.scope.io)

    def reset_target(self):
        self.scope.io.nrst = 0
        time.sleep(0.2) # 0.2sec
        self.scope.io.nrst = 'high_z'
        time.sleep(0.2)

    def shutdown(self):
        print('***Shutdown***')
        # disables glitch and glitch outputs
        self.scope.glitch_disable()
        self.scope.dis()
        self.target.dis()
        exit()

    def test_glitch(self):
        for repeat in numpy.arange(1, 3000, 1):
            self.scope.glitch.repeat = repeat
                
            self.scope.arm()

            # should reset glitch module to make sure nothing stuck high
            self.scope.io.glitch_hp = False
            self.scope.io.glitch_hp = True
            self.scope.io.glitch_lp = False
            self.scope.io.glitch_lp = True