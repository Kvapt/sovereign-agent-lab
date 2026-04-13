"""
Exercise 2 — Answers
====================
Fill this in after running exercise2_langgraph.py.
Run `python grade.py ex2` to check for obvious issues.
"""

# ── Task A ─────────────────────────────────────────────────────────────────

# List of tool names called during Task A, in order of first appearance.
# Look at [TOOL_CALL] lines in your terminal output.
# Example: ["check_pub_availability", "get_edinburgh_weather"]

TASK_A_TOOLS_CALLED = [
    "check_pub_availability",
    "calculate_catering_cost",
    "get_edinburgh_weather",
    "generate_event_flyer",
]

# Which venue did the agent confirm? Must be one of:
# "The Albanach", "The Haymarket Vaults", or "none"
TASK_A_CONFIRMED_VENUE = "The Albanach"

# Total catering cost the agent calculated. Float, e.g. 5600.0
# Write 0.0 if the agent didn't calculate it.
TASK_A_CATERING_COST_GBP = 5600.0

# Did the weather tool return outdoor_ok = True or False?
TASK_A_OUTDOOR_OK = False

# Optional — anything unexpected.
TASK_A_NOTES = "The agent only checked The Albanach and never called check_pub_availability for The Haymarket Vaults — it confirmed The Albanach on the first check and moved on without needing the fallback. Three tool calls (catering, weather, flyer) were issued in parallel after the availability check resolved."

# ── Task B ─────────────────────────────────────────────────────────────────
#
# The scaffold ships with a working generate_event_flyer that has two paths:
#
#   - Live mode: if FLYER_IMAGE_MODEL is set in .env, the tool calls that
#     model and returns a real image URL.
#   - Placeholder mode: otherwise (the default) the tool returns a
#     deterministic placehold.co URL with mode="placeholder".
#
# Both paths return success=True. Both count as "implemented" for grading.
# This is not the original Task B — the original asked you to write a direct
# FLUX image call, but Nebius removed FLUX on 2026-04-13. See CHANGELOG.md
# §Changed for why we pivoted the task.

# Did your run of the flyer tool produce a success=True result?
# (This will be True for both live and placeholder mode — both are valid.)
TASK_B_IMPLEMENTED = True

# Which path did your run take? "live" or "placeholder"
# Look for the "mode" field in the TOOL_RESULT output of Task B.
# If you didn't set FLYER_IMAGE_MODEL in .env, you will get "placeholder".
TASK_B_MODE = "placeholder"

# The image URL returned by the tool. Copy exactly from your terminal output.
# In placeholder mode this will be a placehold.co URL.
# In live mode it will be a provider CDN URL.
TASK_B_IMAGE_URL = "https://placehold.co/1200x628/1a1a2e/eaeaea?text=The+Haymarket+Vaults+%7C+160+guests&id=2ef939fbbaf6"

# The prompt sent to the image model. Copy from terminal output.
TASK_B_PROMPT_USED = "Professional event flyer for Edinburgh AI Meetup, tech professionals, modern venue at The Haymarket Vaults, Edinburgh. 160 guests tonight. Warm lighting, Scottish architecture background, clean modern typography."

# Why did the agent's behaviour NOT change when Nebius removed FLUX?
# One sentence. This is the point of the lesson.
TASK_B_WHY_AGENT_SURVIVED = """
The agent survived because the tool returned a structured success=True response
with a valid fallback URL regardless of whether a live image provider was
available — the ReAct loop only sees a successful tool result either way, so
the agent's control flow never broke.
"""

# ── Task C ─────────────────────────────────────────────────────────────────

# Scenario 1: first choice unavailable
# Quote the specific message where the agent changed course. Min 20 words.
SCENARIO_1_PIVOT_MOMENT = """
After receiving the tool result for The Bow Bar — capacity 80, status full,
meets_all_constraints false — the agent immediately issued a second
check_pub_availability call for The Haymarket Vaults without any user
instruction to do so. The pivot happened silently between the first TOOL_RESULT
and the second TOOL_CALL, driven entirely by the model's own reasoning.
"""

SCENARIO_1_FALLBACK_VENUE = "The Haymarket Vaults"

# Scenario 2: impossible constraint (300 guests)
# Did the agent recommend a pub name not in the known venues list?
SCENARIO_2_HALLUCINATED = False

# Paste the final [AI] message.
SCENARIO_2_FINAL_ANSWER = """
The agent checked four venues — The Albanach (180, too small), The Haymarket
Vaults (160, too small), The Guilford Arms (200, no vegan), The Bow Bar (80,
full) — and correctly concluded that none of the known venues can accommodate
300 guests with vegan options. It admitted failure rather than inventing a
fictional venue.
"""

# Scenario 3: out of scope (train times)
# Did the agent try to call a tool?
SCENARIO_3_TRIED_A_TOOL = False

SCENARIO_3_RESPONSE = "The agent recognised that none of its tools (check_pub_availability, get_edinburgh_weather, calculate_catering_cost, generate_event_flyer) were relevant to train schedules and declined to answer, stating it could not use any of the provided functions for this request."

# Would this behaviour be acceptable in a real booking assistant? Min 30 words.
SCENARIO_3_ACCEPTABLE = """
Yes, this behaviour is acceptable and correct for a scoped booking assistant.
The agent stayed within its defined tool boundary rather than hallucinating a
train timetable or calling an irrelevant tool. In production, the right response
to an out-of-scope question is a clean, honest decline — not an improvised
answer that could be wrong or mislead the user.
"""

# ── Task D ─────────────────────────────────────────────────────────────────

# Paste the Mermaid output from `python exercise2_langgraph.py task_d` here.
TASK_D_MERMAID_OUTPUT = """
---
config:
  flowchart:
    curve: linear
---
graph TD;
	__start__([<p>__start__</p>]):::first
	agent(agent)
	tools(tools)
	__end__([<p>__end__</p>]):::last
	__start__ --> agent;
	agent -.-> __end__;
	agent -.-> tools;
	tools --> agent;
	classDef default fill:#f2f0ff,line-height:1.2
	classDef first fill-opacity:0
	classDef last fill:#bfb6fc
"""

# Compare the LangGraph graph to exercise3_rasa/data/flows.yml. Min 30 words.
TASK_D_COMPARISON = """
The LangGraph Mermaid graph has exactly three nodes: __start__, agent, and tools,
connected in a single loop. There are no explicit paths — the model decides at
runtime whether to call a tool or terminate. Nothing about the task structure is
visible in the graph itself.

flows.yml is the opposite: every task the agent can perform is written out
explicitly (confirm_booking, handle_out_of_scope), each with named steps in a
fixed order. The routing logic is readable by a human without running anything.
LangGraph encodes zero task knowledge in its graph; Rasa CALM encodes all of it.
"""

# ── Reflection ─────────────────────────────────────────────────────────────

# The most unexpected thing the agent did. Min 40 words.
# Must reference a specific behaviour from your run.

MOST_SURPRISING = """
The most unexpected behaviour was in Task A: the agent was explicitly told to
check both The Albanach and The Haymarket Vaults, but it only called
check_pub_availability once — for The Albanach. Once that returned
meets_all_constraints=true, the agent skipped the second venue entirely and
issued the catering, weather, and flyer calls in parallel. It interpreted the
instruction as "check until you find one that works" rather than "check both
regardless", which is arguably more efficient but directly ignores the literal
task description. This shows that ReAct agents optimise for goal completion, not
instruction literal-compliance — a meaningful distinction for auditable systems.
"""
