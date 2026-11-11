---
name: monument_translation_orchestrator
description: Orchestrates Phase 0/1/2 Bookend Hybrid Model Routing (Argon -> Flash -> Argon), multi-monument sequestered concurrency, 8 engine-codified house-style defaults, Statutory Mandates 1-13, Drive E vault extraction, and Re-Run vs. Patch decisions.
---

# Monument Translation Orchestrator Skill Guidelines

Use this skill whenever onboarding, planning, executing, auditing, pausing, resuming, or sealing a liturgical monument in `Liturgical Monuments/`.

## 1. 3-Phase Bookend Hybrid Model Routing (`Rule 14`)
1. **Phase 0 (`PHASE_0_ARGON_PLANNING` on `Gemini 4 Argon (High)`)**:
   - Run `py scripts/autonomous_orchestrator.py --preflight --monument <ID>` to generate `Audit_Reports/phase0_preflight_brief.json` and `recommended_publication_spec`.
   - **Hard Vision Cap (`<= 8` Leaves / `<= 2` Batches)**: Inspect at most Batch 1 (`Page_0001.jpg`–`Page_0005.jpg`) and Batch 2 (`Page_(N-2).jpg`–`Page_N.jpg`). Mid-codex visual searches (`p6`..`p(N-3)`) are prohibited. Normalize rotated scans via `--rotate-jpgs 90/180/270`.
   - **Gate 0 Fast-Fail (`--defer-monument`)**: If Batch 1 reveals a modern excerpt, secondary monograph, or truncated scan, stop immediately and run `--defer-monument --monument <ID> --reason "..."`.
   - **Circuit-Breaker**: Cohort 1 dispatch is blocked until `implementation_plan.md` is approved, UI is switched `Argon` → `Gemini 3.8 Flash`, and `--unlock-flash-sprint` is executed.
2. **Phase 1 (`PHASE_1_FLASH_SPRINT` on `Gemini 3.8 Flash`)**:
   - Dispatch 10-leaf cohorts strictly via `invoke_subagent` (`ephemeral_translator`, `Model="flash"`, `EnableWriteTools=True`, `EnableSubagentTools=False`, `EnableMCPTools=False`). Never use two-chat copy-paste relay.
   - Verify each cohort via `py scripts/autonomous_orchestrator.py --verify-cohort --monument <ID>` (4-part self-healing + max 1 `Flash` retry + 4-signal `argon_review_queue.json` quarantine).
3. **Phase 2 (`PHASE_2_ARGON_DEEP_AUDIT` on `Gemini 4 Argon (High)`)**:
   - At `remaining_pages == 0`, halt at `AWAITING_ARGON_POST_SPRINT_AUDIT` for UI switch `Flash` → `Argon (High)`.
   - Run `--run-argon-audit`, then `--compile-publication`, and upon operator sign-off run `--approve-grand-pause` (syncs `../Typikon Coded/Data/Inbox/`, commits/pushes, emits next `/plan` prompt, and retires the chat session).

## 2. Zero-Redundancy `/grill-me` & Sequestered Concurrency
* Never re-ask the **8 Engine-Codified Liturgical Defaults** or **Statutory Mandates 1–13** during Phase 0 `/grill-me`; only ask questions if the 8 bookend leaves expose a genuine physical anomaly.
* Always pass `--monument <ID>` (or `$env:ACTIVE_MONUMENT_ID`) on mutating CLI calls; manage leases via `--claim-next-monument`, `--pause-monument`, and `--resume-monument`.

## 3. On-Demand Reference Playbooks
* [`references/bookend_routing_and_concurrency.md`](references/bookend_routing_and_concurrency.md) — Phase 0/1/2 CLI commands, 4-signal `argon_review_queue.json`, self-healing, Grand Pause sealing, and cross-process locking.
* [`references/house_style_and_work_order_mandates.md`](references/house_style_and_work_order_mandates.md) — All 8 `engine_codified_decisions` (`publication_spec_scaffolds.json`) and Statutory Mandates 1–13 (`work_order_template.md`).
* [`references/drive_e_vault_and_extraction.md`](references/drive_e_vault_and_extraction.md) — Drive E master vault tiering, NTFS junctions, 2-tier `extract_cohort_leaves.py`, and recursive `.rglob()` law.
* [`references/rerun_vs_patch_and_autopsy.md`](references/rerun_vs_patch_and_autopsy.md) — Rule 18 4-criterion Re-Run vs. Patch matrix, pre-rerun archiving, and `PA-NNN` process autopsy generation.
