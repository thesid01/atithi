# -*- coding: utf-8 -*-
"""This module contains the MindMeld HR assistant blueprint application"""

from chatbot.root import app

import chatbot.greeting
import chatbot.general
import chatbot.faq
import chatbot.tourism
import chatbot.hotel
import chatbot.food
import chatbot.reminder

__all__ = ['app']
