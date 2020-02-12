from spi_flash import spi_flash
import sys

def test_func(mem, addr, data):
    if mem.chk_dev():
        ret = mem.get_jid()
        mid = ret.pop(0)
        print("Manufature ID: ", hex(mid))
        print("JEDEC ID: ", end="")
        for i in ret:
            print (hex(i), end=" ")
        print()
    else:
        print ("Wrong device")
        mem.close()
        return False

    if mem.erase(addr) == False:
        print ("Erase failed")
        return False

    if mem.write(addr, data):
        ret = mem.read(addr, len(data))
    else:
        print ("Write failed")
        mem.close()
        return False

    if ret != data:
        print ("R/W failed with data:", ret)
        return False

    return True

def test():
    try:
        addr = [0x1f, 0x00, 0x00]
        data = [0x09, 0x05, 0x02, 0x07]
        mem = spi_flash(0, 0)
        mem.setup(speed=1100000, mode=3)

        mem.reset()

        if test_func(mem, addr, data):
            print ("R/W test sucessed")
        else:
            print ("R/W test failed")
    except Exception as err:
        err_cls = err.__class__.__name__
        detail = err.args[0]
        cl, exc, tb = sys.exc_info()
        last_call_stk = traceback.extract_tb(tb)[-1]

        file_name = lastCallStack[0]
        line_num = lastCallStack[1]
        func_name = lastCallStack[2]
        print ("File: ", file_name, " line: ", line_num, " in function: ", func_name, ", ", err_cls, detail)

if __name__ == "__main__":
    test()
