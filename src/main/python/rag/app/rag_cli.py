import sys
from typing import Optional, List
from rag.config.config import Config
from rag.config.config_loader import ConfigLoader
from rag.app.rag_orchestrator import RagOrchestrator


def extract_arg(args: List[str], key: str) -> Optional[str]:
    if args is None:
        return None
    for i in range(len(args)):
        if key == args[i] and i + 1 < len(args):
            return args[i + 1]
    return None


def prompt_question() -> Optional[str]:
    try:
        return input("Question: ")
    except (EOFError, KeyboardInterrupt):
        return None


def main() -> None:
    args: List[str] = sys.argv[1:]
    config_path: Optional[str] = extract_arg(args, "--config")
    cli_question: Optional[str] = extract_arg(args, "--q")
    cli_reranker: Optional[str] = extract_arg(args, "--reranker")

    base_config: Config = ConfigLoader.load(config_path)
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

