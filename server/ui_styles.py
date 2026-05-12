"""Light theme CSS, SVG diagrams, and HTML content for the ESCTR Gradio UI."""

INJECT_CSS = """<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@300;400;500;600;700&display=swap');
.gradio-container{background:linear-gradient(135deg,#dbeafe 0%,#e0e7ff 40%,#ede9fe 70%,#ecfdf5 100%)!important;font-family:'IBM Plex Mono',monospace!important;color:#1e293b!important;max-width:960px!important;margin:0 auto!important}
.tabs>.tab-nav{justify-content:center!important;border-bottom:none!important;gap:4px!important;padding:8px 0!important;background:transparent!important}
.tabs>.tab-nav>button{border:1px solid #cbd5e1!important;border-radius:6px!important;padding:8px 20px!important;font-family:'IBM Plex Mono',monospace!important;font-weight:500!important;background:#fff!important;color:#64748b!important;font-size:13px!important}
.tabs>.tab-nav>button.selected{border-color:#1e293b!important;color:#1e293b!important;font-weight:600!important;background:#f8fafc!important}
.tabitem{background:transparent!important;border:none!important}
label,span{font-family:'IBM Plex Mono',monospace!important;color:#334155!important}
.prose{max-width:760px;margin:0 auto;line-height:1.8;color:#334155}
.prose h2{color:#0f172a;font-size:1.5rem;font-weight:700;margin:2.5rem 0 1rem;border-bottom:1px solid #e2e8f0;padding-bottom:8px}
.prose h3{color:#1e293b;font-size:1.15rem;font-weight:600;margin:1.8rem 0 0.8rem}
.prose p{margin:0.8rem 0;font-size:0.92rem}
.prose a{color:#4f46e5;text-decoration:none}
.prose code{background:#f1f5f9;padding:2px 6px;border-radius:4px;font-size:0.85em;color:#7c3aed;border:1px solid #e2e8f0}
.prose blockquote{border-left:3px solid #6366f1;padding:0.5rem 1rem;margin:1rem 0;color:#64748b;font-style:italic;background:#f8fafc;border-radius:0 6px 6px 0}
.prose table{width:100%;border-collapse:collapse;margin:1.2rem 0;font-size:0.85rem}
.prose th{background:#f1f5f9;text-align:left;padding:10px 12px;border:1px solid #e2e8f0;color:#1e293b;font-weight:600}
.prose td{padding:8px 12px;border:1px solid #e2e8f0;color:#334155}
.prose tr:hover td{background:#f8fafc}
.prose .formula{background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:1rem 1.5rem;margin:1rem 0;text-align:center;font-size:1rem;color:#7c3aed;letter-spacing:0.02em}
.prose img{border-radius:8px;border:1px solid #e2e8f0;max-width:100%;margin:0.5rem 0;box-shadow:0 1px 3px rgba(0,0,0,0.08)}
.svgbox{text-align:center;margin:1.5rem 0}
.svgbox svg{max-width:100%}
.lb-table{width:100%;border-collapse:collapse;font-family:'IBM Plex Mono',monospace;font-size:0.85rem;margin:1rem 0}
.lb-table th{background:#f1f5f9;color:#1e293b;padding:12px 14px;text-align:left;border:1px solid #e2e8f0;font-weight:600}
.lb-table td{padding:10px 14px;border:1px solid #e2e8f0;color:#334155}
.lb-table tr:hover td{background:#f8fafc}
.lb-table .rank{color:#64748b;font-weight:600;text-align:center}
.lb-table .model{font-weight:500;color:#0f172a}
.lb-table .best{color:#16a34a;font-weight:700}
.lb-table .ongoing{color:#ca8a04;font-style:italic}
input,textarea,select,.gr-input,.gr-text-input{background:#fff!important;color:#1e293b!important;border-color:#cbd5e1!important;font-family:'IBM Plex Mono',monospace!important}
.gr-button{font-family:'IBM Plex Mono',monospace!important;color:#1e293b!important}
.gr-panel,.gr-box,.gr-form,.gr-group{background:#fff!important;border-color:#e2e8f0!important}
.gr-accordion{background:#f8fafc!important;border-color:#e2e8f0!important}
textarea{font-family:'IBM Plex Mono',monospace!important;font-size:0.82rem!important;color:#1e293b!important}
/* Force dark text on light background — override Gradio 6 theme */
*{--body-text-color:#1e293b!important;--block-label-text-color:#334155!important;--block-title-text-color:#0f172a!important;--input-text-color:#1e293b!important;--color-accent:#4f46e5!important}
.gradio-container *:not(svg *):not(.svgbox *){color:inherit}
.gradio-container{color:#1e293b!important}
.gradio-container p,.gradio-container span,.gradio-container div,.gradio-container li,.gradio-container td,.gradio-container th,.gradio-container label,.gradio-container h1,.gradio-container h2,.gradio-container h3,.gradio-container h4,.gradio-container h5,.gradio-container h6{color:#1e293b!important;font-family:'IBM Plex Mono',monospace!important}
.gradio-container .prose p,.gradio-container .prose span,.gradio-container .prose li,.gradio-container .prose td{color:#334155!important}
.gradio-container .prose h2{color:#0f172a!important}
.gradio-container .prose h3{color:#1e293b!important}
.gradio-container .prose blockquote,.gradio-container .prose blockquote *{color:#64748b!important}
.gradio-container .prose code{color:#7c3aed!important}
.gradio-container .prose a{color:#4f46e5!important}
.gradio-container .prose th{color:#1e293b!important}
.gradio-container .lb-table th{color:#1e293b!important}
.gradio-container .lb-table td{color:#334155!important}
.gradio-container .lb-table .best{color:#16a34a!important}
.gradio-container .lb-table .ongoing,.gradio-container .lb-table .ongoing *{color:#ca8a04!important}
.gradio-container .lb-table .rank{color:#64748b!important}
.gradio-container .formula,.gradio-container .formula *{color:#7c3aed!important}
.gradio-container .markdown-text,.gradio-container .md,.gradio-container .gr-markdown{color:#1e293b!important}
[data-testid] label,[data-testid] span{color:#334155!important}
.block-label,.block-title,.label-text{color:#334155!important}
</style>"""

