#!/usr/bin/env python3
"""Rebuild the `directory` branch: the no-code edition submitted to Anthropic's plugin directory.

The directory accepts scripts only from Verified organizations, so this edition drops
scripts/ and tells Claude to compute by hand, checking itself against the NBR guide's
worked examples (tested: 10 of 10 tricky cases matched the calculator).

Run from anywhere in the repo, after every change to main:
    python3 tools/build_directory.py          # commit on the directory branch
    python3 tools/build_directory.py --push   # ...and push it
"""
import argparse
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

BRANCH = "directory"
SKILL = "skills/bd-income-tax-return"
ALLOWED = {".md", ".json", ".png"}
ALLOWED_NAMES = {"LICENSE", ".gitignore"}

HAND_METHOD = """Then compute by hand, showing every line, in this order (rules and page numbers: `references/rules-2026-27.md`; machine-readable figures: `rules/2026-27.json`):
1. Income by head, exemptions (salary 1/3 or govt pay-scale rule; agriculture/para 20A; listed-gain 50L), income deductions → income at slab rates; special-rate income (dividend, long-term capital gain, gold, developer flat) separately.
2. Slab tax with the category threshold; tax on special-rate income → **gross tax**.
3. Firm-share relief (tax × firm share / slab income); turnover-tax top-up if turnover tax exceeds the slab tax share on business income.
4. Rebate = lowest of 3% of rebate base / 10% of eligible investment (after category caps) / 7.5L, and not more than the tax.
5. Minimum tax (5,000; 1,000 first-time) if income exceeds the threshold.
6. Car advance tax: tax = max(regular tax, car AIT).
7. Surcharge = rate (by net wealth, or 10% for >1 car / big house) × **gross tax before rebate**; plus environmental surcharge on all but the cheapest non-electric car.
8. Less TDS, advance tax, car AIT and environmental surcharge already paid → payable u/s 173.
9. Filing-time incentive / extra on the s.173 payable → net payable or refund.

`examples/nbr-guide-2026-27.json` holds all 32 worked examples from the NBR guide with the figures the guide prints, one per taxpayer type (govt and private employees, landlord, farmer, hatchery owner, capital gains, firm partner, car owners, late filer, doctor, engineer, importer…). Before answering, find the closest example and check that your method reproduces its numbers; if it doesn't, find your mistake first. Use a quick calculation in code if you can run code, and never round away paisa in your working.

"""

README = """# Bangladesh income tax 2026-27 — Claude plugin (directory edition)

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
"""


def git(*args, cwd):
    return subprocess.run(["git", *args], cwd=cwd, check=True, text=True, capture_output=True).stdout.strip()


def replace(text, old, new, where):
    if old not in text:
        raise SystemExit(f"build_directory: expected text not found in {where}: {old[:60]!r}. Update this script.")
    return text.replace(old, new)


