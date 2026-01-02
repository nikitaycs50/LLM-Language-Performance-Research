"""
Mistral AI Language Performance Evaluation - Real-World Usage
Tests hypothesis: Russian vs English performance for everyday user queries
"""

import json
from typing import List, Dict
import time
from datetime import datetime
from dotenv import load_dotenv
import os
from pathlib import Path

# Get the project root directory (one level up from scripts/)
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent

# Load environment variables from .env file in project root
load_dotenv(PROJECT_ROOT / ".env")

# Real-World Test Dataset - Everyday User Queries
TEST_DATASET = {
    "practical_advice": [
        {
            "id": "pa_01",
            "russian": "Как лучше всего удалить жирное пятно с хлопковой рубашки?",
            "english": "What's the best way to remove a grease stain from a cotton shirt?",
            "category": "Household Tips",
            "evaluation_criteria": ["actionable steps", "specific products/methods", "safety warnings"]
        },
        {
            "id": "pa_02",
            "russian": "Подскажи простой рецепт борща для новичка",
            "english": "Give me a simple borscht recipe for a beginner",
            "category": "Cooking",
            "evaluation_criteria": ["ingredient list", "step-by-step instructions", "cooking time"]
        },
        {
            "id": "pa_03",
            "russian": "Как быстро заснуть, если не спится?",
            "english": "How can I fall asleep quickly when I can't sleep?",
            "category": "Health & Wellness",
            "evaluation_criteria": ["multiple techniques", "scientific basis", "practical applicability"]
        }
    ],
    
    "tech_support": [
        {
            "id": "ts_01",
            "russian": "Почему телефон быстро разряжается и как это исправить?",
            "english": "Why does my phone battery drain quickly and how to fix it?",
            "category": "Smartphone Issues",
            "evaluation_criteria": ["common causes", "troubleshooting steps", "settings to check"]
        },
        {
            "id": "ts_02",
            "russian": "Как очистить память на компьютере, чтобы он работал быстрее?",
            "english": "How do I clear memory on my computer to make it faster?",
            "category": "Computer Performance",
            "evaluation_criteria": ["specific methods", "safety considerations", "expected results"]
        },
        {
            "id": "ts_03",
            "russian": "Не могу подключиться к WiFi, что делать?",
            "english": "I can't connect to WiFi, what should I do?",
            "category": "Network Troubleshooting",
            "evaluation_criteria": ["diagnostic steps", "common solutions", "ordered by likelihood"]
        }
    ],
    
    "education_help": [
        {
            "id": "eh_01",
            "russian": "Объясни простыми словами, как работает фотосинтез",
            "english": "Explain in simple terms how photosynthesis works",
            "category": "Science Explanation",
            "evaluation_criteria": ["clarity for lay audience", "accuracy", "helpful analogies"]
        },
        {
            "id": "eh_02",
            "russian": "Помоги решить квадратное уравнение: x² + 5x + 6 = 0",
            "english": "Help me solve the quadratic equation: x² + 5x + 6 = 0",
            "category": "Math Help",
            "evaluation_criteria": ["correct solution", "step-by-step process", "explanation of method"]
        },
        {
            "id": "eh_03",
            "russian": "Какие основные причины Первой мировой войны?",
            "english": "What were the main causes of World War I?",
            "category": "History",
            "evaluation_criteria": ["multiple factors listed", "historical accuracy", "clear organization"]
        }
    ],
    
    "career_finance": [
        {
            "id": "cf_01",
            "russian": "Как правильно составить резюме для IT-специалиста?",
            "english": "How to write a resume properly for an IT professional?",
            "category": "Career Advice",
            "evaluation_criteria": ["specific IT-relevant tips", "structure recommendations", "common mistakes"]
        },
        {
            "id": "cf_02",
            "russian": "Стоит ли брать ипотеку или лучше копить на квартиру?",
            "english": "Should I take a mortgage or save up for an apartment?",
            "category": "Financial Planning",
            "evaluation_criteria": ["pros and cons both sides", "factors to consider", "balanced perspective"]
        },
        {
            "id": "cf_03",
            "russian": "Как попросить повышение зарплаты у начальника?",
            "english": "How do I ask my boss for a salary raise?",
            "category": "Workplace Communication",
            "evaluation_criteria": ["preparation steps", "communication tactics", "timing advice"]
        }
    ],
    
    "entertainment": [
        {
            "id": "ent_01",
            "russian": "Посоветуй фильм для вечера пятницы, люблю триллеры",
            "english": "Recommend a movie for Friday night, I like thrillers",
            "category": "Entertainment Recommendation",
            "evaluation_criteria": ["multiple suggestions", "brief descriptions", "variety of options"]
        },
        {
            "id": "ent_02",
            "russian": "Какую книгу почитать для саморазвития?",
            "english": "What book should I read for self-improvement?",
            "category": "Book Recommendations",
            "evaluation_criteria": ["relevant suggestions", "brief rationale", "different approaches"]
        },
        {
            "id": "ent_03",
            "russian": "Чем заняться в дождливый выходной дома?",
            "english": "What to do on a rainy weekend at home?",
            "category": "Activity Ideas",
            "evaluation_criteria": ["variety of activities", "different interests covered", "practical suggestions"]
        }
    ],
    
    "relationships_social": [
        {
            "id": "rs_01",
            "russian": "Как извиниться перед другом после ссоры?",
            "english": "How to apologize to a friend after an argument?",
            "category": "Interpersonal Relationships",
            "evaluation_criteria": ["empathetic approach", "concrete steps", "dos and don'ts"]
        },
        {
            "id": "rs_02",
            "russian": "Как начать разговор с незнакомым человеком?",
            "english": "How to start a conversation with a stranger?",
            "category": "Social Skills",
            "evaluation_criteria": ["practical openers", "context consideration", "follow-up tips"]
        },
        {
            "id": "rs_03",
            "russian": "Что подарить на день рождения коллеге?",
            "english": "What to give as a birthday gift to a colleague?",
            "category": "Gift Ideas",
            "evaluation_criteria": ["appropriate suggestions", "budget considerations", "workplace-appropriate"]
        }
    ],
    
    "general_knowledge": [
        {
            "id": "gk_01",
            "russian": "Почему небо голубое?",
            "english": "Why is the sky blue?",
            "category": "Science Facts",
            "evaluation_criteria": ["scientifically accurate", "understandable explanation", "appropriate detail level"]
        },
        {
            "id": "gk_02",
            "russian": "Сколько планет в Солнечной системе и как они называются?",
            "english": "How many planets are in the Solar System and what are their names?",
            "category": "Basic Astronomy",
            "evaluation_criteria": ["factually correct (8 planets)", "proper order optional", "clear listing"]
        },
        {
            "id": "gk_03",
            "russian": "Какая разница между вирусом и бактерией?",
            "english": "What's the difference between a virus and a bacteria?",
            "category": "Medical Knowledge",
            "evaluation_criteria": ["key differences explained", "examples provided", "accurate biology"]
        }
    ]
}


