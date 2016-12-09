#!/usr/bin/env python
import ctypes
from ctypes.util import find_library


_path = find_library('libcogito')
_mod = ctypes.cdll.LoadLibrary(_path)

# typedef struct cg_buf {
#   size_t length;
#   size_t capacity;
#   char *content;
# } cg_buf_t;
class CgBuf(ctypes.Structure):
    _fields_ = [('length', ctypes.c_size_t),
                ('capacity', ctypes.c_size_t),
                ('content', ctypes.c_char_p), ]

# response_t cg_to_json
cg_to_json = _mod.cg_to_json
cg_to_json.argtypes = (ctypes.POINTER(CgBuf), ctypes.c_char_p, )
cg_to_json.restype = ctypes.c_int

# response_t cg_to_iam
cg_to_iam = _mod.cg_to_iam
cg_to_iam.argtypes = (ctypes.POINTER(CgBuf), ctypes.c_char_p, )
cg_to_iam.restype = ctypes.c_int


def to_iam(args):
    return check_status(cg_to_iam(args).contents)


def to_json(args):
    return check_status(cg_to_json(args).contents)


def check_status(response):
    if response != 0:
        raise CogitoError(response.message)
    return response


class CogitoError(Exception):
    pass
