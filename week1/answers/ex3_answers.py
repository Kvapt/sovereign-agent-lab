"""
Exercise 3 — Answers
====================
Fill this in after completing the three Rasa conversations.

CALM vs Old Rasa — what changed
---------------------------------
The old open-source Rasa approach used:
  - nlu.yml: intent training examples
  - rules.yml: explicit dialogue rules
  - FormValidationAction: Python class to parse slot values

Rasa Pro CALM uses:
  - flows.yml: natural language descriptions of what each flow does
  - from_llm slots: the LLM extracts values from conversation
  - ONE custom action: ActionValidateBooking for the business rules

The conversation is the same from the manager's perspective.
The machinery underneath is completely different.

CONVERSATION SCRIPTS
---------------------
Conversation 1 (happy path):
  You:    calling to confirm a booking
  Agent:  [asks guest count]
  You:    160 guests
  Agent:  [asks vegan count]
  You:    about 50 need vegan
  Agent:  [asks deposit]
  You:    £200 deposit
  Agent:  [confirms or escalates?]

Conversation 2 (deposit too high):
  Same as above but use a deposit above £300 (e.g. "£500 deposit").

Conversation 3 (out of scope):
  Start normally, then when asked for vegan count say something like
  "can you arrange parking for the speakers?" and observe what happens.
  Does CALM handle this differently than the old rules approach?
"""

# ── Conversation 1: Happy path ─────────────────────────────────────────────

CONVERSATION_1_TRACE = """
Your input ->  I want to confirm a booking
How many guests are you confirming for tonight's event?
Your input ->  160
And how many of those guests will need vegan meals?
Your input ->  like 50
What deposit amount in GBP are you proposing to secure the booking?
Your input ->  200
Thank you — booking confirmed. 160 guests, 50 requiring vegan meals, £200 deposit accepted. I'll send written confirmation to the organiser shortly.
"""

CONVERSATION_1_OUTCOME = "confirmed"

# ── Conversation 2: Deposit too high ───────────────────────────────────────

CONVERSATION_2_TRACE = """
Your input ->  I want to confirm a booking
How many guests are you confirming for tonight's event?
Your input ->  160
And how many of those guests will need vegan meals?
Your input ->  50
What deposit amount in GBP are you proposing to secure the booking?
Your input ->  600
I need to check one thing with the organiser before I can confirm. The issue is: a deposit of £600 exceeds the organiser's authorised limit of £300. Can I call you back within 15 minutes?
"""

CONVERSATION_2_OUTCOME = "escalated"
CONVERSATION_2_REASON  = "a deposit of £600 exceeds the organiser's authorised limit of £300"

# ── Conversation 3: Out of scope ───────────────────────────────────────────

CONVERSATION_3_TRACE = """
Your input ->  I want to confirm a booking
How many guests are you confirming for tonight's event?
Your input ->  160
And how many of those guests will need vegan meals?
Your input ->  can you arrange parking for the speakers?
I can only help with confirming tonight's venue booking. For anything else, please contact the event organiser directly.
Would you like to continue with confirm booking?
"""

# Describe what CALM did after the out-of-scope message. Min 20 words.
CONVERSATION_3_WHAT_HAPPENED = """
CALM immediately routed to the handle_out_of_scope flow and responded with a
clean, fixed deflection message: "I can only help with confirming tonight's
venue booking. For anything else, please contact the event organiser directly."
It then offered to resume the booking flow, keeping the conversation recoverable
rather than terminating it.
"""

# Compare Rasa CALM's handling of the out-of-scope request to what
# LangGraph did in Exercise 2 Scenario 3. Min 40 words.
OUT_OF_SCOPE_COMPARISON = """
Both handled the out-of-scope request correctly, but in fundamentally different
ways. LangGraph's agent reasoned at runtime that none of its tools were relevant
to train schedules and generated a freeform decline. The response was improvised
by the model each time.

Rasa CALM routed to an explicit handle_out_of_scope flow defined in flows.yml,
which ran a fixed utter_out_of_scope response. The deflection message is
deterministic and auditable — the same wording every time, with no model
improvisation. For a legal or financial context, CALM's approach is preferable:
the exact words the agent says are reviewable and controllable, not left to
the model's judgement on each call.
"""

# ── Task B: Cutoff guard ───────────────────────────────────────────────────

TASK_B_DONE = True

# List every file you changed.
TASK_B_FILES_CHANGED = ["exercise3_rasa/actions/actions.py"]

# How did you test that it works? Min 20 words.
TASK_B_HOW_YOU_TESTED = """
Uncommented the four-line cutoff guard block in actions/actions.py, then
temporarily changed the condition to `if True:` to force escalation regardless
of time. Ran a conversation, confirmed the agent escalated with the reason
"it is past 16:45 — insufficient time to process the confirmation before the
5 PM deadline", then reverted the condition back to the original time check
and retrained.
"""

# ── CALM vs Old Rasa ───────────────────────────────────────────────────────

CALM_VS_OLD_RASA = """
CALM gains by eliminating the slot-parsing boilerplate: the LLM extracts "like
50" or "about one-sixty" into float values automatically via from_llm mappings,
whereas old Rasa needed a ValidateBookingConfirmationForm with regex for each
slot. It also drops nlu.yml intent examples and rules.yml dialogue paths —
the flow description in plain English replaces both.

The cost is predictability at the language layer. The LLM's slot extraction is
probabilistic; old Rasa's regex was deterministic. For the business rules
themselves — deposit cap, capacity ceiling, vegan ratio — Python still handles
everything, because those decisions cannot be left to a model that might reason
around a constraint. The old approach was easier to trust for the extraction
step; CALM trades that certainty for dramatically less code.
"""

# ── The setup cost ─────────────────────────────────────────────────────────

SETUP_COST_VALUE = """
The setup cost bought strict behavioural boundaries. The Rasa CALM agent cannot
improvise a response it wasn't trained on, cannot call a tool not defined in
flows.yml, and cannot deviate from the step sequence in flows.yml once a flow
is active. For the pub manager confirmation call, that is a feature, not a
limitation — every possible agent utterance is reviewable in advance, and no
amount of unusual phrasing from the manager can cause the agent to invent a
new action or skip the deposit check.

LangGraph could do all of those things: it could call any tool, invent a
response, or skip steps based on its own reasoning. For research tasks that is
powerful. For a financially binding confirmation call where every word could
create a legal commitment, the inability to go off-script is exactly what you
want.
"""