def call_mistral_api(prompt: str, language: str, api_key: str = None, model: str = "mistral-large-latest") -> Dict:
    """
    Call Mistral API with the given prompt
    
    Args:
        prompt: The question/prompt to send
        language: 'russian' or 'english'
        api_key: Your Mistral API key (optional, will load from .env if not provided)
        model: Mistral model to use
    
    Returns:
        Dict with response and metadata
    """
    # Get API key from environment if not provided
    if api_key is None:
        api_key = os.getenv("MISTRAL_API_KEY")
    
    if api_key is None:
        raise ValueError("MISTRAL_API_KEY not found in environment or passed as parameter")
    
    # Import Mistral client (new SDK - imported here to avoid dependency if not using API)
    from mistralai import Mistral
    from mistralai.models import usermessage
    
    client = Mistral(api_key=api_key)
    messages = [usermessage.UserMessage(role="user", content=prompt)]
    
    start_time = time.time()
    chat_response = client.chat.complete(
        model=model,
        messages=messages,
    )
    latency = (time.time() - start_time) * 1000
    
    return {
        "response_text": chat_response.choices[0].message.content,
        "tokens_used": chat_response.usage.total_tokens,
        "latency_ms": latency,
        "language": language,
        "model": model
    }


def evaluate_response_quality(response: str, criteria: List[str], language: str) -> Dict:
    """
    Evaluate response quality based on criteria
    
    This should ideally involve:
    1. Human evaluation (most reliable)
    2. LLM-as-judge (GPT-4/Claude as evaluator)
    3. Automated metrics (BLEU, ROUGE, etc.)
    
    Returns scores for each criterion
    """
    # IMPLEMENTATION REQUIRED
    # For robust results, use LLM-as-judge or human evaluation
    
    scores = {}
    for criterion in criteria:
        # Placeholder - implement actual evaluation
        scores[criterion] = {
            "present": None,  # True/False - is criterion met?
            "quality": None,  # 1-5 scale
            "notes": "Requires manual evaluation"
        }
    
    return {
        "criteria_scores": scores,
        "overall_quality": None,  # 1-5 scale
        "completeness": None,  # 1-5 scale
        "clarity": None,  # 1-5 scale
        "accuracy": None,  # 1-5 scale
        "helpfulness": None,  # 1-5 scale
        "language": language
    }


