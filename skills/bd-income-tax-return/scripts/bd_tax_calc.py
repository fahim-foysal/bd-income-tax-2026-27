#!/usr/bin/env python3
"""Bangladesh individual income tax calculator + IT-10B reconciliation.

Usage:
    python bd_tax_calc.py taxpayer.json --rules ../rules/2026-27.json [--json]
    python bd_tax_calc.py --selftest ../examples/nbr-guide-2026-27.json --rules ../rules/2026-27.json

Input (taxpayer.json). All amounts in taka, paisa allowed. Every key is optional.
{
  "category": "general",          # general | woman | senior (65+) | disabled | third_gender
                                  # | freedom_fighter | july_fighter  -> tax-free threshold
  "disabled_dependents": 0,       # +50,000 threshold per disabled child (only ONE parent claims)
  "first_time_filer": false,      # minimum tax 1,000 instead of 5,000
  "filing_date": "2026-11-25",    # incentive / extra charge; after the deadline = late (s.174)
  "notice_212": false,            # late return filed after a s.212(1) notice (15% / 10,000)

  "employment": [
    {"employer": "Acme", "receipts": 900000, "tds": 0},
      # private: ALL receipts incl. perquisites; 1/3 (max 5L) exemption is applied here
    {"employer": "Ministry", "govt_pay_scale": true, "receipts": 791000,
     "exempt_allowances": 29300, "tds": 0}
      # govt pay scale (SRO 225/2023): receipts = basic + festival + other bonus only;
      # listed allowances are exempt and there is NO 1/3 exemption
  ],
  "rent": [
    {"annual_rent": 1440000, "commercial": false, "let_fraction": 0.6667,
     "municipal_tax": 24000, "land_revenue": 900, "loan_interest": 30000, "insurance": 0,
     "adjustable_advance_closing": 1280000, "nonrefundable_premium": 0, "tds": 0}
  ],
  "agriculture": 0,               # net agricultural income (crops, dairy, nursery ...)
  "agro_20a": 0,                  # net income from 6th Sch. para 20A activities (poultry,
                                  # fish/shrimp hatchery, feed, seed, dairy products, sericulture)
  "business": [
    {"description": "Shop", "net_income": 662000, "turnover": 4500000,
     "turnover_rate": "default", "tds": 0}
  ],
  "other_income": [               # slab-rate income: interest, sanchayapatra interest, tuition ...
    {"head": "financial_assets", "description": "Bank interest", "amount": 2683.16, "tds": 402.48},
    {"head": "firm_share", "amount": 300000},       # gets the average-rate relief
    {"description": "...", "amount": 0, "tds": 0, "final_tax": true}  # only for truly final
                                                    # deductions (s.163(3)/(4)); tax = TDS
  ],
  "special_rate_income": [        # kind: dividend | cg_long (held >5y) | cg_short (slab)
    {"kind": "dividend", "amount": 100000, "tds": 10000}   # | cg_developer_flat
  ],                                                       # | cg_gold_jewellery | cg_listed_securities
  "income_deductions": [ {"description": "Center for Zakat Management", "amount": 70000} ],
  "exempt_income": [ {"description": "Pension", "amount": 360000} ],
  "advance_tax": 0,
  "investments": [                # made inside the income year only
    {"category": "dps", "amount": 75000},           # caps from rules: dps, sanchayapatra
    {"category": "mutual_fund", "amount": 103109}
  ],
  "net_wealth": 0,                # closing net wealth from IT-10B (surcharge)
  "house_over_8000_sqft": false,
  "tobacco_income": 0,            # income from making tobacco products (2.5% surcharge)
  "cars": [ {"cc": 2000}, {"kw": 400, "electric": true}, {"type": "microbus"} ],
  "car_ait_paid": null,           # default: assume the table AIT was paid at fitness renewal
  "env_surcharge_paid": null,     # default: assume paid with the fitness renewal
  "wealth": {                     # optional IT-10B reconciliation
    "opening_net_wealth": 191499,
    "assets": [ {"description": "Bank", "amount": 116960} ],
    "liabilities": [],
    "other_receipts": [ {"description": "Gift from parents", "amount": 102000} ],
    "lifestyle_expenses": [ {"description": "Rent", "amount": 300000} ],   # include tax paid
    "other_outflows": [ {"description": "Donation", "amount": 3400} ]
  }
}
If "lifestyle_expenses" is omitted, the script prints the expense total that balances IT-10B.
"""
import argparse
import json
from datetime import date
from decimal import Decimal, ROUND_HALF_UP

