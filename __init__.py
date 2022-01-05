# Copyright 2021 Magnus Anderson <magnus@iastate.edu>
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# See <https://www.gnu.org/licenses/>.

"""
Anki-touch addon. Swipe to show the back of a card and to answer it.
"""

from anki import hooks
from anki.template import TemplateRenderContext
from aqt import dialogs, gui_hooks, mw
from aqt.browser import PreviewDialog
from aqt.clayout import CardLayout
from aqt.qt import Qt
from aqt.reviewer import Reviewer

# Globals
inQuestion = True
downX = -1.
SWIPE_NEEDED_PIXELS = 150

# Responding to clicks
def on_js_message(handled, msg, context):
    global downX
    global inQuestion

    if isinstance(context, CardLayout) and (
        msg.startswith("ct_click_") or msg.startswith("ct_dblclick_")
    ):
        # card layout is a modal dialog, so we can't display there
        return handled

    if not isinstance(context, Reviewer) and not isinstance(context, PreviewDialog):
        # only function in review and preview screens
        return handled

    if msg.startswith("anki_touch "):
        msg = msg.removeprefix("anki_touch ")
        if msg.startswith("down "):
            msg = msg.removeprefix("down ")
            downX = float(msg)
        elif msg.startswith("up "):
            msg = msg.removeprefix("up ")
            diffX = float(msg) - downX
            if diffX < -SWIPE_NEEDED_PIXELS:
                if not inQuestion:
                    answer_question(False)
                else:
                    show_back()
            elif diffX > SWIPE_NEEDED_PIXELS:
                if not inQuestion:
                    answer_question(True)
                else:
                    show_back()
        return True, None

    return handled

def show_back():
    if mw.reviewer.state == "question":
        mw.reviewer._getTypedAnswer()
    else:
        print("Error in anki_touch addon - please open an issue")

def answer_question(didSucceed):
    if mw.reviewer.state == "answer":
        mw.reviewer._answerCard(
            mw.reviewer._defaultEase() if didSucceed else 1
        )
    else:
        print("Error in anki_touch addon - please open an issue")

gui_hooks.webview_did_receive_js_message.append(on_js_message)

# Adding CSS/JS to card

# There are two types of events we listen to: click and touch ones
# Touchstart/end events and mousedown/up events are handled if the x changes sufficiently (hardcoded as 150px)
# On the front to show cards
# On the back to answer cards
swipe_handler = """
<script type="text/javascript">
function intercept_down(event) {
    pycmd("anki_touch down " + event.x)
}
function intercept_up(event) {
    pycmd("anki_touch up " + event.x)
}
function touch_down(event) {
    touch = event.changedTouches[0];
    pycmd("anki_touch down " + touch.pageX)
}
function touch_up(event) {
    touch = event.changedTouches[0];
    pycmd("anki_touch up " + touch.pageX)
}
// Do this hack with document.anki_touch because somehow the event listeners persist across questions
if (!document.anki_touch) {
    document.addEventListener("mousedown", intercept_down);
    document.addEventListener("mouseup", intercept_up);
    document.addEventListener("touchstart", touch_down);
    document.addEventListener("touchend", touch_up);
}
document.anki_touch = true;
</script>
"""

# Inject the javascript that handles swipes
def on_card_show(html, card, context):
    return html + swipe_handler
gui_hooks.card_will_show.append(on_card_show)

# Set the global variable that tracks if we're in question or answer
def show_question(card):
    global inQuestion
    inQuestion = True
def show_answer(card):
    global inQuestion
    inQuestion = False
gui_hooks.reviewer_did_show_question.append(show_question);
gui_hooks.reviewer_did_show_answer.append(show_answer);
