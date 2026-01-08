# Research Methodology

This document provides a detailed overview of the research methodology used in the Language-Dependent Communication Strategies study.

---

## Research Design

### Paired Comparison Design

We employed a **paired comparison design** with controlled conditions to isolate language effects from content variance. Each test case consisted of:

- One Russian query
- One English query with equivalent semantic intent
- Both submitted to the same model under identical conditions
- Responses analyzed across multiple dimensions

**Key principle:** Queries were not direct translations but natural phrasings a native speaker would use, ensuring ecological validity.

### Research Questions

**RQ1:** Do Russian and English inputs to the same LLM produce responses of different length, density, and processing characteristics when controlling for semantic equivalence?

**RQ2:** If differences exist, do they reflect mere translation variance or systematic patterns in communication strategy and information architecture?

**RQ3:** Can observed differences be mapped to user optimization profiles (e.g., expert vs. novice, reference vs. tutorial), and what are the implications for multilingual AI system design?

---

## Query Selection and Dataset Construction

### Categories

We selected seven everyday use categories representing realistic user needs:

1. **Practical Advice** (n=3): Household tips, cooking, health/wellness
2. **Technical Support** (n=3): Smartphone, computer, network issues
3. **Education Help** (n=3): Science, mathematics, history
4. **Career & Finance** (n=3): Resume writing, financial planning, workplace communication
5. **Entertainment** (n=3): Movie/book recommendations, activity ideas
6. **Social Skills** (n=3): Interpersonal relationships, conversation, gift-giving
7. **General Knowledge** (n=3): Science facts, astronomy, medical information

**Rationale:** These categories reflect common LLM use cases as reported in user surveys and avoid narrow academic domains that might favor either language.

### Query Construction Principles

For each category, we created semantically equivalent pairs following these rules:

1. **Natural phrasing:** Each query uses idiomatic expressions native speakers would employ
2. **Equivalent specificity:** Same level of detail requested (no hidden complexity differences)
3. **Neutral framing:** Avoid leading questions or culturally specific references
4. **Actionable intent:** User seeks practical help, not abstract discussion

**Example pair:**
```
Russian: "Как быстро заснуть, если не спится?"
English: "How can I fall asleep quickly when I can't sleep?"

Intent: User wants practical sleep advice
Specificity: Both ask for "quick" methods
Framing: Both imply current difficulty
```

### Evaluation Criteria

For each query, we predefined 3 evaluation criteria representing what constitutes a "good" answer:

- **Household tips:** actionable steps, specific products/methods, safety warnings
- **Tech support:** common causes, troubleshooting steps, settings to check
- **Education:** clarity for lay audience, accuracy, helpful analogies
- **Career advice:** specific domain tips, structure recommendations, common mistakes

These criteria enabled systematic assessment of response completeness.

---

## Experimental Setup

### Technical Configuration

**Model:** Mistral AI `mistral-large-latest`  
**API Endpoint:** Mistral AI API  
**Request Parameters:**
```python
{
  "model": "mistral-large-latest",
  "max_tokens": 1000,  # Handled by API
  "messages": [{"role": "user", "content": query}]
}
```

**Environment:**
- Python 3.10+
- mistralai SDK
- Rate limiting: 1-second delay between requests
- No temperature or sampling parameter adjustments (defaults used)

### Data Collection Procedure

1. Load query pairs from structured JSON (see `scripts/lang_perf.py`)
2. For each pair:
   - Submit Russian query
   - Record response text, token count, latency
   - Wait 1 second
   - Submit English query
   - Record response text, token count, latency
   - Wait 1 second before next pair
3. Save all responses with metadata to JSON

**Temporal control:** All data collected on January 2, 2026, between 09:54-11:11 UTC to minimize time-of-day effects.

**Execution summary:**
- Total queries: 42 (21 pairs)
- Total time: ~48 minutes
- Model version: mistral-large-latest (snapshot: 2026-01-02)

See `data/lang_perf_run_output.txt` for complete execution log.

---

## Data Collected

For each response, we captured:

### Text Data
- Full response (unedited, as returned by API)
- Query text (original)

### Automatic Metrics
- Character count
- Word count (split on whitespace)
- Has numbered list (boolean)
- Has bullet points (boolean)

### API Metadata
- Total tokens used (input + output)
- Latency (milliseconds, from request to response)
- Model identifier
- Timestamp (ISO 8601 format)

### Data Format

All data is stored in JSON format following this structure:

```json
{
  "test_id": "pa_01",
  "category": "Household Tips",
  "russian": {
    "query": "...",
    "response": "...",
    "tokens": 1234,
    "latency_ms": 28198,
    "word_count": 527,
    "timestamp": "2026-01-02T09:54:49.773771"
  },
  "english": {
    "query": "...",
    "response": "...",
    "tokens": 987,
    "latency_ms": 20619,
    "word_count": 667,
    "timestamp": "2026-01-02T09:55:18.234567"
  },
  "evaluation_criteria": ["actionable steps", "specific products/methods", "safety warnings"]
}
```

