"""Interactive Gradio UI for the ESCTR Environment."""

from pathlib import Path
import random

import gradio as gr

from .environment import ESCTREnvironment
from .models import ESCTRAction


CSS = """
body, .gradio-container {
    background-color: #e8f4f8 !important;
    font-family: 'Times New Roman', Times, Georgia, serif !important;
    color: #2d3748 !important;
    font-size: 18px !important;
}
.gradio-container {
    max-width: 1120px !important;
    margin: 0 auto !important;
}
footer, .gradio-container > footer, .built-with { display: none !important; }

.main-header {
    text-align: center;
    padding: 1rem 0.5rem 0.6rem 0.5rem;
}
.main-header h1 {
    margin: 0;
    font-size: 2.05rem;
    font-weight: 600;
    color: #1a202c;
}
.main-header .subtitle {
    margin-top: 0.25rem;
    color: #5a6b7a;
    font-style: italic;
    font-size: 1rem;
}
.main-header .links {
    margin-top: 0.4rem;
    font-size: 0.86rem;
    color: #718096;
}
.main-header .links a {
    color: #3d4f5f;
    text-decoration: none;
    border-bottom: 1px dotted #8a9caa;
}
.main-header .links a:hover { opacity: 0.7; }

.tabs, .tab-nav, .tabitem, .tabitem > .column {
    border: none !important;
    background: transparent !important;
    box-shadow: none !important;
}
.tab-nav {
    justify-content: center !important;
    gap: 0.2rem !important;
    margin-bottom: 0.2rem !important;
}
.tab-nav button {
    border: 1px solid transparent !important;
    background: none !important;
    color: #2d3748 !important;
    border-radius: 3px !important;
    font-size: 0.94rem !important;
    padding: 0.38rem 0.88rem !important;
}
.tab-nav button.selected {
    font-weight: 700 !important;
    border-color: #2d3748 !important;
    color: #1a202c !important;
}

.surface {
    background: #f7fcfe;
    border: 1px solid #d8e7ee;
    border-radius: 8px;
    padding: 0.9rem;
}

.esctr-page .markdown-body,
.esctr-page .prose {
    max-width: 820px !important;
    margin: 0 auto !important;
    line-height: 1.85 !important;
    color: #3b4a5a !important;
}
.esctr-page h1, .esctr-page h2, .esctr-page h3 {
    color: #1a202c !important;
    font-weight: 600 !important;
}
.esctr-page table { width: 100%; border-collapse: collapse; margin: 1rem 0; }
.esctr-page th, .esctr-page td {
    border-bottom: 1px solid #d7e5ec;
    padding: 0.45rem 0.5rem;
    text-align: left;
}

.log-box textarea {
    font-family: 'Courier New', Consolas, monospace !important;
    font-size: 0.8rem !important;
    line-height: 1.55 !important;
}
.reward-big textarea {
    font-size: 1.9rem !important;
    font-weight: 700 !important;
    text-align: center !important;
}
.tool-btn { min-height: 42px !important; }
.plot-img img {
    border-radius: 6px;
    border: 1px solid #dbe7ee;
    background: #f7fcfe;
}
"""


# ── Overview Tab Content ─────────────────────────────────────────────────────

OVERVIEW_MD = """
# ESCTR
*Enterprise Supply Chain & Tax Reconciliation*

ESCTR is an OpenEnv-compatible reinforcement learning environment for enterprise financial operations.
An agent plays the role of a financial controller and must investigate discrepancies, compute valid
adjustments, and handle adversarial vendor interactions.

## Task Suite

| Task | Difficulty | Objective |
|---|---|---|
| Procurement Reconciliation | Easy | Detect and quantify invoice overcharges |
| SLA Enforcement | Medium | Compute penalties from delivery delays and SLA terms |
| Adversarial Auditing | Hard | Resolve disputes and reject invalid settlement tactics |

## Tools

- `query_database` for operational and financial tables
- `read_document` for raw contract and transaction artifacts
- `communicate_vendor` for negotiation and claim rebuttal
- `submit_financial_decision` for final terminal adjustment

## Reward Shape

`R_total = alpha * R_outcome + beta * R_trajectory - penalties`

- Outcome rewards exact final correctness
- Trajectory rewards disciplined investigative flow
- Penalties discourage invalid actions and poor process
"""


# ── Training Tab Content ─────────────────────────────────────────────────────

