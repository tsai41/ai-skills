# Example Codex Review Prompts

This document provides real-world examples of effective Codex review prompts for various scenarios.

## Security Reviews

### Web Application Authentication
```bash
codex exec --model gpt-5-codex "Review src/auth/ for authentication and session management security:

Critical checks:
- Password storage and hashing (bcrypt, scrypt usage)
- Session token generation (cryptographically secure randomness)
- Session invalidation on logout
- Concurrent session handling
- Brute force protection
- Password reset flow security
- Remember me token security
- CSRF token validation

Flag any issues as Critical, High, or Medium severity with specific line numbers."
```

### API Security
```bash
codex exec --model gpt-5-codex "Security audit of REST API in src/api/:

1. Authentication: JWT validation, token expiry, refresh token security
2. Authorization: Role-based access control, resource ownership checks
3. Input validation: SQL injection, NoSQL injection, XXE, command injection
4. Rate limiting: Per-user, per-endpoint, per-IP limits
5. Data exposure: PII leakage, sensitive data in logs/errors
6. CORS configuration
7. API versioning and deprecation handling

Provide exploitation scenarios for each vulnerability found."
```

### Cryptography Review
```bash
codex exec --model gpt-5-codex "Review cryptographic implementations in src/crypto/:

- Key generation: Sufficient entropy, appropriate key sizes
- Encryption: Proper algorithm selection (AES-256-GCM, ChaCha20-Poly1305)
- Initialization vectors: Uniqueness, randomness
- Key storage: Key derivation functions, secure storage
- Hashing: Algorithm selection (SHA-256+, Argon2, bcrypt)
- Digital signatures: Proper verification, algorithm choice
- Random number generation: CSPRNG usage

Identify use of deprecated algorithms, weak keys, or insecure practices."
```

## Performance Reviews

### Database Query Optimization
```bash
codex exec --model gpt-5-codex "Analyze database operations in src/models/ for performance:

Focus on:
1. N+1 query problems (missing eager loading, select_related, prefetch_related)
2. Missing database indexes on frequently queried columns
3. Full table scans that could use indexes
4. Inefficient JOIN operations
5. Unnecessary database hits (could be cached)
6. Large result sets loaded into memory
7. Missing pagination on list queries
8. Suboptimal use of database-specific features

For each issue, show the problematic query and suggest optimized alternative."
```

### Async/Await Optimization
```bash
codex exec --model gpt-5-codex "Review async code in src/services/ for performance issues:

Check for:
- Blocking calls in async functions (file I/O, network without await)
- Missing asyncio.gather() for parallel operations
- Unnecessary await calls (already resolved futures)
- Event loop blocking operations
- Inefficient use of async context managers
- Thread pool executor usage for CPU-bound tasks
- Missing timeouts on network operations

Identify each blocking call with line numbers and suggest async alternatives."
```

### Frontend Performance
```bash
codex exec --model gpt-5-codex "Analyze React components in src/components/ for performance:

1. Unnecessary re-renders (missing useMemo, useCallback, React.memo)
2. Large component trees (should split into smaller components)
3. Inline function definitions in render
4. Large bundle sizes (missing code splitting, lazy loading)
5. Unoptimized images (missing lazy loading, responsive images)
6. Synchronous rendering blocking UI
7. Missing virtualization for long lists

Suggest specific React optimization patterns for each issue."
```

## Architecture Reviews

### Microservices Architecture
```bash
codex exec --model gpt-5-codex "Review microservices architecture in this repository:

Evaluate:
1. Service boundaries: Are they properly separated by domain?
2. Inter-service communication: REST vs message queues, sync vs async
3. Data management: Database per service, shared database issues
4. Distributed transaction handling: Saga pattern, eventual consistency
5. Service discovery and load balancing
6. Circuit breakers and fault tolerance
7. API gateway usage
8. Observability: Logging, tracing, metrics
9. Deployment independence

Compare with microservices best practices. Suggest improvements or alternatives."
```

### Clean Architecture Compliance
```bash
codex exec --model gpt-5-codex "Assess Clean Architecture implementation:

Check:
- Dependency Rule: Dependencies point inward only
- Entity layer: Core business logic, framework-independent
- Use Case layer: Application-specific business rules
- Interface Adapters: Controllers, presenters, gateways
- Frameworks/Drivers: External concerns (DB, UI, etc.)

Identify violations:
- Business logic in controllers
- Direct database dependencies in use cases
- Framework coupling in entities
- Missing abstractions/interfaces

Rate compliance 1-10 and suggest refactoring path."
```

### Monolith to Microservices
```bash
codex exec --model gpt-5-codex "Analyze monolithic application for microservices extraction:

Current structure: src/

Recommend:
1. Service boundaries based on bounded contexts
2. Database decomposition strategy
3. Strangler fig pattern implementation steps
4. API gateway design
5. Shared library strategy
6. Data migration approach
7. Gradual rollout plan
8. Risk assessment for each extraction

Prioritize services by extraction value vs complexity."
```

## Code Quality Reviews

### Test Coverage Analysis
```bash
codex exec --model gpt-5-codex "Review test coverage and quality in tests/:

Analyze:
1. Coverage gaps: Untested functions, branches, edge cases
2. Test quality: Unit vs integration mix, mocking appropriateness
3. Test organization: Structure, naming, setup/teardown
4. Brittle tests: Fragile assertions, timing dependencies
5. Missing test scenarios: Error cases, boundary conditions
6. Test duplication
7. Flaky tests: Non-deterministic behavior

For critical functions without tests, generate test cases covering:
- Happy path
- Error conditions
- Edge cases
- Boundary values"
```

