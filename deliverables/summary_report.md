# Summary Report: Securing Containerized Microservices

## Steps Taken

This project focused on securing a vulnerable multi-service Python Flask application. The work was divided into six structured parts:

1. **Environment Setup and Initial Scan:**
   - Cloned the Week 7 homework from GitHub.
   - Used `make start` to deploy the `before/` version of the app via Docker Compose.
   - Performed static code analysis with Bandit (`make check`), CVE scanning (`make scan`), and Docker Bench security checks (`make host-security`).
   - Verified app endpoints: `/`, `/ping?ip=8.8.8.8`, and `/calculate?expr=2+3`.

2. **Code and Container Remediation:**
   - Replaced `eval()` with `ast.literal_eval()` in `app.py`.
   - Added input validation for user-supplied IPs and expressions.
   - Eliminated hardcoded secrets and restricted Flask binding to `127.0.0.1`.
   - Switched to a minimal `python:3.13-alpine` base image.
   - Created a non-root user (`appuser`) and applied `USER` directive.
   - Added a `HEALTHCHECK` to the Dockerfile.
   - Enforced memory, PID, and read-only filesystem limits in `docker-compose.yml`.
   - Used `.env` files for secret and configuration isolation.

3. **Threat Modeling:**
   - Conducted STRIDE analysis on endpoints.
   - Mapped MITRE ATT&CK for Containers (e.g., T1609, T1611).
   - Created a NIST 800-53 mapping table for each control (e.g., AC-3, SI-10).

4. **Security Architecture:**
   - Designed a hardened deployment diagram with isolated network, secure containers, and limited privileges.
   - Implemented an auto-hardening Python script (`docker_security_fixes.py`) to apply security settings automatically.

5. **Verification and Testing:**
   - Re-deployed the `after/` version with `make start`.
   - Re-ran all security scans to verify issues were remediated.
   - Confirmed all endpoints function as intended without errors.

6. **Final Packaging:**
   - Documented changes in deliverables directory including architecture diagram, threat model, auto-hardening script, and this summary.

---

## Vulnerabilities Found and Fixed

| Vulnerability                              | Status   | Fix Summary |
|-------------------------------------------|----------|-------------|
| Use of `eval()` in `/calculate` endpoint  |  Fixed | Replaced with `ast.literal_eval()` |
| Unvalidated user input in `/ping`         |  Fixed | Added regex validation for IPs |
| Hardcoded secret in `app.py`              |  Fixed | Removed and externalized via `.env` |
| Flask binding to `0.0.0.0`                |  Fixed | Bound to `127.0.0.1` |
| Running container as root                 |  Fixed | Added `appuser` and `USER` directive |
| Missing `HEALTHCHECK` in Dockerfile       |  Fixed | Health probe added for `/` endpoint |
| No container limits or security_opts      |  Fixed | Added `read_only`, `mem_limit`, `pids_limit` |

---

## Architecture and Security Improvements

The hardened architecture minimizes the attack surface by enforcing secure defaults across all layers. User input is validated before processing, containers operate with least privilege, and all services are monitored via `HEALTHCHECK`. The use of multi-stage builds and minimal base images reduces dependency vulnerabilities and image bloat. Docker Bench now confirms limited risk from kernel namespaces, resource overuse, or excessive container privileges.

---

## Reflection and Lessons Learned

This exercise emphasized the importance of defense-in-depth (DiD) for microservice deployments. Merely deploying in containers is not secure by default. Each layer—code, Dockerfile, network, and orchestrator—needs explicit controls. Tools like Bandit, Docker Scout, and Docker Bench proved invaluable for detection. The iterative process of scanning, remediating, and validating highlighted the importance of CI-integrated security and reproducible hardening steps. In future deployments, integrating these into CI/CD pipelines and adopting runtime policies (e.g., AppArmor, Seccomp) would further improve the posture.

---