HEADER_HTML = """<div style="text-align:center;padding:2rem 1rem 0.5rem">
<h1 style="font-family:'IBM Plex Mono',monospace;font-size:2rem;font-weight:700;color:#0f172a;margin:0;letter-spacing:-0.02em">ESCTR</h1>
<p style="font-family:'IBM Plex Mono',monospace;font-size:0.95rem;color:#64748b;margin:4px 0;font-style:italic">Enterprise Supply Chain &amp; Tax Reconciliation</p>
<p style="font-family:'IBM Plex Mono',monospace;font-size:0.75rem;color:#94a3b8;margin:4px 0">
<a href="https://huggingface.co/spaces/musharraf7/esctr-environment/blob/main/Blog.md" style="color:#4f46e5;text-decoration:none">Blog</a> · 
<a href="https://github.com/Musharraf1128/esctr-environment" style="color:#4f46e5;text-decoration:none">GitHub</a> · 
<a href="https://huggingface.co/spaces/musharraf7/esctr-grpo-trained" style="color:#4f46e5;text-decoration:none">Training Dashboard</a>
</p></div>"""

ARCH_SVG = """<div class="svgbox"><svg width="720" height="320" viewBox="0 0 720 320" xmlns="http://www.w3.org/2000/svg">
<rect x="0" y="0" width="720" height="320" fill="#f8fafc" rx="8"/>
<rect x="260" y="10" width="450" height="300" rx="8" fill="none" stroke="#cbd5e1" stroke-width="1.5"/>
<text x="485" y="35" text-anchor="middle" font-family="IBM Plex Mono,monospace" font-size="12" fill="#4f46e5" font-weight="600">ESCTR Environment</text>
<rect x="20" y="100" width="190" height="120" rx="6" fill="#fff" stroke="#4f46e5" stroke-width="1.5"/>
<text x="115" y="150" text-anchor="middle" font-family="IBM Plex Mono,monospace" font-size="14" fill="#0f172a" font-weight="600">Agent</text>
<text x="115" y="172" text-anchor="middle" font-family="IBM Plex Mono,monospace" font-size="10" fill="#64748b">(Qwen3 LLM)</text>
<text x="115" y="190" text-anchor="middle" font-family="IBM Plex Mono,monospace" font-size="10" fill="#64748b">GRPO-trained</text>
<defs><marker id="ah" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6" fill="#4f46e5"/></marker>
<marker id="ag" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6" fill="#16a34a"/></marker></defs>
<line x1="210" y1="140" x2="280" y2="140" stroke="#4f46e5" stroke-width="1.5" marker-end="url(#ah)"/>
<text x="245" y="132" text-anchor="middle" font-family="IBM Plex Mono,monospace" font-size="9" fill="#64748b">action</text>
<line x1="280" y1="180" x2="210" y2="180" stroke="#16a34a" stroke-width="1.5" marker-end="url(#ag)"/>
<text x="245" y="198" text-anchor="middle" font-family="IBM Plex Mono,monospace" font-size="9" fill="#64748b">obs</text>
<rect x="290" y="60" width="200" height="200" rx="6" fill="#fff" stroke="#e2e8f0" stroke-width="1"/>
<text x="390" y="85" text-anchor="middle" font-family="IBM Plex Mono,monospace" font-size="12" fill="#1e293b" font-weight="500">Tool Engine</text>
<text x="310" y="115" font-family="IBM Plex Mono,monospace" font-size="10" fill="#4f46e5">▸ query_database</text>
<text x="310" y="140" font-family="IBM Plex Mono,monospace" font-size="10" fill="#4f46e5">▸ read_document</text>
<text x="310" y="165" font-family="IBM Plex Mono,monospace" font-size="10" fill="#4f46e5">▸ communicate_vendor</text>
<text x="310" y="194" font-family="IBM Plex Mono,monospace" font-size="10" fill="#dc2626">▸ submit_financial_decision</text>
<text x="310" y="210" font-family="IBM Plex Mono,monospace" font-size="8" fill="#94a3b8">  (terminal action)</text>
<text x="310" y="238" font-family="IBM Plex Mono,monospace" font-size="9" fill="#64748b">Procedurally generated</text>
<text x="310" y="251" font-family="IBM Plex Mono,monospace" font-size="9" fill="#64748b">from seed — deterministic</text>
<rect x="530" y="80" width="160" height="140" rx="6" fill="#fff" stroke="#e2e8f0" stroke-width="1"/>
<text x="610" y="108" text-anchor="middle" font-family="IBM Plex Mono,monospace" font-size="11" fill="#1e293b" font-weight="500">Reward Verifier</text>
<text x="545" y="135" font-family="IBM Plex Mono,monospace" font-size="9" fill="#16a34a">R_outcome  60-70%</text>
<text x="545" y="155" font-family="IBM Plex Mono,monospace" font-size="9" fill="#16a34a">R_trajectory 30-40%</text>
<text x="545" y="175" font-family="IBM Plex Mono,monospace" font-size="9" fill="#dc2626">- penalties</text>
<text x="610" y="205" text-anchor="middle" font-family="IBM Plex Mono,monospace" font-size="10" fill="#7c3aed">R ∈ (0.01, 0.99)</text>
<line x1="490" y1="150" x2="530" y2="150" stroke="#cbd5e1" stroke-width="1" marker-end="url(#ah)"/>
</svg></div>"""

