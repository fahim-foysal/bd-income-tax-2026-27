# etaxnbr.gov.bd e-Return — screen-by-screen walkthrough

Recorded from a real salaried-employee filing for tax year 2026-27 (November 2026). Labels may shift slightly between years; if a screen differs, take a screenshot and adapt rather than guessing.

## Contents
1. Before you start
2. Login and choosing the year
3. Assessment
4. Additional information
5. Income: employment, financial assets, exempt income
6. Rebate
7. Donation (6th Schedule)
8. Expenditure (IT-10BB)
9. Assets & Liabilities (IT-10B)
10. Tax & Payment
11. Return View and submit
12. After submission: acknowledgement, PSR certificate
13. Trap list

## 1. Before you start
- The taxpayer needs a **TIN** and a mobile number **biometrically registered to their own NID** (check by dialling 16001). Registration: eReturn → "I am not yet registered" → TIN + mobile (without the leading 0) → OTP → set password.
- If you are driving a browser: the taxpayer types the password/OTP and clicks Sign in themselves. They also make the payment.

## 2. Login and choosing the year
- Dashboard left menu: Home, Submission (Regular e-Return, Revised Return u/s 180(2)), Time Extension, Tax Record.
- **The Assessment Year dropdown (top right) may default to last year.** Switch it to the correct year *before* opening Regular e-Return; a modal asks to confirm ("Change").
- The site may hold a **saved draft** from an earlier session (prefilled salary breakdown, assets, expenses). Read every prefilled value; don't assume it's current.

## 3. Assessment
- Return scheme Self; assessment year and income-year dates prefilled; Resident.
- **Tax Exempted Income — "Any income which is fully exempted from tax?"** Answer Yes only for genuinely exempt income (foreign remittance income, IT/software business, exempt bonds, pension, etc.). The salary 1/3 exemption is NOT entered here — it's computed on the employment screen. Switching Yes→No pops "This action will remove all your exempted income data" — fine if that section is empty.
- Heads of income: tick Income from Employment, Income from Financial Assets (bank interest), and anything else that applies.
- Button: Save & Continue.

## 4. Additional information
- Location of main source of income (city corporation) — minimum tax no longer depends on location for 2026-27.
- Special categories (freedom fighter, disability, third gender, parent of a person with disability).
- **Tax rebate: "Claim tax rebate for investment?"** → Yes if any eligible investment.
- **Donation (6th Schedule Part-2)** → see section 7; answering No later deletes any data there (warning modal).
- IT-10B requirements: gross wealth > 50 lakh? motor car? offshore property? shareholder director? house property? and "IT10B may not be mandatory. Still want to submit?" → **Yes** is recommended for anyone with gifts, gold, investments or a first return — it documents the source of wealth for future years.

## 5. Income
Tabs: Income from Employment · Income from Financial Assets · Tax Exempted Income (only if ticked).

**Employment** (one tab per employer; "Add Employment" for more):
- Employment type: Private / other than government pay scale. Employer name, designation.
- Particulars: Basic Salary, House Rent Allowance, Medical Allowance, Conveyance Allowance, Festival Bonus, "+ Add More" for others. Totals must equal gross receipts for the income year.
- Non-cash benefits: rent-free/concessional accommodation, vehicle, other.
- **Employment Summary** button shows Total, Tax Exempted Amount (1/3 or 5 lakh cap) and Taxable Amount — check it matches your computation.

**Financial assets** → Financial Assets Type: choose "Interest/Profit (Bank/FI)" and click the **green tick** to confirm. Other types: Sanchayapatra interest, treasury bonds, dividend, "Interest from any other securities" (use this for interest received *without* TDS).
- Row fields: Bank/FI name (dropdown), Account type (DPS / FDR / Savings-SND-Others), **Branch name (required — save fails without it)**, Account no, Gross interest, Related fees/charges, TDS, Year-end balance.
- **Whole taka only.** Typing "2683.16" is silently turned into 2,68,316. Enter 2683. Same for every amount field on the site.
- Totals row shows Net Income and Total TDS.

## 6. Rebate
Investment categories with tick boxes:
- Life insurance premium
- **Deposit Pension Scheme (DPS)**: Bank/FI, account no, deposit amount (income-year installments only); allowable amount auto-capped.
- Approved Sanchayapatra & other govt. securities
- **Unit Certificate / Mutual Fund / ETF / Joint Investment Scheme**: Name, account/BO no., issue date, investment amount. Use "Add" for each purchase.
- Listed stocks, GPF, RPF, superannuation, benevolent fund / group insurance, Zakat fund, Universal Pension Scheme
- **Others → Investment under 6th Schedule Part 3 / Investment under SRO** (SRO no., year, description, amount) — approved donations whose receipt cites an SRO go here.
- Footer: Total Actual Investment and Total Allowable Investment for Rebate.

