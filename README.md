# AI Skills

Public AI engineering skills for Codex.

## Shipwright

**From one-line intent to reviewed, verified software.**

Shipwright is an end-to-end software delivery skill for new implementations and intentional changes. Give it the outcome you want; Shipwright carries the work through requirement analysis, architecture, dependency-aware execution, independent review, verification, and exact Git completion.

### High quality per token

Shipwright is deliberately optimized for **quality per token**, not maximum-model-everywhere execution.

It spends intelligence where it has the highest leverage:

| Work | GPT-5.6 optimized route |
|---|---|
| Long-running orchestration | GPT-5.6 Luna — `xhigh` |
| Repository scouting | GPT-5.6 Luna — `medium` |
| Requirement analysis | GPT-5.6 Sol — `high` |
| Architecture | GPT-5.6 Sol — `high` |
| Dependency decomposition | GPT-5.6 Sol — `high` |
| Simple implementation | GPT-5.6 Luna — `medium` |
| Medium implementation | GPT-5.6 Luna — `max` |
| Hard implementation | GPT-5.6 Terra — `high` |
| Standard independent review | GPT-5.6 Sol — `medium` |
| Deep independent review | GPT-5.6 Sol — `high` |

Instead of spending frontier-model tokens on every long-running control-plane turn, Shipwright keeps orchestration on **Luna xhigh**, uses **Sol** for requirements, architecture, decomposition and independent review, and reserves **Terra** for implementation that remains genuinely hard after decomposition.

It also reduces context waste by giving each agent only the authority and evidence it needs, while a durable run state outside conversational memory prevents long or interrupted implementations from repeatedly reconstructing progress.

### Full delivery cycle

```text
one-line intent / requested change
        ↓
repository orientation
        ↓
requirement completeness + focused challenge
        ↓
resolved Requirement Authority
        ↓
architecture assessment / technical decisions
        ↓
durable execution plan
        ↓
dependency-first decomposition
        ↓
safe parallel implementation
        ↓
integration
        ↓
independent blind-first review
        ↓
correction + fresh re-review
        ↓
verification
        ↓
commit / authorized push
        ↓
DONE
```

The parent Codex session is a controller, not the product designer or coding worker. For best efficiency, run the parent Shipwright session on **GPT-5.6 Luna with `xhigh` reasoning**.

### Install

Clone this repository once:

```bash
git clone --depth 1 https://github.com/salujagurdeep/ai-skills.git
cd ai-skills
```

Install Shipwright for your user account, making it available in every repository:

```bash
python3 install.py shipwright --scope user --dry-run
python3 install.py shipwright --scope user
```

Or install it only for one project:

```bash
python3 install.py shipwright --scope project --repo /path/to/project --dry-run
python3 install.py shipwright --scope project --repo /path/to/project
```

The installer places both the Shipwright skill and its bundled Codex agent profiles in the appropriate user- or project-level locations. It refuses to overwrite an existing Shipwright installation unless `--replace` is supplied.

Restart Codex after installation.

### Use

```text
$shipwright Add organization-level SSO to this application.
```

or:

```text
$shipwright Change the checkout flow so a saved address can be edited before payment.
```

Resume an interrupted run with:

```text
$shipwright resume
```

### Recommended for large repositories: Graphify

Shipwright works without a repository graph. For large or relationship-heavy codebases, however, it is designed to **prefer Graphify when available** for orientation and dependency queries before broad file loading.

Graphify is an independent third-party open-source project. It is not bundled with or affiliated with Shipwright.

Current Codex installation:

```bash
uv tool install graphifyy
graphify install --platform codex
```

Project-scoped installation:

```bash
graphify install --project --platform codex
```

Official project: <https://github.com/Graphify-Labs/graphify>

### GPT-5.6 optimization

Shipwright ships explicit profiles for GPT-5.6 Sol, Luna and Terra. The `gpt-5.6` alias is GPT-5.6 Sol; Shipwright uses the explicit `gpt-5.6-sol` model ID for high-leverage reasoning roles.

If an exact route is unavailable in a user's Codex environment, Shipwright reports the route mismatch instead of silently pretending the intended optimization was used.

### License

MIT. See [LICENSE](LICENSE).
