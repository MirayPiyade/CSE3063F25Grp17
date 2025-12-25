import time
from typing import List, Dict, Any, Tuple
from rag.app.rag_orchestrator import RagOrchestrator
from rag.config.config import Config
from rag.app.context import Context

class RagEvaluator:
    def __init__(self, orchestrator_factory):
        self.orchestrator_factory = orchestrator_factory

    def evaluate(self, test_cases: List[Dict[str, Any]]) -> Dict[str, Any]:
        results = []
        total_latency = 0
        total_hits = 0
        
        for case in test_cases:
            question = case["question"]
            expected_doc_id = case.get("expected_doc_id")
            
            start_time = time.time()
            
            # Create a fresh orchestrator for each run to avoid cache pollution if needed
            # (Though in this design we might re-use, let's create fresh config per question)
            orchestrator = self.orchestrator_factory(question)
            
            # Run pipeline
            # We need to access context, so we might need to modify RagOrchestrator.run()
            # to return context or expose it.
            # Assuming we refactor run() to return context:
            context = orchestrator.run_with_context() 
            
            latency = time.time() - start_time
            total_latency += latency
            
            # Check Retrieval Quality (Hits)
            raw_hits = context.get_hits()
            hit_ids = [h.doc_id for h in raw_hits] if raw_hits else []
            
            # Support list of expected IDs or single ID
            expected_ids = case.get("expected_doc_ids", [])
            if not expected_ids and "expected_doc_id" in case:
                expected_ids = [case["expected_doc_id"]]
            
            # Hit is true if ANY expected ID is found in ANY retrieved ID (substring match allowed)
            is_hit = False
            for target_id in expected_ids:
                if any(target_id in hid for hid in hit_ids):
                    is_hit = True
                    break
            
            if is_hit:
                total_hits += 1
                
            # Check Answer Quality (Keywords)
            answer_obj = context.get_answer()
            answer_text = answer_obj.text.lower() if answer_obj else ""
            expected_keywords = case.get("expected_keywords", [])
            
            # Match if likely all keywords are present? Or valid subset?
            # Let's say if >50% of keywords are present
            kw_matches = sum(1 for kw in expected_keywords if kw.lower() in answer_text)
            is_answer_match = (kw_matches >= 1) if expected_keywords else False # At least 1 match for now
            
            results.append({
                "question": question,
                "latency_sec": round(latency, 2),
                "retrieved_ids": hit_ids,
                "expected_ids": expected_ids,
                "is_hit": is_hit,
                "is_answer_match": is_answer_match,
                "answer_text": answer_text[:100] + "..." if answer_text else ""
            })
            
        total_q = len(test_cases)
        total_answer_matches = sum(1 for r in results if r["is_answer_match"])
        
        return {
            "metrics": {
                "avg_latency": round(total_latency / total_q, 2) if total_q else 0,
                "hit_rate": round(total_hits / total_q, 2) if total_q else 0,
                "answer_match_rate": round(total_answer_matches / total_q, 2) if total_q else 0, 
                "total_questions": total_q
            },
            "details": results
        }