## 7. Donation (6th Schedule) screen
Appears only if answered Yes on Additional Information. Category dropdown is a fixed list (e.g., fund under PMEAT Act 2012, girls' school/college, technical & vocational institute, named foundations, national R&D institutes). Requires receiver bank + account, receipt number/date, *your* bank + account, amount. **Don't enter the same donation here and on the Rebate screen.** If you've used the Rebate/SRO route, go back and answer No.

## 8. Expenditure (IT-10BB)
Rows (amount + comment): Food, clothing and other essentials · Accommodation · Auto & transportation (expandable) · Household & utility (expandable) · Education · Festival & other special (expandable) · Any other expenses · **Tax, charges etc. paid during the income year** (expand: payment of tax at source & advance tax — put bank-interest TDS here; payment of tax/surcharge for last year) · Interest on personal loan · Environmental surcharge.
- The return view may merge "Any other expenses" into the festival line — totals are what matter.
- Donations you gave are NOT here; they go on the Assets page under Other Outflow.

## 9. Assets & Liabilities (IT-10B)
- "Import and Autofill" from last year's submission (for repeat filers).
- **Assets**: business capital; non-agricultural / agricultural property; **financial assets** (shares/debentures/unit certificates: BO/instrument no., acquisition type, broker/AMC, cost value; sanchayapatra; FDR; **DPS** (can "Import from Income"); loans given; provident fund; other); motor car; **Gold, diamond, gems** (particulars, acquisition Purchase/Inheritance/Gift, **quantity — required**, unit Bhori/Tola/Gram/Kg, value at cost); furniture/electronics; other significant assets; **cash & fund outside business** (bank accounts — can import from income; cash in hand); other deposits/advances; assets outside Bangladesh.
- **Liabilities** outside business.
- **Other outflow**: annual living expense (pulled from Expenditure), loss deduction, **gift/donation/contribution given** (particulars, receiver name, receiver TIN, amount).
- **Sources of fund**: income shown in return and tax-exempted income (both auto), **Other receipts** (rows: particulars, reference, amount — gifts from relatives, gift of jewellery, loan received, non-income credits).
- **Net wealth at the last date of previous income year** (first-time filer: what they held on the previous 30 June).
- **Summary**: gross wealth, liabilities, net wealth, previous net wealth, change, other outflow, total outflow, source of fund, **Difference — must be 0**. Saving with a non-zero difference shows "You have shortage of fund, still want to continue?" — you can save the draft, but fix it before filing.
- Unsaved changes are lost if you navigate away; required fields left empty block Save Draft ("Please fill all the required fields").

## 10. Tax & Payment
- Particulars of total income (by head), net total income, tax exempted income.
- Tax computation: gross tax, rebate on investment, tax after rebate, minimum payable tax, surcharges, penalties, **Total Amount Payable**. Click the blue **Save** under the computation.
- Payment block: Source tax (TDS), Advance income tax, Tax paid with return, etc.
- Final payable: total payable, incentive (1st quarter), total payment & adjustments, refundable, **Net Payable**.
- **Pay Now first** (card / MFS / internet banking; generates a challan, e.g. via Sonali Bank) — the taxpayer does this. Afterwards "Tax paid with return" fills in and Net Payable becomes 0. The page may reopen in a new tab.
- Only then "Proceed to online return".

## 11. Return View and submit
Return View shows the complete IT-11GA, Schedule 1 (salary), Schedule 5 (rebate), IT-10BB, IT-10B, sources-of-fund attachment, financial-asset attachment and tax-payment attachment (challan no., status VERIFIED). Read it through with the taxpayer, then **Submit Return** only on their explicit instruction. Download the acknowledgement receipt.

## 12. After submission
- Tax Record menu: TIN certificate, **Income Tax Certificate** (PSR — custom criteria tick boxes add Total Income / Net Wealth / Paid Tax to the certificate; Download button), acknowledgement receipt, final return view, challan history, archive. Choose the assessment year in the top dropdown first.
- Mistake found? Submission → Revised Return u/s 180(2), within 180 days.

## 13. Trap list
1. Assessment year dropdown on the wrong year.
2. Old draft values silently prefilled.
3. Decimal points stripped → amounts ×100. Enter whole taka.
4. Branch name required for bank interest rows.
5. Gold quantity required; record value at cost, weight from the receipt (or derived from the BAJUS rate on the purchase date if the receipt is lost).
6. Exempt-income / donation Yes→No toggles delete that section's data.
7. Donation counted twice (Rebate SRO and 6th Schedule).
8. Cash spent on an asset (e.g., part of a gold purchase paid in cash) must be removed from living expenses, or the IT-10B shows a shortage.
9. Paying after submitting, or submitting with Net Payable > 0.
10. Native dropdowns: if automated selection doesn't stick, click the select, type the option's first letters, press Enter.
