# Bangladesh income tax 2026-27 — a Claude skill

> **Tax year 2026-27** (income year 1 July 2025 – 30 June 2026), NBR Aykor Nirdeshika 2026-2027 and Finance Act 2026. For other years, look for the matching repo (`bd-income-tax-<year>`).

A [Claude skill](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview) that helps an individual taxpayer in Bangladesh prepare and submit their income tax return on the NBR e-Return portal (**etaxnbr.gov.bd**). It covers everything from reading your bank statement to downloading your acknowledgement slip.

It was built from a real, successful 2026-27 filing by a salaried software engineer. The screen-by-screen notes come from what actually happened on the live site, including the traps that cost time.

## What it does
- **Reads your documents**: salary certificate, bank statements, DPS / sanchayapatra / mutual fund certificates, donation receipts. It then lists what's still missing.
- **Reviews every bank credit and debit like an auditor**: salary inside the income-year window, interest and the tax deducted from it, remittances, gifts, asset purchases, and unexplained items it should ask you about.
- **Computes your tax exactly** with `scripts/bd_tax_calc.py`, following each step:
  - salary exemption
  - slab tax
  - investment rebate, showing which limit applies
  - minimum tax
  - filing-time incentive or extra charge
  - tax already deducted at source
  - final amount payable or refundable
- **Builds IT-10B (assets & liabilities) and IT-10BB (living expenses)** so the net-wealth reconciliation shows **Difference = 0**.
- **Walks you through every e-Return screen**, with known traps. For example, the site silently strips decimal points and multiplies your figure by 100, and it requires a branch name and a gold weight.
- **Covers after filing**: the acknowledgement slip, the income tax certificate (PSR), revised returns, and what to carry forward to next year.

It's designed to keep your return **accurate**. It will show you every legal way to pay less, such as rebate-eligible investments and where the 3% cap starts to apply, but it won't help hide income or mislabel payments.

## Install

**Claude.ai / Claude desktop app** (code execution must be on)
1. Download `bd-income-tax-return-2026-27.zip` from the [latest release](https://github.com/fahim-foysal/bd-income-tax-2026-27/releases/latest).
2. In Claude, open **Customize → Skills** ([claude.ai/customize/skills](https://claude.ai/customize/skills)), upload the ZIP and switch the skill on.

Team / Enterprise admins can add it once for the whole organisation.

**Claude Code** (as a plugin, gets updates):
```
/plugin marketplace add fahim-foysal/bd-income-tax-2026-27
/plugin install bd-income-tax-return@bd-income-tax
```
Or copy only the skill folder:
```bash
git clone https://github.com/fahim-foysal/bd-income-tax-2026-27
cp -r bd-income-tax-2026-27/skills/bd-income-tax-return ~/.claude/skills/
```

**Claude API:** upload `skills/bd-income-tax-return/` with `POST /v1/skills`, then pass it in `container.skills` together with the code-execution tool. **Agent SDK:** put the folder in your project's `.claude/skills/`. The calculator needs only the Python standard library.

## Use
Start a chat (a Claude Project works well for keeping documents together), attach your salary certificate, bank statement(s) and investment certificates, and say something like:

> Help me file my Bangladesh income tax return for 2026-27. My salary was 65,000 until December and 85,000 after.

To use the calculator directly:
```bash
cd skills/bd-income-tax-return
python scripts/bd_tax_calc.py examples/salaried-2026-27.json --rules rules/2026-27.json
```
See the docstring at the top of the script for the input format.

## Files
All skill files live in `skills/bd-income-tax-return/`; `.claude-plugin/` makes the repo a Claude Code plugin marketplace.
```
SKILL.md                            workflow Claude follows
references/rules-2026-27.md         slabs, exemption, rebate, minimum tax, filing-time rules (NBR guide pages)
references/withholding-tax-2026-27.md  TDS/collection rates an individual meets, gross-up rule
references/etaxnbr-walkthrough.md   every e-Return screen, fields, and traps
references/it10b-reconciliation.md  net-wealth method with a worked example
rules/2026-27.json                  machine-readable rules for the calculator
scripts/bd_tax_calc.py              calculator + IT-10B reconciliation
examples/salaried-2026-27.json      anonymised real case (net payable Tk 1,785.35)
examples/nbr-guide-2026-27.json     all 32 worked examples from the NBR guide (run --selftest)
```

## Keeping it current
Tax rules change every July with the Finance Act. Each tax year gets its own repo name (`bd-income-tax-<year>`) so nobody uses last year's rules by mistake. To add a new year:
1. Copy `rules/2026-27.json` to `rules/<year>.json` and update the slabs, caps and minimum tax from that year's NBR *Aykor Nirdeshika* and Finance Act.
2. Add `references/rules-<year>.md` with page citations.
3. Re-check the walkthrough against the live site, update the year in the `description` of `SKILL.md`, `.claude-plugin/` and this README, and rename the repo.
4. Build the Claude.ai ZIP with `tools/build_zip.sh` and attach it to a GitHub release.

The calculator covers every taxpayer type in the NBR guide's worked examples (thresholds by category, government pay scale, rent, agriculture/para 20A, business and turnover tax, capital gains, dividend, firm share, surcharges, car advance tax, filing-time incentive and late filing). Check it with (from `skills/bd-income-tax-return/`):
```bash
python scripts/bd_tax_calc.py --selftest examples/nbr-guide-2026-27.json --rules rules/2026-27.json
```
Pull requests are welcome, especially more real filings and non-resident cases.

## What it runs and what it sends
- **Runs:** one local Python script, `scripts/bd_tax_calc.py` (standard library only). It reads a JSON file of figures and the rules file in this repo, and prints the computation.
- **Sends:** nothing. The plugin makes no network calls, has no MCP servers or hooks, and does not store your data anywhere. Your documents stay in your Claude conversation.
- **Reads:** only the files you give Claude for the task (salary certificate, bank statements, investment certificates).
- When you ask it to help on etaxnbr.gov.bd, Claude uses its own browser tools and never presses the final *Submit Return* without your explicit go-ahead. You log in and pay yourself.

## Disclaimer
This is not legal or tax advice. It was tested on one real return; tax law and the e-Return portal change. You are responsible for the return you sign: check the figures against the official NBR guide, keep your proofs, and consult a tax practitioner for anything complex.

## License
MIT. See [LICENSE](LICENSE).
