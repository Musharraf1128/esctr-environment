#!/usr/bin/env python3
"""Generate judge-friendly demo artifacts (trace + mermaid graph)."""

import json
import os

from server.environment import ESCTREnvironment
from server.models import ESCTRAction


def run_baseline_episode(seed: int) -> dict:
    env = ESCTREnvironment()
    env.reset(task_name="adversarial_auditing", seed=seed)
    final = env.step(
        ESCTRAction(
            action_type="submit_financial_decision",
            adjustment_amount=0.0,
            adjustment_reason="Immediate decision without investigation",
        )
    )
    return {
        "type": "baseline",
        "seed": seed,
        "reward": final.reward,
        "metadata": final.metadata,
    }


def run_trained_style_episode(seed: int) -> dict:
    env = ESCTREnvironment()
    env.reset(task_name="adversarial_auditing", seed=seed)
    env.step(ESCTRAction(action_type="query_database", query_parameters={"table": "shipping_logs"}))
    env.step(ESCTRAction(action_type="query_database", query_parameters={"table": "sla_contracts"}))
    env.step(ESCTRAction(action_type="query_database", query_parameters={"table": "warehouse_logs"}))
    env.step(ESCTRAction(action_type="communicate_vendor", message_content="We reject settlement; provide evidence."))

    # Deterministic ground-truth amount for demo artifact generation.
    amount = env._scenario.correct_adjustment  # noqa: SLF001
    final = env.step(
        ESCTRAction(
            action_type="submit_financial_decision",
            adjustment_amount=amount,
            adjustment_reason="Warehouse logs + SLA terms confirm full contractual penalty.",
        )
    )
    return {
        "type": "trained_style",
        "seed": seed,
        "reward": final.reward,
        "metadata": final.metadata,
    }


def main():
    os.makedirs("artifacts", exist_ok=True)
    seed = 42
    baseline = run_baseline_episode(seed)
    trained = run_trained_style_episode(seed)

    with open("artifacts/demo_episode_trace.json", "w", encoding="utf-8") as f:
        json.dump({"baseline": baseline, "trained_style": trained}, f, indent=2)

    mermaid = trained["metadata"].get("action_graph_mermaid", "graph TD\n  A([No graph])")
    with open("artifacts/demo_action_graph.mmd", "w", encoding="utf-8") as f:
        f.write(mermaid + "\n")

    print("Wrote artifacts/demo_episode_trace.json")
    print("Wrote artifacts/demo_action_graph.mmd")


if __name__ == "__main__":
    main()
