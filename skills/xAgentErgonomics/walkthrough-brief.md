# Walkthrough brief — TEMPLATE

Copy to the scratchpad, one copy per task. Replace <REPO>, <TASK> and <REPORT_PATH>. Add
nothing else: no answer key, no diagnosis, no other task. The agent must start with only what
the repository gives every new session.

# Operator task — <REPO>

You operate the system in <REPO>. You know only what the repository tells you. Do one task,
then report how you did it.

## Rules
- **Do not change the repository.** No Edit or Write on any file in <REPO>.
- **Run only commands that the repository states are read-only, and `--help`.** For any other
  command, write the command and the output that would decide the task, then stop.
- A command the documents mark as planned does not exist. Say so. Do not run it.
- **Read nothing outside <REPO>** except this file.
- Bash: no `$()`, no `cd X &&`, no `VAR=` prefixes.
- Mark each guess as a guess.

## Task
<TASK>

## Report
Write these sections to <REPORT_PATH>, then reply with the path only.

1. **Answer.** Your answer, then `sure` or `guess`.
2. **Path.** Each file read and each command run, in order, one line each, with the reason.
3. **Missing.** Each thing you looked for and did not find, and the place you looked first.
4. **Names.** Each concept with two names, and each name whose meaning you had to infer.
5. **Cost.** Each command you did not run because you could not tell its cost or its effect.
