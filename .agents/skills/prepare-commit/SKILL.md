---
name: prepare-commit
description: Analyze Git changes, propose coherent staging boundaries, and prepare professional Conventional Commit messages without modifying Git state unless explicitly approved.
---

# Prepare Commit

Use this skill when the user asks to prepare, organize, split, or review changes before creating a Git commit.

The purpose of this workflow is to help produce coherent commits and professional Conventional Commit messages while preserving explicit user control over Git operations.

## Commit Convention

Use the following format:

```text
type(scope): short imperative description

Concise explanation of the purpose of the commit.

- Important change 1
- Important change 2
- Important change 3
```

### Types

Use an appropriate Conventional Commit type, such as:

* `feat`
* `fix`
* `refactor`
* `style`
* `docs`
* `test`
* `chore`

### Scope

Use the relevant Django application, module, or meaningful project area as the scope.

### Subject

The subject must:

* be written in English;
* be short and precise;
* use the imperative mood;
* describe the actual purpose of the commit;
* avoid vague wording.

The body should explain the purpose and rationale of the commit, not merely repeat filenames or implementation details.

---

## Workflow

### 1. Inspect the changes

Inspect the relevant Git state before making recommendations.

Read-only Git commands may be used when useful, including:

```text
git status
git diff
git diff --cached
git log
```

Do not modify repository state during inspection.

### 2. Identify logical groups

Determine whether the changes belong to one coherent concern.

Group changes by logical purpose rather than by file.

A single file may contain changes belonging to different commits, and several files may belong to the same commit.

### 3. Detect mixed concerns

If unrelated concerns are mixed together, do not force them into a single commit.

Instead:

* identify the logical groups;
* explain the proposed split;
* indicate which changes belong to each group;
* recommend interactive staging when appropriate.

Prefer small, coherent commits that each represent one understandable change.

### 4. Prepare commit messages

For each proposed commit, provide a Conventional Commit message following the project convention.

The message must reflect the true objective of the changes.

Avoid:

* vague subjects;
* unnecessarily technical wording;
* implementation-only descriptions;
* combining unrelated concerns.

### 5. Wait for user validation

After presenting the proposed grouping and commit message or messages, wait for the user's decision.

Do not automatically stage or commit changes.

---

## Git Safety

The following operations require explicit user approval before execution:

* `git add`
* `git restore`
* `git reset`
* `git commit`
* `git merge`
* `git rebase`
* `git push`
* any other command that changes repository state or history.

Never discard user changes without explicit confirmation.

---

## Expected Output

When relevant, provide:

1. assessment of whether the current changes form one coherent commit;
2. proposed logical grouping;
3. recommended split if necessary;
4. commit message for each group;
5. concise technical clarification when needed.

If the current staged diff is already coherent, avoid inventing unnecessary splits.

The priority is clarity, logical cohesion, and safe human-controlled Git usage.
