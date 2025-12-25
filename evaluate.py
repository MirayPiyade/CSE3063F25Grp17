import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src" / "main" / "python"))

import json
import argparse
from typing import Optional, List, Dict
from pathlib import Path
from rich.console import Console
from rich.table import Table

from rag.config.config_loader import ConfigLoader
from rag.app.rag_orchestrator import RagOrchestrator
from rag.app.policy_router import PolicyRouter
from rag.eval.evaluator import RagEvaluator

def run_evaluation(mode_name: str, config_path: str, test_cases: List, verbose: bool = True) -> Optional[Dict]:
    try:
        # Load base config
        base_config = ConfigLoader.load(config_path)
        base_config = base_config.with_cache_disabled()
        
        def orchestrator_factory(question: str) -> RagOrchestrator:
            cfg = base_config.with_question(question)
            cfg = cfg.with_cache_disabled() # Ensure it's disabled per request too
            return RagOrchestrator(cfg)

        evaluator = RagEvaluator(orchestrator_factory)
        report = evaluator.evaluate(test_cases)
        return report
    except Exception as e:
        print(f"Failed to evaluate {mode_name}: {e}")
        return None

def main() -> None:
    parser = argparse.ArgumentParser(description="Run Evaluation Harness for RAG")
    parser.add_argument("--mode", type=str, required=True, help="Mode/Policy to evaluate (e.g. offline-stub, hybrid-vector) or 'all'")
    parser.add_argument("--input", type=str, default="data/eval_questions.json", help="Path to evaluation dataset")
    args = parser.parse_args()

    # Load dataset
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: dataset not found at {input_path}")
        sys.exit(1)
        
    with open(input_path, 'r', encoding='utf-8') as f:
        test_cases = json.load(f)
        
    router = PolicyRouter()
    modes_to_run = []
    
    if args.mode.lower() == 'all':
        modes_to_run = router.list_policies()
    else:
        path = router.get_config_path(args.mode)
        if not path:
             print(f"Error: Unknown mode '{args.mode}'.")
             sys.exit(1)
        modes_to_run = [router.policies[args.mode]]

    results = []
    console = Console()

    for policy in modes_to_run:
        console.print(f"\n[bold cyan]Evaluating Policy: {policy.name}[/bold cyan] (Config: {policy.config_path})")
        report = run_evaluation(policy.name, policy.config_path, test_cases)
        
        if report:
            metrics = report["metrics"]
            results.append({
                "mode": policy.name,
                "hit_rate": metrics["hit_rate"],
                "answer_rate": metrics["answer_match_rate"],
                "avg_latency": metrics["avg_latency"],
                "total": metrics["total_questions"]
            })
            
            # Print minimal details if running all, or full if single?
            # Let's print full details for each to ensure visibility
            t_details = Table(show_header=True, header_style="bold magenta")
            t_details.add_column("Question", width=40)
            t_details.add_column("Hit?", justify="center")
            t_details.add_column("Ans Match?", justify="center")
            t_details.add_column("Latency")
            
            for row in report["details"]:
                is_hit_str = "[green]YES[/green]" if row["is_hit"] else "[red]NO[/red]"
                is_ans_str = "[green]YES[/green]" if row["is_answer_match"] else "[red]NO[/red]"
                t_details.add_row(
                    row["question"], 
                    is_hit_str, 
                    is_ans_str,
                    f"{row['latency_sec']}s"
                )
            console.print(t_details)

    # Final Comparative Table
    if len(results) > 1:
        console.print("\n[bold underline]Comparative Benchmark Results[/bold underline]\n")
        t_comp = Table(show_header=True, header_style="bold yellow")
        t_comp.add_column("Mode", style="cyan")
        t_comp.add_column("Hit Rate", style="green")
        t_comp.add_column("Ans Rate", style="magenta")
        t_comp.add_column("Avg Latency", style="white")
        
        for res in results:
            t_comp.add_row(
                res["mode"],
                f"{res['hit_rate'] * 100:.1f}%",
                f"{res['answer_rate'] * 100:.1f}%",
                f"{res['avg_latency']}s"
            )
        console.print(t_comp)

if __name__ == "__main__":
    main()