EPISODE_SVG = """<div class="svgbox"><svg width="600" height="300" viewBox="0 0 600 300" xmlns="http://www.w3.org/2000/svg">
<rect x="0" y="0" width="600" height="300" fill="#f8fafc" rx="8"/>
<text x="300" y="25" text-anchor="middle" font-family="IBM Plex Mono,monospace" font-size="12" fill="#64748b" font-weight="500">Typical Episode Flow</text>
<defs><marker id="ah2" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6" fill="#4f46e5"/></marker></defs>
<rect x="40" y="40" width="220" height="36" rx="4" fill="#fff" stroke="#4f46e5" stroke-width="1"/>
<text x="150" y="63" text-anchor="middle" font-family="IBM Plex Mono,monospace" font-size="10" fill="#4f46e5">① query_database(POs)</text>
<line x1="150" y1="76" x2="150" y2="96" stroke="#cbd5e1" stroke-width="1" marker-end="url(#ah2)"/>
<rect x="40" y="96" width="220" height="36" rx="4" fill="#fff" stroke="#4f46e5" stroke-width="1"/>
<text x="150" y="119" text-anchor="middle" font-family="IBM Plex Mono,monospace" font-size="10" fill="#4f46e5">② query_database(invoices)</text>
<line x1="150" y1="132" x2="150" y2="152" stroke="#cbd5e1" stroke-width="1" marker-end="url(#ah2)"/>
<rect x="40" y="152" width="220" height="36" rx="4" fill="#fff" stroke="#4f46e5" stroke-width="1"/>
<text x="150" y="175" text-anchor="middle" font-family="IBM Plex Mono,monospace" font-size="10" fill="#4f46e5">③ read_document(PO-XXXX)</text>
<line x1="150" y1="188" x2="150" y2="208" stroke="#cbd5e1" stroke-width="1" marker-end="url(#ah2)"/>
<rect x="40" y="208" width="220" height="36" rx="4" fill="#fff" stroke="#4f46e5" stroke-width="1"/>
<text x="150" y="231" text-anchor="middle" font-family="IBM Plex Mono,monospace" font-size="10" fill="#4f46e5">④ read_document(INV-XXXX)</text>
<line x1="150" y1="244" x2="150" y2="264" stroke="#cbd5e1" stroke-width="1" marker-end="url(#ah2)"/>
<rect x="40" y="264" width="220" height="36" rx="4" fill="#fff" stroke="#dc2626" stroke-width="1.5"/>
<text x="150" y="287" text-anchor="middle" font-family="IBM Plex Mono,monospace" font-size="10" fill="#dc2626">⑤ submit_financial_decision</text>
<rect x="340" y="55" width="230" height="230" rx="6" fill="#fff" stroke="#e2e8f0" stroke-width="1"/>
<text x="455" y="80" text-anchor="middle" font-family="IBM Plex Mono,monospace" font-size="11" fill="#1e293b" font-weight="500">Agent Reasoning</text>
<text x="355" y="110" font-family="IBM Plex Mono,monospace" font-size="9" fill="#64748b">① Discover relevant PO IDs</text>
<text x="355" y="135" font-family="IBM Plex Mono,monospace" font-size="9" fill="#64748b">② Discover invoice IDs</text>
<text x="355" y="160" font-family="IBM Plex Mono,monospace" font-size="9" fill="#64748b">③ Cross-reference prices</text>
<text x="355" y="185" font-family="IBM Plex Mono,monospace" font-size="9" fill="#64748b">④ Calculate discrepancy</text>
<text x="355" y="215" font-family="IBM Plex Mono,monospace" font-size="9" fill="#16a34a">⑤ Submit exact adjustment</text>
<text x="355" y="245" font-family="IBM Plex Mono,monospace" font-size="9" fill="#7c3aed">   → Reward computed</text>
<text x="355" y="268" font-family="IBM Plex Mono,monospace" font-size="9" fill="#7c3aed">   → R = f(accuracy,</text>
<text x="355" y="281" font-family="IBM Plex Mono,monospace" font-size="9" fill="#7c3aed">        procedure, steps)</text>
</svg></div>"""

