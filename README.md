# Making Sense of Parsers

This python library was mostly implemented for a talk I gave at PythonNW in Manchester

It has an example of a PEG for parsing dice expressions and maths, implemented using parsimonious.

A dice expression looks like `2d6+3` or `(1d6+2)*3 + 3d4`.  You can even input slightly foolish dice expressions like `1d8*1d8`

## Using

Install dependencies with `pipenv install`.

The module can be executed via `python -m`.  If called with no arguments, it starts up an interactive shell.

```
python -m parsimonious_dice
> 2d6+3
9
```

## Installing

It's not currently on pypi, but with `flit install` you can install it locally.