D = lambda x: Decimal(str(x))
P2 = Decimal("0.01")
ZERO = Decimal(0)


def r2(x):
    return x.quantize(P2, rounding=ROUND_HALF_UP)


def fmt(x):
    """Bangladeshi digit grouping: 12,34,567.89"""
    x = r2(D(x))
    neg = x < 0
    whole, frac = f"{abs(x):.2f}".split(".")
    if len(whole) > 3:
        head, tail = whole[:-3], whole[-3:]
        groups = []
        while len(head) > 2:
            groups.insert(0, head[-2:])
            head = head[:-2]
        if head:
            groups.insert(0, head)
        whole = ",".join(groups + [tail])
    return ("-" if neg else "") + whole + "." + frac


def total(items, key="amount"):
    return sum((D(x.get(key, 0)) for x in items), ZERO)


def band(value, table):
    """Look up [[upper_limit_or_null, amount], ...] (limits inclusive)."""
    for limit, amt in table:
        if limit is None or value <= D(limit):
            return D(amt)


def slab_tax(income, slabs):
    tax, remaining, lines = ZERO, income, []
    for width, rate in slabs:
        if remaining <= 0:
            break
        part = remaining if width is None else min(remaining, D(width))
        t = part * D(rate)
        lines.append((part, rate, t))
        tax += t
        remaining -= part
    return tax, lines


def quarter_key(d):
    return {7: "jul-sep", 8: "jul-sep", 9: "jul-sep", 10: "oct-dec", 11: "oct-dec", 12: "oct-dec",
            1: "jan-mar", 2: "jan-mar", 3: "jan-mar", 4: "apr-jun", 5: "apr-jun", 6: "apr-jun"}[d.month]


def car_charges(cars, rules):
    """Advance tax on private cars (s.153) and environmental surcharge."""
    ca = rules["car_ait"]
    ait = []
    for c in cars:
        if c.get("type") in ("microbus", "double_cabin"):
            ait.append(D(ca["microbus_or_double_cabin"]))
        elif "kw" in c:
            ait.append(band(D(c["kw"]), ca["kw"]))
        else:
            ait.append(band(D(c["cc"]), ca["cc"]))
    # every car beyond the first pays 50% more; the guide's example leaves the cheapest one at base
    order = sorted(range(len(ait)), key=lambda i: ait[i])
    for i in order[1:]:
        ait[i] *= 1 + D(ca["extra_car_pct"])
    # environmental surcharge: ICE cars only (EVs exempt from 1 July 2026), all but the cheapest
    env = sorted(band(D(c["cc"]), rules["env_surcharge_cc"])
                 for c in cars if not c.get("electric") and "cc" in c)
    return sum(ait, ZERO), sum(env[1:], ZERO)


