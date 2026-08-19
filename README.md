# AI Skills

Reusable AI engineering skills for Codex.

## Shipwright

**From one-line intent to reviewed, verified code.**

Shipwright is an end-to-end software delivery skill for new implementations and changes to existing products. Give it the outcome you want; it drives the work through:

- repository orientation;
- requirement completeness analysis and focused clarification;
- architecture assessment and technical design;
- a durable run plan outside the product repository;
- dependency-first decomposition and safe parallel implementation;
- integration and independent review;
- correction and re-review;
- verification and Git completion.

The controller is deliberately a coordinator, not the product or architecture decision-maker. Specialized reasoning stages establish requirements, architecture and execution plans, while the controller persists run state and follows the plan through to completion.

### Install in Codex

Use the built-in skill installer:

```text
$skill-installer install https://github.com/salujagurdeep/ai-skills/tree/main/skills/shipwright
```

Restart Codex after installation.

### Use

```text
$shipwright Add organization-level SSO to this application.
```

or:

```text
$shipwright Change the existing checkout flow so a saved address can be edited before payment.
```

Shipwright uses the models and agent capabilities available in the user's Codex environment; it does not require a specific named model or an external audit service.
