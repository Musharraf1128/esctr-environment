"""
ESCTR — Research Interface

Dark-themed Gradio UI with IBM Plex Mono typography.
Tabs: Blog · Playground · Leaderboard
"""

import gradio as gr
import random
from .environment import ESCTREnvironment
from .models import ESCTRAction
from .ui_styles import (
    INJECT_CSS, HEADER_HTML, ARCH_SVG, EPISODE_SVG,
    BLOG_HTML, LEADERBOARD_HTML,
)


# ── State management ─────────────────────────────────────────────────────────

def create_env():
    return ESCTREnvironment()


def reset_episode(task_name, seed_text):
    """Reset the environment with a task and seed."""
    env = create_env()
    seed = int(seed_text) if seed_text.strip() else random.randint(0, 99999)
    obs = env.reset(task_name=task_name, seed=seed)

    log = f"{'='*60}\n"
    log += f"  ESCTR — New Episode\n"
    log += f"  Task: {task_name} | Seed: {seed}\n"
    log += f"{'='*60}\n\n"
    log += f"BRIEFING:\n{obs.system_response}\n\n"
    log += f"{'─'*60}\n"

    status = f"Step 0 | Reward: 0.00 | Investigating..."

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
        return env, log + "\n>> Reset the environment first.\n", "0.00", "Not started", step_count

    try:
        action = ESCTRAction(action_type=action_type, **kwargs)
        obs = env.step(action)
    except Exception as e:
        log += f"\nERROR: {str(e)}\n"
        return env, log, "0.00", "Error", step_count

    step_count += 1
    reward = obs.reward
    done = obs.done

    param_str = ", ".join(f'{k}="{v}"' for k, v in kwargs.items() if v)
    log += f"\n[Step {step_count}] {action_type}({param_str})\n"
    log += f"{'─'*40}\n"

    response = obs.system_response
    if len(response) > 1500:
        response = response[:1500] + "\n... [truncated]"
    log += f"{response}\n"
    log += f"{'─'*40}\n"

    if done:
        log += f"\n{'='*60}\n"
        log += f"  EPISODE COMPLETE\n"
        log += f"  Final Reward: {reward:.4f}\n"
        log += f"  Steps Used: {step_count}\n"
        log += f"{'='*60}\n"
        status = f"Done in {step_count} steps | Final Reward: {reward:.4f}"
    else:
        status = f"Step {step_count} | Reward: {reward:.4f} | Investigating..."

    return env, log, f"{reward:.4f}", status, step_count


def query_db(env, log, step_count, table):
    if not table:
        log += "\n>> Select a table.\n"
        return env, log, "0.00", "Select a table", step_count
    return execute_tool(env, log, step_count, "query_database",
                        query_parameters={"table": table})


def read_doc(env, log, step_count, doc_id):
    if not doc_id.strip():
        log += "\n>> Enter a document ID.\n"
        return env, log, "0.00", "Enter ID", step_count
    return execute_tool(env, log, step_count, "read_document",
                        document_id=doc_id.strip())


def contact_vendor(env, log, step_count, message):
    if not message.strip():
        log += "\n>> Enter a message.\n"
        return env, log, "0.00", "Enter message", step_count
    return execute_tool(env, log, step_count, "communicate_vendor",
                        message_content=message.strip())


def submit_decision(env, log, step_count, amount, reason):
    try:
        amt = float(amount)
    except (ValueError, TypeError):
        log += "\n>> Enter a valid numeric amount.\n"
        return env, log, "0.00", "Invalid amount", step_count
    if not reason.strip():
        reason = "Financial adjustment based on investigation"
    return execute_tool(env, log, step_count, "submit_financial_decision",
                        adjustment_amount=amt, adjustment_reason=reason.strip())


# ── Build UI ─────────────────────────────────────────────────────────────────

