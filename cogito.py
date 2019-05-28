"""A tiny python library that links against libcogito"""

import os
import ctypes
from ctypes.util import find_library

if os.getenv("COGITO_PATH") is None:
    COGITO_PATH = find_library("cogito")
else:
    COGITO_PATH = os.environ["COGITO_PATH"]

if COGITO_PATH is None:
    message = "libcogito is missing from your system. " \
        "Please install by running the following steps:\n"

    if os.popen("uname").read().strip() == "Darwin":
        message += """
    $ brew tap cogito-lang/formulae
    $ brew install cogito
"""
    else:
        message += """
    $ FILE=$(mktemp)
    $ wget 'https://github.com/cogito-lang/libcogito/releases/download/v0.2.0/libcogito_0.2.0-1_amd64.deb' -qO $FILE
    $ sudo dpkg -i $FILE && rm $FILE
"""

    raise NameError(message)


class CogitoBuffer(ctypes.Structure):
    """
    A ctypes structure that wraps the cg_buf struct from libcogito

    typedef struct cg_buf {
      size_t length;
      size_t capacity;
      char *content;
    } cg_buf_t;
    """
    _fields_ = [("length", ctypes.c_size_t),
                ("capacity", ctypes.c_size_t),
                ("content", ctypes.c_char_p), ]


class CogitoError(Exception):
    pass


COGITO = ctypes.cdll.LoadLibrary(COGITO_PATH)

# int cg_to_json(cg_buf_t *buffer, char *str);
COGITO.cg_to_json.argtypes = (ctypes.POINTER(CogitoBuffer), ctypes.c_char_p)
COGITO.cg_to_json.restype = ctypes.c_int

# int cg_to_iam(cg_buf_t *buffer, char *str);
COGITO.cg_to_iam.argtypes = (ctypes.POINTER(CogitoBuffer), ctypes.c_char_p)
COGITO.cg_to_iam.restype = ctypes.c_int

# cg_buf_t* cg_buf_build(void);
COGITO.cg_buf_build.argtypes = None
COGITO.cg_buf_build.restype = ctypes.POINTER(CogitoBuffer)

# void cg_buf_free(cg_buf_t *buffer);
COGITO.cg_buf_free.argtypes = (ctypes.POINTER(CogitoBuffer), )
COGITO.cg_buf_free.restype = None


def to_iam(content):
    buffer = COGITO.cg_buf_build()
    if COGITO.cg_to_iam(buffer, ctypes.c_char_p(content.encode("utf-8"))) != 0:
        raise CogitoError("IAM conversion failed")

    response = buffer.contents.content.decode("utf-8")
    COGITO.cg_buf_free(buffer)

    return response


def to_json(content, substitutions=None):
    for key, value in (substitutions or {}).items():
        content = content.replace("${{{}}}".format(key), value)

    buffer = COGITO.cg_buf_build()
    if COGITO.cg_to_json(buffer, ctypes.c_char_p(content.encode("utf-8"))) != 0:
        raise CogitoError("JSON conversion failed")

    response = buffer.contents.content.decode("utf-8")
    COGITO.cg_buf_free(buffer)

    return response
