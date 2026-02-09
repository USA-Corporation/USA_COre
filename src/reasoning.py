import time
import hashlib
from typing import Dict, List, Optional
from collections import defaultdict
import numpy as np

class ReasoningEngine:
    """Production reasoning engine with caching"""
    
    def __init__(self, max_depth: int = 10):
        self.max_depth = max_depth
        self.reasoning_cache = {}
        self.concept_graph = defaultdict(set)
        self.pattern_library = []
        self.performance_stats = {
            "queries_processed": 0,
            "cache_hits": 0,
            "avg_depth": 0,
            "total_time": 0
        }
        
        # Initialize with logical operators
        self._initialize_operators()
    
    def _initialize_operators(self):
        """Initialize logical operators"""
        operators = [
            "AND", "OR", "NOT", "IMPLIES", "IFF",
            "FORALL", "EXISTS", "EQUALS", "NOT_EQUALS"
        ]
        
        for op in operators:
            self.concept_graph[op].add(f"operator_{op}")
    
    def reason_about(self, query: str, context: Dict, depth: int = 3) -> Dict:
        """Reason about a query with caching"""
        start_time = time.time()
        
        # Check cache first
        cache_key = self._generate_cache_key(query, context, depth)
        if cache_key in self.reasoning_cache:
            self.performance_stats["cache_hits"] += 1
            return self.reasoning_cache[cache_key]
        
        # Perform reasoning
        result = self._perform_reasoning(query, context, depth)
        
        # Cache result
        self.reasoning_cache[cache_key] = result
        
        # Update stats
        self.performance_stats["queries_processed"] += 1
        self.performance_stats["total_time"] += time.time() - start_time
        self.performance_stats["avg_depth"] = (
            self.performance_stats["avg_depth"] * (self.performance_stats["queries_processed"] - 1) + depth
        ) / self.performance_stats["queries_processed"]
        
        return result
    
    def _generate_cache_key(self, query: str, context: Dict, depth: int) -> str:
        """Generate cache key"""
        key_data = {
            "query": query,
            "depth": depth,
            "context_hash": hashlib.md5(json.dumps(context, sort_keys=True).encode()).hexdigest()[:16]
        }
        return hashlib.sha256(json.dumps(key_data, sort_keys=True).encode()).hexdigest()[:32]
    
    def _perform_reasoning(self, query: str, context: Dict, depth: int) -> Dict:
        """Perform actual reasoning"""
        
        # Extract components
        components = self._extract_components(query)
        
        # Base reasoning
        base_result = self._base_reasoning(components, context)
        
        # Recursive refinement if needed
        refined = None
        if depth > 1 and base_result.get("needs_refinement", False):
            refined = self._recursive_refinement(base_result, depth - 1)
        
        # Calculate metrics
        certainty = self._calculate_certainty(base_result, refined)
        emergence = self._calculate_emergence(base_result, refined, depth)
        
        result = {
            "query": query,
            "components": components,
            "base_result": base_result,
            "refined": refined,
            "depth_used": depth,
            "certainty": certainty,
            "emergence": emergence,
            "timestamp": time.time(),
            "hash": self._hash_result(base_result, refined)
        }
        
        return result
    
    def _extract_components(self, query: str) -> Dict:
        """Extract reasoning components from query"""
        words = query.split()
        
        components = {
            "entities": [],
            "relations": [],
            "quantifiers": [],
            "modalities": [],
            "actions": [],
            "attributes": []
        }
        
        # Simple extraction (in production, use NLP)
        for word in words:
            word_lower = word.lower()
            
            # Entities (proper nouns)
            if word[0].isupper() and len(word) > 2:
                components["entities"].append(word)
            
            # Relations
            elif word_lower in ["is", "has", "can", "does", "will", "should", "must"]:
                components["relations"].append(word_lower)
            
            # Quantifiers
            elif word_lower in ["all", "every", "some", "no", "none"]:
                components["quantifiers"].append(word_lower)
            
            # Modalities
            elif word_lower in ["possible", "necessary", "impossible"]:
                components["modalities"].append(word_lower)
            
            # Actions
            elif word_lower.endswith(("ing", "ed")):
                components["actions"].append(word_lower)
        
        return components
    
    def _base_reasoning(self, components: Dict, context: Dict) -> Dict:
        """Base reasoning step"""
        result = {
            "direct_inferences": [],
            "contradictions": [],
            "implications": [],
            "unknowns": [],
            "patterns_found": [],
            "needs_refinement": False
        }
        
        # Check entities
        for entity in components["entities"]:
            if entity in self.concept_graph:
                result["direct_inferences"].append({
                    "type": "entity_known",
                    "entity": entity,
                    "relations": list(self.concept_graph[entity])
                })
            else:
                result["unknowns"].append(entity)
        
        # Check for contradictions
        if self._check_contradictions(components):
            result["contradictions"].append("Logical contradiction detected")
        
        # Find patterns
        patterns = self._find_patterns(components)
        result["patterns_found"] = patterns
        
        # Check if needs refinement
        result["needs_refinement"] = (
            len(result["unknowns"]) > 0 or
            len(result["contradictions"]) > 0 or
            len(patterns) == 0
        )
        
        return result
    
    def _check_contradictions(self, components: Dict) -> bool:
        """Check for logical contradictions"""
        # Check for negation patterns
        query_str = str(components).lower()
        
        contradiction_patterns = [
            "not and ", "and not ", "but not ", "however not",
            "false true", "true false", "yes no", "no yes"
        ]
        
        return any(pattern in query_str for pattern in contradiction_patterns)
    
    def _find_patterns(self, components: Dict) -> List[Dict]:
        """Find reasoning patterns"""
        patterns = []
        
        # Pattern 1: If-then structure
        if "if" in str(components).lower() and "then" in str(components).lower():
            patterns.append({
                "type": "implication",
                "certainty": 0.8,
                "description": "If-then logical structure"
            })
        
        # Pattern 2: Quantified statement
        if components["quantifiers"]:
            patterns.append({
                "type": "quantified",
                "certainty": 0.7,
                "description": f"Quantified with {components['quantifiers']}"
            })
        
        # Pattern 3: Action-oriented
        if components["actions"]:
            patterns.append({
                "type": "action",
                "certainty": 0.6,
                "description": f"Action-oriented: {components['actions'][:2]}"
            })
        
        return patterns
    
    def _recursive_refinement(self, base_result: Dict, remaining_depth: int) -> Dict:
        """Recursive refinement"""
        refinements = []
        
        # Refine unknowns
        for unknown in base_result.get("unknowns", []):
            refinement = self._hypothesize_entity(unknown)
            refinements.append(refinement)
        
        # Resolve contradictions
        for contradiction in base_result.get("contradictions", []):
            resolution = self._resolve_contradiction(contradiction)
            refinements.append(resolution)
        
        # Explore implications
        implications = self._explore_implications(base_result)
        refinements.extend(implications)
        
        return {
            "refinements": refinements,
            "depth": remaining_depth,
            "novel_insights": self._extract_novel_insights(refinements)
        }
    
    def _calculate_certainty(self, base_result: Dict, refined: Optional[Dict]) -> float:
        """Calculate reasoning certainty"""
        base_certainty = 0.7
        
        # Adjust for unknowns
        unknowns_penalty = len(base_result.get("unknowns", [])) * 0.1
        
        # Adjust for contradictions
        contradictions_penalty = len(base_result.get("contradictions", [])) * 0.2
        
        # Bonus for refinement
        refinement_bonus = 0.0
        if refined and refined.get("refinements"):
            refinement_bonus = min(0.3, len(refined["refinements"]) * 0.05)
        
        # Bonus for patterns
        pattern_bonus = len(base_result.get("patterns_found", [])) * 0.05
        
        certainty = base_certainty - unknowns_penalty - contradictions_penalty
        certainty += refinement_bonus + pattern_bonus
        
        return max(0.1, min(1.0, certainty))
    
    def _calculate_emergence(self, base_result: Dict, refined: Optional[Dict], depth: int) -> float:
        """Calculate emergence E_m"""
        if not refined:
            return 0.0
        
        novel_insights = refined.get("novel_insights", [])
        if not novel_insights:
            return 0.0
        
        # Count unique insights
        insight_hashes = [hashlib.md5(str(insight).encode()).hexdigest()[:8] 
                         for insight in novel_insights]
        unique_insights = len(set(insight_hashes))
        
        # Depth factor
        depth_factor = 1.0 + (depth * 0.1)
        
        # Complexity factor
        complexity = len(base_result.get("patterns_found", [])) + len(base_result.get("direct_inferences", []))
        complexity_factor = np.sqrt(max(1, complexity))
        
        # Emergence formula
        emergence = np.log2(1 + unique_insights) * depth_factor * complexity_factor
        
        return min(5.0, emergence)
    
    def _hash_result(self, base_result: Dict, refined: Optional[Dict]) -> str:
        """Hash reasoning result"""
        result_str = json.dumps({
            "base": base_result,
            "refined": refined
        }, sort_keys=True)
        
        return hashlib.sha256(result_str.encode()).hexdigest()[:32]
    
    def get_component_count(self) -> int:
        """Get number of reasoning components"""
        # Count unique concepts in graph
        return len(self.concept_graph)
    
    def get_stats(self) -> Dict:
        """Get performance statistics"""
        return {
            **self.performance_stats,
            "cache_size": len(self.reasoning_cache),
            "concept_count": len(self.concept_graph),
            "avg_response_time": self.performance_stats["total_time"] / max(1, self.performance_stats["queries_processed"]),
            "cache_hit_rate": self.performance_stats["cache_hits"] / max(1, self.performance_stats["queries_processed"])
        }
