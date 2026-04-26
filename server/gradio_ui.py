"""
Interactive Gradio UI for the ESCTR Environment.

Tabbed layout inspired by NetOps — clean, professional, information-dense.
Tabs: Overview · Playground · Training · About
"""

import gradio as gr
import random
from .environment import ESCTREnvironment
from .models import ESCTRAction


# ── Theming ──────────────────────────────────────────────────────────────────

THEME = gr.themes.Soft(
    primary_hue=gr.themes.colors.indigo,
    secondary_hue=gr.themes.colors.emerald,
    neutral_hue=gr.themes.colors.slate,
    font=gr.themes.GoogleFont("Inter"),
    font_mono=gr.themes.GoogleFont("JetBrains Mono"),
)

CSS = """
/* ── Global ─────────────────────────────────────────────── */
.gradio-container {
    background: linear-gradient(135deg, #e0e7ff 0%, #dbeafe 30%, #e0f2fe 60%, #ecfdf5 100%) !important;
    max-width: 960px !important;
    margin: 0 auto !important;
}
.main-header {
    text-align: center;
    padding: 2rem 1rem 1rem;
}
.main-header h1 {
    font-size: 2.2rem;
    font-weight: 800;
    color: #1e293b;
    margin-bottom: 0.25rem;
    letter-spacing: -0.02em;
}
.main-header .subtitle {
    font-size: 1.05rem;
    color: #64748b;
    font-style: italic;
    margin-bottom: 0.5rem;
}
.main-header .links {
    font-size: 0.85rem;
    color: #94a3b8;
}
.main-header .links a {
    color: #6366f1;
    text-decoration: none;
    margin: 0 0.5rem;
}
.main-header .links a:hover {
    text-decoration: underline;
}

/* ── Tabs ─────────────────────────────────────────────── */
.tabs > .tab-nav {
    justify-content: center !important;
    border-bottom: none !important;
    gap: 0.25rem !important;
    padding: 0.5rem 0 !important;
}
.tabs > .tab-nav > button {
    border: 1px solid #cbd5e1 !important;
    border-radius: 6px !important;
    padding: 0.5rem 1.25rem !important;
    font-weight: 500 !important;
    background: white !important;
    color: #475569 !important;
    font-size: 0.9rem !important;
}
.tabs > .tab-nav > button.selected {
    border-color: #6366f1 !important;
    color: #4f46e5 !important;
    font-weight: 600 !important;
    background: #eef2ff !important;
}

/* ── Content area ───────────────────────────────────── */
.tab-content {
    background: white;
    border-radius: 12px;
    padding: 2rem;
    margin: 0.5rem 0;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
}
.prose { max-width: 720px; margin: 0 auto; line-height: 1.75; color: #334155; }
.prose h2 { color: #1e293b; font-weight: 700; margin-top: 2rem; }
.prose h3 { color: #334155; font-weight: 600; }
.prose a { color: #6366f1; }
.prose code { background: #f1f5f9; padding: 0.15em 0.35em; border-radius: 4px; font-size: 0.85em; }
.prose table { width: 100%; border-collapse: collapse; margin: 1rem 0; }
.prose th { background: #f8fafc; text-align: left; padding: 0.6rem; border-bottom: 2px solid #e2e8f0; font-weight: 600; }
.prose td { padding: 0.5rem 0.6rem; border-bottom: 1px solid #f1f5f9; }

/* ── Playground ────────────────────────────────────── */
.log-box textarea { font-family: 'JetBrains Mono', monospace !important; font-size: 0.82rem !important; }
.reward-big { font-size: 2.5rem !important; font-weight: 800 !important; text-align: center !important; }
.tool-btn { min-height: 44px !important; }

/* ── Metric cards ──────────────────────────────────── */
.metric-card {
    background: linear-gradient(135deg, #eef2ff, #e0e7ff);
    border-radius: 12px;
    padding: 1.25rem;
    text-align: center;
}
.metric-card .value { font-size: 1.8rem; font-weight: 800; color: #4f46e5; }
.metric-card .label { font-size: 0.8rem; color: #64748b; margin-top: 0.25rem; }

/* ── Plot images ────────────────────────────────────── */
.plot-img img { border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
"""


