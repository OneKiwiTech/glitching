from lite32bit import Lite32bit

def main():
    lite = Lite32bit()
    lite.target.baud = 115200
    lite.get_scope_info()
    lite.get_target_info()
    lite.get_scope_setup()
    lite.program_target()
    lite.reboot_flush()
    #lite.shutdown()
    print('loop')
    while(True):
        #pw = bytearray([0x00]*5)
        pw = bytearray([0x74, 0x6F, 0x75, 0x63, 0x68]) # correct password ASCII representation
        lite.target.simpleserial_write('p', pw)

        val = lite.target.simpleserial_read_witherrors('r', 1, glitch_timeout=250)#For loop check
        valid = val['valid']
        if valid:
            response = val['payload']
            raw_serial = val['full_response']
            error_code = val['rv']

        print(val)

if __name__ == "__main__":
    main()