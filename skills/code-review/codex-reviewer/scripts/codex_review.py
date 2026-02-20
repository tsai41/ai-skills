#!/usr/bin/env python3
"""
Codex Review Helper Script

This script provides convenient wrappers for common Codex code review patterns.
It simplifies the process of running focused reviews and parsing results.
"""

import subprocess
import json
import sys
from pathlib import Path
from typing import Optional, List, Dict

class CodexReviewer:
    """Helper class for running Codex code reviews."""
    
    def __init__(self, model: str = "gpt-5-codex", json_output: bool = True):
        self.model = model
        self.json_output = json_output
        
    def run_review(
        self, 
        prompt: str, 
        sandbox: str = "read-only",
        reasoning_effort: str = "medium",
        output_file: Optional[str] = None
    ) -> Dict:
        """
        Run a Codex review with the given prompt.
        
        Args:
            prompt: The review prompt
            sandbox: Sandbox mode (read-only, workspace-write, danger-full-access)
            reasoning_effort: low, medium, or high
            output_file: Optional file to write full output
            
        Returns:
            Dict with 'success', 'output', 'error', and optionally 'events'
        """
        cmd = [
            "codex", "exec",
            "--model", self.model,
            "--sandbox", sandbox,
            "--config", f"reasoning_effort={reasoning_effort}"
        ]
        
        if self.json_output:
            cmd.append("--json")
            
        cmd.append(prompt)
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            output = result.stdout
            
            if output_file:
                with open(output_file, 'w') as f:
                    f.write(output)
            
            response = {
                "success": result.returncode == 0,
                "output": output,
                "error": result.stderr if result.returncode != 0 else None
            }
            
            if self.json_output:
                response["events"] = self._parse_jsonl(output)
                response["summary"] = self._extract_summary(response["events"])
                
            return response
            
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "output": None,
                "error": "Codex review timed out after 5 minutes"
            }
        except FileNotFoundError:
            return {
                "success": False,
                "output": None,
                "error": "Codex CLI not found. Please install it first."
            }
        except Exception as e:
            return {
                "success": False,
                "output": None,
                "error": f"Unexpected error: {str(e)}"
            }
    
    def _parse_jsonl(self, jsonl_text: str) -> List[Dict]:
        """Parse JSONL output into list of events."""
        events = []
        for line in jsonl_text.strip().split('\n'):
            if line:
                try:
                    events.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
        return events
    
    def _extract_summary(self, events: List[Dict]) -> Optional[str]:
        """Extract the final agent message from events."""
        for event in reversed(events):
            if event.get("type") == "item.completed":
                item = event.get("item", {})
                if item.get("type") == "agent_message":
                    return item.get("text")
        return None
    
    # Predefined review patterns
    
    def security_review(self, target: str) -> Dict:
        """Run a comprehensive security review."""
        prompt = f"""Perform a thorough security audit of {target}. Check for:

1. Authentication and authorization vulnerabilities
2. Input validation issues (SQL injection, XSS, command injection)
3. Cryptographic weaknesses
4. Sensitive data exposure
5. Rate limiting and DoS vulnerabilities
6. Session management issues
7. CSRF protection
8. Security misconfiguration

Provide:
- Severity rating (Critical/High/Medium/Low) for each issue
- Specific line numbers
- Exploitation scenarios
- Remediation recommendations"""
        
        return self.run_review(prompt, reasoning_effort="high")
    
    def performance_review(self, target: str) -> Dict:
        """Run a performance-focused review."""
        prompt = f"""Analyze {target} for performance issues:

1. Algorithmic complexity problems (O(n²) where O(n) possible, etc.)
2. Database query inefficiencies (N+1 queries, missing indexes)
3. Memory leaks or excessive allocations
4. Blocking operations that should be async
5. Resource cleanup issues
6. Caching opportunities
7. Unnecessary computations in loops

For each issue:
- Explain the performance impact
- Provide line numbers
- Suggest optimized alternatives with code examples"""
        
        return self.run_review(prompt, reasoning_effort="medium")
    
    def architecture_review(self, target: str, context: str = "") -> Dict:
        """Review architectural decisions and patterns."""
        prompt = f"""Review the architecture of {target}. {context}

Evaluate:
1. Separation of concerns and modularity
2. Coupling and cohesion
3. Design pattern usage and appropriateness
4. SOLID principles adherence
5. Scalability considerations
6. Maintainability and extensibility
7. Error handling strategy
8. Dependency management

Provide:
- Architectural strengths
- Design issues or anti-patterns
- Refactoring suggestions with reasoning
- Alternative architectural approaches"""
        
        return self.run_review(prompt, reasoning_effort="high")
    
    def code_quality_review(self, target: str) -> Dict:
        """Review code quality and maintainability."""
        prompt = f"""Review {target} for code quality:

1. Complexity metrics (identify functions >20 lines or high cyclomatic complexity)
2. Code duplication and DRY violations
3. Naming conventions and clarity
4. Comment quality and necessity
5. Error handling completeness
6. Function/method size and single responsibility
7. Test coverage and testability
8. Documentation completeness

Rate code quality 1-10 and provide specific improvements."""
        
        return self.run_review(prompt, reasoning_effort="medium")
    
    def diff_review(self, base: str = "main", head: str = "HEAD") -> Dict:
        """Review changes between two git refs."""
        prompt = f"""Review the git diff between {base} and {head}:

1. Identify breaking changes and backward compatibility issues
2. Check for regression risks
3. Evaluate test coverage for new/modified code
4. Verify documentation updates
5. Assess security implications of changes
6. Check for performance regressions
7. Review error handling in new code

Organize feedback by:
- File path
- Severity (Critical/High/Medium/Low)
- Type (Bug Risk/Breaking Change/Security/Performance/Quality)"""
        
        return self.run_review(prompt, reasoning_effort="high")
    
    def focused_review(self, target: str, focus_areas: List[str]) -> Dict:
        """Run a review focused on specific concerns."""
        areas = "\n".join(f"{i+1}. {area}" for i, area in enumerate(focus_areas))
        prompt = f"""Review {target} focusing ONLY on these specific concerns:

{areas}

Ignore all other issues. Provide detailed analysis of only the specified areas."""
        
        return self.run_review(prompt, reasoning_effort="medium")


def main():
    """CLI interface for the Codex reviewer."""
    if len(sys.argv) < 3:
        print("Usage: python codex_review.py <review_type> <target> [options]")
        print("\nReview types:")
        print("  security    - Security audit")
        print("  performance - Performance analysis")
        print("  architecture - Architecture review")
        print("  quality     - Code quality review")
        print("  diff        - Git diff review")
        print("\nExample:")
        print("  python codex_review.py security src/auth/")
        return 1
    
    review_type = sys.argv[1]
    target = sys.argv[2]
    
    reviewer = CodexReviewer()
    
    if review_type == "security":
        result = reviewer.security_review(target)
    elif review_type == "performance":
        result = reviewer.performance_review(target)
    elif review_type == "architecture":
        context = sys.argv[3] if len(sys.argv) > 3 else ""
        result = reviewer.architecture_review(target, context)
    elif review_type == "quality":
        result = reviewer.code_quality_review(target)
    elif review_type == "diff":
        base = sys.argv[3] if len(sys.argv) > 3 else "main"
        result = reviewer.diff_review(base, target)
    else:
        print(f"Unknown review type: {review_type}")
        return 1
    
    if result["success"]:
        print("\n=== CODEX REVIEW RESULTS ===\n")
        if result.get("summary"):
            print(result["summary"])
        else:
            print(result["output"])
        return 0
    else:
        print(f"Error: {result['error']}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