# ── Overview Tab Content ─────────────────────────────────────────────────────

OVERVIEW_MD = """
<div class="prose">

## ESCTR: Enterprise Supply Chain & Tax Reconciliation

> *Training LLMs to be autonomous financial auditors — powered by Reinforcement Learning with Verifiable Rewards (RLVR)*

Every day, enterprises process millions of procurement transactions. Between Purchase Orders,
shipping manifests, SLA contracts, and vendor invoices — discrepancies are inevitable.
Resolving them means humans manually cross-referencing siloed databases, interpreting
contract clauses, and performing precise arithmetic under pressure.

**ESCTR** frames this as a reinforcement learning problem. The agent operates as a
financial controller, armed with four ERP tools, navigating a multi-step audit pipeline
against adversarial vendors — graded by mathematically precise, verifiable reward signals.

### Three Tasks, Escalating Stakes

| Task | Difficulty | What the Agent Must Do |
|------|-----------|----------------------|
| **Procurement Reconciliation** | 🟢 Easy | Identify overcharged line items, calculate exact overcharge |
| **SLA Enforcement** | 🟡 Medium | Discover late shipments, retrieve SLA contract, compute penalty |
| **Adversarial Auditing** | 🔴 Hard | All above *plus* disprove vendor counter-claims using warehouse logs |

### Four ERP Tools

- `query_database` — search purchase orders, invoices, shipping logs, SLA contracts, warehouse logs
- `read_document` — retrieve the full text of any document by ID
- `communicate_vendor` — negotiate with an adversarial vendor that lies, deflects, and offers bad settlements
- `submit_financial_decision` — submit the final adjustment (terminal action, ends the episode)

### Reward Design

```
R_total = α · R_outcome + β · R_trajectory − penalties
```

- **R_outcome** (60–70%): Did the agent submit the *exact* correct adjustment?
- **R_trajectory** (30–40%): Did the agent follow proper investigative procedure?
- **Penalties**: Step costs, hallucination, accepting bad settlements

Every scenario is **procedurally generated from a seed** — infinite training configurations with
deterministic, reproducible grading. No memorization possible.

---

*Use the **Playground** tab to try the environment interactively, or see **Training** for results from three model runs.*

</div>
"""


# ── Training Tab Content ─────────────────────────────────────────────────────

TRAINING_MD = """
<div class="prose">

## Training: Three Models, Three GPUs, One Reward Signal

We trained three models using **TRL's GRPOTrainer** with `environment_factory`,
iterating across model sizes from 0.6B to 4B — following the approach of
**small models + fast iteration**.

### 🚀 Qwen3-4B (Production Model)

Trained on RTX 4090 (24GB VRAM) with 4-bit QLoRA. After overcoming "zero-reward collapse"
through **shaped investigation rewards** and **high-temperature exploration (T=1.5)**, the model
achieved:

| Metric | Value |
|--------|-------|
| Peak Reward | **0.27** (vs 0.09 baseline) |
| Tool Calls/Episode | Converged to **4.0** |
| Tool Failures | **0** across 300 episodes |
| Training Time | **71.3 minutes** |

### 🔄 Qwen3-1.7B (HF Jobs — In Progress)

Running on HuggingFace infrastructure (T4-medium), confirming reward architecture transfers cleanly:

| Step | Loss | Reward | Tool Calls | Entropy |
|------|------|--------|------------|---------|
| 5 | 0.184 | **0.195** | **3.9** | 0.132 |
| 10 | 0.116 | 0.195 | **3.9** | 0.127 |
| 15 | 0.088 | 0.180 | 3.6 | 0.028 |
| 20 | 0.186 | 0.190 | 3.8 | 0.047 |

### ✅ Qwen3-0.6B (Proof of Concept)

Initial validation: reward improved from **0.09 → 0.30** (+222%) over 500 episodes on T4 GPU.

</div>
"""


# ── About Tab Content ────────────────────────────────────────────────────────

