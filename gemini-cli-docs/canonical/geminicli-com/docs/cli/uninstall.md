---
source_url: https://geminicli.com/docs/cli/uninstall
source_type: llms-txt
content_hash: sha256:a066af1bfcdaef37665912e13c48d208260f0736361b7e9cd027175e37457878
sitemap_url: https://geminicli.com/llms.txt
fetch_method: markdown
etag: '"4551bfdfcd0ee71334d8179e6982d4363450a03b33c0c332fcfaba54241e8906"'
last_modified: '2026-02-13T20:13:35Z'
---

# Uninstalling the CLI

Your uninstall method depends on how you ran the CLI. Follow the instructions
for either npx or a global npm installation.

## Method 1: Using npx

npx runs packages from a temporary cache without a permanent installation. To
"uninstall" the CLI, you must clear this cache, which will remove gemini-cli and
any other packages previously executed with npx.

The npx cache is a directory named `_npx` inside your main npm cache folder. You
can find your npm cache path by running `npm config get cache`.

**For macOS / Linux**

```bash
# The path is typically ~/.npm/_npx
rm -rf "$(npm config get cache)/_npx"
```

**For Windows**

_Command Prompt_

```cmd
:: The path is typically %LocalAppData%\npm-cache\_npx
rmdir /s /q "%LocalAppData%\npm-cache\_npx"
```

_PowerShell_

```powershell
# The path is typically $env:LocalAppData\npm-cache\_npx
Remove-Item -Path (Join-Path $env:LocalAppData "npm-cache\_npx") -Recurse -Force
```

## Method 2: Using npm (global install)

If you installed the CLI globally (e.g., `npm install -g @google/gemini-cli`),
use the `npm uninstall` command with the `-g` flag to remove it.

```bash
npm uninstall -g @google/gemini-cli
```

This command completely removes the package from your system.

## Method 3: Homebrew

If you installed the CLI globally using Homebrew (e.g.,
`brew install gemini-cli`), use the `brew uninstall` command to remove it.

```bash
brew uninstall gemini-cli
```

## Method 4: MacPorts

If you installed the CLI globally using MacPorts (e.g.,
`sudo port install gemini-cli`), use the `port uninstall` command to remove it.

```bash
sudo port uninstall gemini-cli
```
