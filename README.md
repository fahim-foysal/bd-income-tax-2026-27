# Bangladesh income tax 2026-27 — Claude plugin (directory edition)

> **Tax year 2026-27** (income year 1 July 2025 – 30 June 2026), built on the NBR *Aykor Nirdeshika 2026-2027* and the Finance Act 2026.

This plugin helps an individual taxpayer in Bangladesh work out their income tax and prepare the return on the NBR e-Return portal (etaxnbr.gov.bd). It covers:
- the tax slabs and higher tax-free thresholds for women, people aged 65+, people with disability, third gender and freedom fighters;
- private and government pay-scale salary, rent, agriculture and fisheries, business, capital gains, dividends and firm shares;
- the investment rebate, minimum tax, turnover tax, wealth and car surcharges, car advance tax, and the early-filing incentive or late-filing charge;
- the IT-10B assets statement and IT-10BB living-expense statement, built so the net-wealth reconciliation balances;
- a screen-by-screen walkthrough of the e-Return site.

Just ask Claude something like "How much income tax do I pay for 2026-27? I'm a woman, salary 12 lakh, DPS 1 lakh."

## This edition has no code
Claude computes the tax step by step from the rules in this plugin, and checks its method against the closest of the 32 worked examples printed in the NBR guide. In testing, it matched an exact calculator on 10 of 10 complicated cases. The **full edition**, with a Python calculator that reproduces all 32 guide examples automatically, is on the `main` branch of [fahim-foysal/bd-income-tax-2026-27](https://github.com/fahim-foysal/bd-income-tax-2026-27).

## What it runs and what it sends
- **Runs:** nothing. The plugin contains only instructions (Markdown), rules and examples (JSON) and an icon.
- **Sends:** nothing. No network calls, MCP servers or hooks, and no data is stored. Your documents stay in your Claude conversation.
- When you ask it to help on etaxnbr.gov.bd, Claude never presses the final *Submit Return* without your explicit go-ahead. You log in and pay yourself.

## Privacy
The plugin stores and sends nothing. See the [privacy policy](PRIVACY.md).

## Disclaimer
This is not legal or tax advice. Tax law and the e-Return portal change. You are responsible for the return you sign: check the figures against the official NBR guide, keep your proofs, and consult a tax practitioner for anything complex.

## License
MIT. See [LICENSE](LICENSE).
