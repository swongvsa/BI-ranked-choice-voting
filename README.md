# Ranked Choice Voting Processor

A Python-based tool for processing ranked choice voting results, supporting multiple year groups and data processing stages.

## Project Structure

```text
.
├── main.py                 # Main entry point
├── vote_result_cal.py      # Vote calculation logic
├── luckydraw.py           # Random selection functionality
├── data/
│   ├── raw/               # Original voting data
│   │   ├── BI_results_Y6-8.csv
│   │   └── BI_results_Y9-12.csv
│   ├── processed/         # Cleaned data (emails removed)
│   │   ├── BI_results_no_emails_Y6-8.csv
│   │   └── BI_results_no_emails_Y9-12.csv
│   └── final_results.md   # Final voting results
```

## Features

- Processes ranked choice voting data
- Supports multiple year groups (Y6-8 and Y9-12)
- Removes sensitive information (emails) during processing
- Generates final results in markdown format
- Includes lucky draw functionality

## Requirements

This project uses Python. The specific version requirement is defined in `.python-version`.

Dependencies are managed through `pyproject.toml`.

use 'uv sync' to update dependencies
install uv
for macOS and linux: Use curl to download the script and execute it with sh:
`curl -LsSf https://astral.sh/uv/install.sh | sh`

see also: [https://uv.astral.sh](https://uv.astral.sh)

## Usage

1. Place raw voting data in the `data/raw/` directory

2. Run the main script:

```bash
uv run main.py
```

```bash
python main.py
```

3. Find processed results in:
   - `data/processed/` for intermediate files
   - `data/final_results.md` for final results

## Development

- Use `pyproject.toml` for dependency management
- Follow the existing data processing pipeline:
  1. Raw data input
  2. Email removal
  3. Vote calculation
  4. Results generation

## Data Output

The system processes voting data in multiple stages:

1. Raw data: Stored in `data/raw/` (not included in the repository for privacy)
2. Processed data: Email addresses removed, stored in `data/processed/`
3. Final results: Compiled and stored in `data/final_results.md`

This multi-stage approach ensures voter privacy while maintaining data integrity throughout the processing pipeline.
