#!/usr/bin/env python
import ctypes
from ctypes.util import find_library


_path = find_library('libcogito')
_mod = ctypes.cdll.LoadLibrary(_path)

# typedef struct response {
# 	  int status;
# 	  char *message;
# 	} response_t;
class ResponseT(ctypes.Structure):
    _fields_ = [('status', ctypes.c_int),
                ('message', ctypes.c_char_p), ]

# response_t cg_to_json
cg_to_json = _mod.cg_to_json
cg_to_json.argtypes = (ctypes.c_char_p, )
cg_to_json.restype = ctypes.POINTER(ResponseT)

# response_t cg_to_iam
cg_to_iam = _mod.cg_to_iam
cg_to_iam.argtypes = (ctypes.c_char_p, )
cg_to_iam.restype = ctypes.POINTER(ResponseT)


def to_iam(args):
    return check_status(cg_to_iam(args).contents)


def to_json(args):
    return check_status(cg_to_json(args).contents)


def check_status(response):
    if response.status != 0:
        raise CogitoError(response.message)
    return response.message


class CogitoError(Exception):
    pass
