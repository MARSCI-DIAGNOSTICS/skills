---
source_url: https://developers.openai.com/codex/autofix-ci
source_type: llms-txt
content_hash: sha256:b5d30e53e2aa0eddd0f270fbfaca0d5f9c6bef6c8eb323ebf20dadf12b3f7ab9
sitemap_url: https://developers.openai.com/codex/llms.txt
fetch_method: markdown
---

# Autofix CI failures with Codex

Codex can keep your continuous integration (CI) signal green by running automatically whenever a workflow fails. This guide adapts the official Codex cookbook so GitHub Actions can invoke the Codex CLI, apply targeted fixes, verify tests, and open a pull request for review.

## End-to-end flow

Below is the pipeline flow we'll implement:

1. A primary workflow named `CI` (rename as needed) runs as normal.
2. When the workflow finishes with a failure, a second workflow installs Codex, gathers context, and delegates to the Codex CLI via `openai/codex-action`.
3. Codex iterates locally in the GitHub-hosted runner, applies a minimal fix, and pushes a pull request back to the failing branch for review.

![Diagram of the Codex autofix workflow in CI, from failing jobs to Codex creating a pull request.](/images/codex/autofix/ci-codex-workflow.png)

## Prerequisites

- A repository with GitHub Actions enabled and a primary workflow to monitor.
- The `OPENAI_API_KEY` secret configured either at the repo or organization level so Codex CLI can authenticate.
- Python available in the runner image (needed for `codex login`).
- Repository permissions that allow GitHub Actions to create branches and pull requests.

![Screenshot of the GitHub pull request permission toggle required for Codex autofix workflows.](/images/codex/autofix/github-pr-settings.png)

## Step 1: Add the GitHub Action to your CI Pipeline

Create a workflow such as `.github/workflows/codex-autofix.yml` that listens for failed runs from your primary workflow. Update the `workflows` array if your pipeline uses a different name. The job installs dependencies, runs Codex with a guard-railed prompt, re-runs your tests, and uses `peter-evans/create-pull-request` to stage a reviewable fix.

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
      - name: Check OpenAI API Key Set
        run: |
          if [ -z "$OPENAI_API_KEY" ]; then
            echo "OPENAI_API_KEY secret is not set. Skipping auto-fix." >&2
            exit 1
          fi
      - name: Checkout Failing Ref
        uses: actions/checkout@v5
        with:
          ref: ${{ env.FAILED_HEAD_SHA }}
          fetch-depth: 0
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - name: Install dependencies
        run: |
          if [ -f package-lock.json ]; then npm ci; else npm i; fi
      - name: Run Codex
        uses: openai/codex-action@main
        id: codex
        with:
          openai_api_key: ${{ secrets.OPENAI_API_KEY }}
          prompt: >-
            You are working in a Node.js monorepo with Jest tests and GitHub Actions. Read the repository,
            run the test suite, identify the minimal change needed to make all tests pass, implement only that change,
            and stop. Do not refactor unrelated code or files. Keep changes small and surgical.
          codex_args: '["--config","sandbox_mode=\"workspace-write\""]'
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

## Step 2: Watch the follow-up workflow run

When the main workflow fails you can monitor both the failure and the Codex follow-up under the Actions tab. 

![Screenshot of a failing GitHub Actions workflow that will trigger the Codex autofix job.](/images/codex/autofix/failing-workflow.png)

The autofix workflow will appear as soon as the triggering workflow finishes.

![Screenshot of the Codex autofix workflow execution in GitHub Actions.](/images/codex/autofix/codex-workflow.png)

## Step 3: Review the generated pull request

After Codex finishes, it opens a pull request on a branch named `codex/auto-fix-<run_id>` that contains the proposed patch along with a summary referencing the failed run. Review and merge as you would with any contribution.

![Screenshot of a pull request opened by the Codex autofix workflow.](/images/codex/autofix/codex-pr.png)

## Conclusion

Embedding Codex CLI in CI automates repetitive cleanup steps after failures. You can adapt the same scaffold to run different test commands, adjust prompts for your stack, or extend the workflow with additional safeguards while keeping Codex in control of quick fixes.