def compute(tp, rules):
    notes = []
    fdate = date.fromisoformat(tp["filing_date"]) if tp.get("filing_date") else None
    late = bool(fdate and fdate > date.fromisoformat(rules["return_deadline"]))

    # --- Threshold
    cat = tp.get("category", "general")
    threshold = D(rules["thresholds"][cat]) + D(rules["disabled_dependent_extra"]) * tp.get("disabled_dependents", 0)
    slabs = [[threshold, 0]] + rules["slabs"][1:]

    # --- Employment
    emp = tp.get("employment", [])
    priv = total([e for e in emp if not e.get("govt_pay_scale")], "receipts")
    govt = total([e for e in emp if e.get("govt_pay_scale")], "receipts")
    se = rules["salary_exemption"]
    emp_exempt = r2(min(priv * D(se["fraction"]), D(se["cap"])))
    govt_exempt = total(emp, "exempt_allowances")
    emp_taxable = priv - emp_exempt + govt
    tds = total(emp, "tds")

    # --- Rent (s.35-39)
    rr = rules["rent"]
    rent_income = ZERO
    for p in tp.get("rent", []):
        rent = D(p["annual_rent"])
        repairs = rent * D(rr["repairs_commercial" if p.get("commercial") else "repairs_residential"])
        costs = sum((D(p.get(k, 0)) for k in ("municipal_tax", "land_revenue", "loan_interest", "insurance")), ZERO)
        special = D(p.get("adjustable_advance_closing", 0)) * D(rr["adjustable_advance_pct"]) + D(p.get("nonrefundable_premium", 0))
        rent_income += rent - repairs - costs * D(p.get("let_fraction", 1)) + special
        tds += D(p.get("tds", 0))
    rent_income = r2(rent_income)

    # --- Business / profession
    biz = tp.get("business", [])
    biz_income = total(biz, "net_income")
    tds += total(biz, "tds")
    turnover_tax = r2(sum((D(b.get("turnover", 0)) * D(rules["turnover_tax"][b.get("turnover_rate", "default")])
                           for b in biz), ZERO))

    # --- Other slab income, firm share, final-tax income
    slab_other = firm = final_income = final_tax = ZERO
    for o in tp.get("other_income", []):
        amt, t = D(o["amount"]), D(o.get("tds", 0))
        if o.get("final_tax"):
            final_income += amt
            final_tax += t
        else:
            slab_other += amt
            firm += amt if o.get("head") == "firm_share" else ZERO
            tds += t

    # --- Special-rate income (Seventh Schedule)
    special_tax = special_income = cg_short = ZERO
    listed_exempt = ZERO
    for s in tp.get("special_rate_income", []):
        amt, kind = D(s["amount"]), s["kind"]
        tds += D(s.get("tds", 0))
        if kind == "cg_short":
            cg_short += amt
            continue
        if kind == "cg_listed_securities":
            ex = min(amt, D(rules["listed_securities_gain_exempt"]) - listed_exempt)
            listed_exempt += ex
            amt -= ex
        special_income += amt
        special_tax += amt * D(rules["special_rates"][kind])
    special_tax = r2(special_tax)

    # --- Agriculture (6th Sch. Part 1 para 20 / 20A). Both are lost on a late return (s.174(4)).
    agri, agro = D(tp.get("agriculture", 0)), D(tp.get("agro_20a", 0))
    non_fin = total([o for o in tp.get("other_income", []) if o.get("head") != "financial_assets"])
    only_agri = not (emp or tp.get("rent") or biz or non_fin or agro or cg_short or special_income)
    agri_ex = min(agri, D(rules["agriculture_exemption"])) if only_agri and not late else ZERO
    agro_ex = min(agro, D(rules["agro_20a_exemption"])) if not late else ZERO
    if late and (agri or agro):
        notes.append("Late return: the agriculture / para 20A exemptions are lost (s.174(4)).")
    if late and tp.get("exempt_income"):
        notes.append("Late return: only 6th Sch. Part 1 paras 1,4,5,6,7,8,17,35 and the salary exemption survive; "
                     "check each exempt_income item and move lost ones to other_income.")

    deductions = total(tp.get("income_deductions", []))
    slab_income = max(ZERO, emp_taxable + rent_income + biz_income + slab_other + cg_short
                      + agri - agri_ex + agro - agro_ex - deductions)
    total_income = slab_income + special_income + final_income

    slab_t, slab_lines = slab_tax(slab_income, slabs)
    slab_t = r2(slab_t)
    gross_tax = slab_t + special_tax   # surcharge base (guide applies it before rebate)

    firm_relief = r2(slab_t * firm / slab_income) if firm and slab_income else ZERO
    turnover_extra = ZERO
    if turnover_tax and slab_income:
        biz_share = r2(slab_t * biz_income / slab_income)
        if turnover_tax > biz_share:
            turnover_extra = turnover_tax - biz_share
            notes.append(f"Turnover tax {fmt(turnover_tax)} exceeds the slab tax on business income "
                         f"{fmt(biz_share)}; the difference is added.")
    tax_before_rebate = gross_tax - firm_relief + turnover_extra

    # --- Rebate (s.78)
    rb = rules["rebate"]
    caps = rb.get("category_caps", {})
    by_cat = {}
    for inv in tp.get("investments", []):
        by_cat[inv["category"]] = by_cat.get(inv["category"], ZERO) + D(inv["amount"])
    allowable = {c: (min(v, D(caps[c])) if c in caps else v) for c, v in by_cat.items()}
    eligible = sum(allowable.values(), ZERO)
    rebate_base = slab_income - firm      # excludes exempt, reduced-rate, firm-share, final-tax income
    limb_a, limb_b, limb_c = r2(rebate_base * D(rb["income_pct"])), r2(eligible * D(rb["investment_pct"])), D(rb["absolute_cap"])
    rebate = min(limb_a, limb_b, limb_c)
    binding = {limb_a: "3% of income", limb_b: "10% of investment", limb_c: "absolute cap"}[rebate]
    rebate = min(rebate, max(ZERO, tax_before_rebate))
    tax_after_rebate = tax_before_rebate - rebate

    # --- Minimum tax
    mt = rules["minimum_tax"]
    min_tax = D(mt["first_time_filer"] if tp.get("first_time_filer") else mt["regular"])
    applies_min = slab_income + special_income > threshold
    regular_tax = max(tax_after_rebate, min_tax) if applies_min else tax_after_rebate

    # --- Cars: advance tax is a floor (excess not refunded), env. surcharge on extra cars
    cars = tp.get("cars", [])
    car_ait, env = car_charges(cars, rules)
    income_tax = max(regular_tax, car_ait)
    if car_ait > regular_tax:
        notes.append(f"Car advance tax {fmt(car_ait)} exceeds regular tax {fmt(regular_tax)}: the car AIT is the tax, the excess is not refundable.")

    # --- Net-wealth surcharge
    su = rules["surcharge"]
    nw = D(tp.get("net_wealth", 0))
    s_rate = band(nw, su["wealth_bands"])
    if s_rate == 0 and (len(cars) > 1 or tp.get("house_over_8000_sqft")):
        s_rate = D(su["multi_car_or_big_house_rate"])
    surcharge = r2(gross_tax * s_rate + D(tp.get("tobacco_income", 0)) * D(su["tobacco_income_pct"]))

    total_tax = income_tax + final_tax + surcharge + env
    car_paid = D(tp["car_ait_paid"]) if tp.get("car_ait_paid") is not None else car_ait
    env_paid = D(tp["env_surcharge_paid"]) if tp.get("env_surcharge_paid") is not None else env
    credits = tds + final_tax + D(tp.get("advance_tax", 0)) + car_paid + env_paid
    base_173 = total_tax - credits

    # --- Filing-time adjustment, on the s.173 payable (after TDS / advance tax)
    adj, adj_note = ZERO, "no filing date given"
    if fdate:
        key = ("late_after_notice" if tp.get("notice_212") else "late") if late else quarter_key(fdate)
        ft = rules["filing_time"][key]
        if ft["type"] == "none":
            adj_note = f"{key}: no incentive or extra"
        elif base_173 <= 0:
            adj_note = f"{key}: nothing payable u/s 173, so no {ft['type']} computed (check with the guide)"
        elif ft["type"] == "incentive":
            adj = -min(r2(base_173 * D(ft["pct"])), D(ft["cap"]))
            adj_note = f"{key}: incentive {ft['pct']*100:.0f}% (max {fmt(ft['cap'])})"
        else:
            adj = max(r2(base_173 * D(ft["pct"])), D(ft["floor"]))
            adj_note = f"{key}: extra, higher of {ft['pct']*100:.0f}% or {fmt(ft['floor'])}"
    net = base_173 + adj

    out = dict(
        category=cat, threshold=threshold, late=late,
        employment_receipts=priv + govt, employment_exempt=emp_exempt, govt_exempt_allowances=govt_exempt,
        employment_taxable=emp_taxable, rent_income=rent_income, business_income=biz_income,
        agriculture=agri, agriculture_exempt=agri_ex, agro_20a=agro, agro_20a_exempt=agro_ex,
        other_slab_income=slab_other, firm_share=firm, cg_short=cg_short, deductions=deductions,
        special_income=special_income, listed_gain_exempt=listed_exempt, final_tax_income=final_income,
        slab_income=slab_income, total_income=total_income,
        slab_lines=slab_lines, slab_tax=slab_t, special_tax=special_tax, gross_tax=gross_tax,
        firm_relief=firm_relief, turnover_tax=turnover_tax, turnover_extra=turnover_extra,
        investments=by_cat, allowable=allowable, eligible_investment=eligible,
        rebate_limbs=dict(a=limb_a, b=limb_b, c=limb_c), rebate=rebate, rebate_binding=binding,
        tax_after_rebate=tax_after_rebate, minimum_tax=min_tax, minimum_applies=applies_min,
        regular_tax=regular_tax, car_ait=car_ait, income_tax=income_tax, final_tax=final_tax,
        surcharge_rate=s_rate, surcharge=surcharge, env_surcharge=env, total_tax=total_tax,
        credits=credits, payable_173=base_173, filing_adjustment=adj, filing_note=adj_note, net=net,
        investment_to_reach_cap=(max(ZERO, r2(min(limb_a, limb_c, tax_before_rebate) / D(rb["investment_pct"])) - eligible)
                                 if tax_before_rebate > 0 else ZERO),
        notes=notes,
    )

    # --- IT-10B reconciliation
    w = tp.get("wealth")
    if w:
        exempt_total = emp_exempt + govt_exempt + agri_ex + agro_ex + listed_exempt + total(tp.get("exempt_income", []))
        sources = total_income + deductions + exempt_total + total(w.get("other_receipts", []))
        closing = total(w.get("assets", [])) - total(w.get("liabilities", []))
        change = closing - D(w.get("opening_net_wealth", 0))
        outflow_other = total(w.get("other_outflows", []))
        if "lifestyle_expenses" in w:
            lifestyle = total(w["lifestyle_expenses"])
            diff = sources - lifestyle - outflow_other - change
        else:
            lifestyle, diff = sources - outflow_other - change, ZERO
        out["wealth"] = dict(sources=sources, closing_net_wealth=closing, change=change, lifestyle=lifestyle,
                             other_outflows=outflow_other, difference=diff,
                             lifestyle_given="lifestyle_expenses" in w)
    return out