ABOUT_MD = """
<div class="prose">

## Technical Summary

| Parameter | 0.6B Run | 4B Run | 1.7B Run |
|-----------|----------|--------|----------|
| Model | Qwen/Qwen3-0.6B | Qwen/Qwen3-4B | Qwen/Qwen3-1.7B |
| GPU | T4 (Colab) | RTX 4090 (RunPod) | T4 (HF Jobs) |
| Quantization | None | 4-bit QLoRA | 4-bit QLoRA |
| Adapter | Full model | LoRA (r=16) | LoRA (r=16) |
| Episodes | 500 | 300 | 500 (ongoing) |
| Training Time | ~2 hours | ~71 minutes | ~7 hours |
| Framework | TRL GRPOTrainer | TRL GRPOTrainer | TRL GRPOTrainer |

## Links

- 🏢 [Live Environment](https://huggingface.co/spaces/musharraf7/esctr-environment)
- 📝 [Blog Post](https://huggingface.co/spaces/musharraf7/esctr-environment/blob/main/Blog.md)
- 📊 [Training Dashboard (Trackio)](https://huggingface.co/spaces/musharraf7/esctr-grpo-trained)
- 💻 [Source Code (GitHub)](https://github.com/Musharraf1128/esctr-environment)
- 🏋️ Training Scripts:
  [train.py](https://huggingface.co/spaces/musharraf7/esctr-environment/blob/main/train.py) ·
  [train_4b.py](https://huggingface.co/spaces/musharraf7/esctr-environment/blob/main/train_4b.py) ·
  [train_hf_jobs.py](https://huggingface.co/spaces/musharraf7/esctr-environment/blob/main/train_hf_jobs.py)

## Why This Matters

ESCTR demonstrates that **RLVR can teach LLMs enterprise-grade financial reasoning** — a
domain nearly absent from existing RL training benchmarks.

Unlike game environments, our environment tests capabilities that exist in production:

- **Real-world professional skills** — procurement auditing, SLA enforcement, dispute resolution
- **Adversarial reasoning** — vendor negotiation with active deception
- **Verifiable, precise rewards** — exact answers from contract mathematics
- **Production integration** — the tool interface could plug into SAP or Oracle

---

*Built for the [OpenEnv Hackathon](https://github.com/meta-pytorch/OpenEnv) by Musharraf.*

</div>
"""


# ── State management ─────────────────────────────────────────────────────────

def create_env():
    return ESCTREnvironment()


def reset_episode(task_name, seed_text):
    """Reset the environment with a task and seed."""
    env = create_env()
    seed = int(seed_text) if seed_text.strip() else random.randint(0, 99999)
    obs = env.reset(task_name=task_name, seed=seed)

    log = f"{'='*60}\n"
    log += f"  🏢 ESCTR — New Episode\n"
    log += f"  Task: {task_name} | Seed: {seed}\n"
    log += f"{'='*60}\n\n"
    log += f"📋 BRIEFING:\n{obs.system_response}\n\n"
    log += f"{'─'*60}\n"

    status = f"⏳ Step 0 | Reward: 0.00 | Investigating..."

    return (
        env, log, "0.00", status, str(seed), 0,
        gr.update(interactive=True),
        gr.update(interactive=True),
        gr.update(interactive=True),
        gr.update(interactive=True),
    )


def execute_tool(env, log, step_count, action_type, **kwargs):
    """Execute a tool action and update the log."""
    if env is None:
        return env, log + "\n⚠️ Please reset the environment first!\n", "0.00", "Not started", step_count

    try:
        action = ESCTRAction(action_type=action_type, **kwargs)
        obs = env.step(action)
    except Exception as e:
        log += f"\n❌ ERROR: {str(e)}\n"
        return env, log, "0.00", "Error", step_count

    step_count += 1
    reward = obs.reward
    done = obs.done

    param_str = ", ".join(f'{k}="{v}"' for k, v in kwargs.items() if v)
    log += f"\n🔧 Step {step_count}: {action_type}({param_str})\n"
    log += f"{'─'*40}\n"

    response = obs.system_response
    if len(response) > 1500:
        response = response[:1500] + "\n... [truncated]"
    log += f"{response}\n"
    log += f"{'─'*40}\n"

    if done:
        log += f"\n{'='*60}\n"
        log += f"  ✅ EPISODE COMPLETE\n"
        log += f"  Final Reward: {reward:.4f}\n"
        log += f"  Steps Used: {step_count}\n"
        log += f"{'='*60}\n"
        status = f"✅ Done in {step_count} steps | Final Reward: {reward:.4f}"
    else:
        status = f"⏳ Step {step_count} | Reward: {reward:.4f} | Investigating..."

    return env, log, f"{reward:.4f}", status, step_count


