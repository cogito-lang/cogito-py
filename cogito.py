#!/usr/bin/env python
import ctypes
from ctypes.util import find_library

_path = find_library('libcogito')
print _path

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

# int cg_to_json
cg_to_json = _mod.cg_to_json
cg_to_json.argtypes = (ctypes.POINTER(CgBuf), ctypes.c_char_p)
cg_to_json.restype = ctypes.c_int

# int cg_to_iam
cg_to_iam = _mod.cg_to_iam
cg_to_iam.argtypes = (ctypes.POINTER(CgBuf), ctypes.c_char_p)
cg_to_iam.restype = ctypes.c_int

# cg_buf_t* cg_buf_build(void);
cg_buf_build = _mod.cg_buf_build
cg_buf_build.argtypes = None
cg_buf_build.restype = ctypes.POINTER(CgBuf)

# void cg_buf_free(cg_buf_t *buffer);
cg_buf_free = _mod.cg_buf_free
cg_buf_free.argtypes = (ctypes.POINTER(CgBuf), )
cg_buf_free.restype = None

def to_iam(args):
    buf = cg_buf_build()
    if cg_to_iam(buf, args) != 0:
        raise CogitoError("IAM conversion failed")
    response = buf.contents.content
    cg_buf_free(buf)
    return response

def to_json(args):
    buf = cg_buf_build()
    if cg_to_json(buf, args) != 0:
        raise CogitoError("JSON conversion failed")
    response = buf.contents.content
    cg_buf_free(buf)
    return response

class CogitoError(Exception):
    pass