### Code Complexity Reduction
```bash
codex exec --model gpt-5-codex "Identify complex code in src/ needing refactoring:

Find:
- Functions >50 lines or >10 cyclomatic complexity
- Deeply nested conditionals (>3 levels)
- Long parameter lists (>5 parameters)
- God classes (>500 lines or >10 responsibilities)
- Switch statements that could be polymorphism
- Code duplication (>5 similar lines in multiple places)

For each complex section:
- Current complexity metrics
- Refactoring approach (Extract Method, Replace Conditional with Polymorphism, etc.)
- Proposed simplified structure"
```

### Dependency Audit
```bash
codex exec --model gpt-5-codex "Audit dependencies in package.json and imports:

Check:
1. Unused dependencies (not imported anywhere)
2. Outdated packages (security vulnerabilities)
3. Duplicate functionality (multiple libraries for same purpose)
4. Bundle size impact (large libraries for small features)
5. Transitive dependency issues
6. License compatibility
7. Deprecated packages
8. Tree-shaking opportunities

Recommend: Removals, updates, or lightweight alternatives."
```

## Pull Request Reviews

### Comprehensive PR Review
```bash
codex exec --model gpt-5-codex "Review the current pull request diff against main:

Complete analysis:
1. **Correctness**: Logic errors, edge cases, potential bugs
2. **Security**: New vulnerabilities introduced
3. **Performance**: Regression risks, optimization opportunities
4. **Tests**: Adequate coverage for changes, test quality
5. **Documentation**: Comments, docstrings, README updates
6. **Style**: Code consistency, naming conventions
7. **Breaking changes**: API compatibility, migration guide needed
8. **Dependencies**: New dependencies justified

Organize findings by file:
[filename]
  - Critical: [issue with line numbers]
  - Important: [issue with line numbers]
  - Suggestions: [improvements]

Final verdict: ✅ Approve / 🔄 Request Changes / 💬 Comment"
```

### Breaking Change Review
```bash
codex exec --model gpt-5-codex "Review PR for breaking changes and backward compatibility:

Scan for:
1. Public API changes: Function signatures, return types
2. Configuration changes: Removed/renamed settings
3. Database schema changes: Migrations, data loss risks
4. Behavior changes: Different output for same input
5. Removed features or endpoints
6. Dependency upgrades with breaking changes
7. Changed error handling or exceptions

For each breaking change:
- Severity and impact scope
- Affected consumers
- Migration path
- Version bump recommendation (major/minor/patch)"
```

## Specification Validation

### API Spec vs Implementation
```bash
codex exec --model gpt-5-codex "Compare OpenAPI spec in api-spec.yaml with implementation in src/api/:

Validate:
1. All endpoints from spec are implemented
2. Request/response schemas match exactly
3. HTTP methods and status codes correct
4. Authentication requirements enforced
5. Validation rules applied
6. Error responses match spec
7. Headers and content types correct
8. Query parameters and path variables validated

List discrepancies with:
- Spec definition
- Actual implementation
- Recommended fix"
```

### Requirements Traceability
```bash
codex exec --model gpt-5-codex "Verify REQUIREMENTS.md implementation completeness:

For each requirement:
1. Locate implementing code
2. Verify correctness of implementation
3. Check test coverage
4. Validate acceptance criteria met

Report:
- ✅ Fully implemented and tested requirements
- ⚠️  Partially implemented (missing aspects)
- ❌ Not implemented
- 🐛 Incorrectly implemented

Provide requirement ID, status, file locations, and gaps."
```

## Advanced Patterns

### Multi-Stage Review
```bash
# Stage 1: Quick scan
codex exec --model gpt-5-codex "Quick scan of src/new-feature/ for obvious issues: syntax errors, import problems, unused variables, missing types"

# Stage 2: Security deep dive
codex exec --model gpt-5-codex "Deep security audit of src/new-feature/ - focus on input validation, authentication, authorization, data exposure"

# Stage 3: Architecture alignment
codex exec --model gpt-5-codex "Review src/new-feature/ architecture - does it follow existing patterns? Is it consistent with rest of codebase?"
```

### Follow-up Review
```bash
# Initial review
codex exec --model gpt-5-codex -o initial-review.txt "Review src/payment.py for security and correctness"

# Follow-up on specific issue
codex exec --model gpt-5-codex resume --last "You mentioned potential race condition in transaction processing. Show detailed sequence diagram of the race and suggest fix with code."
```

### Comparative Review
```bash
codex exec --model gpt-5-codex "Compare two implementation approaches:

Approach A: src/feature-v1/
Approach B: src/feature-v2/

Evaluate each on:
- Performance (speed, memory, scalability)
- Maintainability (complexity, readability)
- Testability
- Error handling
- Extensibility

Recommend which approach to adopt and why."
```

## Tips for Effective Prompts

1. **Be specific about scope**: File paths, directories, or git refs
2. **State priorities**: What matters most (security, performance, maintainability)
3. **Request structure**: Bullet points, severity ratings, line numbers
4. **Provide context**: Framework, language version, architecture style
5. **Set constraints**: "Ignore style issues" or "Only critical security issues"
6. **Request examples**: "Show code example of fix" or "Provide test case"
7. **Define severity levels**: Critical/High/Medium/Low with clear criteria
8. **Ask for actionable output**: Not just "there are issues" but specific fixes