LEADERBOARD_HTML = """<div class="prose">
<h2 style="text-align:center">Model Leaderboard</h2>
<p style="text-align:center;color:#64748b;font-style:italic;font-size:0.85rem">All models trained on the ESCTR environment using TRL's GRPOTrainer with <code>environment_factory</code>.</p>
<table class="lb-table">
<thead><tr><th class="rank">#</th><th>Model</th><th>Params</th><th>Method</th><th>GPU</th><th>Peak Reward</th><th>Tool Calls</th><th>Failures</th><th>Time</th></tr></thead>
<tbody>
<tr><td class="rank">1</td><td class="model">Qwen3-0.6B</td><td>0.6B</td><td>GRPO</td><td>T4</td><td class="best">0.30</td><td>4.0</td><td>0</td><td>~2h</td></tr>
<tr><td class="rank">2</td><td class="model">Qwen3-4B (LoRA)</td><td>4B</td><td>GRPO + Shaped</td><td>RTX 4090</td><td class="best">0.27</td><td>4.0</td><td>0</td><td>71m</td></tr>
<tr><td class="rank">3</td><td class="model ongoing">Qwen3-1.7B (LoRA)</td><td>1.7B</td><td>GRPO + Shaped</td><td>T4 (HF)</td><td class="ongoing">0.195*</td><td>3.9</td><td>0</td><td>~7h</td></tr>
<tr style="opacity:0.45"><td class="rank">—</td><td class="model">Baseline (untrained)</td><td>—</td><td>—</td><td>—</td><td>0.09</td><td>1-4</td><td>frequent</td><td>—</td></tr>
</tbody></table>
<p style="font-size:0.8rem;color:#94a3b8">* In-progress run on HF Jobs. Peak reward at step 20. Zero tool failures across all logged steps.</p>

<h3>Key Findings</h3>
<table>
<thead><tr><th>Metric</th><th>Untrained</th><th>Trained (best)</th></tr></thead>
<tbody>
<tr><td>Mean Reward</td><td>0.09</td><td><strong style="color:#16a34a">0.30</strong> (+233%)</td></tr>
<tr><td>Tool Success Rate</td><td>60%</td><td><strong style="color:#16a34a">100%</strong></td></tr>
<tr><td>Investigation Completeness</td><td>40%</td><td><strong style="color:#16a34a">100%</strong></td></tr>
<tr><td>Tool Calls / Episode</td><td>Erratic (1-4)</td><td><strong style="color:#16a34a">Stable 4.0</strong></td></tr>
</tbody></table>
</div>"""

