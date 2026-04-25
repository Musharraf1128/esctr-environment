# ESCTR Submission Checklist (Finale)

## Non-Negotiables

- [x] OpenEnv-compliant environment with `reset`/`step`/`state` and typed schemas
- [x] `openenv.yaml` present and valid
- [x] 3 tasks with increasing difficulty and deterministic graders
- [x] Baseline inference script at repo root: `inference.py`
- [x] Required logging format in inference: `[START]`, `[STEP]`, `[END]`
- [x] Dockerized deployment (`Dockerfile`) with healthcheck
- [x] Hugging Face Space deployment target configured
- [x] README explains problem, environment, training setup, and results
- [x] Training evidence plots committed in `plots/`

## High-Impact Differentiators (Shipped)

- [x] Dynamic distractors in procurement records (anti-pattern-matching pressure)
- [x] Risk-first scorecard metrics in grader metadata
- [x] Auditable action trace endpoint (`/trace`)
- [x] Mermaid action graph output (`action_graph_mermaid`) for episode explainability
- [x] Interactive demo route (`/demo`) separated from API routes for deployment safety

## Final Packaging Pass (Before Submit)

- [ ] Verify Space build logs are clean and app starts
- [ ] Confirm `/reset` returns `200` on deployed Space
- [ ] Confirm `/demo` renders Gradio UI on deployed Space
- [ ] Run one full `inference.py` pass against deployed environment
- [ ] Ensure README links include Space + training dashboard + storytelling artifact (slides/video/blog)
- [ ] Freeze final commit and avoid post-deadline changes

## Submission Lock Commands

```bash
# 1) Space endpoint checks
curl -s -o /tmp/esctr_health.json -w "%{http_code}\n" https://musharraf7-esctr-environment.hf.space/health
curl -s -o /tmp/esctr_reset.json -w "%{http_code}\n" -X POST -H "Content-Type: application/json" \
  -d '{"task_name":"procurement_reconciliation","seed":42}' https://musharraf7-esctr-environment.hf.space/reset
curl -s -o /tmp/esctr_demo.html -w "%{http_code}\n" https://musharraf7-esctr-environment.hf.space/demo

# 2) Baseline run against deployed space
export ENV_URL="https://musharraf7-esctr-environment.hf.space"
python inference.py

# 3) Optional artifact regeneration
python ablation.py
python generate_demo_artifacts.py
```
