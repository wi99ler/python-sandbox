import signal
from RestrictedPython import compile_restricted
from RestrictedPython import Eval
from RestrictedPython import utility_builtins

# from RestrictedPython import safe_builtins
# from RestrictedPython import limited_builtins
# from RestrictedPython import Guards

name = "raynear"
myList = ["ray", "near", "cute", "yun", "suho"]
loc = {}

f = open("./logic1.py")
byte_code = compile_restricted(f.read(), "<inline code>", "exec", None)
f.close()


# config and inject data and function
global_builtins = {"__builtins__": utility_builtins}.copy()
global_builtins["_getiter_"] = Eval.default_guarded_getiter
global_builtins["str"] = str
global_builtins["name"] = name
global_builtins["myList"] = myList
# global_builtins["_iter_unpack_sequence_"] = Guards.guarded_iter_unpack_sequence


### time out
class TimeOutException(Exception):
    pass


def alarm_handler(signum, frame):
    raise TimeOutException()


signal.signal(signal.SIGALRM, alarm_handler)
signal.alarm(1)

try:
    exec(byte_code, {"__builtins__": global_builtins}, loc)
except TimeOutException as e:
    print(e)

print(loc["logic"]())
