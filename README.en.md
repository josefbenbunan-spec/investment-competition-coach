# investment-competition-coach

[Versión en español](README.md)

A Claude skill that coaches and spars with student teams in investment competitions: the Wharton Global High School Investment Competition, the CFA Research Challenge, school stock-market leagues and any contest where a team has to design a strategy or a portfolio for a client from a case study.

The skill's instructions are written in Spanish, but it answers in whatever language the team writes in. When the competition runs in English it uses the English technical terms the judges will expect.

## What it does

- Asks in the chat for the client case, the rules, the deliverables and the competition's AI policy. It does not depend on any particular edition, so it works year after year.
- Builds a client profile with the team, tagging every item as stated in the case, inferred, or pending.
- Walks the team through the phases: understanding the client, the Investment Policy Statement (IPS), asset allocation, security selection, managing the portfolio during the competition, and the final report.
- Works through Socratic questions, stress scenarios and mock judging sessions.
- Checks the team's numbers with a bundled script: required return, weights against the IPS ranges, and performance against the benchmark.
- Does not write text for the deliverables. At the end of each session it produces the AI-use log for the Works Cited and a save point to continue in another chat.

## An example

> **Team:** Write the return objectives section of our IPS for us, we're running late.
>
> **Coach:** That section has to be written by you, it's what the judges are evaluating. I'll help you prepare it. Which of your client's goals has a specific date and amount?

*(Illustrative example of the intended behaviour.)*

## Installation

### Claude (web and desktop)

1. Download `investment-competition-coach.zip` from the [latest release](https://github.com/josefbenbunan-spec/investment-competition-coach/releases/latest).
2. In Claude, open the Skills section, click **+**, then **Create skill** and **Upload a skill**, and upload the ZIP.
3. Make sure code execution is turned on in your settings. The skill uses it to check calculations.

### Claude Code

```bash
git clone https://github.com/josefbenbunan-spec/investment-competition-coach.git
cp -r investment-competition-coach/skills/investment-competition-coach ~/.claude/skills/
```

### With the skills CLI

```bash
npx skills add josefbenbunan-spec/investment-competition-coach
```

## How to use it

Just write something like *"We're in the Wharton investment competition and want to start working on the case"*. The skill will ask for what it needs.

Tip: create a Project in Claude for each competition and upload the case as a file, so you don't have to paste it into every chat.

To try it without a real case, use the made-up case in [`ejemplos/caso-ejemplo.md`](ejemplos/caso-ejemplo.md) (in Spanish). If you change the skill, run the prompts in [`ejemplos/casos-de-prueba.md`](ejemplos/casos-de-prueba.md) to check it still behaves as intended.

## Structure

```
skills/investment-competition-coach/
├── SKILL.md                      # main instructions
├── references/
│   ├── ips-framework.md          # IPS concepts
│   ├── sparring-questions.md     # questions by phase, judge mode, stress scenarios
│   ├── final-report.md           # measuring and explaining results in the final report
│   └── ai-use-log.md             # AI-use log format and save point
├── assets/
│   └── case-intake.md            # client profile template
└── scripts/
    └── check.py                  # calculation checks (standard library only)
ejemplos/
├── caso-ejemplo.md               # made-up case to try the skill
└── casos-de-prueba.md            # prompts to check the skill's behaviour
```

## Disclaimer

Educational tool. Not financial advice. Each team is responsible for following its competition's rules and disclosing AI use as required.
