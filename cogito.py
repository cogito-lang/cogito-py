#!/usr/bin/env python
import ctypes
from ctypes.util import find_library

_path = find_library('libcogito')
_mod = ctypes.cdll.LoadLibrary(_path)

# typedef struct response {
# 	  int status;
# 	  char *message;
# 	} response_t;
# https://docs.python.org/2/library/ctypes.html#fundamental-data-types
class ResponseT(ctypes.Structure):
  _fields_ = [('status', ctypes.c_int),
              ('message', ctypes.c_char_p),]

# response_t cg_to_json()
to_json = _mod.cg_to_json
to_json.argtypes = (ctypes.c_char_p, )
to_json.restype = ctypes.POINTER(ResponseT)

# response_T
to_iam = _mod.cg_to_iam
to_iam.argtypes = (ctypes.c_char_p, )
to_iam.restype = ctypes.POINTER(ResponseT)
