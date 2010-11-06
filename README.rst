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

Just from source::

    git clone git://github.com/1stvamp/gh-hooky.git
    cd gh-spooky
    # You might want to put this in a virtualenv
    pip install -E --requirement ./requirements.txt
    cd src/hooky
    cp settings.py.example settings.py
    # Edit settings with your DB info etc.
    ./manage.py syncdb
    ./manage.py runserver

Usage
=====
Setup, get it running from a publically accessable address, and then login to ``hooky`` using whatever account details you've created.

When you've logged in, you can enter your Github username and API key, as well as a secret key for the post_commit hook calls from Github, I'd suggest running something like::

    $ dd if=/dev/urandom count=1 | tr -cd 'A-Za-z0-9' | cut -c1-30; echo

When you've saved your details you'll be given a commit hook URL you can put into the '''Post Receive URLs''' section of your repository admin '''Service Hooks''' section.
