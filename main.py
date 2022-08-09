from lite32bit import Lite32bit

def main():
    lite = Lite32bit()
    lite.get_scope_info()
    lite.setup_scope()
    lite.get_scope_setup()
    #lite.test_glitch()
    lite.shutdown()

if __name__ == "__main__":
    main()