def build(src: Path, out: Path):
    # plugin manifest and assets
    (out / ".claude-plugin").mkdir()
    manifest = json.loads((src / ".claude-plugin/plugin.json").read_text())
    manifest["description"] += " No-code edition: Claude computes from the bundled rules and NBR worked examples."
    (out / ".claude-plugin/plugin.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    shutil.copy(src / manifest["icon"], out / manifest["icon"])
    for name in ("LICENSE", ".gitignore", "PRIVACY.md"):
        shutil.copy(src / name, out / name)
    (out / "README.md").write_text(README)

    # skill without scripts/
    shutil.copytree(src / SKILL, out / SKILL, ignore=shutil.ignore_patterns("scripts", "__pycache__", "*.pyc"))
    sk = out / SKILL

    p = sk / "SKILL.md"
    s = p.read_text()
    start = s.find("Then use `scripts/bd_tax_calc.py`")
    end = s.find("Show the result as a table")
    if start < 0 or end < start:
        raise SystemExit("build_directory: Step 4 anchors not found in SKILL.md. Update this script.")
    s = s[:start] + HAND_METHOD + s[end:]
    s = replace(s, "run the calculator, and show the computation table", "compute as in Step 4, and show the computation table", p.name)
    s = replace(s, "json` for the calculator.", "json`.", p.name)
    p.write_text(s)

    p = sk / "references/rules-2026-27.md"
    s = p.read_text()
    s = replace(s, ", and the calculator reproduces every one (`--selftest`).", ".", p.name)
    s = replace(s, "| Category (`category` in the calculator) | Threshold |", "| Category | Threshold |", p.name)
    s = replace(s, ' Calculator: `"govt_pay_scale": true`.', "", p.name)
    s = replace(s, ' Calculator: `other_income` item with `"head": "firm_share"`.', "", p.name)
    s = replace(s, " Calculator: `income_deductions`.", "", p.name)
    s = replace(s, "  - The calculator compares turnover tax with the slab tax share attributable to business income.\n",
                "  - Compare turnover tax with the slab tax share attributable to business income.\n", p.name)
    p.write_text(s)

    p = sk / "examples/nbr-guide-2026-27.json"
    data = json.loads(p.read_text())
    data["_note"] = ("Worked examples from NBR Aykor Nirdeshika 2026-2027 (page in the name). "
                     "'expect' holds the figures the guide prints; 'input' lists each taxpayer's facts.")
    p.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n")

    # nothing the directory treats as code may slip through
    for f in out.rglob("*"):
        if f.is_file() and ".git" not in f.parts and f.suffix not in ALLOWED and f.name not in ALLOWED_NAMES:
            raise SystemExit(f"build_directory: disallowed file {f.relative_to(out)}")
    for f in out.rglob("*"):
        if f.is_file() and f.suffix == ".md" and ("bd_tax_calc" in f.read_text() or "calculator" in f.read_text() and f.name != "README.md"):
            raise SystemExit(f"build_directory: script still mentioned in {f.relative_to(out)}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--push", action="store_true")
    args = ap.parse_args()
    root = Path(git("rev-parse", "--show-toplevel", cwd=Path.cwd()))
    src_rev = git("rev-parse", "--short", "HEAD", cwd=root)
    tmp = Path(tempfile.mkdtemp(prefix="bd-directory-"))
    wt = tmp / "wt"
    if git("remote", cwd=root):
        git("fetch", "-q", "origin", cwd=root)
    branches = git("branch", "-a", "--format=%(refname:short)", cwd=root).split()
    try:
        if BRANCH in branches:
            git("worktree", "add", "-q", str(wt), BRANCH, cwd=root)
        elif f"origin/{BRANCH}" in branches:
            git("worktree", "add", "-q", "-b", BRANCH, str(wt), f"origin/{BRANCH}", cwd=root)
        else:
            git("worktree", "add", "-q", "--detach", str(wt), cwd=root)
            git("checkout", "-q", "--orphan", BRANCH, cwd=wt)
        for item in wt.iterdir():
            if item.name != ".git":
                shutil.rmtree(item) if item.is_dir() else item.unlink()
        stage = tmp / "stage"
        stage.mkdir()
        build(root, stage)
        shutil.copytree(stage, wt, dirs_exist_ok=True)
        git("add", "-A", cwd=wt)
        if not git("status", "--porcelain", cwd=wt):
            print(f"{BRANCH}: already up to date with main@{src_rev}")
        else:
            git("commit", "-q", "-m", f"Directory edition built from main@{src_rev}", cwd=wt)
            print(f"{BRANCH}: committed {git('rev-parse', '--short', 'HEAD', cwd=wt)} from main@{src_rev}")
        if args.push:
            git("push", "-q", "-u", "origin", BRANCH, cwd=wt)
            print(f"{BRANCH}: pushed")
    finally:
        subprocess.run(["git", "worktree", "remove", "--force", str(wt)], cwd=root, capture_output=True)
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