def build_gradio_app():
    with gr.Blocks(title="ESCTR Environment") as demo:

        # Hidden state
        env_state = gr.State(None)
        step_counter = gr.State(0)

        # Inject dark theme CSS + header
        gr.HTML(INJECT_CSS)
        gr.HTML(HEADER_HTML)

        with gr.Tabs():

            # ── Tab 1: Blog ───────────────────────────────────
            with gr.Tab("Blog"):
                gr.HTML(BLOG_HTML)

            # ── Tab 2: Playground ─────────────────────────────
            with gr.Tab("Playground"):
                gr.HTML(EPISODE_SVG)

                with gr.Row():
                    # Left: Controls
                    with gr.Column(scale=1):
                        gr.Markdown("### Episode Controls")

                        task_dropdown = gr.Dropdown(
                            choices=[
                                ("Procurement Reconciliation (Easy)",
                                 "procurement_reconciliation"),
                                ("SLA Enforcement (Medium)",
                                 "sla_enforcement"),
                                ("Adversarial Auditing (Hard)",
                                 "adversarial_auditing"),
                            ],
                            value="procurement_reconciliation",
                            label="Task",
                        )
                        seed_input = gr.Textbox(
                            label="Seed (empty = random)",
                            placeholder="42",
                            value="",
                        )
                        reset_btn = gr.Button(
                            "Start New Episode",
                            variant="primary", size="lg",
                        )

                        gr.Markdown("---")
                        gr.Markdown("### Tools")

                        with gr.Accordion("query_database", open=True):
                            db_table = gr.Dropdown(
                                choices=[
                                    "purchase_orders", "invoices",
                                    "shipping_logs", "sla_contracts",
                                    "warehouse_logs",
                                ],
                                label="Table",
                                value="purchase_orders",
                            )
                            query_btn = gr.Button("Run Query")

                        with gr.Accordion("read_document", open=False):
                            doc_id_input = gr.Textbox(
                                label="Document ID",
                                placeholder="PO-2025-1234",
                            )
                            read_btn = gr.Button("Read")

                        with gr.Accordion("communicate_vendor", open=False):
                            vendor_msg = gr.Textbox(
                                label="Message",
                                placeholder="We reject your settlement...",
                                lines=2,
                            )
                            vendor_btn = gr.Button("Send")

                        with gr.Accordion(
                            "submit_financial_decision", open=False
                        ):
                            adj_amount = gr.Textbox(
                                label="Adjustment ($)",
                                placeholder="-450.00",
                            )
                            adj_reason = gr.Textbox(
                                label="Reason",
                                placeholder="Overcharge on line item...",
                                lines=2,
                            )
                            submit_btn = gr.Button(
                                "Submit Decision", variant="stop",
                            )

                    # Right: Log
                    with gr.Column(scale=2):
                        status_bar = gr.Textbox(
                            label="Status",
                            value="Click 'Start New Episode' to begin",
                            interactive=False,
                        )

                        with gr.Row():
                            reward_display = gr.Textbox(
                                label="Reward",
                                value="—",
                                interactive=False,
                            )
                            seed_display = gr.Textbox(
                                label="Seed",
                                value="—",
                                interactive=False,
                            )

                        log_output = gr.Textbox(
                            label="Investigation Log",
                            value="Waiting for episode...",
                            lines=22,
                            max_lines=50,
                            interactive=False,
                        )

            # ── Tab 3: Leaderboard ────────────────────────────
            with gr.Tab("Leaderboard"):
                gr.HTML(LEADERBOARD_HTML)

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

        tool_outputs = [
            env_state, log_output, reward_display,
            status_bar, step_counter,
        ]

        query_btn.click(
            fn=query_db,
            inputs=[env_state, log_output, step_counter, db_table],
            outputs=tool_outputs,
        )
        read_btn.click(
            fn=read_doc,
            inputs=[env_state, log_output, step_counter, doc_id_input],
            outputs=tool_outputs,
        )
        vendor_btn.click(
            fn=contact_vendor,
            inputs=[env_state, log_output, step_counter, vendor_msg],
            outputs=tool_outputs,
        )
        submit_btn.click(
            fn=submit_decision,
            inputs=[
                env_state, log_output, step_counter,
                adj_amount, adj_reason,
            ],
            outputs=tool_outputs,
        )

    return demo
