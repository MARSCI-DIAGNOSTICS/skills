---
source_url: https://developers.openai.com/codex/guides/autofix-ci
source_type: llms-txt
content_hash: sha256:89dd76062a400660901f5500bd3cddd2ef31d43e6b22b1314d74a567641afa6f
sitemap_url: https://developers.openai.com/codex/llms.txt
fetch_method: markdown
---

# Auto-fix CI failures with Codex

Codex can become a teammate in your continuous integration (CI) pipeline. This guide adapts Charlie Harrington's Codex cookbook
example to run the Codex CLI inside GitHub Actions whenever your primary workflow fails. Codex inspects the repository, applies a
minimal fix, reruns your tests, and opens a pull request (PR) with the patch so you can review and merge it quickly.

## Prerequisites

Before you begin, make sure you have:

- A GitHub repository with one or more Actions workflows (for example, a "CI" workflow that installs dependencies and runs
  tests).
- An `OPENAI_API_KEY` secret defined under **Settings → Secrets and variables → Actions** in your repository or organization.
- Python available in the runner image you use. Codex relies on Python for `codex login`.
- Repository permissions that allow Actions to open pull requests on your behalf. In organization settings, enable "Allow GitHub
  Actions to create and approve pull requests" if it is disabled.

## Understand the flow

1. Your main workflow finishes with a failure.
2. A follow-up workflow installs the Codex CLI and authenticates with your API key.
3. Codex runs in auto mode to diagnose the failure, make a minimal change, and rerun the tests.
4. If the tests now pass, the workflow pushes a branch and opens a PR summarizing the fix.

This keeps broken builds visible while delegating the first pass at repairs to Codex.

## Add the Codex auto-fix workflow

Create `.github/workflows/codex-auto-fix.yml` in your repository with the following contents. Replace `"CI"` in `workflows: ["CI"]`
with the exact name of the workflow you want to monitor for failures.

```yaml
name: Codex Auto-Fix on Failure

on:
  workflow_run:
    # Trigger this job after any run of the primary CI workflow completes
    workflows: ["CI"]
    types: [completed]

permissions:
  contents: write
  pull-requests: write

jobs:
  auto-fix:
    # Only run when the referenced workflow concluded with a failure
    if: ${{ github.event.workflow_run.conclusion == 'failure' }}
    runs-on: ubuntu-latest
    env:
      OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
      FAILED_WORKFLOW_NAME: ${{ github.event.workflow_run.name }}
      FAILED_RUN_URL: ${{ github.event.workflow_run.html_url }}
      FAILED_HEAD_BRANCH: ${{ github.event.workflow_run.head_branch }}
      FAILED_HEAD_SHA: ${{ github.event.workflow_run.head_sha }}
    steps:
      - name: Check prerequisites
        run: |
          if [ -z "$OPENAI_API_KEY" ]; then
            echo "OPENAI_API_KEY secret is not set. Skipping auto-fix." >&2
            exit 1
          fi

      - name: Checkout failing ref
        uses: actions/checkout@v5
        with:
          ref: ${{ env.FAILED_HEAD_SHA }}
          fetch-depth: 0

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: "20"
          cache: "npm"

      - name: Install dependencies
        run: |
          if [ -f package-lock.json ]; then npm ci; else npm i; fi

      - name: Prepare Codex prerequisites
        shell: bash
        run: |
          # Ensure python3 exists for Codex' login helper
          if ! command -v python3 >/dev/null 2>&1; then
            sudo apt-get update
            sudo apt-get install -y python3
          fi

          # Ensure Codex config dir exists and is writable
          mkdir -p "$HOME/.codex"
          # (Optional) pin an explicit home for Codex config/logs
          echo "CODEX_HOME=$HOME/.codex" >> $GITHUB_ENV

      - name: Install Codex CLI
        run: npm i -g @openai/codex

      - name: Authenticate Codex (non-interactive)
        env:
          # if you set CODEX_HOME above, export it here too
          CODEX_HOME: ${{ env.CODEX_HOME }}
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: codex login --api-key "$OPENAI_API_KEY"

      - name: Run Codex to fix CI failure
        run: |
          codex exec --full-auto --sandbox workspace-write "You are working in a Node.js monorepo with Jest tests and GitHub Actions. Read the repository, run the test suite, identify the minimal change needed to make all tests pass, implement only that change, and stop. Do not refactor unrelated code or files. Keep changes small and surgical."

      - name: Verify tests
        run: npm test --silent

      - name: Create pull request with fixes
        if: success()
        uses: peter-evans/create-pull-request@v6
        with:
          commit-message: "fix(ci): auto-fix failing tests via Codex"
          branch: codex/auto-fix-${{ github.event.workflow_run.run_id }}
          base: ${{ env.FAILED_HEAD_BRANCH }}
          title: "Auto-fix failing CI via Codex"
          body: |
            Codex automatically generated this PR in response to a CI failure on workflow `${{ env.FAILED_WORKFLOW_NAME }}`.

            Failed run: ${{ env.FAILED_RUN_URL }}
            Head branch: `${{ env.FAILED_HEAD_BRANCH }}`

            This PR contains minimal changes intended solely to make the CI pass.
```

### Customize for your stack

- Swap in your preferred runtime setup step (for example `actions/setup-python` or `actions/setup-java`).
- Adjust the package installation and test commands to mirror your workflow. Codex benefits from deterministic steps that match
  how you run CI locally.
- Modify the `codex exec` prompt with more context about your repository, frameworks, or coding conventions.

## Monitor the workflow

When a workflow run fails, the new Codex job appears in the **Actions** tab. Watch the logs to see Codex read the repo, make
changes, and rerun tests. If the job succeeds, it pushes a branch named `codex/auto-fix-<run_id>` and opens a PR summarizing the
failure context.

## Review the pull request

Review the generated PR just like any other contribution. Because Codex keeps changes minimal, you can quickly spot whether the
fix is safe to merge. If additional work is required, leave comments or push extra commits before merging.

## Conclusion

Embedding Codex into your CI loop accelerates recovery from failing builds and keeps your main branch healthy. Use this workflow
as a template and iterate on the prompt or commands to match your stack. To explore more Codex automation patterns, read the
[Codex CLI repository](https://github.com/openai/codex/) and the rest of the Codex cookbook.
