from lite32bit import Lite32bit

def main():
    lite = Lite32bit()
    lite.target.baud = 115200
    lite.get_scope_info()
    lite.get_target_info()
    lite.get_scope_setup()
    lite.program_target()
    lite.reboot_flush()
    lite.shutdown()
    exit()

if __name__ == "__main__":
    main()