def query_db(env, log, step_count, table):
    if not table:
        log += "\n⚠️ Select a table.\n"
        return env, log, "0.00", "Select a table", step_count
    return execute_tool(env, log, step_count, "query_database", query_parameters={"table": table})


def read_doc(env, log, step_count, doc_id):
    if not doc_id.strip():
        log += "\n⚠️ Enter a document ID.\n"
        return env, log, "0.00", "Enter ID", step_count
    return execute_tool(env, log, step_count, "read_document", document_id=doc_id.strip())


def contact_vendor(env, log, step_count, message):
    if not message.strip():
        log += "\n⚠️ Enter a message.\n"
        return env, log, "0.00", "Enter message", step_count
    return execute_tool(env, log, step_count, "communicate_vendor", message_content=message.strip())


def submit_decision(env, log, step_count, amount, reason):
    try:
        amt = float(amount)
    except (ValueError, TypeError):
        log += "\n⚠️ Enter a valid numeric amount.\n"
        return env, log, "0.00", "Invalid amount", step_count
    if not reason.strip():
        reason = "Financial adjustment based on investigation"
    return execute_tool(env, log, step_count, "submit_financial_decision",
                        adjustment_amount=amt, adjustment_reason=reason.strip())


# ── Build UI ─────────────────────────────────────────────────────────────────

PLOT_BASE = "https://raw.githubusercontent.com/Musharraf1128/esctr-environment/main/plots"