PLOT_BASE = "https://raw.githubusercontent.com/Musharraf1128/esctr-environment/main/plots"

BLOG_HTML = f"""<div class="prose">

<blockquote>Training LLMs to investigate procurement fraud, enforce SLA penalties, and reject bad vendor settlements — autonomously.</blockquote>

<h2>The Problem</h2>
<p>Every day, enterprises process millions of procurement transactions. Between Purchase Orders, shipping manifests, SLA contracts, and vendor invoices — discrepancies are inevitable. A vendor bills <code>$45/unit</code> instead of the contracted <code>$40</code>. A shipment arrives 5 days late, triggering penalty clauses. The vendor disputes the penalty.</p>
<p>Resolving these disputes means humans manually cross-referencing siloed databases, interpreting contract clauses, and performing precise arithmetic under pressure. Current LLMs can't solve this reliably — not because the individual steps are hard, but because the <em>combination</em> is: multi-step tool use, precise arithmetic, adversarial reasoning, and state tracking across 10-20 interaction steps.</p>
<p>This is the capability gap that <strong>Reinforcement Learning with Verifiable Rewards (RLVR)</strong> was designed to close.</p>

<h2>The Environment</h2>
{ARCH_SVG}
<p>ESCTR gives the agent three scenarios of increasing complexity:</p>
<table>
<thead><tr><th>Task</th><th>Difficulty</th><th>What the Agent Must Do</th></tr></thead>
<tbody>
<tr><td><strong>Procurement Reconciliation</strong></td><td>🟢 Easy</td><td>Identify overcharged line items, calculate exact overcharge</td></tr>
<tr><td><strong>SLA Enforcement</strong></td><td>🟡 Medium</td><td>Discover late shipments, retrieve SLA contract, compute penalty</td></tr>
<tr><td><strong>Adversarial Auditing</strong></td><td>🔴 Hard</td><td>All above + disprove vendor counter-claims using warehouse logs</td></tr>
</tbody></table>
<p>Every scenario is <strong>procedurally generated from a seed</strong> — infinite training configurations with deterministic, reproducible grading. No memorization possible.</p>

<h2>Reward Design</h2>
<div class="formula">R<sub>total</sub> = α · R<sub>outcome</sub> + β · R<sub>trajectory</sub> − penalties</div>
<p><strong>R<sub>outcome</sub></strong> (60-70%): Did the agent submit the exact correct adjustment? <strong>R<sub>trajectory</sub></strong> (30-40%): Did the agent follow proper investigative procedure? <strong>Penalties</strong>: step costs (−0.005/step), hallucination (−0.02), accepting bad settlements (−0.20).</p>
<p>The correct answer is always a <strong>precise floating-point number</strong> derived from contract terms. No LLM-as-judge, no fuzzy rubric — pure programmatic verification.</p>

<h2>Training Journey</h2>

<h3>Phase 1 — Proof of Concept (0.6B)</h3>
<p>Validated the training loop with Qwen3-0.6B on a T4 GPU. Reward improved from <strong>0.09 → 0.30</strong> (+222%) in 500 episodes. The model learned the canonical investigation procedure with zero tool failures.</p>
<div style="display:flex;gap:12px;flex-wrap:wrap">
<img src="{PLOT_BASE}/reward_curve.png" style="flex:1;min-width:280px" alt="0.6B reward curve"/>
<img src="{PLOT_BASE}/training_dashboard.png" style="flex:1;min-width:280px" alt="Training dashboard"/>
</div>

<h3>Phase 2 — Scaling to 4B, and Hitting a Wall</h3>
<p>Scaled to Qwen3-4B on an RTX 4090 with LoRA. First three attempts <strong>completely failed</strong> — loss flat at 0.0.</p>
<p><strong>Problem 1: Token Budget Exhaustion.</strong> The model consumed its entire 512-token budget on <code>&lt;think&gt;</code> blocks before making a single tool call.</p>
<p><strong>Problem 2: Deterministic Starvation.</strong> At <code>temperature=1.0</code>, all K=4 rollouts were identical. Zero reward variance → zero gradient signal.</p>

<h3>Phase 2.5 — The Fix</h3>
<p><strong>1. Shaped Rewards</strong> — +0.05 partial credit per valid investigation step.<br/>
<strong>2. High Temperature</strong> — T=1.5 with K=4 rollouts forced exploration diversity.</p>

<h3>Phase 3 — Success: 4B in 71 Minutes</h3>
<div style="display:flex;gap:12px;flex-wrap:wrap">
<img src="{PLOT_BASE}/reward_curve_4b.png" style="flex:1;min-width:280px" alt="4B reward curve"/>
<img src="{PLOT_BASE}/tool_calls_4b.png" style="flex:1;min-width:280px" alt="4B tool discipline"/>
</div>
<p>The tool graph tells the story: early chaos (2-4.25 calls/episode) collapses into rigid discipline — exactly 4.0 tool calls, the optimal investigate-investigate-investigate-submit pipeline.</p>

<h3>Phase 4 — Iterating on 1.7B (HF Jobs)</h3>
<p>Launched on HuggingFace's T4-medium. Early metrics confirm the shaped reward architecture transfers cleanly to a different model size with <strong>zero modifications</strong>.</p>
<table>
<thead><tr><th>Step</th><th>Loss</th><th>Reward</th><th>Tool Calls</th><th>Entropy</th></tr></thead>
<tbody>
<tr><td>5</td><td>0.184</td><td><strong>0.195</strong></td><td>3.9</td><td>0.132</td></tr>
<tr><td>10</td><td>0.116</td><td>0.195</td><td>3.9</td><td>0.127</td></tr>
<tr><td>15</td><td>0.088</td><td>0.180</td><td>3.6</td><td>0.028</td></tr>
<tr><td>20</td><td>0.186</td><td>0.190</td><td>3.8</td><td>0.047</td></tr>
</tbody></table>

<h2>Technical Summary</h2>
<table>
<thead><tr><th>Param</th><th>0.6B</th><th>4B</th><th>1.7B</th></tr></thead>
<tbody>
<tr><td>Model</td><td>Qwen3-0.6B</td><td>Qwen3-4B</td><td>Qwen3-1.7B</td></tr>
<tr><td>GPU</td><td>T4 (Colab)</td><td>RTX 4090</td><td>T4 (HF Jobs)</td></tr>
<tr><td>Quant</td><td>None</td><td>4-bit QLoRA</td><td>4-bit QLoRA</td></tr>
<tr><td>Adapter</td><td>Full</td><td>LoRA r=16</td><td>LoRA r=16</td></tr>
<tr><td>Episodes</td><td>500</td><td>300</td><td>500</td></tr>
<tr><td>Time</td><td>~2h</td><td>71m</td><td>~7h</td></tr>
</tbody></table>

</div>"""