def report(o, rules):
    L = [f"# Tax computation — tax year {rules['tax_year']}\n",
         f"Category: {o['category']} (tax-free threshold {fmt(o['threshold'])})"
         + (" — LATE RETURN (s.174)" if o["late"] else "") + "\n",
         "| Step | Amount (Tk) |\n|---|---|"]
    row = lambda label, v: L.append(f"| {label} | {fmt(v)} |")
    if o["employment_receipts"]:
        row("Employment receipts (taxable components)", o["employment_receipts"])
        if o["employment_exempt"]:
            row("Less salary exemption (lower of 1/3 or 5,00,000)", -o["employment_exempt"])
        row("Taxable employment income", o["employment_taxable"])
    if o["rent_income"]:
        row("Income from house property", o["rent_income"])
    if o["business_income"]:
        row("Business / profession income", o["business_income"])
    if o["agriculture"]:
        row(f"Agriculture (exempt {fmt(o['agriculture_exempt'])})", o["agriculture"] - o["agriculture_exempt"])
    if o["agro_20a"]:
        row(f"Para 20A income (exempt {fmt(o['agro_20a_exempt'])})", o["agro_20a"] - o["agro_20a_exempt"])
    if o["other_slab_income"]:
        row("Other income at slab rates" + (f" (incl. firm share {fmt(o['firm_share'])})" if o["firm_share"] else ""),
            o["other_slab_income"])
    if o["cg_short"]:
        row("Capital gain held ≤ 5 years (slab)", o["cg_short"])
    if o["deductions"]:
        row("Less income deductions", -o["deductions"])
    row("Income at slab rates", o["slab_income"])
    if o["special_income"]:
        row("Special-rate income (dividend / capital gain)"
            + (f", after {fmt(o['listed_gain_exempt'])} listed-gain exemption" if o["listed_gain_exempt"] else ""),
            o["special_income"])
    if o["final_tax_income"]:
        row("Final-tax income (tax = TDS)", o["final_tax_income"])
    L.append(f"| **Total income** | **{fmt(o['total_income'])}** |")
    for part, rate, t in o["slab_lines"]:
        row(f"Slab: {fmt(part)} @ {rate*100:.0f}%", t)
    if o["special_tax"]:
        row("Tax on special-rate income", o["special_tax"])
    row("Gross tax", o["gross_tax"])
    if o["firm_relief"]:
        row("Less average-rate relief on firm share", -o["firm_relief"])
    if o["turnover_extra"]:
        row(f"Add turnover-tax top-up (turnover tax {fmt(o['turnover_tax'])})", o["turnover_extra"])
    a = o["rebate_limbs"]
    row("Eligible investment (after category caps)", o["eligible_investment"])
    row(f"Rebate = lowest of 3% income {fmt(a['a'])} / 10% investment {fmt(a['b'])} / cap {fmt(a['c'])} → {o['rebate_binding']}",
        -o["rebate"])
    row("Tax after rebate", o["tax_after_rebate"])
    row(f"Minimum tax {fmt(o['minimum_tax'])} ({'applies' if o['minimum_applies'] else 'n/a — income within threshold'}) → regular tax",
        o["regular_tax"])
    if o["car_ait"]:
        row("Car advance tax (floor)", o["car_ait"])
    if o["final_tax"]:
        row("Tax on final-tax income (= TDS)", o["final_tax"])
    if o["surcharge"]:
        row(f"Surcharge ({o['surcharge_rate']*100:.0f}% of gross tax, + tobacco 2.5% if any)", o["surcharge"])
    if o["env_surcharge"]:
        row("Environmental surcharge", o["env_surcharge"])
    row("Total tax", o["total_tax"])
    row("Less TDS / advance tax / car AIT paid", -o["credits"])
    row("Payable u/s 173", o["payable_173"])
    row(f"Filing-time adjustment ({o['filing_note']})", o["filing_adjustment"])
    label = "**Net payable**" if o["net"] >= 0 else "**Refundable**"
    L.append(f"| {label} | **{fmt(abs(o['net']))}** |")
    for n in o["notes"]:
        L.append(f"\n- {n}")
    if o["gross_tax"] <= 0:
        L.append("\nNo tax arises at slab rates, so investments don't change anything this year.")
    elif o["investment_to_reach_cap"] > 0:
        L.append(f"\nMore eligible investment of {fmt(o['investment_to_reach_cap'])} (within the income year) would still cut tax; beyond that the cap binds.")
    else:
        L.append("\nThe rebate is at its limit: more investment would not reduce tax this year.")
    w = o.get("wealth")
    if w:
        L.append("\n# IT-10B reconciliation\n\n| | Tk |\n|---|---|")
        L.append(f"| Sources of fund | {fmt(w['sources'])} |")
        L.append(f"| Closing net wealth | {fmt(w['closing_net_wealth'])} |")
        L.append(f"| Change in net wealth | {fmt(w['change'])} |")
        L.append(f"| Other outflows (gifts/donations given) | {fmt(w['other_outflows'])} |")
        if w["lifestyle_given"]:
            L.append(f"| Lifestyle expenses (IT-10BB) | {fmt(w['lifestyle'])} |")
            L.append(f"| **Difference (must be 0)** | **{fmt(w['difference'])}** |")
        else:
            L.append(f"| **Lifestyle expenses that balance the statement** | **{fmt(w['lifestyle'])}** |")
    return "\n".join(L)


