Orient on and prepare the Phase 0 translation architecture for {title} (`{monument_id}`).

1. **Monument Identity & Codicological Parameters**:
   - **Monument ID**: `{monument_id}`
   - **Title**: {title}
   - **Workspace Directory**: `{workspace_dir}`
   - **Master Source PDF (Drive E)**: `{relative_pdf_path}`
   - **Scope & Geometry**: {total_pages} physical leaves ({total_cohorts} cohorts @ {cohort_size} leaves/cohort)
   - **Governing Register**: `{genre_register}` (per Master Translation Standard MTS-1)

2. **Hard Phase 0 Vision Budget Cap (`MAX_PHASE_0_VISION_LEAVES = 8`, `MAX_PHASE_0_VISION_BATCHES = 2`)**:
   - **Strict Vision Cap**: You may execute **at most 2 `read_file` vision batches** inspecting **at most 8 physical leaf images total** on `Gemini 4 Argon (High)`:
     - **Batch 1 (Front Bookend, <= 5 leaves)**: `{front_leaves_str}` (verify Gate 0 Primary Source Suitability, 1-up vs. 2-up spread geometry, column layout, and front-matter pagination offset).
     - **Batch 2 (Rear Bookend, <= 3 leaves)**: `{rear_leaves_str}` (verify closing leaves, rear Table of Contents, or colophon).
   - **Absolute Ban on Mid-Codex Binary Searches**: Reading internal leaves (`{forbidden_internal_range}`) to locate chapter or Tone transitions during Phase 0 is **permanently prohibited**. Cohort boundaries are strictly mathematical (`{cohort_size}` leaves/cohort) and `publication_spec` landmarks bind to translated Markdown headings in Phase 2.
   - **Gate 0 Fast-Fail Rule**: If Batch 1 (`{front_leaves_str}`) reveals that the PDF is an abridged modern excerpt, chrestomathy, or defective scan rather than a complete source monument, **halt further image reads immediately**, report the Gate 0 defect to the operator, and upon confirmation execute `py scripts/autonomous_orchestrator.py --defer-monument --monument {monument_id} --reason "..."`.

3. **Turn-1 Scope (Read-Only Discovery & Planning Only — Zero Execution)**:
   - Execute `python scratch/search_anti_patterns.py` and `py scripts/autonomous_orchestrator.py --preflight --monument {monument_id}`.
   - Read `{workspace_dir}/Audit_Reports/phase0_preflight_brief.json` (which contains the pre-computed {total_cohorts}-cohort partition table and scaffolded `publication_spec`) and inspect at most the 8 bookend leaves above.
   - Author `implementation_plan.md` (`RequestFeedback: true`, `UserFacing: true`) detailing the pagination coordinate map, pre-computed cohort table, genre register rules, and 3-Phase Bookend Hybrid Model Routing workflow.
   - **STOP** after presenting `implementation_plan.md` and wait for human planning review and alignment. Do not execute any translation cohorts or mutate workspace corpus files.
