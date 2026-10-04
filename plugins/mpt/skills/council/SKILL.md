---
name: council
description: Run a model-pinned five-advisor Codex Council using five independent GPT-5.6 Luna subagents at max reasoning and fast service, followed by GPT-5.6 Sol at max reasoning for evidence-aware synthesis. Use for councils, panels, debates, option selection, difficult decisions, plans, comparisons, content review, business validation, messy-note organization, learning plans, or other recommendations that benefit from distinct perspectives and explicit disagreement.
---

# Council

Produce a practical answer only after a strict five-advisor review. The council is a decision process, not theater: gather independent briefs, verify the completion gate, then let Sol resolve disagreement and synthesize one recommendation.

## Runtime Contract

For every explicit `$council` invocation:

1. Freeze one task packet containing the user request, goal, constraints, known evidence, as-of date when relevant, and authorization boundaries.
2. Dispatch exactly five fresh advisor threads. Use the `luna_worker` agent type when available, or an equivalent explicitly pinned profile with:
   - model: `gpt-5.6-luna`
   - reasoning effort: `max`
   - service tier: `fast`
3. Give every advisor the same frozen task packet plus only its role-specific emphasis. Do not fork the full conversation, reveal another advisor's output, or let advisors debate each other.
4. Wait for all five terminal results. If the runtime cannot run five advisors concurrently, run them in waves without changing their prompts or sharing earlier results.
5. Retry one failed advisor once with the same role and runtime profile. If any unique role still lacks a valid terminal result, report `Failed Council`; do not silently simulate, substitute another model, or present a partial run as a full council.
6. After the five-of-five completion gate passes, synthesize with `gpt-5.6-sol` at `max` reasoning. Use the parent when it is already pinned to that profile; otherwise spawn a dedicated Sol synthesizer when the runtime supports explicit model selection.
7. If Luna/max/fast or Sol/max is unavailable, state the missing capability and stop the full Council workflow instead of weakening the contract silently.

Advisor threads inherit the parent's sandbox, approval, network, MCP, and skill access. Do not request broader permissions merely to improve an opinion. Keep advisory work read-only unless the original user request explicitly authorizes a scoped mutation and the parent assigns it.

## Advisor Roles

- Strategist: test long-term direction, strategic fit, opportunity cost, and second-order effects.
- Skeptic: falsify assumptions, expose blind spots, and describe downside and failure cases.
- Creative: find alternative frames, unconventional options, and sharper formulations within the constraints.
- Operator: turn the goal into executable sequencing, resources, dependencies, validation, and rollback steps.
- Audience Advocate: represent the customer, user, reader, employee, or investor; test trust, clarity, objections, and usability.

Keep the roles non-overlapping. When research is needed, assign distinct evidence lanes or questions instead of asking all five advisors to perform the same search.

## Advisor Prompt And Result

Give each advisor a self-contained prompt containing:

- its assigned role and unique emphasis;
- the frozen task packet;
- relevant source or tool instructions;
- a prohibition on reading peer outputs or writing shared Council artifacts;
- the required result schema.

Require every advisor to use the following literal English field labels exactly once. Write the field values in the user's language, but do not translate, rename, merge, or omit the labels:

- `role`
- `status`
- `recommendation`
- `key reasons`
- `risks`
- `assumptions`
- `facts vs inference`
- `evidence/sources`
- `confidence`
- `what would change my mind`
- `skills/tools used`
- `data limits`

Use `status: complete` when the brief is usable, even if its conclusion is uncertain. Use `status: limited` when the available data constrains the brief, and explain the limitation. A dispatch error, timeout, malformed result, duplicate role, or wrong runtime profile does not pass the completion gate.

## Completion Gate

Before Sol synthesis, confirm:

- exactly five distinct advisor threads returned terminal results;
- every required role appears exactly once;
- every advisor used the Luna/max/fast profile;
- no advisor received a peer's output before finishing;
- every result follows the required schema and records data limits;
- material claims have evidence or are explicitly labeled as inference.

Do not treat repeated use of the same source as independent corroboration. Do not use advisor votes as a truth metric.

## Sol Verification And Synthesis

Give Sol the original task packet and all five completed briefs only after the gate passes. Sol must:

1. identify the strongest evidence and arguments;
2. surface real disagreement and trace it to assumptions, goals, or evidence;
3. recheck material conflicts and time-sensitive claims with appropriate tools or primary sources;
4. distinguish verified facts, inference, and unresolved uncertainty;
5. choose the recommendation that best fits the goal and constraints rather than averaging opinions;
6. preserve important minority warnings and state what would invalidate the recommendation.

For financial, legal, medical, safety-critical, technical, or current product decisions, verify current facts before answering. For financial outputs, state that the result is research support rather than personal investment advice and include invalidation and risk controls.

## Recipes

Read `references/council-recipes.md` when the request matches a reusable prompt type. A recipe shapes the content only; it never changes the five-Luna completion gate or the Sol synthesis contract.

## Output Shape

Use this structure unless a recipe requires additional fields:

```markdown
**Conclusion**
[one practical answer]

**Council Notes**
| Advisor | View | Evidence | Confidence | Skills/Tools Used |
|---|---|---|---|---|

**Disagreement**
[where advisors differ, why, and which assumptions matter]

**Sol Verification**
[verified facts, unresolved claims, and material data limits]

**Final Recommendation**
[ranked or direct answer, including invalidation conditions]

**Next Steps**
1. [first action]
2. [second action]
3. [third action]

**Runtime Ledger**
[five Luna terminal results, Sol synthesis profile, and any retries or limits]
```

## Quality Rules

- Start with the conclusion.
- Keep advisor notes brief; do not create fictional dialogue.
- Prefer explicit tradeoffs over vague balance.
- Separate facts from inference and show uncertainty when data is incomplete.
- Preserve meaningful disagreement instead of forcing consensus.
- Use the user's language unless asked otherwise.
- Never describe model output as consciousness or guaranteed truth.
- Never claim `Full Council` unless the five-of-five gate and Sol synthesis both completed.
