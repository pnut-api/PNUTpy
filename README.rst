PNUTpy: pnut.io API for Python
==============================


PNUTpy aims to be an easy-to-use Python library for interacting with the `pnut.io API <https://docs.pnut.io/api>`_.

Installation
------------

To install, simply:

.. code-block:: bash

    $ pip install pnutpy

Quick Start
-----------

In order to use PNUTpy, You'll need an access token. If you don't already have one, first `create an app`_, and then generate an access token for your app.

.. code-block:: python

    import pnutpy
    pnutpy.api.add_authorization_token(<Access Token Here>)

    # Create a post
    post, meta = pnutpy.api.create_post(data={'text':'Hello pnut.io from pnutpy!'})

.. _create an app: https://pnut.io/