def selftest(path, rules):
    """Run the NBR guide's worked examples and compare with the published figures."""
    with open(path) as f:
        cases = json.load(f)["cases"]
    bad = 0
    for c in cases:
        o = compute(c["input"], rules)
        for k, want in c["expect"].items():
            got = r2(o[k])
            ok = abs(got - D(want)) <= 1   # guide rounds to whole taka
            bad += not ok
            print(f"{'ok ' if ok else 'BAD'} {c['name']}: {k} = {fmt(got)} (guide {fmt(want)})")
    print(f"\n{len(cases)} cases, {bad} mismatches")
    return bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("taxpayer", nargs="?")
    ap.add_argument("--rules", required=True)
    ap.add_argument("--json", action="store_true", help="print raw numbers as JSON")
    ap.add_argument("--selftest", metavar="CASES", help="check against the guide's worked examples")
    args = ap.parse_args()
    with open(args.rules) as f:
        rules = json.load(f)
    if args.selftest:
        raise SystemExit(1 if selftest(args.selftest, rules) else 0)
    with open(args.taxpayer) as f:
        tp = json.load(f)
    o = compute(tp, rules)
    if args.json:
        def conv(x):
            if isinstance(x, Decimal):
                return str(r2(x))
            if isinstance(x, dict):
                return {k: conv(v) for k, v in x.items()}
            if isinstance(x, (list, tuple)):
                return [conv(v) for v in x]
            return x
        print(json.dumps(conv(o), indent=2))
    else:
        print(report(o, rules))


if __name__ == "__main__":
    main()
