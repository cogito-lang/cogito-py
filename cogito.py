"""A tiny python library that links against libcogito"""

import os
import ctypes
from ctypes.util import find_library

if os.getenv("COGITO_PATH") is None:
    COGITO_PATH = find_library("cogito")
else:
    COGITO_PATH = os.environ["COGITO_PATH"]

if COGITO_PATH is None:
    raise NameError(
        "libcogito is missing from your system. " \
        "Please go to https://github.com/cogito-lang/libcogito " \
        "and follow the installation instructions."
    )


class CogitoBuffer(ctypes.Structure):
    # pylint: disable=too-few-public-methods

    """
    A ctypes structure that wraps the cg_buf struct from libcogito

    struct cg_buf {
      size_t length;
      size_t capacity;
      char *content;
    };
    """

    _fields_ = [
        ("length", ctypes.c_size_t),
        ("capacity", ctypes.c_size_t),
        ("content", ctypes.c_char_p)
    ]


class CogitoError(Exception):
    """A generic error to represent when the C library conversion fails"""


class Cogito:
    """A context manager used for allocating and releasing a cogito buffer"""

    def __init__(self):
        self.buffer = None

    def __enter__(self):
        """Allocates and stores a cogito buffer"""

        self.buffer = COGITO.cg_buf_build()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Releases the stored cogito buffer"""

        COGITO.cg_buf_free(self.buffer)

    def to_iam(self, content):
        """
        Calls the native cg_to_iam C function and returns the result that
        is now stored in the buffer struct
        """

        c_char_p = ctypes.c_char_p(content.encode("utf-8"))
        if COGITO.cg_to_iam(self.buffer, c_char_p) != 0:
            raise CogitoError("IAM conversion failed")

        return self.buffer.contents.content.decode("utf-8")

    def to_json(self, content):
        """
        Calls the native cg_to_json C function and returns the result that
        is now stored in the buffer struct
        """

        c_char_p = ctypes.c_char_p(content.encode("utf-8"))
        if COGITO.cg_to_json(self.buffer, c_char_p) != 0:
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
    """Converts the given JSON string into IAM syntax"""

    response = None
    with Cogito() as cogito:
        response = cogito.to_iam(content)

    return response


def to_json(content, substitutions=None):
    """Converts the given IAM string into JSON syntax"""

    for key, value in (substitutions or {}).items():
        content = content.replace("${{{}}}".format(key), value)

    response = None
    with Cogito() as cogito:
        response = cogito.to_json(content)

    return response
