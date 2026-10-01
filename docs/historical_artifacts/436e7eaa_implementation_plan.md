# Implementation Plan: Historical Brain Artifact Discovery, Triaging & Ingestion

Conduct an exhaustive retrospective forensic audit across all Antigravity conversation sessions in `C:\Users\augus\.gemini\antigravity\brain\` to recover, triage, and permanently preserve all stranded session assets belonging to the `Translation` workspace (`augyyyyy/typikon-translated`).

## User Review Required
> [!IMPORTANT]
> - All assets will be ingested non-destructively: original brain session files are never deleted or modified.
> - Destination directories at project root:
>   - `docs/historical_artifacts/` (Tier 1: Markdown reports, analyses, autopsies)
>   - `docs/user_evidence/` (Tier 2: User-uploaded scans and images)
>   - `scripts/archived_pipelines/` (Tier 3: Reusable Python pipelines, scrapers, tools)
>   - `data/historical/` (Tier 4: JSON caches, catalog text dumps, translation data)
> - Naming convention: `<short_conv_id>_<original_filename>` (using first 8 chars of conversation UUID) to avoid name collisions across sessions.
> - A comprehensive `ARTIFACT_REGISTRY.md` will be created at the root of the project with deep links `[conv-uuid](conversation://<uuid>)`, timestamps, file sizes, and parsed summaries.

## Proposed Changes

### Phase 1: Exhaustive Forensic Audit & Conversation Identification
- Scan all conversation directories in `C:\Users\augus\.gemini\antigravity\brain\`.
- Check initial lines of `transcript.jsonl` and full tool calls (`TargetFile`, `Cwd`, `CommandLine`, `CorpusName`) to precisely identify all conversations belonging to the `Translation` workspace (matching both `Projects\Translation` and legacy drive letters `e:\Google Antigravity\Projects\Translation` or corpus `augyyyyy/typikon-translated`).
- Distinguish active sessions in `Translation` from sessions in other spokes (like `Typikon Coded`) that merely mentioned `Translation`.

### Phase 2: Asset Triage & Categorization
- Scan the root, `scratch/`, and `.user_uploaded/` folders of each matched conversation.
- Classify into:
  - **Tier 1 (High-Value Research & Technical Artifacts)**: Markdown analyses, autopsies, plans, audit summaries (filter out empty or generic template stubs).
  - **Tier 2 (User Evidence Uploads)**: Images, scans, PDFs in `.user_uploaded/`.
  - **Tier 3 (Automated Pipelines & Tools)**: Reusable python scripts from `scratch/`.
  - **Tier 4 (Data Assets & Catalogs)**: Extracted JSON, TXT dumps, data files.
  - **Discard/Ignore**: Transient runtime caches, `.bin` files, empty stubs.

### Phase 3: Permanent Ingestion (Safe Copy)
- Create target folders under project root:
  - `docs/historical_artifacts/`
  - `docs/user_evidence/`
  - `scripts/archived_pipelines/`
  - `data/historical/`
- Copy identified assets with prefix `<short_conv_id>_`.
- Verify checksums / file sizes after copying.

### Phase 4: Master Registry Generation
- Generate `ARTIFACT_REGISTRY.md` in the project root.
- Index every ingested asset in structured markdown tables categorized by Tier.
- Include deep links `[conv-uuid](conversation://<uuid>)`, original timestamp, file size, target path, and an executive summary extracted from the header/first 10 lines.

### Phase 5: Verification & Proof
- Run deterministic verification script:
  - Assert existence of all copied files and verify byte matches.
  - Tally total files and total bytes by Tier.
  - Run `git status` to verify staged/untracked files.
  - Present final summary to the user.

## Verification Plan
- Automated Python verification script testing file integrity and link validity.
- Git status check.
