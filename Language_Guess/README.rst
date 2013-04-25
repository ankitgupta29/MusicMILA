guess_language – Guess the natural language of a text
=====================================================


Example usage
-------------

>>> from guess_language import guess_language
>>> guess_language("Hello, World!")
'en'
>>> guess_language("Ces eaux regorgent de renégats et de voleurs.")
'fr'
>>> guess_language("Tienes que seguir tu corazón.")
'es'
>>> guess_language("いいえ！忍者がいます")
'ja'


Installation
------------

To install the package for Python 3, use::

  $ ./setup.py install

To install the package for Python 2, use::

  $ python2 setup.py install

On Windows, you may use one of the MSI binary packages provided on the
`download page <https://bitbucket.org/spirit/guess_language/downloads>`_.


Requirements
------------

- `Python 3.2+ <http://www.python.org>`_ (or 2.7)
- `PyEnchant <http://packages.python.org/pyenchant>`_ (optional)
- `lib3to2 <https://bitbucket.org/amentajo/lib3to2>`_
  (if installing for Python 2)


This is a Python 3 version of
`guess-language <http://code.google.com/p/guess-language>`_
with further improvements.
