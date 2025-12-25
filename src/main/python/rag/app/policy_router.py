from typing import Dict, List, Optional
from dataclasses import dataclass
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

@dataclass
class Policy:
    name: str
    description: str
    config_path: str

class PolicyRouter:
    def __init__(self):
        self.policies: Dict[str, Policy] = {
            "default": Policy(
                "default", 
                "Vector Search + LLM Answer (MongoDB)", 
                "config/config.yaml"
            ),
            "keyword-simple": Policy(
                "keyword-simple",
                "Keyword Search + Simple Rerank",
                "config/keyword_simple_config.yaml"
            ),
            "offline-stub": Policy(
                "offline-stub", 
                "Stub Vector + Stub Embed (Offline Test)", 
                "config/vector_stub_config.yaml"
            )
        }
        self.console = Console()

    def list_policies(self) -> List[Policy]:
        return list(self.policies.values())

    def get_config_path(self, policy_name: str) -> Optional[str]:
        policy = self.policies.get(policy_name)
        return policy.config_path if policy else None

    def interactive_select(self) -> Optional[str]:
        self.console.print("\n[bold cyan]Select a RAG Mode (Policy):[/bold cyan]")
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="dim", width=4)
        table.add_column("Mode Name", style="cyan")
        table.add_column("Description", style="white")

        policies = self.list_policies()
        for idx, policy in enumerate(policies, 1):
            table.add_row(str(idx), policy.name, policy.description)

        self.console.print(table)
        
        choices = [str(i) for i in range(1, len(policies) + 1)]
        selection = Prompt.ask("Enter choice", choices=choices, default="1")
        
        selected_policy = policies[int(selection) - 1]
        self.console.print(f"\n[green]Selected:[/green] {selected_policy.name} -> {selected_policy.config_path}\n")
        return selected_policy.config_path
