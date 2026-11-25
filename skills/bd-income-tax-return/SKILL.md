---
name: bd-income-tax-return
description: Calculate Bangladesh individual income tax for tax year 2026-27 (NBR rules) and prepare the e-Return. Use for any BD income tax, TIN, e-Return, rebate, IT-10B or "how much tax" question in taka.
---

# Bangladesh Income Tax Return (individual, e-Return)

This skill helps a resident individual taxpayer in Bangladesh produce an **accurate** return and file it on **etaxnbr.gov.bd**. It was built from a real end-to-end filing; the gotchas in `references/etaxnbr-walkthrough.md` are things that actually went wrong on the live site.

The deliverable is a filed return, or — when you can't operate the site — a complete, field-by-field filing sheet the taxpayer can type in themselves.

**Just a tax calculation?** If the person only wants to know how much tax they owe (a quick estimate, a "what if I invest more", a comparison), skip the filing workflow: ask the questions in Step 4 that change the answer, run the calculator, and show the computation table. Offer the full return prep afterwards in one line.

## When this applies
Bangladesh income tax, NBR, e-Return, etaxnbr, TIN, a tax return ("aykor", "ritarn"), salary tax in BDT, DPS or sanchayapatra rebate, IT-10B, IT-10BB, PSR / income tax certificate, or "how much tax do I owe" with taka or lakh figures — even for a quick estimate. It covers slabs and higher thresholds (women, 65+, disabled, third gender, freedom fighters), private and government pay-scale salary, rent, agriculture/fisheries, business, capital gains, dividend, firm share, investment rebate, minimum and turnover tax, surcharges, car advance tax, filing-time incentive or late charge, and the IT-10B/IT-10BB reconciliation.

## Ground rules (read first)

**Accuracy over a lower number.** Taxpayers often ask to "adjust" figures so tax comes out under some target, to drop an income item, or to relabel an employer payment as a gift. Don't do that: the bank statement, employer, banks and asset managers report to NBR, and a mismatch costs the taxpayer tax plus penalty later. Instead, show every *legal* lever (below) and its exact effect, and say plainly where the floor is. If the taxpayer states a fact that changes the treatment (e.g., "that transfer was from my parents"), you can record it — but point out the evidence that would have to back it up (sending account, a signed gift note) and that the declaration on the return is theirs.

Legal levers worth checking every time:
- Eligible investments made **within the income year** with proper certificates (DPS, sanchayapatra, listed shares / mutual funds, life insurance premium, provident fund, approved donations, zakat fund).
- The rebate is capped at 3% of income — once the 10%-of-investment figure reaches the 3% cap, more investment saves nothing. Tell the user where that point is.
- A payment made on or before 30 June but processed later (e.g., mutual fund units allotted in July): the certificate normally puts it in the next year. Claiming it in the current year on a bank receipt is arguable but risky; it must never be claimed in both years. Lay out both options.
- Items that are genuinely not employment income (business travel reimbursements actually spent, employer group insurance premium) — only with employer documentation.
- Filing timing incentives/penalties for the year (see rules file).

**Not legal advice.** Say once, briefly, that you're not a tax lawyer and the taxpayer signs the declaration. Don't repeat it.

**Browser safety when filling the live site.** The taxpayer logs in (password + OTP) and makes the payment themselves. You may fill screens and click Save/Continue once they've agreed, but never the final **Submit Return** without an explicit, current "submit" from them.

## Step 1 — Pin down the tax year and this year's rules

The tax law changes every July via the Finance Act. Income year = 1 July – 30 June; the return is for the *assessment/tax year* that follows (income Jul 2025–Jun 2026 → tax year 2026-27).

- Load `references/rules-2026-27.md` if the year matches. For any other year, do not reuse those numbers: look for that year's NBR "Aykor Nirdeshika" (return guide) and Finance Act, web-search the slab/threshold changes, and write a new `rules/<year>.json` for the calculator.
- The NBR guide is in Bengali and often extracts as garbled Bijoy-font text. Don't guess from garbled text — cite page numbers the user can check, or use rules the user confirms.

## Step 2 — Intake: collect documents, then list what's missing

Ask for (and read) whatever exists; don't calculate until gaps are listed:

| Need | Why |
|---|---|
| TIN; NID-linked mobile number; first return or not | Login OTP; minimum tax differs for first-time filers |
| Salary certificate / payslips | Gross vs net, components, TDS, PF |
| Statements of **every** bank account for the income year (ideally a month either side) | Salary, interest + TDS, investments, asset purchases, unexplained credits, year-end balances |
| Investment certificates (DPS, sanchayapatra, mutual fund/BO, insurance, donation receipts) | Rebate; check dates fall inside the year |
| Last year's return / IT-10B (if any) | Opening net wealth |
| Assets held on 30 June: gold (weight), cash, MFS (bKash/Nagad) balances, vehicles, property, loans given/taken | IT-10B |
| Rough living costs: rent, family support, utilities, education, travel | IT-10BB |
| Any freelance / YouTube / foreign income, rent, business | Other heads; check current exemptions before treating anything as exempt |

## Step 3 — Read the bank statement like an auditor

