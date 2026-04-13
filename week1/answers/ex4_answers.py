"""
Exercise 4 — Answers
====================
Fill this in after running exercise4_mcp_client.py.
"""

# ── Basic results ──────────────────────────────────────────────────────────

# Tool names as shown in "Discovered N tools" output.
TOOLS_DISCOVERED = ["search_venues", "get_venue_details"]

QUERY_1_VENUE_NAME    = "The Haymarket Vaults"
QUERY_1_VENUE_ADDRESS = "1 Dalry Road, Edinburgh"
QUERY_2_FINAL_ANSWER  = "No venues in the known database can accommodate 300 guests with vegan options — the search returned zero matches."

# ── The experiment ─────────────────────────────────────────────────────────
# Required: modify venue_server.py, rerun, revert.

EX4_EXPERIMENT_DONE = True

# What changed, and which files did or didn't need updating? Min 30 words.
EX4_EXPERIMENT_RESULT = """
Changing The Albanach's status from 'available' to 'full' in
mcp_venue_server.py immediately affected Query 1: the search returned only
The Haymarket Vaults (count: 1) instead of both venues (count: 2). The
agent then picked Haymarket Vaults as the only match.

Crucially, no other files needed updating — not exercise4_mcp_client.py,
not research_agent.py, not any answer file. The MCP client discovered tools
dynamically and the tool's filtering logic (status == 'available') ran
server-side. The agent code saw a different result without knowing anything
had changed. That is the point: the tool boundary is clean.
"""

# ── MCP vs hardcoded ───────────────────────────────────────────────────────

LINES_OF_TOOL_CODE_EX2 = 7   # import lines in exercise2_langgraph.py referencing venue tools
LINES_OF_TOOL_CODE_EX4 = 0   # exercise4_mcp_client.py has zero venue-specific tool code — tools are discovered

# What does MCP buy you beyond "the tools are in a separate file"? Min 30 words.
MCP_VALUE_PROPOSITION = """
MCP buys dynamic discovery and protocol independence. In Exercise 2 the
agent had a hardcoded import list — adding a tool meant editing the agent
file. In Exercise 4 the agent calls ListTools at startup and gets whatever
the server currently exposes. A new tool added to mcp_venue_server.py
becomes available to every MCP client — LangGraph, Rasa, or any future
client — without touching any client code.

It also means the two halves of PyNanoClaw can share the same tool server
without knowing about each other. The autonomous loop and the structured
agent both discover tools from the same endpoint. That shared layer is what
makes a hybrid system coherent rather than two disconnected scripts.
"""

# ── PyNanoClaw architecture — SPECULATION QUESTION ─────────────────────────

WEEK_5_ARCHITECTURE = """
- The Planner is a strong-reasoning model that lives upstream of the ReAct
  loop in the autonomous-loop half. It takes Rod's raw WhatsApp message and
  produces an ordered list of subgoals (check venues, check weather, estimate
  cost, generate flyer, hand off to structured agent) so the Executor never
  has to reason about task structure — only about tool calls.

- The Executor is research_agent.py extended with real tools (web search,
  file ops, handoff_to_structured). It lives inside the autonomous-loop half
  and runs the ReAct cycle against the subgoal list the Planner produced.
  This is the Week 1 loop with additions, not a replacement.

- The Shared MCP Tool Server (mcp_venue_server.py grown larger) is the
  shared layer between both halves. It exposes every capability either half
  needs — venue search, web search, calendar access, email — and both halves
  discover tools from it dynamically. Neither half hardcodes what the other
  half can do.

- The Handoff Bridge (bridge/handoff.py) is a tool in the autonomous loop
  that delegates human-conversation tasks to the Rasa structured agent. When
  the pub manager calls back, the Executor calls handoff_to_structured and
  the Rasa half takes over the conversation. It lives in the shared layer.

- The Structured Agent (exercise3_rasa/ extended) handles the pub manager
  call with the same deterministic business rules from Week 1, but now wired
  to the shared MCP server for live venue lookups and equipped with a RAG
  knowledge base for questions outside flows.yml. It can delegate research
  back to the loop via the same bridge.
"""

# ── The guiding question ───────────────────────────────────────────────────
# Which agent for the research? Which for the call? Why does swapping feel wrong?
# Must reference specific things you observed in your runs. Min 60 words.

GUIDING_QUESTION_ANSWER = """
LangGraph handles the research; Rasa CALM handles the pub manager call.
Swapping them feels wrong because of what each one did in practice.

In Exercise 2, the LangGraph agent skipped checking The Haymarket Vaults
entirely once The Albanach passed — it optimised for goal completion rather
than following instructions literally. That's exactly what you want for
research: flexible, outcome-driven reasoning that pivots when a venue is
full and admits failure when 300 guests can't be placed. You cannot script
that path in advance.

In Exercise 3, the Rasa agent confirmed 160 guests and £200 deposit without
improvising a single word, and escalated £600 with a fixed, auditable reason
string ("exceeds the organiser's authorised limit of £300"). Python enforced
the cap — the LLM couldn't reason around it. That's exactly what you want
for a financial commitment: deterministic, reviewable, guaranteed.

If you swapped them — Rasa doing the research, LangGraph taking the manager
call — Rasa would need a pre-written flow for every possible venue outcome
(impossible), and LangGraph might negotiate the deposit ("well, it's only
slightly above £300") instead of enforcing it. The architecture matches the
risk profile of each sub-problem.
"""
