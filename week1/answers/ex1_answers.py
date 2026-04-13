"""
Exercise 1 — Answers
====================
Fill this in after running exercise1_context.py.
Run `python grade.py ex1` to check for obvious issues before submitting.
"""

# ── Part A ─────────────────────────────────────────────────────────────────

# The exact answer the model gave for each condition.
# Copy-paste from your terminal output (the → "..." part).

PART_A_PLAIN_ANSWER    = "The Haymarket Vaults"
PART_A_XML_ANSWER      = "The Albanach"
PART_A_SANDWICH_ANSWER = "The Albanach"

# Was each answer correct? True or False.
# Correct = contains "Haymarket" or "Albanach" (both satisfy all constraints).

PART_A_PLAIN_CORRECT    = True
PART_A_XML_CORRECT      = True
PART_A_SANDWICH_CORRECT = True

# Explain what you observed. Minimum 30 words.

PART_A_EXPLANATION = """
All three formatting conditions produced correct answers on the baseline dataset
using Llama 3.3 70B. The plain condition returned Haymarket Vaults while XML and
sandwich both returned The Albanach — two valid venues that both satisfy the 160+
capacity, vegan, and available constraints. No structural formatting effect was
visible at this signal-to-noise ratio.
"""

# ── Part B ─────────────────────────────────────────────────────────────────

PART_B_PLAIN_ANSWER    = "The Haymarket Vaults"
PART_B_XML_ANSWER      = "The Albanach"
PART_B_SANDWICH_ANSWER = "The Albanach"

PART_B_PLAIN_CORRECT    = True
PART_B_XML_CORRECT      = True
PART_B_SANDWICH_CORRECT = True

# Did adding near-miss distractors change any results? True or False.
PART_B_CHANGED_RESULTS = False

# Which distractor was more likely to cause a wrong answer, and why?
# Minimum 20 words.
PART_B_HARDEST_DISTRACTOR = """
The Holyrood Arms (capacity=160, vegan=yes, status=full) is the harder distractor
because it matches every positive criterion — right capacity, has vegan options —
and only fails on status=full. A model skimming the list could easily overlook
the status field and select it as the answer.
"""

# ── Part C ─────────────────────────────────────────────────────────────────

# Did the exercise run Part C (small model)?
# Check outputs/ex1_results.json → "part_c_was_run"
PART_C_WAS_RUN = True

PART_C_PLAIN_ANSWER    = "Haymarket Vaults"
PART_C_XML_ANSWER      = "The Haymarket Vaults"
PART_C_SANDWICH_ANSWER = "The Haymarket Vaults"

# Explain what Part C showed, or why it wasn't needed. Minimum 30 words.
PART_C_EXPLANATION = """
Part C ran automatically because both Part A and Part B were all-correct on the
70B model. Gemma 2 2B also answered correctly across all three conditions, though
it used a slightly less formal answer in PLAIN mode ("Haymarket Vaults" vs "The
Haymarket Vaults"). The exercise shows that even a 2B model handles this
particular dataset correctly — the signal-to-noise ratio is still high enough.
The structural formatting effect described by Liu et al. (2023) requires either
a longer context, more distractors, or a task where the answer is buried in the
middle of a large document to reliably manifest.
"""

# ── Core lesson ────────────────────────────────────────────────────────────

# Complete this sentence. Minimum 40 words.
# "Context formatting matters most when..."

CORE_LESSON = """
Context formatting matters most when the signal-to-noise ratio in the prompt is
low — that is, when the correct answer is surrounded by near-miss distractors,
buried in the middle of a long context, or when the model is small and less capable
of attending to distant tokens. On a short, clean list with a strong model like
Llama 3.3 70B, all three formats performed identically. The effect becomes visible
only when the task is genuinely hard: multiple plausible-looking but wrong
candidates, large context windows, or weaker models that struggle with positional
attention. This means agent engineers should invest in careful context structure
not for toy benchmarks but for real production prompts where the model must
distinguish between many similar-looking options.
"""
