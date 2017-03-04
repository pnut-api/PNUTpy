

"""Pnut.io API library

.. moduleauthor:: Robert <ing@codespelunkers.com>

"""
__version__ = '0.3.9'
__author__ = '@33MHz, Pnut.io'
__license__ = 'MIT'

from .models import User, Post, Interaction, Token
from .api import API
from .cursor import cursor

# Global, unauthenticated instance of API
api = API.build_api()

__all__ = ['User', 'Post', 'Interaction', 'Token', 'API', 'api', 'cursor']
