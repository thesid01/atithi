# -*- coding: utf-8 -*-
"""This module contains the MindMeld HR assistant blueprint application"""

from chatbot.root import app

import chatbot.greeting
import chatbot.general
import chatbot.faq

__all__ = ['app']
