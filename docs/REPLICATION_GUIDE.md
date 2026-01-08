# Replication Guide

This guide provides step-by-step instructions for replicating the Language-Dependent Communication Strategies study.

---

## Prerequisites

### Required Software

- **Python 3.10+** (tested with Python 3.10)
- **pip** (Python package manager)
- **Git** (for cloning repository)

### Required Accounts

- **Mistral AI API account** with API key
  - Sign up at: https://mistral.ai
  - Obtain API key from dashboard

### Estimated Costs

- **API costs:** ~$0.50-2.00 USD (depending on Mistral pricing)
- **Time:** ~1 hour (48 minutes data collection + setup)

---

## Step 1: Clone the Repository

```bash
git clone https://github.com/nikitaycs50/LLM-Language-Performance-Research.git
cd LLM-Language-Performance-Research
```

---

## Step 2: Set Up Python Environment

### Option A: Using venv (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Option B: Using conda

```bash
conda create -n llm-research python=3.10
conda activate llm-research
pip install -r requirements.txt
```

---

## Step 3: Configure API Key

### Create `.env` File

Create a `.env` file in the project root directory:

```bash
# Copy example (if exists)
cp .env.example .env

# Or create new file
touch .env
```

### Add Your API Key

Edit `.env` and add your Mistral AI API key:

```bash
MISTRAL_API_KEY=your_api_key_here
```

**Security Note:** Never commit `.env` to version control. It's already in `.gitignore`.

---

## Step 4: Verify Setup

### Check Script Location

The main script should be at `scripts/lang_perf.py`. Verify:

```bash
ls scripts/lang_perf.py
```

### Test API Connection (Optional)

You can test your API key by running a simple test:

```python
from dotenv import load_dotenv
import os
from mistralai import Mistral

load_dotenv()
client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

# Test query
response = client.chat.complete(
    model="mistral-large-latest",
    messages=[{"role": "user", "content": "Hello"}]
)
print(response.choices[0].message.content)
```

---

## Step 5: Run the Experiment

### Basic Execution

Run the data collection script:

```bash
python scripts/lang_perf.py
```

### Expected Output

You should see output similar to:

```
======================================================================
REAL-WORLD MISTRAL LANGUAGE EVALUATION
======================================================================

Starting experiment...
API key will be loaded from .env file
======================================================================

======================================================================
MISTRAL AI LANGUAGE PERFORMANCE - EVERYDAY USER QUERIES
======================================================================
Model: mistral-large-latest
Timestamp: 2026-01-02T09:54:49.773771
Total test cases: 21
======================================================================

### Category: PRACTICAL ADVICE ###

[TEST pa_01] Household Tips
✓ Completed pa_01

[TEST pa_02] Cooking
✓ Completed pa_02
...
```

### Execution Time

- **Total queries:** 42 (21 pairs)
- **Estimated time:** ~48 minutes
- **Rate limiting:** 1 second between requests (built into script)

### Output Files

After completion, you should have:

- `data/everyday_results.json` - Complete dataset with all responses
- `data/lang_perf_run_output.txt` - Execution log (if script generates it)

---

## Step 6: Analyze Results

### Run Analysis

The script includes an analysis mode:

```bash
python scripts/lang_perf.py analyze
```

### Expected Analysis Output

```
======================================================================
ANALYSIS: RUSSIAN vs ENGLISH PERFORMANCE
======================================================================

### OBJECTIVE METRICS ###

Average response length:
  Russian: 526.9 words
  English: 666.8 words
  Difference: 140.0 words (-21.0%)

Average response time:
  Russian: 28198ms
  English: 20619ms

### BY CATEGORY ###

Activity Ideas:
  Tests: 1
  Russian avg: 599.0 words | English avg: 910.0 words
...
```

### Export for Human Evaluation

Export results to CSV for manual evaluation:

```bash
python scripts/lang_perf.py export
```