def calculate_response_metrics(response: str, language: str) -> Dict:
    """
    Calculate objective metrics about the response
    """
    return {
        "char_count": len(response),
        "word_count": len(response.split()),
        "has_numbered_list": any(line.strip().startswith(tuple('123456789')) for line in response.split('\n')),
        "has_bullet_points": '•' in response or '*' in response or '-' in response[:100],
        "language": language
    }


def run_experiment(api_key: str = None, output_file: str = "everyday_results.json", model: str = "mistral-large-latest", agent_id: str = None):
    """
    Run the full experiment comparing Russian vs English for everyday queries
    
    Args:
        api_key: Mistral API key (optional, will load from .env if not provided)
        output_file: Path to save results JSON file
        model: Mistral model to use
        agent_id: Agent/experiment identifier (optional, will load from .env if not provided)
    """
    # Get API key from parameter or environment variable
    if api_key is None:
        api_key = os.getenv("MISTRAL_API_KEY")
    
    if api_key is None:
        print("WARNING: No API key provided. Set MISTRAL_API_KEY in .env file or pass api_key parameter.")
        print("Continuing with simulated responses...")
    
    # Get agent_id from parameter or environment variable
    if agent_id is None:
        agent_id = os.getenv("AGENT_ID")
    
    results = []
    timestamp = datetime.now().isoformat()
    
    print("=" * 70)
    print("MISTRAL AI LANGUAGE PERFORMANCE - EVERYDAY USER QUERIES")
    print("=" * 70)
    print(f"Model: {model}")
    print(f"Timestamp: {timestamp}")
    print(f"Total test cases: {sum(len(cases) for cases in TEST_DATASET.values())}")
    print("=" * 70)
    
    for category, test_cases in TEST_DATASET.items():
        print(f"\n### Category: {category.replace('_', ' ').upper()} ###\n")
        
        for test in test_cases:
            test_result = {
                "id": test["id"],
                "category": test["category"],
                "evaluation_criteria": test["evaluation_criteria"],
                "timestamp": datetime.now().isoformat()
            }
            
            print(f"\n[TEST {test['id']}] {test['category']}")
            
            # Test Russian
            russian_response = call_mistral_api(test["russian"], "russian", api_key, model)
            time.sleep(1)  # Rate limiting
            
            # Test English  
            english_response = call_mistral_api(test["english"], "english", api_key, model)
            time.sleep(1)
            
            # Calculate metrics
            russian_metrics = calculate_response_metrics(russian_response["response_text"], "russian")
            english_metrics = calculate_response_metrics(english_response["response_text"], "english")
            
            # Evaluate quality (requires implementation)
            russian_eval = evaluate_response_quality(
                russian_response["response_text"], 
                test["evaluation_criteria"],
                "russian"
            )
            english_eval = evaluate_response_quality(
                english_response["response_text"], 
                test["evaluation_criteria"],
                "english"
            )
            
            test_result["russian"] = {
                "query": test["russian"],
                "response": russian_response["response_text"],
                "evaluation": russian_eval,
                "metrics": russian_metrics,
                "api_metadata": {
                    "tokens": russian_response["tokens_used"],
                    "latency_ms": russian_response["latency_ms"],
                    "model": russian_response["model"]
                }
            }
            
            test_result["english"] = {
                "query": test["english"],
                "response": english_response["response_text"],
                "evaluation": english_eval,
                "metrics": english_metrics,
                "api_metadata": {
                    "tokens": english_response["tokens_used"],
                    "latency_ms": english_response["latency_ms"],
                    "model": english_response["model"]
                }
            }
            
            results.append(test_result)
            print(f"✓ Completed {test['id']}")
    
    # Save results
    output_data = {
        "metadata": {
            "experiment_type": "everyday_queries",
            "model": model,
            "timestamp": timestamp,
            "total_tests": len(results),
            "agent_id": agent_id
        },
        "results": results
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'=' * 70}")
    print(f"✓ Experiment complete! Results saved to {output_file}")
    print(f"Total test pairs: {len(results)}")
    print(f"{'=' * 70}")
    
    return results


