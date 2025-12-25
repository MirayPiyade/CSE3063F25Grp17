import sys
from typing import Optional, List
from rag.config.config import Config
from rag.config.config_loader import ConfigLoader
from rag.config.config_loader import ConfigLoader
from rag.app.rag_orchestrator import RagOrchestrator
from rag.app.policy_router import PolicyRouter


def extract_arg(args: List[str], key: str) -> Optional[str]:
    if args is None:
        return None
    for i in range(len(args)):
        if key == args[i] and i + 1 < len(args):
            return args[i + 1]
    return None


from rich.console import Console

def prompt_question() -> Optional[str]:
    try:
        console = Console()
        return console.input("[bold italic #DA70D6]✨Question✨:[/bold italic #DA70D6] ")
    except (EOFError, KeyboardInterrupt):
        return None


def main() -> None:
    args: List[str] = sys.argv[1:]
    config_path: Optional[str] = extract_arg(args, "--config")
    mode_name: Optional[str] = extract_arg(args, "--mode")
    
    # If no config and no mode provided, and no batch, interactive select
    if not config_path and not mode_name and not extract_arg(args, "--batch"):
        router = PolicyRouter()
        config_path = router.interactive_select()
    
    # If mode provided, resolve to config path
    if mode_name:
        router = PolicyRouter()
        resolved = router.get_config_path(mode_name)
        if resolved:
            config_path = resolved
        else:
             print(f"Unknown mode: {mode_name}")
             # optional: fallback to interactive? or exit. Exit is safer for scripting.
             sys.exit(1)

    cli_question: Optional[str] = extract_arg(args, "--q")
    cli_reranker: Optional[str] = extract_arg(args, "--reranker")
    batch_path: Optional[str] = extract_arg(args, "--batch")

    base_config: Config = ConfigLoader.load(config_path)

    if batch_path:
        import json
        try:
            with open(batch_path, 'r', encoding='utf-8') as f:
                batch_data = json.load(f)
                
            if isinstance(batch_data, list):
                for item in batch_data:
                    if isinstance(item, dict) and "question" in item:
                        q = item["question"]
                        print(f"\nProcessing question: {q}")
                        effective_config = base_config.with_question(q)
                        if cli_reranker and cli_reranker.strip():
                            effective_config = effective_config.with_reranker_type(cli_reranker)
                        
                        orchestrator = RagOrchestrator(effective_config)
                        orchestrator.run()
                    else:
                         print(f"Skipping invalid item in batch: {item}")
            else:
                 print("Batch file must contain a JSON list of objects associated with 'question' key..")

        except Exception as e:
            print(f"Error processing batch file: {e}")
            sys.exit(1)
        return

    question: Optional[str] = cli_question if cli_question else base_config.question
    if not question or not question.strip():
        question = prompt_question()

    effective_config: Config = base_config.with_question(question or "")
    if cli_reranker and cli_reranker.strip():
        effective_config = effective_config.with_reranker_type(cli_reranker)

    orchestrator: RagOrchestrator = RagOrchestrator(effective_config)
    orchestrator.run()


if __name__ == "__main__":
    main()