This creates `data/human_evaluation.csv` with structured data for manual review.

---

## Step 7: Verify Results

### Check Data File

Verify `data/everyday_results.json` contains:

- 21 test cases
- Each with Russian and English responses
- Metadata (tokens, latency, timestamps)
- Evaluation criteria

### Compare with Original Results

Compare your results with the original dataset:

- **Original average Russian:** 527 words
- **Original average English:** 667 words
- **Original Russian latency:** ~28.2 seconds
- **Original English latency:** ~20.6 seconds

**Note:** Results may vary slightly due to:
- Model updates
- API server load
- Network conditions
- Random sampling (if model uses sampling)

---

## Troubleshooting

### Common Issues

#### 1. API Key Not Found

**Error:** `MISTRAL_API_KEY not found`

**Solution:**
- Verify `.env` file exists in project root
- Check `.env` contains `MISTRAL_API_KEY=your_key`
- Ensure script loads `.env` (check `load_dotenv()` call)

#### 2. Import Errors

**Error:** `ModuleNotFoundError: No module named 'mistralai'`

**Solution:**
```bash
pip install -r requirements.txt
```

#### 3. Rate Limiting

**Error:** `429 Too Many Requests`

**Solution:**
- Script includes 1-second delay between requests
- If still hitting limits, increase delay in script
- Check Mistral API rate limits in dashboard

#### 4. API Errors

**Error:** `401 Unauthorized` or `403 Forbidden`

**Solution:**
- Verify API key is correct
- Check API key has necessary permissions
- Verify account is active and has credits

#### 5. File Not Found

**Error:** `FileNotFoundError: everyday_results.json`

**Solution:**
- Ensure `data/` directory exists
- Check script has write permissions
- Verify script is run from project root

---

## Customization

### Modify Query Dataset

Edit `scripts/lang_perf.py` to modify the `TEST_DATASET` dictionary:

```python
TEST_DATASET = {
    "your_category": [
        {
            "id": "test_01",
            "russian": "Ваш запрос на русском",
            "english": "Your query in English",
            "category": "Category Name",
            "evaluation_criteria": ["criterion1", "criterion2"]
        }
    ]
}
```

### Change Model

Modify the model parameter in the script:

```python
model = "mistral-large-latest"  # Change to desired model
```

**Note:** Different models may have different API parameters and pricing.

### Adjust Rate Limiting

Modify the delay between requests:

```python
time.sleep(1)  # Change to desired seconds
```

---

## Expected Results

### Quantitative Metrics

Based on original study:

| Metric | Russian | English | Difference |
|--------|---------|---------|------------|
| Avg words | ~527 | ~667 | -21% |
| Avg latency | ~28.2s | ~20.6s | +37% |
| Information density | Higher | Lower | +15% |

### Qualitative Patterns

- **Russian:** More hierarchical, structured, expert-oriented
- **English:** More narrative, comprehensive, learner-oriented

See full research paper for detailed qualitative analysis.

---

## Next Steps

### 1. Compare Your Results

- Compare quantitative metrics with original study
- Note any significant differences
- Document model version and date

### 2. Extend the Study

- Add more query pairs
- Test different categories
- Try different models
- Test additional languages

### 3. Contribute

- Share your results
- Submit improvements to scripts
- Extend methodology
- See `CONTRIBUTING.md` for guidelines

---

## Resources

- **Full Research Paper:** `paper/full_research_paper.md`
- **Methodology Details:** `docs/METHODOLOGY.md`
- **Dataset:** `data/everyday_results.json`
- **Original Execution Log:** `data/lang_perf_run_output.txt`
- **Mistral AI Docs:** https://docs.mistral.ai

---

## Support

For issues or questions:

1. Check this guide and `docs/METHODOLOGY.md`
2. Review original execution log: `data/lang_perf_run_output.txt`
3. Open an issue on GitHub
4. Contact: yampolski.net

---

**Good luck with your replication!**
