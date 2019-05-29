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

    _fields_ = [
        ("length", ctypes.c_size_t),
        ("capacity", ctypes.c_size_t),
        ("content", ctypes.c_char_p)
    ]


class CogitoError(Exception):
    pass


class Cogito:
    def __init__(self):
        self.buffer = None

    def __enter__(self):
        self.buffer = COGITO.cg_buf_build()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        COGITO.cg_buf_free(self.buffer)

    def to_iam(self, content):
        if COGITO.cg_to_iam(self.buffer, ctypes.c_char_p(content.encode("utf-8"))) != 0:
            raise CogitoError("IAM conversion failed")

        return self.buffer.contents.content.decode("utf-8")

    def to_json(self, content):
        if COGITO.cg_to_json(self.buffer, ctypes.c_char_p(content.encode("utf-8"))) != 0:
            raise CogitoError("JSON conversion failed")

        return self.buffer.contents.content.decode("utf-8")


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
    response = None
    with Cogito() as cogito:
        response = cogito.to_iam(content)

    return response


def to_json(content, substitutions=None):
    for key, value in (substitutions or {}).items():
        content = content.replace("${{{}}}".format(key), value)

    response = None
    with Cogito() as cogito:
        response = cogito.to_json(content)

    return response