See `data/everyday_results.json` for the complete dataset.

---

## Analysis Framework

We developed a three-dimensional analysis framework:

### 1. Content Quality Analysis

**Dimensions examined:**
- **Depth:** Number of distinct points covered
- **Detail:** Elaboration per point (examples, explanations)
- **Accuracy:** Technical correctness (domain expertise required)
- **Tone:** Formal vs conversational, assumptive vs explanatory
- **Consistency:** Uniformity of quality across response sections

**Method:** Systematic reading of all 42 responses with structured note-taking on each dimension.

### 2. Structural Organization Analysis

**Quantitative measurements:**
- Heading levels (count of `###`, `####`, etc.)
- Section lengths (words per section)
- List usage (bullets vs numbered vs none)
- Table frequency
- Code block usage
- Average bullet point length

**Qualitative assessment:**
- Information flow patterns (deductive vs inductive)
- Transition style (abrupt vs smooth)
- Navigation aids (summaries, TOCs, cross-references)
- Visual density (white space vs text blocks)

### 3. Helpfulness and Completeness Analysis

**Evaluation protocol:**

1. **Completeness check:** Does response address all aspects of query?
   - Complete ✓
   - Partial (specify what's missing) ⚠️
   - Incomplete ✗

2. **Actionability assessment:** Can user complete task with only this response?
   - Yes, completely
   - Yes, with minor external lookup
   - No, needs significant research

3. **Edge case coverage:** Are boundary conditions and exceptions handled?

4. **User optimization profile:** What user type benefits most?
   - Expert vs novice
   - Quick reference vs deep learning
   - Technical vs non-technical background

---

## Validity Considerations

### Internal Validity

**Controls implemented:**
- Same model version throughout
- Identical API parameters
- Sequential testing (no concurrent requests)
- Consistent rate limiting
- No prompt engineering or system messages

**Potential confounds:**
- Query order (always Russian first) - could introduce ordering effects, though unlikely given model statelessness
- API server load variations - mitigated by consistent timing
- Model updates during collection - verified version stability

### External Validity

**Generalizability:**
- ✓ Queries represent common real-world use cases
- ✓ Multiple domains tested
- ⚠️ Single model (Mistral) - findings may not transfer to GPT/Claude
- ⚠️ Two languages only - broader multilingual patterns unknown
- ⚠️ Everyday queries - specialized professional domains not tested

### Construct Validity

**Semantic equivalence verification:**
- Native speaker review (author fluent in both languages)
- Intent matching confirmed per pair
- No systematic complexity differences detected

**Measurement validity:**
- Multiple analysis dimensions reduce single-metric bias
- Structured evaluation frameworks applied systematically
- Inter-rater reliability: Single evaluator (author) - limitation acknowledged

---

## Limitations

1. **Single model tested:** Results specific to Mistral AI; generalization requires testing across models
2. **Sample size:** 21 query pairs provide strong indicators but larger samples would strengthen conclusions
3. **No human evaluation:** Quality assessments based on structural analysis, not user studies
4. **Query design:** Everyday questions may not represent specialized professional use cases
5. **Temporal constraint:** Single snapshot; model updates may alter patterns
6. **Single evaluator:** Analysis conducted by one researcher; inter-rater reliability not measured

See Section 13 of the full research paper for comprehensive limitations discussion.

---

## Statistical Approach

**Descriptive statistics used:**
- Mean response lengths (words)
- Mean processing times (latency)
- Information density calculations (actionable points per word)
- Category-level comparisons

**No inferential statistics:** Sample size (n=21 pairs) insufficient for reliable hypothesis testing. Findings are descriptive and exploratory, intended to generate hypotheses for future research.

---

## Reproducibility

All experimental conditions, data, and analysis code are available:

- **Scripts:** `scripts/lang_perf.py` - Data collection script
- **Data:** `data/everyday_results.json` - Complete dataset
- **Execution log:** `data/lang_perf_run_output.txt` - Detailed run log
- **Analysis:** See full research paper for detailed analysis

See `docs/REPLICATION_GUIDE.md` for step-by-step replication instructions.

---

**Keywords:** Large Language Models, Multilingual NLP, Communication Strategies, Information Architecture, User Experience, Mistral AI, Russian-English Comparison, LLM, AI

---

**Author:** Nikita Yampolski  
**Contact:** yampolski.net  
**Date:** January 2026  
**Model Tested:** Mistral AI mistral-large-latest  
**Institution/Affiliation:** ProductRocket.ch