def analyze_results(results_file: str = "everyday_results.json"):
    """
    Analyze comparative performance
    """
    with open(results_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    results = data["results"]
    
    print("\n" + "=" * 70)
    print("ANALYSIS: RUSSIAN vs ENGLISH PERFORMANCE")
    print("=" * 70)
    
    # Objective metrics comparison
    print("\n### OBJECTIVE METRICS ###\n")
    
    total_russian_words = sum(r["russian"]["metrics"]["word_count"] for r in results)
    total_english_words = sum(r["english"]["metrics"]["word_count"] for r in results)
    avg_russian_words = total_russian_words / len(results)
    avg_english_words = total_english_words / len(results)
    
    print(f"Average response length:")
    print(f"  Russian: {avg_russian_words:.1f} words")
    print(f"  English: {avg_english_words:.1f} words")
    print(f"  Difference: {abs(avg_russian_words - avg_english_words):.1f} words ({((avg_russian_words/avg_english_words - 1) * 100):.1f}%)")
    
    avg_russian_latency = sum(r["russian"]["api_metadata"]["latency_ms"] for r in results) / len(results)
    avg_english_latency = sum(r["english"]["api_metadata"]["latency_ms"] for r in results) / len(results)
    
    print(f"\nAverage response time:")
    print(f"  Russian: {avg_russian_latency:.0f}ms")
    print(f"  English: {avg_english_latency:.0f}ms")
    
    # Category breakdown
    print("\n### BY CATEGORY ###\n")
    categories = {}
    for result in results:
        cat = result["category"]
        if cat not in categories:
            categories[cat] = {
                "count": 0,
                "russian_avg_words": [],
                "english_avg_words": []
            }
        categories[cat]["count"] += 1
        categories[cat]["russian_avg_words"].append(result["russian"]["metrics"]["word_count"])
        categories[cat]["english_avg_words"].append(result["english"]["metrics"]["word_count"])
    
    for cat, stats in sorted(categories.items()):
        rus_avg = sum(stats["russian_avg_words"]) / len(stats["russian_avg_words"])
        eng_avg = sum(stats["english_avg_words"]) / len(stats["english_avg_words"])
        print(f"{cat}:")
        print(f"  Tests: {stats['count']}")
        print(f"  Russian avg: {rus_avg:.1f} words | English avg: {eng_avg:.1f} words")
    
    print("\n" + "=" * 70)
    print("\nNOTE: Quality evaluation requires manual assessment or LLM-as-judge")
    print("See evaluation fields in JSON for detailed scoring framework")
    print("=" * 70)


def export_for_human_evaluation(results_file: str = "everyday_results.json", 
                                 output_csv: str = "human_evaluation.csv"):
    """
    Export results in format suitable for human evaluation
    """
    import csv
    
    with open(results_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    with open(output_csv, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            "ID", "Category", "Query_Russian", "Response_Russian",
            "Query_English", "Response_English",
            "Score_Russian_Quality", "Score_English_Quality",
            "Score_Russian_Accuracy", "Score_English_Accuracy",
            "Score_Russian_Helpfulness", "Score_English_Helpfulness",
            "Winner", "Notes"
        ])
        
        for result in data["results"]:
            writer.writerow([
                result["id"],
                result["category"],
                result["russian"]["query"],
                result["russian"]["response"],
                result["english"]["query"],
                result["english"]["response"],
                "",  # To be filled by human evaluator
                "",
                "",
                "",
                "",
                "",
                "",  # Winner: Russian/English/Tie
                ""   # Notes
            ])
    
    print(f"✓ Exported {len(data['results'])} test pairs to {output_csv} for human evaluation")


if __name__ == "__main__":
    import sys
    
    # Check if user wants to run analysis or export instead
    if len(sys.argv) > 1:
        if sys.argv[1] == "analyze":
            results_file = sys.argv[2] if len(sys.argv) > 2 else "everyday_results.json"
            analyze_results(results_file)
        elif sys.argv[1] == "export":
            results_file = sys.argv[2] if len(sys.argv) > 2 else "everyday_results.json"
            output_csv = sys.argv[3] if len(sys.argv) > 3 else "human_evaluation.csv"
            export_for_human_evaluation(results_file, output_csv)
        elif sys.argv[1] == "help":
            print("\n" + "=" * 70)
            print("REAL-WORLD MISTRAL LANGUAGE EVALUATION")
            print("=" * 70)
            print("\nThis script tests everyday user queries across 7 categories:")
            print("1. Practical Advice (household, cooking, health)")
            print("2. Tech Support (phones, computers, networks)")
            print("3. Education Help (science, math, history)")
            print("4. Career & Finance (resume, salary, mortgages)")
            print("5. Entertainment (movies, books, activities)")
            print("6. Relationships & Social (friends, conversations, gifts)")
            print("7. General Knowledge (science facts, basic info)")
            
            print(f"\nTotal test pairs: {sum(len(cases) for cases in TEST_DATASET.values())}")
            
            print("\n" + "=" * 70)
            print("USAGE:")
            print("  python scripts/lang_perf.py                    # Run experiment")
            print("  python scripts/lang_perf.py analyze            # Analyze results")
            print("  python scripts/lang_perf.py export            # Export for human evaluation")
            print("  python scripts/lang_perf.py help              # Show this help")
            print("=" * 70)
        else:
            print(f"Unknown command: {sys.argv[1]}")
            print("Use 'help' to see usage instructions")
    else:
        # Default: Run the experiment
        print("\n" + "=" * 70)
        print("REAL-WORLD MISTRAL LANGUAGE EVALUATION")
        print("=" * 70)
        print("\nStarting experiment...")
        print("API key will be loaded from .env file")
        print("=" * 70 + "\n")
        
        try:
            results = run_experiment()
            print("\n" + "=" * 70)
            print("EXPERIMENT COMPLETE!")
            print("=" * 70)
            print("\nNext steps:")
            print("  python scripts/lang_perf.py analyze            # Analyze results")
            print("  python scripts/lang_perf.py export            # Export for human evaluation")
            print("=" * 70)
        except ValueError as e:
            print(f"\nERROR: {e}")
            print("\nPlease ensure your .env file contains:")
            print("  MISTRAL_API_KEY=your-actual-api-key-here")
            print("\nYou can create it by copying .env_example:")
            print("  cp .env_example .env")
            sys.exit(1)
        except Exception as e:
            print(f"\nERROR: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)