def build_gradio_app():
    with gr.Blocks(title="ESCTR Environment") as demo:

        # Hidden state
        env_state = gr.State(None)
        step_counter = gr.State(0)

        # ── Header ────────────────────────────────────────────
        gr.HTML("""
        <div class="main-header">
            <h1>🏢 ESCTR</h1>
            <div class="subtitle">Enterprise Supply Chain & Tax Reconciliation</div>
            <div class="links">
                OpenEnv Hackathon 2026 ·
                <a href="https://huggingface.co/spaces/musharraf7/esctr-environment/blob/main/Blog.md" target="_blank">Blog</a> ·
                <a href="https://github.com/Musharraf1128/esctr-environment" target="_blank">GitHub</a> ·
                <a href="https://huggingface.co/spaces/musharraf7/esctr-grpo-trained" target="_blank">Training Dashboard</a>
            </div>
        </div>
        """)

        # ── Tabs ──────────────────────────────────────────────
        with gr.Tabs():

            # ── Tab 1: Overview ───────────────────────────────
            with gr.Tab("Overview"):
                gr.HTML(OVERVIEW_MD)

            # ── Tab 2: Playground ─────────────────────────────
            with gr.Tab("Playground"):
                with gr.Row():
                    # Left: Controls
                    with gr.Column(scale=1):
                        gr.Markdown("### 🎮 Episode Controls")

                        task_dropdown = gr.Dropdown(
                            choices=[
                                ("🟢 Procurement Reconciliation", "procurement_reconciliation"),
                                ("🟡 SLA Enforcement", "sla_enforcement"),
                                ("🔴 Adversarial Auditing", "adversarial_auditing"),
                            ],
                            value="procurement_reconciliation",
                            label="Task",
                        )
                        seed_input = gr.Textbox(
                            label="Seed (empty = random)",
                            placeholder="e.g., 42",
                            value="",
                        )
                        reset_btn = gr.Button("🔄 Start New Episode", variant="primary", size="lg")

                        gr.Markdown("---")
                        gr.Markdown("### 🔧 Tools")

                        with gr.Accordion("📊 Query Database", open=True):
                            db_table = gr.Dropdown(
                                choices=["purchase_orders", "invoices", "shipping_logs", "sla_contracts", "warehouse_logs"],
                                label="Table", value="purchase_orders",
                            )
                            query_btn = gr.Button("Run Query", elem_classes="tool-btn")

                        with gr.Accordion("📄 Read Document", open=False):
                            doc_id_input = gr.Textbox(label="Document ID", placeholder="PO-2025-1234")
                            read_btn = gr.Button("Read Document", elem_classes="tool-btn")

                        with gr.Accordion("💬 Contact Vendor", open=False):
                            vendor_msg = gr.Textbox(label="Message", placeholder="We reject your settlement...", lines=2)
                            vendor_btn = gr.Button("Send Message", elem_classes="tool-btn")

                        with gr.Accordion("⚖️ Submit Decision", open=False):
                            adj_amount = gr.Textbox(label="Adjustment ($)", placeholder="-450.00")
                            adj_reason = gr.Textbox(label="Reason", placeholder="Overcharge on line item...", lines=2)
                            submit_btn = gr.Button("Submit Decision", variant="stop", elem_classes="tool-btn")

                    # Right: Log & Results
                    with gr.Column(scale=2):
                        status_bar = gr.Textbox(label="Status", value="Click 'Start New Episode' to begin", interactive=False)

                        with gr.Row():
                            reward_display = gr.Textbox(
                                label="💰 Reward", value="—",
                                interactive=False, elem_classes="reward-big",
                            )
                            seed_display = gr.Textbox(label="🎲 Seed", value="—", interactive=False)

                        log_output = gr.Textbox(
                            label="Investigation Log",
                            value="Waiting for episode...",
                            lines=22, max_lines=50,
                            interactive=False, elem_classes="log-box",
                        )

            # ── Tab 3: Training ───────────────────────────────
            with gr.Tab("Training"):
                gr.HTML(TRAINING_MD)

                gr.Markdown("### 📈 Training Plots")

                with gr.Row():
                    gr.Image(
                        value=f"{PLOT_BASE}/reward_curve_4b.png",
                        label="4B Reward Curve",
                        elem_classes="plot-img",
                    )
                    gr.Image(
                        value=f"{PLOT_BASE}/tool_calls_4b.png",
                        label="4B Tool Discipline",
                        elem_classes="plot-img",
                    )

                with gr.Row():
                    gr.Image(
                        value=f"{PLOT_BASE}/reward_curve.png",
                        label="0.6B Reward Curve",
                        elem_classes="plot-img",
                    )
                    gr.Image(
                        value=f"{PLOT_BASE}/training_dashboard.png",
                        label="Training Dashboard",
                        elem_classes="plot-img",
                    )

                with gr.Row():
                    gr.Image(
                        value=f"{PLOT_BASE}/comparison_chart.png",
                        label="Baseline vs Trained",
                        elem_classes="plot-img",
                    )
                    gr.Image(
                        value=f"{PLOT_BASE}/loss_curve.png",
                        label="Loss Curve",
                        elem_classes="plot-img",
                    )

            # ── Tab 4: About ─────────────────────────────────
            with gr.Tab("About"):
                gr.HTML(ABOUT_MD)

        # ── Event Handlers ────────────────────────────────────

        reset_outputs = [
            env_state, log_output, reward_display, status_bar,
            seed_display, step_counter,
            query_btn, read_btn, vendor_btn, submit_btn,
        ]
        reset_btn.click(
            fn=reset_episode,
            inputs=[task_dropdown, seed_input],
            outputs=reset_outputs,
        )

        tool_outputs = [env_state, log_output, reward_display, status_bar, step_counter]

        query_btn.click(fn=query_db, inputs=[env_state, log_output, step_counter, db_table], outputs=tool_outputs)
        read_btn.click(fn=read_doc, inputs=[env_state, log_output, step_counter, doc_id_input], outputs=tool_outputs)
        vendor_btn.click(fn=contact_vendor, inputs=[env_state, log_output, step_counter, vendor_msg], outputs=tool_outputs)
        submit_btn.click(fn=submit_decision, inputs=[env_state, log_output, step_counter, adj_amount, adj_reason], outputs=tool_outputs)

    return demo
