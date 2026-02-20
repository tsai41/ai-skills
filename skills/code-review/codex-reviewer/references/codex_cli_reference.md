# Codex CLI Reference for Code Review

This reference provides detailed information about using Codex CLI for code review scenarios.

## Command Reference

### Basic Execution

```bash
codex exec "prompt text"
```

Non-interactive mode for single-shot reviews and analysis.

### Model Selection

```bash
codex exec --model gpt-5-codex "prompt"
```

**Recommended models for code review:**
- `gpt-5-codex`: Optimized for software engineering tasks (recommended)
- `gpt-5`: General purpose, faster for simple tasks
- `o3`: Highest reasoning capability for complex analysis

### Sandbox Modes

Control file and network access:

```bash
codex exec --sandbox read-only "prompt"          # Default: Read files only
codex exec --sandbox workspace-write "prompt"    # Write within workspace
codex exec --sandbox danger-full-access "prompt" # Full system access (use cautiously)
codex exec --full-auto "prompt"                  # Shorthand for workspace-write with auto-approval
```

### Output Control

```bash
codex exec "prompt"                               # Stream to stderr, final message to stdout
codex exec -o output.txt "prompt"                 # Write final message to file
codex exec --json "prompt"                        # Output JSONL event stream
codex exec --json "prompt" > review.jsonl         # Save JSONL to file
```

### Approval Policies

```bash
codex exec --config approval_policy=untrusted "prompt"  # Prompt for untrusted commands
codex exec --config approval_policy=on-request "prompt" # Prompt when needed
codex exec --config approval_policy=never "prompt"      # Never prompt (read-only safe)
```

### Reasoning Configuration

```bash
codex exec --config reasoning_effort=low "prompt"     # Fast, less thorough
codex exec --config reasoning_effort=medium "prompt"  # Default balanced
codex exec --config reasoning_effort=high "prompt"    # Deep analysis, slower
```

## Review-Specific Patterns

### Security Review

```bash
codex exec --model gpt-5-codex "Perform a security audit of [file/directory]. Check for:
- Authentication and authorization issues
- Input validation vulnerabilities (SQL injection, XSS, etc.)
- Cryptographic weaknesses
- Sensitive data exposure
- Rate limiting and DoS concerns
Provide severity ratings and specific line numbers."
```

### Performance Review

```bash
codex exec --model gpt-5-codex "Analyze [file/directory] for performance issues:
- Inefficient algorithms and data structures
- N+1 query problems
- Memory leaks or excessive allocations
- Blocking operations that should be async
- Database query optimization opportunities
Suggest specific improvements with code examples."
```

### Architecture Review

```bash
codex exec --model gpt-5-codex "Review the architecture in [directory]:
- Evaluate separation of concerns
- Identify tight coupling issues
- Check adherence to design patterns
- Assess scalability concerns
- Suggest refactoring opportunities
Compare current design with best practices for [framework/technology]."
```

### Code Quality Review

```bash
codex exec --model gpt-5-codex "Review [files] for code quality:
- Complexity metrics (functions that are too long/complex)
- Code duplication and DRY violations
- Naming conventions and clarity
- Error handling completeness
- Test coverage gaps
Focus on maintainability and readability."
```

### Diff/PR Review

```bash
codex exec --model gpt-5-codex "Review the git diff between [branch1] and [branch2]:
- Identify breaking changes
- Check for regression risks
- Evaluate test coverage for changes
- Verify documentation updates
- Assess backward compatibility
Provide feedback organized by file and severity."
```

## JSONL Event Format

When using `--json` flag, Codex outputs JSONL events:

### Event Types

**thread.started**
```json
{"type":"thread.started","thread_id":"0199a213-81c0-7800-8aa1-bbab2a035a53"}
```

**turn.started**
```json
{"type":"turn.started"}
```

**item.completed** (reasoning)
```json
{
  "type":"item.completed",
  "item":{
    "id":"item_0",
    "type":"reasoning",
    "text":"**Analysis of authentication flow**"
  }
}
```

