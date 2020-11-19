import os
import signal
import pymysql
from dotenv import load_dotenv

from RestrictedPython import compile_restricted
from RestrictedPython import Eval
from RestrictedPython import utility_builtins

# from RestrictedPython import safe_builtins
# from RestrictedPython import limited_builtins
# from RestrictedPython import Guards

load_dotenv()

db_pw = os.getenv("DB_PASSWORD")

logic_db = pymysql.connect(user="root", passwd=db_pw, host="127.0.0.1", db="algotrade", charset="utf8")

cursor = logic_db.cursor(pymysql.cursors.DictCursor)

sql = "SELECT * FROM logic where user=1 limit 1;"
cursor.execute(sql)
result = cursor.fetchall()

print(result)

name = "raynear"
myList = ["ray", "near", "cute", "yun", "suho"]
loc = {}


# config and inject data and function
global_builtins = {"__builtins__": utility_builtins}.copy()
global_builtins["_getiter_"] = Eval.default_guarded_getiter
global_builtins["_getattr_"] = getattr
global_builtins["getattr"] = getattr
global_builtins["_setattr_"] = setattr
global_builtins["setattr"] = setattr
global_builtins["_print_"] = print
global_builtins["str"] = str
global_builtins["name"] = name
global_builtins["myList"] = myList
# global_builtins["_iter_unpack_sequence_"] = Guards.guarded_iter_unpack_sequence

byte_code = compile_restricted(result[0]["content"], "<inline code>", "exec", None)

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
