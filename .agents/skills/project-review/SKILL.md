---

name: project-review
description: Review a Django REST Framework project or selected changes for functional correctness, immediate technical quality, documentation, and significant design issues.
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Project Review

Use this skill when the user explicitly asks for a technical review, project review, code review, consistency check, or pre-commit verification.

The primary objective is to identify real and actionable problems without turning the review into an unnecessarily exhaustive or academic exercise.

Consult `AGENTS.md`, `CARNET_DE_BORD.md`, the current codebase, and the relevant project requirements when evaluating the implementation.

---

## Review Priorities

Review findings in the following order.

### 1. Functional Correctness

Prioritize problems that can prevent the application from working correctly or violate the intended behavior.

Look for:

* non-functional code;
* logical inconsistencies;
* obvious runtime errors;
* broken or missing imports;
* incorrect use of Django or Django REST Framework;
* violations of documented business requirements;
* authorization or security mistakes relevant to the reviewed code;
* immediate regression risks.

These issues take priority over style or refactoring suggestions.

### 2. Immediate Technical Quality

Then identify clear maintainability problems such as:

* unused imports;
* dead code;
* misleading or inconsistent naming;
* duplicated logic when it creates an immediate maintenance problem;
* confusing structure;
* obvious anti-patterns;
* unnecessary complexity;
* violations of established project conventions.

Do not propose refactoring solely for stylistic preference.

### 3. Documentation

Evaluate whether documentation is sufficient where it adds real value.

Look for:

* missing or misleading docstrings;
* documentation that no longer matches behavior;
* complex logic that would benefit from clarification;
* missing explanation of significant non-obvious decisions.

Do not demand comments or docstrings that merely restate obvious code.

### 4. Design Improvements

Finally, identify design improvements only when they provide meaningful value.

Examples include:

* simplification of unnecessarily complex logic;
* clearer separation of responsibilities;
* significant Django or DRF architectural issues;
* important opportunities to use framework-native mechanisms;
* architectural inconsistencies with documented project decisions.

Avoid premature abstraction and unnecessary refactoring.

---

## Project Requirements

When reviewing behavior, distinguish between:

* explicit SoftDesk requirements;
* established architectural decisions;
* professional recommendations;
* optional improvements.

Do not report an optional improvement as though it were a project requirement.

If the implementation conflicts with `CARNET_DE_BORD.md` or the project specification, clearly identify the discrepancy.

If the documentation and implementation disagree, do not silently choose one as correct.

---

## Tests

Do not make automated tests the primary focus of the review unless:

* the user explicitly asks for test review;
* the current project stage requires them;
* the reviewed change creates a significant regression risk;
* or tests are directly relevant to an identified problem.

Tests may be mentioned as a future or supporting improvement without dominating the review.

---

## Review Modes

Adapt the depth of the review to the user's request.

### Full Project Review

Use when the user asks for a broader project consistency or technical review.

Inspect the relevant architecture and code paths rather than reviewing files in isolation.

### Targeted Review

Use when the user asks about a specific feature, file, implementation, or concern.

Keep findings scoped to that request unless an adjacent issue is important enough to affect correctness.

### Pre-Commit Check

Use a lightweight review focused on:

* obvious functional errors;
* accidental code;
* broken imports;
* dead or unused code;
* glaring naming or documentation problems;
* immediate regression risks.

Do not turn a pre-commit check into a full architecture review unless a blocking issue requires it.

---

## Severity

Classify the overall result as one of:

### OK

No significant issue identified. Minor optional improvements may remain.

### Attention

The code is broadly usable, but one or more issues should be considered before continuing or committing.

### Blocking

At least one issue should be corrected before the code is considered functionally or technically safe to continue with.

Do not exaggerate severity.

---

## Expected Output

Structure the review as:

### Verdict

`OK`, `Attention`, or `Blocking`, followed by a concise explanation.

### Blocking Issues

List only genuine blocking issues.

If there are none, state that clearly.

### Secondary Issues

List actionable non-blocking technical problems.

### Improvement Suggestions

Include only improvements that provide meaningful value.

### Documentation

Briefly assess relevant documentation quality.

### Tests

Mention testing only when relevant under the rules above.

Keep findings concise, prioritized, and actionable.

The objective is to help the user move forward without breaking the project.
