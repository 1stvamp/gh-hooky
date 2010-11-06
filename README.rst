About
=====
`gh-hooky` is a simple django app that supplies post-commit hook callbacks for updating Github issues based on commit message info.

Setup
=====
Using `buildout`::

    cd gh-hooky
    ./configure
    buildout
    cp src/hooky/settings.py.exampe src/hooky/settings.py
    # Edit settings with your DB info etc.
    bin/django syncdb
    bin/django runserver

Usage
=====
lorem ipsum dolar set ...
