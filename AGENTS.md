# Repository Guidelines

## Project Structure & Module Organization
The core package lives in `pyner/`, with `cli.py` exposing the command-line entry point, `core.py` coordinating search workflows, and feature-specific logic split into `fetchers/`, `parsers/`, `prisma/`, and `utils/`. Domain taxonomies reside in `domain_vocabularies.py`, while reusable configuration helpers sit in `config.py`. Place reproducible datasets in `data/` (subfolders `raw/`, `processed/`, `excluded/`, `prisma_flows/`) and reference material in `docs/`. End-to-end usage examples live in `examples/`, and new regression or unit tests belong in `tests/`, mirroring the module layout.

## Build, Test, and Development Commands
- `pip install -e ".[dev]"`: editable install with tooling (`pytest`, `black`, `flake8`, `mypy`).
- `pyner --organism "Arabidopsis thaliana" --condition "salt stress" --experiment "RNA-seq" --label demo`: run a representative CLI search; redirect `--output-dir` for custom destinations.
- `pytest`: execute the default suite from `tests/`.
- `pytest --cov=pyner --cov-report=term-missing`: enforce coverage and surface gaps before submitting.

## Coding Style & Naming Conventions
Use 4-space indentation and include type hints for public APIs. Follow Black’s defaults (line length 88) and run `black .` before committing. Apply `flake8` to catch lint issues and reserve `__all__` only for curated exports. Name modules and files with lowercase and underscores (`query_builder.py`), classes in PascalCase, and user-facing CLI options in kebab-case aligned with `pyner.cli`.

## Testing Guidelines
Structure tests as `tests/test_<module>.py`, grouping related fixtures near their usage. Prefer descriptive function names such as `test_fetcher_handles_empty_result`. When adding data-driven tests, stage lightweight fixtures under `tests/fixtures/` and avoid large binaries; instead reference assets in `data/raw/`. Keep coverage near the default `pytest --cov` target and attach HTML reports stored in `test_results/` to diagnose misses.

## Commit & Pull Request Guidelines
Follow the Git history’s imperative, sentence-case convention (`Implement parser fallback`, `Fix PRISMA summary export`). Scope commits narrowly and reference issues with `Refs #123` when relevant. PRs should summarize behavior changes, outline validation (commands run, sample outputs), and note documentation updates. Include screenshots only when altering generated reports. Remove temporary files and keep CI green before requesting review.

## Security & Configuration Tips
Store NCBI credentials via environment variables (`NCBI_EMAIL`, `NCBI_API_KEY`) or an untracked `config_local.py`; never commit secrets. Sanitise downloaded datasets before sharing and log provenance in `logs/` for traceability. When integrating new data sources, document authentication or rate-limit requirements in `docs/DATABASES.md`.