Work through every credit and large debit and classify it. Typical findings:
- **Salary credits** — filter by the income-year window using the *credit date* (a June salary paid on 19 June belongs to the year that June ends). Confirm gross vs net with the user.
- **Festival bonuses** — they are employment income if paid by the employer, even when the salary statement omits them.
- **Interest and TDS** — banks post interest half-yearly with a matching "Tax on Int." debit. 15% instead of 10% usually means the bank lacks the TIN; credit the actual amount and tell the user to submit their TIN.
- **Any other deduction at source** (fees, honoraria, land sale, gold sold to a dealer, dividends, lottery): check the rate and gross up "tax-free" payments with `references/withholding-tax-2026-27.md`.
- **Foreign remittance + 2.5% government incentive** — ask what it was (salary from abroad? freelance? gift?). Each is treated differently.
- **Transfers to/from people** — gifts, loans given/repaid, family support, rent. These don't change tax but must make the IT-10B reconcile.
- **Asset purchases** ("gold payment", transfers to an AMC/broker, DPS installments).
- **Unexplained credits** — ask; never assume income or non-income.

Ask the user about each unclear item in one batch, with dates and amounts, so they can answer quickly.

## Step 4 — Compute the tax

Before computing, settle the facts that change the answer, because the rules differ a lot between taxpayers. Ask in one batch, and only about what you don't already know:
- **Category** — woman, 65+, disabled, third gender, gazetted war-wounded freedom fighter / July fighter, or parent of a disabled child (raises the tax-free threshold from Tk 4L up to 5.5L).
- **Employer type** — on a government pay scale (incl. state-owned banks)? Then only basic + festival/bonus is taxable and there is *no* 1/3 exemption. Otherwise all receipts count and 1/3 (max 5L) is exempt.
- **First return ever?** (minimum tax 1,000 instead of 5,000.)
- **Filing date** — early filing earns an incentive; January onwards adds an extra charge; after 30 June it's a late return that also loses agriculture/freelance-type exemptions.
- Other heads: rent, agriculture or para 20A (poultry, hatchery, feed…), business turnover, capital gains (holding period!), dividends, firm share.
- **Net wealth, number of cars (cc / kW, electric?), house over 8,000 sq ft** — these trigger surcharge, car advance tax and environmental surcharge.

Then use `scripts/bd_tax_calc.py` (reads a JSON of figures plus `rules/<year>.json`) so the arithmetic is exact and reproducible:

```bash
python scripts/bd_tax_calc.py taxpayer.json --rules rules/2026-27.json
```

See the docstring at the top of the script for the input format. It prints:
income by head → exemptions → total income → slab and special-rate tax → firm-share relief / turnover-tax top-up → rebate (with which limb binds) → minimum tax → car AIT floor → surcharges → less TDS/advance tax → s.173 payable → filing-time adjustment → net payable/refundable, plus any notes and the IT-10B reconciliation.

`examples/nbr-guide-2026-27.json` holds all 32 worked examples from the NBR guide, one per taxpayer type (govt and private employees, landlord, farmer, hatchery owner, capital gains, firm partner, car owners, late filer, doctor, engineer, importer…). When a case looks unusual, find the closest example there and model the input on it. After editing a rules file or the script, run `--selftest` on that file; every case must still match.

Show the result as a table with the rule/page cited for each line, and never round away paisa in your own working (the e-Return itself only accepts whole taka — round only when entering).

## Step 5 — Build IT-10B and IT-10BB so they reconcile

Read `references/it10b-reconciliation.md`. The identity the e-Return enforces is:

> Net wealth (end) − Net wealth (start) = Total income + exempt income + gifts/other receipts − lifestyle expenses − other outflows (gifts/donations given, losses)

The Summary block on the Assets page shows a **Difference** that must be 0. Cash in hand is a legitimate balancing figure only within reason — prefer the user's real estimate. For first-time filers the opening net wealth is simply what they held on the previous 30 June.

## Step 6 — File on etaxnbr.gov.bd

Follow `references/etaxnbr-walkthrough.md` screen by screen. It lists every screen, the fields, and the traps (decimal points silently stripped, required branch name, gold quantity, assessment-year dropdown, exempt-income toggles that delete data, donation double-counting, pay-before-submit).

Order: Assessment → Additional info → Income (employment, financial assets, exempt) → Rebate → (Donation 6th Schedule) → Expenditure → Assets & Liabilities → Tax & Payment (Save, then the user pays) → Return View (review with the user) → user says submit → acknowledgement.

## Step 7 — After filing

- Download the **acknowledgement slip** and keep the **challan**.
- **Income tax certificate (PSR)**: Tax Record → Income Tax Certificate. Custom criteria can add Total Income / Net Wealth / Paid Tax. Available later too.
- Revised return u/s 180(2) is possible within 180 days if something was wrong.
- Write a short carry-forward note: closing net wealth (next year's opening), investments paid this year but certified next year (claim once only), DPS installments that fall in the next year, TIN to give the bank.
- List the proofs to keep: statements, certificates, receipts, gift notes, rent proof, challan, acknowledgement.
