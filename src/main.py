from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from typing import TYPE_CHECKING

from anki.cards import Card
from anki.scheduler.v3 import Scheduler
from aqt import gui_hooks, mw
from aqt.qt import *
from aqt.reviewer import Reviewer
from aqt.webview import WebContent

if TYPE_CHECKING:
    from aqt.main import MainWindowState
sys.path.append(os.path.join(os.path.dirname(__file__), "vendor"))

from .consts import consts


@dataclass
class ReviewSessionContext:
    reps: int


review_session_context = ReviewSessionContext(0)


def on_reviewer_did_show_question(card: Card) -> None:
    _, counts = mw.reviewer._v3.counts()
    mw.reviewer.web.eval(
        f"addRepBlocks({sum(counts)}, {review_session_context.reps - sum(counts)})"
    )


def add_reviewer_bar(web_content: WebContent, context: object | None) -> None:
    if not isinstance(context, Reviewer):
        return
    web_base = f"/_addons/{consts.module}/web"
    web_content.body += "<div id='rep-bar'></div>"
    web_content.css.append(f"{web_base}/rep_bar.css")
    web_content.js.append(f"{web_base}/rep_bar.js")
    web_content.body += f"<style>:root {{--rep-block-width: {100 / review_session_context.reps}%}}</style>"
    web_content.body += (
        f"<script>addRepBlocks({review_session_context.reps}, 0);</script>"
    )


def on_state_will_change(
    new_state: MainWindowState, old_state: MainWindowState
) -> None:
    if new_state == "review":
        review_session_context.reps = 0
        if isinstance(mw.col.sched, Scheduler):
            out = mw.col.sched.get_queued_cards()
            review_session_context.reps = (
                out.new_count + out.learning_count + out.review_count
            )


gui_hooks.reviewer_did_show_question.append(on_reviewer_did_show_question)
gui_hooks.webview_will_set_content.append(add_reviewer_bar)
gui_hooks.state_will_change.append(on_state_will_change)
mw.addonManager.setWebExports(__name__, r"web/.*")
