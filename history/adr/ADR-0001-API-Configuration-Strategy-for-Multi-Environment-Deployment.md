# ADR-0001: API Configuration Strategy for Multi-Environment Deployment

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Accepted
- **Date:** 2025-12-26
- **Feature:** 2-frontend-backend-connection
- **Context:** Need to handle API endpoint configuration across different deployment environments (localhost development vs Vercel production) while maintaining security and proper CORS configuration.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security?
     2) Alternatives: Multiple viable options considered with tradeoffs?
     3) Scope: Cross-cutting concern (not an isolated detail)?
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

Implement environment-aware API configuration using:
- Dynamic API URL resolution based on runtime environment detection
- Docusaurus client modules to inject environment-specific configuration at build time
- Fallback strategy for different deployment scenarios (localhost vs production)

Specifically:
- Frontend: Use window.location.origin detection to determine environment
- Build-time: Docusaurus clientModules to set global API_BASE_URL
- Runtime: Fallback to environment variables or hardcoded defaults

## Consequences

### Positive

- Enables seamless deployment across multiple environments without code changes
- Maintains security by using appropriate CORS configuration for each environment
- Provides flexibility for different backend deployment strategies (Hugging Face Spaces, self-hosted, etc.)
- Reduces deployment complexity and configuration management overhead

### Negative

- Adds complexity to API service code with environment detection logic
- Requires careful management of CORS settings across environments
- Potential for misconfiguration if backend deployment URL changes

## Alternatives Considered

Alternative A: Environment-specific build configurations using separate config files
- Why rejected: Would require maintaining multiple config files and build processes

Alternative B: Hardcoded environment-specific URLs in code
- Why rejected: Would require code changes for each environment and is not maintainable

Alternative C: Server-side proxy for all API requests
- Why rejected: Would add additional infrastructure complexity and potential latency

## References

- Feature Spec: specs/2-frontend-backend-connection/spec.md
- Implementation Plan: specs/2-frontend-backend-connection/plan.md
- Related ADRs: none
- Evaluator Evidence: history/prompts/2-frontend-backend-connection/0001-fix-chatbot-deployment.green.prompt.md