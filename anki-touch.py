# -*- mode: Python ; coding: utf-8 -*-
#
# Copyright (C) 2014 tobynet
#
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/copyleft/agpl.html

__Version__ = "0.1.0"

"""Add-on for Anki 2.x that helps using with the touch interface."""

from aqt import *

from aqt import mw
from aqt.utils import showInfo, tooltip
from anki.hooks import wrap

pressed_position = None;

def show_answer():
    print("Touch addon installed")
    u"""Change state to answer"""
    if mw.reviewer.state == "question":
        mw.reviewer._showAnswerHack()


def answer_card(correct):
    u"""Answer with correct or incrrect"""
    tooltip("CORRECT!!" if correct else "miss...", 1000)
    mw.reviewer._answerCard(
      mw.reviewer._defaultEase() if correct else 1)


def is_correct_area(pressed_pos,released_pos):
    u"""Pointing position is in a correct area?"""
    return pressed_pos.x() < released_pos.x()


def my_event(event):
    u"""Hook event to detect touch"""
    tooltip("Event: " + event)
    if event.type() == QEvent.TouchBegin:
        show_answer()


def my_mouse_press_event(event):
    u"""Hook mouse event to detect pressed button firstly"""
    global pressed_position

    #tooltip("press: {0}".format(event.pos().x()))
    show_answer()
    pressed_position = event.pos()


def my_mouse_release_event(event):
    u"""Hook mouse event to detect swipe"""
    global pressed_position

    #tooltip("release: {0} ({1})".format(event.pos().x(), event.pos().x() - pressed_position.x()))
    if mw.reviewer.state == "answer":
        answer_card(
            is_correct_area(
                pressed_pos = pressed_position,
                released_pos = event.pos()))


import pprint

# Hook some events
#mw.web.mousePressEvent = wrap(mw.web.mousePressEvent, my_mouse_press_event)
#mw.web.mouseReleaseEvent = wrap(mw.web.mouseReleaseEvent, my_mouse_release_event)
mw.web.mousePressEvent = my_mouse_press_event
mw.web.mouseReleaseEvent = my_mouse_release_event

# I can't hook "mw.web.event", why?????
#mw.web.event = wrap(mw.web.event, my_event)

