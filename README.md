# cogito-py

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

## Development

To run tests, run `pytest`.

## Contributing

Bug reports and pull requests are welcome on GitHub at https://github.com/localytics/cogito-py.

## License

The package is available as open source under the terms of the [MIT License](http://opensource.org/licenses/MIT).
