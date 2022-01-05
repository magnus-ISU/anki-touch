# Copyright 2021 Magnus Anderson <magnus@iastate.edu>
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# See <https://www.gnu.org/licenses/>.

"""
An example of porting old template/wrapping code to Anki 2.1.20.
The add-on now looks for {{clickable:Tags}} instead of just {{Tags}}
on the template.
"""

from anki import hooks
from anki.template import TemplateRenderContext
from aqt import dialogs, gui_hooks, mw
from aqt.browser import PreviewDialog
from aqt.clayout import CardLayout
from aqt.qt import Qt
from aqt.reviewer import Reviewer

from aqt.utils import tooltip

# Responding to clicks
############################


def on_js_message(handled, msg, context):
    print("on_js_message: " + msg)
    if isinstance(context, CardLayout) and (
        msg.startswith("ct_click_") or msg.startswith("ct_dblclick_")
    ):
        # card layout is a modal dialog, so we can't display there
        tooltip("Can't be used in card layout screen.")
        return handled

    if not isinstance(context, Reviewer) and not isinstance(context, PreviewDialog):
        # only function in review and preview screens
        return handled

#    if msg.startswith("ct_click_"):
#        tag = msg.replace("ct_click_", "")
#        browser = dialogs.open("Browser", mw)
#        browser.setFilter('"tag:%s"' % tag)
#        return True, None
#    elif msg.startswith("ct_dblclick_"):
#        tag, deck = msg.replace("ct_dblclick_", "").split("|")
#        browser = dialogs.open("Browser", mw)
#        browser.setFilter('"tag:%s" "deck:%s"' % (tag, deck))
#        browser.setWindowState(
#            browser.windowState() & ~Qt.WindowMinimized | Qt.WindowActive
#        )
#        return True, None
    if msg.startswith("anki_touch_"):
        print("on_js_message2")
        return True, None

    return handled


gui_hooks.webview_did_receive_js_message.append(on_js_message)

# Adding CSS/JS to card
############################

add_to_card = """
<style>
  kbd {
    box-shadow: inset 0 1px 0 0 white;
    background:
      gradient(
        linear,
        left top,
        left bottom,
        color-stop(0.05, #f9f9f9),
        color-stop(1, #e9e9e9)
      );
    background-color: #f9f9f9;
    border-radius: 4px;
    border: 1px solid gainsboro;
    display: inline-block;
    font-size: 15px;
    height: 15px;
    line-height: 15px;
    padding: 4px 4px;
    margin: 5px;
    text-align: center;
    text-shadow: 1px 1px 0 white;
    cursor: pointer;
    cursor: hand;
  }

  .nightMode kbd { color: black; }
</style>
<script type="text/javascript">
function ct_click(tag) {
    pycmd("ct_click_" + tag)
}
function ct_dblclick(tag, deck) {
    pycmd("ct_dblclick_" + tag + "|" + deck)
}
</script>
"""

# Handling {{clickable:Tags}}
################################

click_handler = """
<script type="text/javascript">
function intercept_click(thing) {
    pycmd("anki_touch_" + thing)
}
pycmd("anki_touch_start");
document.addEventListener("click", intercept_click);
</script>
"""

# Inject the javascript that handles clicks
def on_card_show(html, card, context):
    print("on_card_show")
    return html + click_handler
gui_hooks.card_will_show.append(on_card_show)

inQuestion = True
def show_question(card):
    global inQuestion
    inQuestion = True

def show_answer(card):
    global inQuestion
    inQuestion = False

gui_hooks.reviewer_did_show_question.append(show_question);
gui_hooks.reviewer_did_show_answer.append(show_answer);
