#!/usr/bin/env python3
"""
Run ablation experiments for ESCTR reward/risk analysis.

Variants:
1) base_env                  -> no distractors, no risk shaping
2) distractors_only          -> distractors enabled, risk shaping off
3) distractors_risk_shaping  -> distractors enabled, risk shaping on
"""

import json
import os
import re
from statistics import mean

from server.environment import ESCTREnvironment
from server.models import ESCTRAction


LINE_RE = re.compile(
    r"^(LI-\d+)\s+.*?\s+(\d+)\s+\$([0-9,]+\.\d{2})\s+\$([0-9,]+\.\d{2})$",
    re.MULTILINE,
)


def _to_float(text: str) -> float:
    return float(text.replace(",", ""))


def scripted_procurement_episode(seed: int) -> tuple[float, dict]:
    env = ESCTREnvironment()
    env.reset(task_name="procurement_reconciliation", seed=seed)

    po_summary = env.step(
        ESCTRAction(action_type="query_database", query_parameters={"table": "purchase_orders"})
    )
    inv_summary = env.step(
        ESCTRAction(action_type="query_database", query_parameters={"table": "invoices"})
    )

    po_id = re.search(r"\[PRIMARY\] PO Number: ([A-Z]+-\d{4}-\d{4})", po_summary.system_response)
    inv_id = re.search(r"\[PRIMARY\] Invoice: ([A-Z]+-\d{4}-\d{4})", inv_summary.system_response)
    if not po_id or not inv_id:
        raise RuntimeError("Could not parse primary PO/Invoice IDs from query output.")

    po_doc = env.step(
        ESCTRAction(action_type="read_document", document_id=po_id.group(1))
    )
    inv_doc = env.step(
        ESCTRAction(action_type="read_document", document_id=inv_id.group(1))
    )

    po_rows = {m.group(1): _to_float(m.group(4)) for m in LINE_RE.finditer(po_doc.system_response)}
    inv_rows = {m.group(1): _to_float(m.group(4)) for m in LINE_RE.finditer(inv_doc.system_response)}

    # Slightly biased adjustment to simulate realistic model error and expose risk shaping effects.
    oracle_adjustment = env._scenario.correct_adjustment  # noqa: SLF001
    target_adjustment = round(oracle_adjustment * 0.90, 2)

    final = env.step(
        ESCTRAction(
            action_type="submit_financial_decision",
            adjustment_amount=target_adjustment,
            adjustment_reason=(
                "Noisy adjustment for ablation measurement after full investigation path "
                f"(oracle={oracle_adjustment:.2f}, submitted={target_adjustment:.2f})"
            ),
        )
    )
    return final.reward, final.metadata


def run_variant(name: str, distractors: bool, risk_shaping: bool, seeds: range) -> dict:
    os.environ["ESCTR_ENABLE_DISTRACTORS"] = "1" if distractors else "0"
    os.environ["ESCTR_ENABLE_RISK_SHAPING"] = "1" if risk_shaping else "0"

    rewards = []
    over = []
    under = []
    shortcut = []
    reliance = []
    for seed in seeds:
        score, meta = scripted_procurement_episode(seed)
        rewards.append(score)
        over.append(float(meta.get("risk_over_penalization", 0.0)))
        under.append(float(meta.get("risk_under_penalization", 0.0)))
        shortcut.append(1.0 if meta.get("risk_procedural_shortcut", False) else 0.0)
        reliance.append(1.0 if meta.get("risk_vendor_reliance", False) else 0.0)

    return {
        "variant": name,
        "episodes": len(rewards),
        "mean_reward": round(mean(rewards), 4),
        "mean_over_penalization_risk": round(mean(over), 4),
        "mean_under_penalization_risk": round(mean(under), 4),
        "procedural_shortcut_rate": round(mean(shortcut), 4),
        "vendor_reliance_rate": round(mean(reliance), 4),
    }


def main():
    seeds = range(0, 30)
    results = [
        run_variant("base_env", distractors=False, risk_shaping=False, seeds=seeds),
        run_variant("distractors_only", distractors=True, risk_shaping=False, seeds=seeds),
        run_variant("distractors_risk_shaping", distractors=True, risk_shaping=True, seeds=seeds),
    ]
    os.makedirs("artifacts", exist_ok=True)
    with open("artifacts/ablation_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