TRAINING_MD = """
# Logs

Training snapshots from ESCTR runs:

- Qwen3-4B: stabilized tool usage with improved reward profile
- Qwen3-1.7B: transfer behavior under HF Jobs infrastructure
- Qwen3-0.6B: proof-of-concept baseline for fast iteration

Plots below summarize reward movement, tool discipline, and loss trajectory.
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


def _load_blog_markdown() -> str:
    root = Path(__file__).resolve().parents[1]
    blog_path = root / "Blog.md"
    if blog_path.exists():
        return blog_path.read_text(encoding="utf-8")
    return "# Blog\n\nBlog content not found."


def build_gradio_app():
    with gr.Blocks(title="ESCTR Environment") as demo:
        gr.HTML(f"<style>{CSS}</style>")

        # Hidden state
        env_state = gr.State(None)
        step_counter = gr.State(0)

        # ── Header ────────────────────────────────────────────
        gr.HTML("""
        <div class="main-header">
            <h1>ESCTR</h1>
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
            with gr.Tab("Readme"):
                gr.Markdown(OVERVIEW_MD, elem_classes=["esctr-page"])

            # ── Tab 2: Playground ─────────────────────────────
            with gr.Tab("Playground"):
                with gr.Row():
                    # Left: Controls
                    with gr.Column(scale=1):
                        gr.HTML('<div class="surface"><h3 style="margin-top:0; margin-bottom:0.7rem;">Episode Controls</h3>')

                        task_dropdown = gr.Dropdown(
                            choices=[
                                ("Procurement Reconciliation", "procurement_reconciliation"),
                                ("SLA Enforcement", "sla_enforcement"),
                                ("Adversarial Auditing", "adversarial_auditing"),
                            ],
                            value="procurement_reconciliation",
                            label="Task",
                        )
                        seed_input = gr.Textbox(
                            label="Seed (empty = random)",
                            placeholder="e.g., 42",
                            value="",
                        )
                        reset_btn = gr.Button("Start New Episode", variant="primary", size="lg")
                        gr.HTML('<div style="height:0.8rem;"></div><h3 style="margin:0.2rem 0 0.65rem 0;">Tools</h3>')

                        with gr.Accordion("Query Database", open=True):
                            db_table = gr.Dropdown(
                                choices=["purchase_orders", "invoices", "shipping_logs", "sla_contracts", "warehouse_logs"],
                                label="Table", value="purchase_orders",
                            )
                            query_btn = gr.Button("Run Query", elem_classes="tool-btn")

                        with gr.Accordion("Read Document", open=False):
                            doc_id_input = gr.Textbox(label="Document ID", placeholder="PO-2025-1234")
                            read_btn = gr.Button("Read Document", elem_classes="tool-btn")

                        with gr.Accordion("Contact Vendor", open=False):
                            vendor_msg = gr.Textbox(label="Message", placeholder="We reject your settlement...", lines=2)
                            vendor_btn = gr.Button("Send Message", elem_classes="tool-btn")

                        with gr.Accordion("Submit Decision", open=False):
                            adj_amount = gr.Textbox(label="Adjustment ($)", placeholder="-450.00")
                            adj_reason = gr.Textbox(label="Reason", placeholder="Overcharge on line item...", lines=2)
                            submit_btn = gr.Button("Submit Decision", variant="stop", elem_classes="tool-btn")
                        gr.HTML('</div>')

                    # Right: Log & Results
                    with gr.Column(scale=2):
                        gr.HTML('<div class="surface">')
                        status_bar = gr.Textbox(label="Status", value="Click 'Start New Episode' to begin", interactive=False)

                        with gr.Row():
                            reward_display = gr.Textbox(
                                label="Reward", value="—",
                                interactive=False, elem_classes="reward-big",
                            )
                            seed_display = gr.Textbox(label="Seed", value="—", interactive=False)

                        log_output = gr.Textbox(
                            label="Investigation Log",
                            value="Waiting for episode...",
                            lines=22, max_lines=50,
                            interactive=False, elem_classes="log-box",
                        )
                        gr.HTML('</div>')

            # ── Tab 3: Training ───────────────────────────────
            with gr.Tab("Logs"):
                gr.Markdown(TRAINING_MD, elem_classes=["esctr-page"])

                gr.Markdown("### Training Plots", elem_classes=["esctr-page"])

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

            # ── Tab 4: Blog ──────────────────────────────────
            with gr.Tab("Blog"):
                gr.Markdown(_load_blog_markdown(), elem_classes=["esctr-page"])

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
