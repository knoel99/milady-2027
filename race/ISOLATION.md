# Isolating the teams

Study of sandbox options for the race, from the vendors' documentation read on 2026-11-12. Diagram: [`diagrams/isolation.html`](diagrams/isolation.html) (rendered with [archify](https://github.com/tt-a1i/archify) 3.2 at commit `7e45f36`, source `diagrams/isolation.archify.json`). "Unconfirmed" means the documentation read did not settle the point.

## Requirements

1. Each agent is isolated from the other teams, from the host and from the judge's machine.
2. Network egress only to an allowlist: its provider's API, PyPI and npm, GitHub read-only, arXiv, HAL and Crossref, the compute broker.
3. The agent never holds its real API key; every API call can be audited (model, effort, cost), including the main session's.
4. CPU, memory and disk limits; identical for every team.
5. Works with the nine harnesses (Claude Code, Codex CLI, Antigravity CLI, Grok Build, Mistral Vibe, Kimi Code CLI, Qwen Code; Claude Code also for Z.ai and DeepSeek), headless, on Scaleway Ubuntu 24.04 instances.

## Options

| Option | Isolation | Egress allowlist | Agent never sees the key | Limits | Needs `/dev/kvm` | Harnesses | Licence, maturity |
|---|---|---|---|---|---|---|---|
| **NVIDIA OpenShell** | Landlock + seccomp + netns, non-root; Docker, Podman, Kubernetes or VM drivers | yes, per host, port **and calling binary**, optional L7 method and path | yes: opaque placeholder, the proxy substitutes the real credential per host | unconfirmed | no for the Docker and Podman drivers | Claude Code, Codex, OpenCode, Copilot listed; others unconfirmed (generic container) | Apache-2.0, 0.1.x, "Early Preview" |
| **NVIDIA NemoClaw** | OpenShell + OpenClaw plugin | as OpenShell | as OpenShell | – | – | OpenClaw only | alpha; not for this use |
| **Docker Sandboxes** (`sbx`) | one microVM per sandbox, own kernel and Docker daemon | yes, per host, deny by default ("Locked Down") | yes: host proxy adds the auth headers; built-ins for Anthropic, OpenAI, Google, xAI, Mistral, custom hosts for the others | unconfirmed | **yes** | Claude Code, Codex, Gemini CLI, OpenCode…; others through the generic shell agent | free but proprietary binary; Docker sign-in required |
| **Anthropic sandbox-runtime** (`srt`) | bubblewrap, shared kernel | yes, domains with wildcards | yes (`credentials.mask`, needs experimental TLS termination) | none | no | any command | Apache-2.0, beta |
| Claude Code built-in sandbox | `srt` around Bash only | yes, but unlisted hosts pass in bypass mode unless `strictAllowlist` | masks env vars from commands; Claude itself keeps its key | none | no | Claude Code only | – |
| Codex sandbox | bubblewrap + seccomp | yes (`network_proxy`), reported ignored in some setups | no | none | no | Codex only | – |
| gVisor (`runsc`) | user-space kernel | no (pair with a proxy) | no | through the container runtime | no (`systrap` platform) | any | Apache-2.0, mature |
| Kata, Firecracker | microVM | no | no | yes | **yes** | any | Apache-2.0, mature |
| Rootless Podman | user namespaces + seccomp + cgroups | no | no | yes | no | any | Apache-2.0, mature |
| E2B, Modal, Daytona | hosted microVM or gVisor | E2B yes; others unconfirmed | E2B in beta | yes | – | any | hosted outside Scaleway; Daytona's open repository archived in October 2026 |

Scaleway facts that constrain the choice: whether POP2 instances expose `/dev/kvm` is not documented (to check on the pilot VM); security groups filter by IP and port only, not by domain; there is no hard spending cap, only billing alerts; IAM keys can be limited to one project.

## Recommendation: three layers

1. **One VM per team, on a Scaleway private network, without public IP** (already the plan). The hypervisor is the main boundary between teams. The security group allows outbound traffic only to the gateway VM.
2. **A gateway VM, the only machine holding keys**, which runs three services:
   - an egress proxy (Squid or Envoy) with a per-team domain allowlist;
   - an API proxy: each agent receives a placeholder key and its harness points at the proxy's URL (`ANTHROPIC_BASE_URL`, Codex `openai_base_url`, `KIMI_MODEL_BASE_URL`, `OPENAI_BASE_URL` for Qwen Code, Vibe's provider URL); the proxy adds the real key, logs model, effort and tokens of every call, the main session's included, and stops a team at its budget;
   - the compute broker, whose job VMs join the same private network.
3. **Inside each team VM, the agent in a rootless Podman container under gVisor**, with CPU, memory and disk limits, the branch as the only mounted volume, and `HTTPS_PROXY` plus `NODE_USE_ENV_PROXY=1` set. A tool that ignores the proxy simply has no route out.

Why this rather than a single product: it is the only design that covers all nine harnesses without depending on any vendor's list of supported agents, it needs no `/dev/kvm`, and the API proxy closes the main gap of the current tooling (the main session's spend was not audited). OpenShell is the closest product to this design and is open source: try it on the pilot team, and adopt it if its resource limits and its support for the less common harnesses hold up. Docker Sandboxes is the most complete product but needs `/dev/kvm`, a closed binary and a Docker sign-in; consider it only if the pilot shows that POP2 exposes `/dev/kvm`.

## To check on the pilot VM

1. `ls -l /dev/kvm; cat /sys/module/kvm_*/parameters/nested` on a POP2 instance.
2. For each harness: does it accept a custom API base URL (unconfirmed for Antigravity CLI and Grok Build; without it, that team keeps its capped key and is audited at the egress proxy only)? Does it go through `HTTPS_PROXY` (run it in the default-deny network and watch the proxy log)?
3. OpenShell: resource limits, and images for Vibe, Kimi Code, Qwen Code, Grok Build and Antigravity.

## Sources

- NVIDIA OpenShell: https://docs.nvidia.com/openshell/latest/about/overview.html, https://docs.nvidia.com/openshell/latest/security/best-practices.md, https://github.com/NVIDIA/OpenShell
- Docker Sandboxes: https://docs.docker.com/ai/sandboxes/, https://docs.docker.com/ai/sandboxes/security/credentials/
- Anthropic sandbox-runtime: https://github.com/anthropic-experimental/sandbox-runtime; Claude Code: https://code.claude.com/docs/en/sandboxing, https://code.claude.com/docs/en/network-config
- Codex: https://learn.chatgpt.com/docs/agent-approvals-security
- gVisor platforms: https://gvisor.dev/docs/user_guide/platforms/; Firecracker: https://github.com/firecracker-microvm/firecracker/blob/main/docs/getting-started.md
- Node.js `NODE_USE_ENV_PROXY`: https://nodejs.org/docs/latest-v26.x/api/cli.html
- Scaleway: security groups https://www.scaleway.com/en/docs/instances/how-to/use-security-groups/, Public Gateways https://www.scaleway.com/en/docs/public-gateways/faq, IAM policies https://www.scaleway.com/en/docs/iam/reference-content/policy/, billing alerts https://www.scaleway.com/en/docs/billing/how-to/use-billing-alerts/
- E2B: https://docs.e2b.dev/sandbox/internet-access; Modal: https://modal.com/docs/guide/sandbox; Daytona: https://github.com/daytonaio/daytona