**item.completed** (command execution)
```json
{
  "type":"item.completed",
  "item":{
    "id":"item_1",
    "type":"command_execution",
    "command":"bash -lc 'grep -r TODO src/'",
    "aggregated_output":"...",
    "exit_code":0,
    "status":"completed"
  }
}
```

**item.completed** (agent message)
```json
{
  "type":"item.completed",
  "item":{
    "id":"item_2",
    "type":"agent_message",
    "text":"Review complete. Found 3 critical issues..."
  }
}
```

**turn.completed**
```json
{
  "type":"turn.completed",
  "usage":{
    "prompt_tokens":1250,
    "completion_tokens":850,
    "total_tokens":2100
  }
}
```

## Environment Variables

```bash
CODEX_API_KEY=sk-...        # Override API key (codex exec only)
RUST_LOG=info               # Control logging level
```

## Configuration File

Codex reads configuration from `~/.config/codex/config.toml` or project-specific `.codex/config.toml`

**Example configuration for code review:**

```toml
model = "gpt-5-codex"
reasoning_effort = "medium"

[profiles.security_review]
model = "gpt-5-codex"
reasoning_effort = "high"
approval_policy = "never"
sandbox_mode = "read-only"

[profiles.full_review]
model = "gpt-5-codex"
reasoning_effort = "high"
approval_policy = "on-request"
sandbox_mode = "workspace-write"
```

Use profiles:
```bash
codex exec -c profile=security_review "Audit authentication code"
```

## Authentication Methods

### ChatGPT Account (Recommended)
```bash
codex  # First run will prompt for authentication
```
Select "Sign in with ChatGPT" and follow browser flow.

### API Key
```bash
export CODEX_API_KEY=your-api-key
codex exec "review code"
```

Or set in config:
```toml
[auth]
api_key = "your-api-key"
```

## Best Practices for Code Review

### 1. Scope Reviews Appropriately
- Single file: `codex exec "Review auth.py for security issues"`
- Directory: `codex exec "Review src/api/ for REST API best practices"`
- Specific concern: `codex exec "Check database.py for SQL injection vulnerabilities"`

### 2. Provide Context
```bash
codex exec "Review payment.py. This is a Django app using Stripe API. 
Focus on: PCI compliance, error handling, idempotency, and webhook security."
```

### 3. Request Structured Output
```bash
codex exec "Review code and format findings as:
## Critical Issues
- [Issue with line numbers and explanation]

## Medium Priority
- [Issue with line numbers and explanation]

## Suggestions
- [Improvement ideas]"
```

### 4. Use Multiple Focused Reviews
Rather than one broad review, run several targeted reviews:

```bash
codex exec "Security audit of authentication system"
codex exec "Performance analysis of database queries"
codex exec "Test coverage assessment"
```

### 5. Combine with Testing
```bash
codex exec --full-auto "Review auth.py, then write and run tests to verify security. 
Report any vulnerabilities found through testing."
```

## Limitations and Workarounds

### Large Codebases
**Problem**: Context window limits for large files/directories
**Workaround**: Review in segments, focus on changed files, or use directory-level reviews

### No Interactive Clarification
**Problem**: Codex exec is non-interactive
**Workaround**: Anticipate questions and provide detailed prompts upfront

### Network Access
**Problem**: Default sandbox blocks network access
**Workaround**: Use `--sandbox workspace-write` with network config or `--sandbox danger-full-access`

### State Persistence
**Problem**: Each `codex exec` call is independent
**Workaround**: Use `resume --last` for follow-up questions on same context

## Comparison with Interactive Codex

| Feature | `codex exec` | Interactive `codex` |
|---------|-------------|---------------------|
| Use case | Automated reviews, CI/CD | Pair programming |
| Interaction | Single shot | Multi-turn conversation |
| Approvals | Configurable | Interactive prompts |
| Output | Structured (JSONL) | TUI display |
| Scripting | Easy | Difficult |

For code review, `codex exec` is generally preferred due to automation capabilities and structured output.
