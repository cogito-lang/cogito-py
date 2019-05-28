# cogito-py

[![Build Status](https://travis-ci.com/cogito-lang/cogito-py.svg?branch=master)](https://travis-ci.com/cogito-lang/cogito-py)
[![PyPI](https://img.shields.io/pypi/v/cogito.svg)](https://pypi.python.org/pypi/cogito)

A tiny python library that links against [libcogito](https://github.com/cogito-lang/libcogito).

## Usage

```python
>>> import cogito
>>> print cogito.to_json('ALLOW a on b;')
[
  {
    "Effect": "Allow",
    "Action": [
      "a"
    ],
    "Resource": [
      "b"
    ]
  }
]

>>> print cogito.to_iam('[{ "Effect": "Allow", "Action": "a", "Resource": "b" }]')
ALLOW
  a
ON
  b;
```

If your `libcogito` library is in a non-standard location, you should set the `COGITO_PATH` environment variable before you import the `cogito` module.

```python
import os
os.environ['COGITO_PATH'] = os.path.join(os.getcwd(), 'local', 'lib', 'libcogito.so')
import cogito
```

## Development

To run tests, run `py.test`. To release a new version:

```sh
pip install twine
python setup.py sdist
python setup.py bdist_wheel --universal
twine upload dist/*
```

## Contributing

Bug reports and pull requests are welcome on GitHub at https://github.com/cogito-lang/cogito-py.

## License

The package is available as open source under the terms of the [MIT License](http://opensource.org/licenses/MIT).
