# cogito-py

[![Build Status](https://travis-ci.com/localytics/cogito-py.svg?token=kQUiABmGkzyHdJdMnCnv&branch=master)](https://travis-ci.com/localytics/cogito-py)

A tiny python library that links against [libcogito](https://github.com/localytics/libcogito).

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

To run tests, run `python test/cogito_test.py`.

## Contributing

Bug reports and pull requests are welcome on GitHub at https://github.com/localytics/cogito-py.

## License

The package is available as open source under the terms of the [MIT License](http://opensource.org/licenses/MIT).
