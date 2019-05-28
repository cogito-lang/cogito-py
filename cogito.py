"""A tiny python library that links against libcogito"""

import os
import ctypes
from ctypes.util import find_library

if os.getenv('COGITO_PATH') is None:
    _path = find_library('cogito')
else:
    _path = os.environ['COGITO_PATH']

if _path is None:
    message = "libcogito is missing from your system. " \
        "Please install by running the following steps:\n"
    if os.popen('uname').read().strip() == 'Darwin':
        message += """
    $ brew tap cogito-lang/formulae
    $ brew install cogito
"""
    else:
        message += """
    $ FILE=$(mktemp)
    $ wget 'https://github.com/cogito-lang/libcogito/releases/download/v0.2.0/libcogito_0.2.0-1_amd64.deb' -qO $FILE
    $ sudo dpkg -i $FILE && rm $FILE
"""  # noqa

    raise NameError(message)


class CgBuf(ctypes.Structure):
    """
    A ctypes structure that wraps the cg_buf struct from libcogito

    typedef struct cg_buf {
      size_t length;
      size_t capacity;
      char *content;
    } cg_buf_t;
    """
    _fields_ = [('length', ctypes.c_size_t),
                ('capacity', ctypes.c_size_t),
                ('content', ctypes.c_char_p), ]


COGITO = ctypes.cdll.LoadLibrary(_path)

# int cg_to_json
COGITO.cg_to_json.argtypes = (ctypes.POINTER(CgBuf), ctypes.c_char_p)
COGITO.cg_to_json.restype = ctypes.c_int

# int cg_to_iam
COGITO.cg_to_iam.argtypes = (ctypes.POINTER(CgBuf), ctypes.c_char_p)
COGITO.cg_to_iam.restype = ctypes.c_int

# cg_buf_t* cg_buf_build(void);
COGITO.cg_buf_build.argtypes = None
COGITO.cg_buf_build.restype = ctypes.POINTER(CgBuf)

# void cg_buf_free(cg_buf_t *buffer);
COGITO.cg_buf_free.argtypes = (ctypes.POINTER(CgBuf), )
COGITO.cg_buf_free.restype = None


def to_iam(args):
    buf = COGITO.cg_buf_build()
    if COGITO.cg_to_iam(buf, ctypes.c_char_p(args.encode("utf-8"))) != 0:
        raise CogitoError("IAM conversion failed")

    response = buf.contents.content.decode("utf-8")
    COGITO.cg_buf_free(buf)
    return response


def to_json(args, subs=None):
    for key, value in (subs or {}).items():
        args = args.replace("${{{}}}".format(key), value)

    buf = COGITO.cg_buf_build()
    if COGITO.cg_to_json(buf, ctypes.c_char_p(args.encode("utf-8"))) != 0:
        raise CogitoError("JSON conversion failed")

    response = buf.contents.content.decode("utf-8")
    COGITO.cg_buf_free(buf)
    return response


class CogitoError(Exception):
    pass
