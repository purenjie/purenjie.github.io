# AI Blog Analysis (LLM + Cache)

This folder contains a two-stage Map-Reduce pipeline that analyzes your blog posts using an LLM, then outputs structured JSON for front-end visualization (ECharts on the About page).

## Prerequisites
- Python 3.9+
- Install dependencies:
  ```bash
  pip install -r scripts/requirements.txt
  ```
- Environment variable:
  ```bash
  export DOUBAO_API_KEY=your_api_key
  ```

## What it does
- Map: For each article under `src/content/blog`, generate a structured JSON (style, sentiment, topics, metrics).
- Cache: Cache per-article result by MD5, saved as `scripts/ai_analysis/cache/ARTICLENAME_MD5.json`.
- Reduce: Aggregate all articles into `public/data/blog-analysis.json` for the About page charts.

## Usage
Run the analysis (two equivalent ways):
```bash
# Method 1: as module
python -m scripts.ai_analysis.run --verbose

# Method 2: as script
python scripts/ai_analysis/run.py --verbose
```
Options:
- `--force`: ignore cache and recompute all
- `--limit N`: only process the first N articles
- `--dry-run`: list target files without calling the LLM
- `--verbose`: print more logs

Output files:
- Cache: `scripts/ai_analysis/cache/ARTICLENAME_MD5.json`
- Manifest: `scripts/ai_analysis/manifest.json`
- Global JSON: `public/data/blog-analysis.json`

## Front-end
The About page renders charts from `/data/blog-analysis.json`. Ensure you rebuild or run dev server after generating the file.

## Notes
- Comments are in English.
- Network errors are retried automatically with backoff.
- Long articles are chunked and merged.
