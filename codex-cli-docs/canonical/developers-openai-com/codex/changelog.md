---
source_url: https://developers.openai.com/codex/changelog
source_type: manual
content_hash: sha256:c53b18687f4c76839d973de872c93260932e38bb32c3007e7b97c790101f69ab
fetch_method: html
---

# Codex Changelog

[December 2025](#month-2025-12)  [November 2025](#month-2025-11)  [October 2025](#month-2025-10)  [September 2025](#month-2025-09)  [August 2025](#month-2025-08)  [June 2025](#month-2025-06)  [May 2025](#month-2025-05)

## December 2025

* 2025-12-13

  ### Codex CLI 0.72.0

  ```
  $ npm install -g @openai/codex@0.72.0
  ```

    View details    

  # Highlights

  + Config API cleanup ([#7924](https://github.com/openai/codex/pull/7924)): new config API and cleaner config loading flow.
  + Remote compact for API-key users ([#7835](https://github.com/openai/codex/pull/7835)): enable remote compacting in key-based sessions.
  + MCP and TUI status visibility ([#7828](https://github.com/openai/codex/pull/7828), [#7907](https://github.com/openai/codex/pull/7907)): restore MCP startup progress messages in the TUI and use latest disk values  
    for server status.
  + Windows and PowerShell quality-of-life ([#7607](https://github.com/openai/codex/pull/7607), [#7893](https://github.com/openai/codex/pull/7893), [#7942](https://github.com/openai/codex/pull/7942), [#7137](https://github.com/openai/codex/pull/7137)): locate pwsh/powershell reliably, parse PowerShell with  
    PowerShell, sign additional Windows executables, and fix WSL2 toasts.
  + Sandbox and safety updates ([#7809](https://github.com/openai/codex/pull/7809), [#7889](https://github.com/openai/codex/pull/7889), [#7728](https://github.com/openai/codex/pull/7728)): Elevated Sandbox 3/4 plus expanded safe command list.
  + Model/prompt UX for gpt-5.2 ([#7934](https://github.com/openai/codex/pull/7934), [#7910](https://github.com/openai/codex/pull/7910), [#7874](https://github.com/openai/codex/pull/7874), [#7911](https://github.com/openai/codex/pull/7911)): prompt updates and clearer xhigh reasoning warnings/docs.

  # PRs Merged

  + fix cargo build switch [#7948](https://github.com/openai/codex/pull/7948) @[iceweasel-oai]
  + fix: restore MCP startup progress messages in TUI (fixes [#7827](https://github.com/openai/codex/issues/7827)) [#7828](https://github.com/openai/codex/pull/7828) @[ivanmurashko]
  + support 1p [#7945](https://github.com/openai/codex/pull/7945) @[aibrahim-oai]
  + Sign two additional exes for Windows [#7942](https://github.com/openai/codex/pull/7942) @[iceweasel-oai]
  + fix: use PowerShell to parse PowerShell [#7607](https://github.com/openai/codex/pull/7607) @[bolinfest]
  + chore(prompt) Update base prompt [#7943](https://github.com/openai/codex/pull/7943) @[dylan-hurd-oai]
  + Elevated Sandbox 4 [#7889](https://github.com/openai/codex/pull/7889) @[iceweasel-oai]
  + chore(prompt) Remove truncation details [#7941](https://github.com/openai/codex/pull/7941) @[dylan-hurd-oai]
  + feat: clean config loading and config api [#7924](https://github.com/openai/codex/pull/7924) @[jif-oai]
  + chores: models manager [#7937](https://github.com/openai/codex/pull/7937) @[aibrahim-oai]
  + Remote compact for API-key users [#7835](https://github.com/openai/codex/pull/7835) @[pakrym-oai]
  + chore(gpt-5.2) prompt update [#7934](https://github.com/openai/codex/pull/7934) @[dylan-hurd-oai]
  + fix: race on rx subscription [#7921](https://github.com/openai/codex/pull/7921) @[jif-oai]
  + fix: break tui [#7876](https://github.com/openai/codex/pull/7876) @[jif-oai]
  + feat: more safe commands [#7728](https://github.com/openai/codex/pull/7728) @[jif-oai]
  + fix(tui): show xhigh reasoning warning for gpt-5.2 [#7910](https://github.com/openai/codex/pull/7910) @[voctory]
  + Make skill name and description limit based on characters not byte counts [#7915](https://github.com/openai/codex/pull/7915) @[etraut-openai]
  + feat: introduce utilities for locating pwsh.exe and powershell.exe [#7893](https://github.com/openai/codex/pull/7893) @[bolinfest]
  + docs: clarify xhigh reasoning effort on gpt-5.2 [#7911](https://github.com/openai/codex/pull/7911) @[voctory]
  + feat: use latest disk value for mcp servers status [#7907](https://github.com/openai/codex/pull/7907) @[shijie-oai]
  + Revert "fix(apply-patch): preserve CRLF line endings on Windows" [#7903](https://github.com/openai/codex/pull/7903) @[dylan-hurd-oai]
  + Make migration screen dynamic [#7896](https://github.com/openai/codex/pull/7896) @[aibrahim-oai]
  + Fix misleading 'maximize' high effort description on xhigh models [#7874](https://github.com/openai/codex/pull/7874) @[voctory]
  + Added deprecation notice for "chat" wire\_api [#7897](https://github.com/openai/codex/pull/7897) @[etraut-openai]
  + Fix toasts on Windows under WSL 2 [#7137](https://github.com/openai/codex/pull/7137) @[dank-openai]
  + fix: policy/*.codexpolicy -> rules/*.rules [#7888](https://github.com/openai/codex/pull/7888) @[bolinfest]
  + Update RMCP client config guidance [#7895](https://github.com/openai/codex/pull/7895) @[nornagon-openai]
  + Update Model Info [#7853](https://github.com/openai/codex/pull/7853) @[aibrahim-oai]
  + Elevated Sandbox 3 [#7809](https://github.com/openai/codex/pull/7809) @[iceweasel-oai]
  + remove release script [#7885](https://github.com/openai/codex/pull/7885) @[aibrahim-oai]
  + Chore: limit find family visability [#7891](https://github.com/openai/codex/pull/7891) @[aibrahim-oai]
  + fix: omit reasoning summary when ReasoningSummary::None [#7845](https://github.com/openai/codex/pull/7845) @[apanasenko-oai]
  + fix: drop stale filedescriptor output hash for nix [#7865](https://github.com/openai/codex/pull/7865) @[tyleranton]
  + fix: dont quit on 'q' in onboarding ApiKeyEntry state [#7869](https://github.com/openai/codex/pull/7869) @[sayan-oai]

  [Full release on Github](https://github.com/openai/codex/releases/tag/rust-v0.72.0)
* 2025-12-11

  ### Codex CLI 0.71.0

  ```
  $ npm install -g @openai/codex@0.71.0
  ```

    View details    

  ### Highlights

  + Introducing gpt-5.2 our latest frontier model with improvements across knowledge, reasoning and coding. [Learn More](https://openai.com/index/introducing-gpt-5-2/)

  ### PRs Merged

  [#7838](https://github.com/openai/codex/pull/7838) Show the default model in model picker [@aibrahim-oai](https://github.com/aibrahim-oai)  
  [#7833](https://github.com/openai/codex/pull/7833) feat(tui2): copy tui crate and normalize snapshots [@joshka-oai](https://github.com/joshka-oai)  
  [#7509](https://github.com/openai/codex/pull/7509) fix: thread/list returning fewer than the requested amount due to filtering CXA-293 [@JaviSoto](https://github.com/JaviSoto)  
  [#7832](https://github.com/openai/codex/pull/7832) fix: ensure accept\_elicitation\_for\_prompt\_rule() test passes locally [@bolinfest](https://github.com/bolinfest)  
  [#7847](https://github.com/openai/codex/pull/7847) fixing typo in execpolicy docs [@zhao-oai](https://github.com/zhao-oai)  
  [#7831](https://github.com/openai/codex/pull/7831) [app-server] make app server not throw error when login id is not found [@celia-oai](https://github.com/celia-oai)  
  [#7848](https://github.com/openai/codex/pull/7848) fix: add a hopefully-temporary sleep to reduce test flakiness [@bolinfest](https://github.com/bolinfest)  
  [#7850](https://github.com/openai/codex/pull/7850) [app-server] Update readme to include mcp endpoints [@celia-oai](https://github.com/celia-oai)  
  [#7851](https://github.com/openai/codex/pull/7851) fix: remove inaccurate #[allow(dead\_code)] marker [@bolinfest](https://github.com/bolinfest)  
  [#7859](https://github.com/openai/codex/pull/7859) Fixed regression that broke fuzzy matching for slash commands [@etraut-openai](https://github.com/etraut-openai)  
  [#7854](https://github.com/openai/codex/pull/7854) Only show Worked for after the final assistant message [@pakrym-oai](https://github.com/pakrym-oai)  
  [#7792](https://github.com/openai/codex/pull/7792) Elevated Sandbox 2 [@iceweasel-oai](https://github.com/iceweasel-oai)  
  [#7855](https://github.com/openai/codex/pull/7855) fix(stuff) [@dylan-hurd-oai](https://github.com/dylan-hurd-oai)  
  [#7870](https://github.com/openai/codex/pull/7870) feat: warning for long snapshots [@jif-oai](https://github.com/jif-oai)  
  [#7786](https://github.com/openai/codex/pull/7786) feat: add shell snapshot for shell command [@jif-oai](https://github.com/jif-oai)  
  [#7875](https://github.com/openai/codex/pull/7875) fix: flaky tests 4 [@jif-oai](https://github.com/jif-oai)  
  [#7882](https://github.com/openai/codex/pull/7882) feat: robin [@aibrahim-oai](https://github.com/aibrahim-oai)  
  [#7884](https://github.com/openai/codex/pull/7884) Revert "Only show Worked for after the final assistant message" [@pakrym-oai](https://github.com/pakrym-oai)

  [Full release on Github](https://github.com/openai/codex/releases/tag/rust-v0.71.0)
* 2025-12-10

  ### Codex CLI 0.69.0

  ```
  $ npm install -g @openai/codex@0.69.0
  ```

    View details    

  ### Highlights

  + Skills: Explicit skill selections now inject SKILL.md content into the turn; skills load once per session and warn if a file  
    can't be read ([#7763](https://github.com/openai/codex/pull/7763)).
  + Config API: config/read is fully typed; config writes preserve comments/order; model is optional to match real configs ([#7658](https://github.com/openai/codex/pull/7658),  
    [#7789](https://github.com/openai/codex/pull/7789), [#7769](https://github.com/openai/codex/pull/7769)).
  + TUI/UX: Log files drop ANSI codes; vim navigation for option selection and transcript pager; transcript continuity fix; slash-  
    command popup no longer triggers on invalid input; experimental tui2 frontend behind a flag ([#7836](https://github.com/openai/codex/pull/7836), [#7784](https://github.com/openai/codex/pull/7784), [#7550](https://github.com/openai/codex/pull/7550), [#7363](https://github.com/openai/codex/pull/7363),  
    [#7704](https://github.com/openai/codex/pull/7704), [#7793](https://github.com/openai/codex/pull/7793)).
  + Exec & sandbox: Shell snapshotting, reworked unified-exec events, elevated sandbox allowances (sendmsg/recvmsg), clearer rate-  
    limit warnings, better request-id logging, and safer escalations ([#7641](https://github.com/openai/codex/pull/7641), [#7775](https://github.com/openai/codex/pull/7775), [#7788](https://github.com/openai/codex/pull/7788), [#7779](https://github.com/openai/codex/pull/7779), [#7795](https://github.com/openai/codex/pull/7795), [#7830](https://github.com/openai/codex/pull/7830), [#7750](https://github.com/openai/codex/pull/7750)).
  + Platform/auth/build: MCP in-session login, remote-branch review support, Windows signing toggles, ConPty vendoring, Nix hash  
    fixes, and safer release guardrails ([#7751](https://github.com/openai/codex/pull/7751), [#7813](https://github.com/openai/codex/pull/7813), [#7757](https://github.com/openai/codex/pull/7757)/[#7804](https://github.com/openai/codex/pull/7804)/[#7806](https://github.com/openai/codex/pull/7806), [#7656](https://github.com/openai/codex/pull/7656), [#7762](https://github.com/openai/codex/pull/7762), [#7834](https://github.com/openai/codex/pull/7834)).
  + Misc fixes: Unsupported images error cleanly, absolute config paths, parallel test stability, duplicated feature spec removal,  
    experimental-model prompt/tools, and more ([#7478](https://github.com/openai/codex/pull/7478), [#7796](https://github.com/openai/codex/pull/7796), [#7589](https://github.com/openai/codex/pull/7589), [#7818](https://github.com/openai/codex/pull/7818), [#7826](https://github.com/openai/codex/pull/7826), [#7823](https://github.com/openai/codex/pull/7823), [#7765](https://github.com/openai/codex/pull/7765)).

  ### PRs Merged

  + [#7836](https://github.com/openai/codex/pull/7836) Disable ansi codes in TUI log file
  + [#7834](https://github.com/openai/codex/pull/7834) Error when trying to push a release while another release is in progress
  + [#7830](https://github.com/openai/codex/pull/7830) Remove conversation\_id and bring back request ID logging
  + [#7826](https://github.com/openai/codex/pull/7826) fix: flaky tests 3
  + [#7823](https://github.com/openai/codex/pull/7823) fix: remove duplicated parallel FeatureSpec
  + [#7818](https://github.com/openai/codex/pull/7818) fix: flaky test 2
  + [#7817](https://github.com/openai/codex/pull/7817) fix: Upgrade @modelcontextprotocol/sdk to ^1.24.0
  + [#7813](https://github.com/openai/codex/pull/7813) feat: use remote branch for review is local trails
  + [#7807](https://github.com/openai/codex/pull/7807) chore: disable trusted signing pkg cache hit
  + [#7806](https://github.com/openai/codex/pull/7806) Revert "Revert "feat: windows codesign with Azure trusted signing""
  + [#7804](https://github.com/openai/codex/pull/7804) Revert "feat: windows codesign with Azure trusted signing"
  + [#7799](https://github.com/openai/codex/pull/7799) Removed experimental "command risk assessment" feature
  + [#7797](https://github.com/openai/codex/pull/7797) parse rg | head a search
  + [#7796](https://github.com/openai/codex/pull/7796) fix: introduce AbsolutePathBuf and resolve relative paths in config.toml
  + [#7795](https://github.com/openai/codex/pull/7795) Express rate limit warning as % remaining
  + [#7793](https://github.com/openai/codex/pull/7793) feat(tui2): add feature-flagged tui2 frontend
  + [#7789](https://github.com/openai/codex/pull/7789) [app-server] Preserve comments & order in config writes
  + [#7788](https://github.com/openai/codex/pull/7788) Elevated Sandbox 1
  + [#7787](https://github.com/openai/codex/pull/7787) fix more typos in execpolicy.md
  + [#7784](https://github.com/openai/codex/pull/7784) Add vim-style navigation for CLI option selection
  + [#7779](https://github.com/openai/codex/pull/7779) allow sendmsg/recvmsg syscalls in Linux sandbox
  + [#7775](https://github.com/openai/codex/pull/7775) chore: rework unified exec events
  + [#7769](https://github.com/openai/codex/pull/7769) make model optional in config
  + [#7765](https://github.com/openai/codex/pull/7765) Use codex-max prompt/tools for experimental models
  + [#7763](https://github.com/openai/codex/pull/7763) Inject SKILL.md when it's explicitly mentioned
  + [#7762](https://github.com/openai/codex/pull/7762) Fix Nix cargo output hashes for rmcp and filedescriptor
  + [#7757](https://github.com/openai/codex/pull/7757) Revert "Revert "feat: windows codesign with Azure trusted signing""
  + [#7756](https://github.com/openai/codex/pull/7756) Vendor ConPtySystem
  + [#7751](https://github.com/openai/codex/pull/7751) feat: support mcp in-session login
  + [#7750](https://github.com/openai/codex/pull/7750) refactor with\_escalated\_permissions to use SandboxPermissions
  + [#7704](https://github.com/openai/codex/pull/7704) fix: Prevent slash command popup from activating on invalid inputs
  + [#7658](https://github.com/openai/codex/pull/7658) [app-server-protocol] Add types for config
  + [#7641](https://github.com/openai/codex/pull/7641) feat: shell snapshotting
  + [#7589](https://github.com/openai/codex/pull/7589) chore: enable parallel tc
  + [#7550](https://github.com/openai/codex/pull/7550) Add vim navigation keys to transcript pager
  + [#7478](https://github.com/openai/codex/pull/7478) Fix: gracefully error out for unsupported images
  + [#7363](https://github.com/openai/codex/pull/7363) Fix transcript pager page continuity
  + [#7779](https://github.com/openai/codex/pull/7779) allow sendmsg/recvmsg syscalls in Linux sandbox (already listed; ensure single entry)
  + [#7788](https://github.com/openai/codex/pull/7788) Elevated Sandbox 1 (already listed)
  + [#7784](https://github.com/openai/codex/pull/7784) Add vim-style navigation for CLI option selection (already listed)
  + [#7807](https://github.com/openai/codex/pull/7807)/7806/7804 Windows signing toggles (grouped above)

  [Full release on Github](https://github.com/openai/codex/releases/tag/rust-v0.69.0)
* 2025-12-09

  ### Codex CLI 0.66.0

  ```
  $ npm install -g @openai/codex@0.66.0
  ```

    View details    

  ### Highlights

  + Execpolicy: TUI can whitelist command prefixes after an approval, sandbox denials propose an amendment you can accept, shell MCP now runs execpolicy so MCP tools follow the same rules, and  
    fallback checks inspect each pipeline segment so unsafe tails (e.g., | rm -rf) are still caught ([#7033](https://github.com/openai/codex/pull/7033), [#7543](https://github.com/openai/codex/pull/7543), [#7609](https://github.com/openai/codex/pull/7609), [#7653](https://github.com/openai/codex/pull/7653), [#7544](https://github.com/openai/codex/pull/7544)).
  + Unified exec & shell stability: status line shows clearer progress, Windows unified-exec crash fixed, long commands wrap without breaking layout, and SSE/session cleanup reduces stuck or  
    dangling sessions after tool calls ([#7563](https://github.com/openai/codex/pull/7563), [#7620](https://github.com/openai/codex/pull/7620), [#7655](https://github.com/openai/codex/pull/7655), [#7594](https://github.com/openai/codex/pull/7594), [#7592](https://github.com/openai/codex/pull/7592)).
  + TUI updates: cross-platform shortcut handling is consistent (Ctrl+N/P and list selection now work everywhere), so navigation matches between overlays, lists, and text areas ([#7583](https://github.com/openai/codex/pull/7583), [#7629](https://github.com/openai/codex/pull/7629)).
  + Apply-patch: Windows CRLF line endings are preserved, new e2e scenarios cover more patch shapes, and Windows-specific test coverage reduces regressions in patch flows ([#7515](https://github.com/openai/codex/pull/7515), [#7567](https://github.com/openai/codex/pull/7567), [#7554](https://github.com/openai/codex/pull/7554)). Thanks to [@cnaples79](https://github.com/cnaples79) who contributed the [core part](https://github.com/openai/codex/pull/4017) of this fix!
  + Cloud exec: codex cloud exec accepts --branch for remote runs and now exposes status/diff/apply flows so you can inspect and apply changes from the cloud path ([#7602](https://github.com/openai/codex/pull/7602), [#7614](https://github.com/openai/codex/pull/7614)).
  + Signing: Linux artifacts are signed via sigstore. ([#7674](https://github.com/openai/codex/pull/7674)).
  + General fixes: parallel tool-call chat now returns correctly, ghost snapshot tokens aren't billed, missing tool names no longer crash the litellm proxy, and migration prompts use HTTPS links  
    ([#7634](https://github.com/openai/codex/pull/7634), [#7638](https://github.com/openai/codex/pull/7638), [#7724](https://github.com/openai/codex/pull/7724), [#7705](https://github.com/openai/codex/pull/7705)).

  ### PRs Merged

  + [#6793](https://github.com/openai/codex/pull/6793) FIX: WSL Paste image does not work [@Waxime64](https://github.com/Waxime64)
  + [#6846](https://github.com/openai/codex/pull/6846) feat(core) Add login to shell\_command tool [@dylan-hurd-oai](https://github.com/dylan-hurd-oai)
  + [#6918](https://github.com/openai/codex/pull/6918) Add Enterprise plan to ChatGPT login description [@ae-openai](https://github.com/ae-openai)
  + [#7033](https://github.com/openai/codex/pull/7033) whitelist command prefix integration in core and tui [@zhao-oai](https://github.com/zhao-oai)
  + [#7310](https://github.com/openai/codex/pull/7310) Inline response recording and remove process\_items indirection [@aibrahim-oai](https://github.com/aibrahim-oai)
  + [#7515](https://github.com/openai/codex/pull/7515) fix(apply-patch): preserve CRLF line endings on Windows [@dylan-hurd-oai](https://github.com/dylan-hurd-oai)
  + [#7543](https://github.com/openai/codex/pull/7543) execpolicy tui flow [@zhao-oai](https://github.com/zhao-oai)
  + [#7544](https://github.com/openai/codex/pull/7544) Refactor execpolicy fallback evaluation [@zhao-oai](https://github.com/zhao-oai)
  + [#7547](https://github.com/openai/codex/pull/7547) Use shared check sandboxing [@pakrym-oai](https://github.com/pakrym-oai)
  + [#7554](https://github.com/openai/codex/pull/7554) chore(core): test apply\_patch\_cli on Windows [@dylan-hurd-oai](https://github.com/dylan-hurd-oai)
  + [#7561](https://github.com/openai/codex/pull/7561) Do not emit start/end events for write stdin [@pakrym-oai](https://github.com/pakrym-oai)
  + [#7563](https://github.com/openai/codex/pull/7563) Slightly better status display for unified exec [@pakrym-oai](https://github.com/pakrym-oai)
  + [#7567](https://github.com/openai/codex/pull/7567) chore(apply-patch) scenarios for e2e testing [@dylan-hurd-oai](https://github.com/dylan-hurd-oai)
  + [#7571](https://github.com/openai/codex/pull/7571) remove model\_family from `config [@aibrahim-oai](https://github.com/aibrahim-oai)
  + [#7580](https://github.com/openai/codex/pull/7580) feat: update sandbox policy to allow TTY [@jif-oai](https://github.com/jif-oai)
  + [#7583](https://github.com/openai/codex/pull/7583) Fix handle\_shortcut\_overlay\_key for cross-platform consistency [@448523760](https://github.com/448523760)
  + [#7588](https://github.com/openai/codex/pull/7588) chore: default warning messages to true [@jif-oai](https://github.com/jif-oai)
  + [#7591](https://github.com/openai/codex/pull/7591) chore: tool tip for /prompt [@jif-oai](https://github.com/jif-oai)
  + [#7592](https://github.com/openai/codex/pull/7592) fix: release session ID when not used [@jif-oai](https://github.com/jif-oai)
  + [#7593](https://github.com/openai/codex/pull/7593) chore: review in read-only [@jif-oai](https://github.com/jif-oai)
  + [#7594](https://github.com/openai/codex/pull/7594) fix: sse for chat [@jif-oai](https://github.com/jif-oai)
  + [#7595](https://github.com/openai/codex/pull/7595) Update execpolicy.md [@zhao-oai](https://github.com/zhao-oai)
  + [#7602](https://github.com/openai/codex/pull/7602) add --branch to codex cloud exec [@nornagon-openai](https://github.com/nornagon-openai)
  + [#7603](https://github.com/openai/codex/pull/7603) Add models endpoint [@aibrahim-oai](https://github.com/aibrahim-oai)
  + [#7605](https://github.com/openai/codex/pull/7605) fix(app-server): add duration\_ms to McpToolCallItem [@owenlin0](https://github.com/owenlin0)
  + [#7609](https://github.com/openai/codex/pull/7609) feat: exec policy integration in shell mcp [@zhao-oai](https://github.com/zhao-oai)
  + [#7610](https://github.com/openai/codex/pull/7610) fix: taking plan type from usage endpoint instead of thru auth token [@zhao-oai](https://github.com/zhao-oai)
  + [#7611](https://github.com/openai/codex/pull/7611) fix(app-server): add will\_retry to ErrorNotification [@owenlin0](https://github.com/owenlin0)
  + [#7614](https://github.com/openai/codex/pull/7614) cloud: status, diff, apply [@nornagon-openai](https://github.com/nornagon-openai)
  + [#7615](https://github.com/openai/codex/pull/7615) chore: refactor to move Arc concern outside exec\_policy\_for [@bolinfest](https://github.com/bolinfest)
  + [#7616](https://github.com/openai/codex/pull/7616) Call models endpoint in models manager [@aibrahim-oai](https://github.com/aibrahim-oai)
  + [#7617](https://github.com/openai/codex/pull/7617) fix: add integration tests for codex-exec-mcp-server with execpolicy [@bolinfest](https://github.com/bolinfest)
  + [#7620](https://github.com/openai/codex/pull/7620) Fix unified\_exec on windows [@pakrym](https://github.com/pakrym)
  + [#7621](https://github.com/openai/codex/pull/7621) Wire with\_remote\_overrides to construct model families [@aibrahim-oai](https://github.com/aibrahim-oai)
  + [#7626](https://github.com/openai/codex/pull/7626) fix typo [@zhao-oai](https://github.com/zhao-oai)
  + [#7629](https://github.com/openai/codex/pull/7629) fix(tui): add missing Ctrl+n/Ctrl+p support to ListSelectionView [@pppp606](https://github.com/pppp606)
  + [#7634](https://github.com/openai/codex/pull/7634) fix: chat completion with parallel tool call [@jif-oai](https://github.com/jif-oai)
  + [#7638](https://github.com/openai/codex/pull/7638) fix: ignore ghost snapshots in token consumption [@jif-oai](https://github.com/jif-oai)
  + [#7645](https://github.com/openai/codex/pull/7645) Also load skills from repo root. [@xl-openai](https://github.com/xl-openai)
  + [#7648](https://github.com/openai/codex/pull/7648) Add remote models feature flag [@aibrahim-oai](https://github.com/aibrahim-oai)
  + [#7651](https://github.com/openai/codex/pull/7651) fix: OTEL HTTP exporter panic and mTLS support [@asm89](https://github.com/asm89)
  + [#7652](https://github.com/openai/codex/pull/7652) Move justfile to repository root [@joshka-oai](https://github.com/joshka-oai)
  + [#7653](https://github.com/openai/codex/pull/7653) proposing execpolicy amendment when prompting due to sandbox denial [@zhao-oai](https://github.com/zhao-oai)
  + [#7654](https://github.com/openai/codex/pull/7654) fix: exec-server stream was erroring for large requests [@bolinfest](https://github.com/bolinfest)
  + [#7655](https://github.com/openai/codex/pull/7655) fix wrap behavior for long commands [@zhao-oai](https://github.com/zhao-oai)
  + [#7660](https://github.com/openai/codex/pull/7660) Restore status header after stream recovery [@joshka-oai](https://github.com/joshka-oai)
  + [#7665](https://github.com/openai/codex/pull/7665) docs: fix documentation of rmcp client flag [@JaySabva](https://github.com/JaySabva)
  + [#7669](https://github.com/openai/codex/pull/7669) fix(doc): TOML otel exporter example — multi-line inline table is invalid [@448523760](https://github.com/448523760)
  + [#7672](https://github.com/openai/codex/pull/7672) docs: Remove experimental\_use\_rmcp\_client from config [@JaySabva](https://github.com/JaySabva)
  + [#7673](https://github.com/openai/codex/pull/7673) docs: point dev checks to just [@voctory](https://github.com/voctory)
  + [#7674](https://github.com/openai/codex/pull/7674) feat: linux codesign with sigstore [@shijie-oai](https://github.com/shijie-oai)
  + [#7675](https://github.com/openai/codex/pull/7675) feat: windows codesign with Azure trusted signing [@shijie-oai](https://github.com/shijie-oai)
  + [#7678](https://github.com/openai/codex/pull/7678) fix: clear out space on ubuntu runners before running Rust tests [@bolinfest](https://github.com/bolinfest)
  + [#7680](https://github.com/openai/codex/pull/7680) fix: ensure macOS CI runners for Rust tests include recent Homebrew fixes [@bolinfest](https://github.com/bolinfest)
  + [#7685](https://github.com/openai/codex/pull/7685) fix: refine the warning message and docs for deprecated tools config [@gameofby](https://github.com/gameofby)
  + [#7705](https://github.com/openai/codex/pull/7705) fix: update URLs to use HTTPS in model migration prompts [@rakleed](https://github.com/rakleed)
  + [#7709](https://github.com/openai/codex/pull/7709) Enhance model picker [@aibrahim-oai](https://github.com/aibrahim-oai)
  + [#7711](https://github.com/openai/codex/pull/7711) Add formatting client version to the x.x.x style. [@aibrahim-oai](https://github.com/aibrahim-oai)
  + [#7713](https://github.com/openai/codex/pull/7713) chore(deps): bump ts-rs from 11.0.1 to 11.1.0 in /codex-rs [@dependabot](https://github.com/dependabot)[bot]
  + [#7714](https://github.com/openai/codex/pull/7714) chore(deps): bump derive\_more from 2.0.1 to 2.1.0 in /codex-rs [@dependabot](https://github.com/dependabot)[bot]
  + [#7715](https://github.com/openai/codex/pull/7715) chore(deps): bump insta from 1.43.2 to 1.44.3 in /codex-rs [@dependabot](https://github.com/dependabot)[bot]
  + [#7716](https://github.com/openai/codex/pull/7716) chore(deps): bump wildmatch from 2.5.0 to 2.6.1 in /codex-rs [@dependabot](https://github.com/dependabot)[bot]
  + [#7722](https://github.com/openai/codex/pull/7722) load models from disk and set a ttl and etag [@aibrahim-oai](https://github.com/aibrahim-oai)
  + [#7724](https://github.com/openai/codex/pull/7724) Fixed regression for chat endpoint; missing tools name caused litellm proxy to crash [@etraut-openai](https://github.com/etraut-openai)
  + [#7729](https://github.com/openai/codex/pull/7729) feat: add is-mutating detection for shell command handler [@jif-oai](https://github.com/jif-oai)
  + [#7745](https://github.com/openai/codex/pull/7745) Make the device auth instructions more clear. [@mzeng-openai](https://github.com/mzeng-openai)
  + [#7747](https://github.com/openai/codex/pull/7747) updating app server types to support execpoilcy amendment [@zhao-oai](https://github.com/zhao-oai)
  + [#7748](https://github.com/openai/codex/pull/7748) Remove legacy ModelInfo and merge it with ModelFamily [@aibrahim-oai](https://github.com/aibrahim-oai)
  + [#7749](https://github.com/openai/codex/pull/7749) fix: pre-main hardening logic must tolerate non-UTF-8 env vars [@bolinfest](https://github.com/bolinfest)
  + [#7753](https://github.com/openai/codex/pull/7753) Revert "feat: windows codesign with Azure trusted signing" [@shijie-oai](https://github.com/shijie-oai)
  + [#7754](https://github.com/openai/codex/pull/7754) override instructions using ModelInfo [@aibrahim-oai](https://github.com/aibrahim-oai)
  + [#7756](https://github.com/openai/codex/pull/7756) use chatgpt provider for /models [@aibrahim-oai](https://github.com/aibrahim-oai)

  [Full release on Github](https://github.com/openai/codex/releases/tag/rust-v0.66.0)
* 2025-12-04

  ### Introducing Codex for Linear

  Assign or mention @Codex in an issue to kick-off a Codex cloud task. As Codex works, it posts updates back to Linear, providing a link to the completed task so you can review, open a PR, or keep working.

  ![Screenshot of a successful Codex task started in Linear](/images/codex/integrations/linear-codex-example.png)

  To learn more about how to connect Codex to Linear both locally through MCP and through the new integration, check out the [Codex for Linear documentation](/codex/integrations/linear).
* 2025-12-04

  ### Codex CLI 0.65.0

  ```
  $ npm install -g @openai/codex@0.65.0
  ```

    View details    

  ### Highlights

  + Codex Max as default ([#7566](https://github.com/openai/codex/pull/7566)): Codex Max is now the default model, and a TUI panic related to async-in-sync code was fixed.
  + Better resume UX ([#7302](https://github.com/openai/codex/pull/7302), [#7303](https://github.com/openai/codex/pull/7303)): Added a /resume slash command and improved resume performance so picking work back up is snappier.
  + Tooltips & tips UX ([#7557](https://github.com/openai/codex/pull/7557), [#7440](https://github.com/openai/codex/pull/7440)): Tips/tooltips are rendered via markdown with a bold "Tip" label and richer Codex tooltips across the app.
  + TUI quality-of-life ([#7530](https://github.com/openai/codex/pull/7530), [#7448](https://github.com/openai/codex/pull/7448), [#7514](https://github.com/openai/codex/pull/7514), [#7461](https://github.com/openai/codex/pull/7461)): TUI gets Ctrl‑P/N navigation, screen-line-capped shell output, restored Windows clipboard image paste, and a refactor for cleaner layout.
  + History and context hygiene ([#6242](https://github.com/openai/codex/pull/6242), [#7483](https://github.com/openai/codex/pull/7483), [#7545](https://github.com/openai/codex/pull/7545), [#7431](https://github.com/openai/codex/pull/7431), [#7483](https://github.com/openai/codex/pull/7483)): history.jsonl is trimmed by history.max\_bytes, common junk dirs (incl. **pycache**) are ignored by default, and paste placeholders stay distinct.

  # PRs Merged

  + use markdown for rendering tips [#7557](https://github.com/openai/codex/pull/7557) @[Jeremy Rose]
  + Migrate codex max [#7566](https://github.com/openai/codex/pull/7566) @[Ahmed Ibrahim]
  + Remove test from [#7481](https://github.com/openai/codex/pull/7481) that doesn't add much value [#7558](https://github.com/openai/codex/pull/7558) @[Eric Traut]
  + [app-server] make `file_path` for config optional [#7560](https://github.com/openai/codex/pull/7560) @[Celia Chen]
  + Migrate model family to models manager [#7565](https://github.com/openai/codex/pull/7565) @[Ahmed Ibrahim]
  + Migrate `tui` to use models manager [#7555](https://github.com/openai/codex/pull/7555) @[Ahmed Ibrahim]
  + Introduce `ModelsManager` and migrate `app-server` to use it. [#7552](https://github.com/openai/codex/pull/7552) @[Ahmed Ibrahim]
  + fix: wrap long exec lines in transcript overlay [#7481](https://github.com/openai/codex/pull/7481) @[muyuanjin]
  + fix: Features should be immutable over the lifetime of a session/thread [#7540](https://github.com/openai/codex/pull/7540) @[Michael Bolin]
  + feat: Support listing and selecting skills via $ or /skills [#7506](https://github.com/openai/codex/pull/7506) @[xl-openai]
  + [app-server] fix: add thread\_id to turn/plan/updated [#7553](https://github.com/openai/codex/pull/7553) @[Owen Lin]
  + feat(tui): map Ctrl-P/N to arrow navigation in textarea [#7530](https://github.com/openai/codex/pull/7530) @[Aofei Sheng]
  + fix(tui): limit user shell output by screen lines [#7448](https://github.com/openai/codex/pull/7448) @[muyuanjin]
  + Migrate model preset [#7542](https://github.com/openai/codex/pull/7542) @[Ahmed Ibrahim]
  + fix: main [#7546](https://github.com/openai/codex/pull/7546) @[jif-oai]
  + feat: add pycache to excluded directories [#7545](https://github.com/openai/codex/pull/7545) @[jif-oai]
  + chore: update unified exec sandboxing detection [#7541](https://github.com/openai/codex/pull/7541) @[jif-oai]
  + add slash resume [#7302](https://github.com/openai/codex/pull/7302) @[Ahmed Ibrahim]
  + chore: conversation\_id -> thread\_id in app-server feedback/upload [#7538](https://github.com/openai/codex/pull/7538) @[Owen Lin]
  + chore: delete unused TodoList item from app-server [#7537](https://github.com/openai/codex/pull/7537) @[Owen Lin]
  + chore: update app-server README [#7510](https://github.com/openai/codex/pull/7510) @[Owen Lin]
  + chore: remove bun env var detect [#7534](https://github.com/openai/codex/pull/7534) @[Shijie Rao]
  + feat: support list mcp servers in app server [#7505](https://github.com/openai/codex/pull/7505) @[Shijie Rao]
  + seatbelt: allow openpty() [#7507](https://github.com/openai/codex/pull/7507) @[Jeremy Rose]
  + feat: codex tool tips [#7440](https://github.com/openai/codex/pull/7440) @[jif-oai]
  + feat: retroactive image placeholder to prevent poisoning [#6774](https://github.com/openai/codex/pull/6774) @[jif-oai]
  + feat: model warning in case of apply patch [#7494](https://github.com/openai/codex/pull/7494) @[jif-oai]
  + fix(tui) Support image paste from clipboard on native Windows [#7514](https://github.com/openai/codex/pull/7514) @[Dylan Hurd]
  + fix(unified\_exec): use platform default shell when unified\_exec shell… [#7486](https://github.com/openai/codex/pull/7486) @[Robby He]
  + Update device code auth strings. [#7498](https://github.com/openai/codex/pull/7498) @[Matthew Zeng]
  + fix: inline function marked as dead code [#7508](https://github.com/openai/codex/pull/7508) @[Michael Bolin]
  + improve resume performance [#7303](https://github.com/openai/codex/pull/7303) @[Ahmed Ibrahim]
  + fix: path resolution bug in npx [#7134](https://github.com/openai/codex/pull/7134) @[Michael Bolin]
  + Ensure duplicate-length paste placeholders stay distinct [#7431](https://github.com/openai/codex/pull/7431) @[Joshua Sutton]
  + feat: support --version flag for @openai/codex-shell-tool-mcp [#7504](https://github.com/openai/codex/pull/7504) @[Michael Bolin]
  + refactor: tui.rs extract several pieces [#7461](https://github.com/openai/codex/pull/7461) @[Josh McKinney]
  + chore: make create\_approval\_requirement\_for\_command an async fn [#7501](https://github.com/openai/codex/pull/7501) @[Michael Bolin]
  + Trim `history.jsonl` when `history.max_bytes` is set [#6242](https://github.com/openai/codex/pull/6242) @[liam]
  + fix: remove serde(flatten) annotation for TurnError [#7499](https://github.com/openai/codex/pull/7499) @[Owen Lin]
  + persisting credits if new snapshot does not contain credit info [#7490](https://github.com/openai/codex/pull/7490) @[zhao-oai]
  + fix: drop lock once it is no longer needed [#7500](https://github.com/openai/codex/pull/7500) @[Michael Bolin]
  + execpolicy helpers [#7032](https://github.com/openai/codex/pull/7032) @[zhao-oai]
  + Show token used when context window is unknown [#7497](https://github.com/openai/codex/pull/7497) @[Ahmed Ibrahim]
  + Use non-blocking mutex [#7467](https://github.com/openai/codex/pull/7467) @[Ahmed Ibrahim]
  + Fix: track only untracked paths in ghost snapshots [#7470](https://github.com/openai/codex/pull/7470) @[lionel-oai]
  + feat: ignore standard directories [#7483](https://github.com/openai/codex/pull/7483) @[jif-oai]
  + fix: add ts number annotations for app-server v2 types [#7492](https://github.com/openai/codex/pull/7492) @[Owen Lin]
  + feat: intercept apply\_patch for unified\_exec [#7446](https://github.com/openai/codex/pull/7446) @[jif-oai]
  + chore: remove mention of experimental/unstable from app-server README [#7474](https://github.com/openai/codex/pull/7474) @[Owen Lin]
  + Add request logging back [#7471](https://github.com/openai/codex/pull/7471) @[pakrym-oai]
  + feat: add one off commands to app-server v2 [#7452](https://github.com/openai/codex/pull/7452) @[jif-oai]
  + feat: add warning message for the model [#7445](https://github.com/openai/codex/pull/7445) @[jif-oai]
  + chore: review everywhere [#7444](https://github.com/openai/codex/pull/7444) @[jif-oai]
  + feat: alias compaction [#7442](https://github.com/openai/codex/pull/7442) @[jif-oai]
  + feat: experimental support for skills.md [#7412](https://github.com/openai/codex/pull/7412) @[Thibault Sottiaux]

  [Full release on Github](https://github.com/openai/codex/releases/tag/rust-v0.65.0)
* 2025-12-02

  ### Codex CLI 0.64.0

  ```
  $ npm install -g @openai/codex@0.64.0
  ```

    View details    

  ## Features

  + Threads and turns now include git info, current working directory, CLI version, source metadata, and propagate thread and turn IDs on every item and error. They emit new notifications for diffs, plan updates, token-usage changes, and compaction events. File-change items provide output deltas, and ImageView items render images inline.
  + Review flow is enhanced with a detached review mode, explicit enter and exit events, review thread IDs, and review history remains visible after rollout filtering changes.
  + Execution gains an experimental "exp" model, unified exec pruning to limit session bloat, per-run custom environment injection, policy-approved command bypass, and Windows protections that flag risky browser or URL launches. History lookup now works on Windows and WSL, and model selection honors use\_model.
  + Safety defaults improve via consolidated world-writable scanning and workspace-write enforcement of read-only .git directories. Sandbox assessment and approval flows align with trust policies.
  + MCP and shell tooling add shell-tool MCP login support, explicit capability declaration, sandbox awareness, publication to npm, and MCP elicitations. The rmcp client is upgraded to 0.10.0 for modern notifications.
  + Observability increases as command items expose process IDs and threads and turns emit token-usage and compaction events. Feedback metadata captures source information.
  + Tooling and ops gain follow-up v2 in the app-server test client, new config management utilities, and refreshed approvals documentation and quickstart placement.

  ## Bug fixes

  + PowerShell apply\_patch parsing is corrected, and apply\_patch tests now cover shell\_command behavior.
  + Sandbox assessment regression is fixed, policy-approved commands are honored, dangerous-command checks are tightened on Windows, and workspace-write enforces .git read-only.
  + MCP startup tolerates missing type fields, stream error messages are clarified, and rmcp nix output hash issues are resolved.
  + Delegate cancellation no longer hangs unified exec, early-exit sessions are cleaned up, and duplicate "waited" renderings are suppressed.
  + recent\_commits with limit zero now returns zero, and the NetBSD process-hardening build is unblocked.
  + Review rollout filtering is disabled so history shows, approval presets respect workspace-write, /approvals trust detection is corrected, and sandbox command assessment edge cases are fixed.
  + Compaction accounts for encrypted reasoning, handles token budgets accurately, and emits reliable token-usage and compaction events.
  + TTY stdin is required, WSL clipboard paths are normalized, and stale conversations are dropped on /new to avoid conflicts.
  + Custom prompt expansion with large pastes is fixed, example-config mistakes are corrected, and relative links and streamable\_shell references are cleaned up. Upgrade messaging is corrected.
  + Windows sandbox treats <workspace\_root>/.git as read-only, and risky browser launches are flagged before execution.
  + CLA allowlist now includes dependabot variants, and enterprises can skip upgrade checks and messages.
  + Flaky tests are stabilized, session recycling is improved, and rollout session initialization surfaces errors for diagnosis.

  ## Maintenance

  + Security and CI add cargo-audit and cargo-deny. GitHub Actions are updated to checkout v6 and upload-artifact v5. macOS 13 builds are dropped. A flaky Ubuntu variant is skipped. The next\_minor\_version script now resets the patch number correctly.
  + Dependencies are updated: libc 0.2.177, webbrowser 1.0.6, regex 1.12.2, toml\_edit 0.23.5, arboard 3.6.1, serde\_with 3.16.1, image 0.25.9, reqwest 0.12.24, tracing 0.1.43, and rmcp 0.10.0.
  + Documentation is refreshed: approvals and config guidance, codex max and xhigh defaults, example-config fixes, CLA guidance, and removal of streamable\_shell references.

  ## PRs Merged

  + fix(scripts) next\_minor\_version should reset patch number by [@dylan-hurd-oai](https://github.com/dylan-hurd-oai) in [#7050](https://github.com/openai/codex/pull/7050)
  + [app-server] feat: expose gitInfo/cwd/etc. on Thread by [@owenlin0](https://github.com/owenlin0) in [#7060](https://github.com/openai/codex/pull/7060)
  + feat: Add exp model to experiment with the tools by [@aibrahim-oai](https://github.com/aibrahim-oai) in [#7115](https://github.com/openai/codex/pull/7115)
  + enable unified exec for experiments by [@aibrahim-oai](https://github.com/aibrahim-oai) in [#7118](https://github.com/openai/codex/pull/7118)
  + [app-server] doc: approvals by [@owenlin0](https://github.com/owenlin0) in [#7105](https://github.com/openai/codex/pull/7105)
  + Windows: flag some invocations that launch browsers/URLs as dangerous by [@iceweasel-oai](https://github.com/iceweasel-oai) in [#7111](https://github.com/openai/codex/pull/7111)
  + Use use\_model by [@pakrym-oai](https://github.com/pakrym-oai) in [#7121](https://github.com/openai/codex/pull/7121)
  + feat: support login as an option on shell-tool-mcp by [@bolinfest](https://github.com/bolinfest) in [#7120](https://github.com/openai/codex/pull/7120)
  + fix(tui): Fail when stdin is not a terminal by [@joshka-oai](https://github.com/joshka-oai) in [#6382](https://github.com/openai/codex/pull/6382)
  + support MCP elicitations by [@nornagon-openai](https://github.com/nornagon-openai) in [#6947](https://github.com/openai/codex/pull/6947)
  + refactor: inline sandbox type lookup in process\_exec\_tool\_call by [@bolinfest](https://github.com/bolinfest) in [#7122](https://github.com/openai/codex/pull/7122)
  + bypass sandbox for policy approved commands by [@zhao-oai](https://github.com/zhao-oai) in [#7110](https://github.com/openai/codex/pull/7110)
  + fix: start publishing @openai/codex-shell-tool-mcp to npm by [@bolinfest](https://github.com/bolinfest) in [#7123](https://github.com/openai/codex/pull/7123)
  + feat: declare server capability in shell-tool-mcp by [@bolinfest](https://github.com/bolinfest) in [#7112](https://github.com/openai/codex/pull/7112)
  + move execpolicy quickstart by [@zhao-oai](https://github.com/zhao-oai) in [#7127](https://github.com/openai/codex/pull/7127)
  + Account for encrypted reasoning for auto compaction by [@aibrahim-oai](https://github.com/aibrahim-oai) in [#7113](https://github.com/openai/codex/pull/7113)
  + chore: use proxy for encrypted summary by [@jif-oai](https://github.com/jif-oai) in [#7252](https://github.com/openai/codex/pull/7252)
  + fix: codex delegate cancellation by [@jif-oai](https://github.com/jif-oai) in [#7092](https://github.com/openai/codex/pull/7092)
  + feat: unified exec basic pruning strategy by [@jif-oai](https://github.com/jif-oai) in [#7239](https://github.com/openai/codex/pull/7239)
  + consolidate world-writable-directories scanning. by [@iceweasel-oai](https://github.com/iceweasel-oai) in [#7234](https://github.com/openai/codex/pull/7234)
  + fix: flaky test by [@jif-oai](https://github.com/jif-oai) in [#7257](https://github.com/openai/codex/pull/7257)
  + [feedback] Add source info into feedback metadata. by [@mzeng-openai](https://github.com/mzeng-openai) in [#7140](https://github.com/openai/codex/pull/7140)
  + fix(windows) support apply\_patch parsing in powershell by [@dylan-hurd-oai](https://github.com/dylan-hurd-oai) in [#7221](https://github.com/openai/codex/pull/7221)
  + chore(deps): bump regex from 1.11.1 to 1.12.2 in /codex-rs by [@dependabot](https://github.com/dependabot)[bot] in [#7222](https://github.com/openai/codex/pull/7222)
  + chore(deps): bump toml\_edit from 0.23.4 to 0.23.5 in /codex-rs by [@dependabot](https://github.com/dependabot)[bot] in [#7223](https://github.com/openai/codex/pull/7223)
  + chore(deps): bump actions/upload-artifact from 4 to 5 by [@dependabot](https://github.com/dependabot)[bot] in [#7229](https://github.com/openai/codex/pull/7229)
  + chore(deps): bump actions/checkout from 5 to 6 by [@dependabot](https://github.com/dependabot)[bot] in [#7230](https://github.com/openai/codex/pull/7230)
  + fix: Fix build process-hardening build on NetBSD by [@0-wiz-0](https://github.com/0-wiz-0) in [#7238](https://github.com/openai/codex/pull/7238)
  + Removed streamable\_shell from docs by [@etraut-openai](https://github.com/etraut-openai) in [#7235](https://github.com/openai/codex/pull/7235)
  + chore(deps): bump libc from 0.2.175 to 0.2.177 in /codex-rs by [@dependabot](https://github.com/dependabot)[bot] in [#7224](https://github.com/openai/codex/pull/7224)
  + chore(deps): bump webbrowser from 1.0.5 to 1.0.6 in /codex-rs by [@dependabot](https://github.com/dependabot)[bot] in [#7225](https://github.com/openai/codex/pull/7225)
  + Added alternate form of dependabot to CLA allow list by [@etraut-openai](https://github.com/etraut-openai) in [#7260](https://github.com/openai/codex/pull/7260)
  + Allow enterprises to skip upgrade checks and messages by [@gpeal](https://github.com/gpeal) in [#7213](https://github.com/openai/codex/pull/7213)
  + fix: custom prompt expansion with large pastes by [@Priya-753](https://github.com/Priya-753) in [#7154](https://github.com/openai/codex/pull/7154)
  + chore(ci): add cargo audit workflow and policy by [@joshka-oai](https://github.com/joshka-oai) in [#7108](https://github.com/openai/codex/pull/7108)
  + chore: add cargo-deny configuration by [@joshka-oai](https://github.com/joshka-oai) in [#7119](https://github.com/openai/codex/pull/7119)
  + Windows Sandbox: treat <workspace\_root>/.git as read-only in workspace-write mode by [@iceweasel-oai](https://github.com/iceweasel-oai) in [#7142](https://github.com/openai/codex/pull/7142)
  + chore: dedup unified exec "waited" rendering by [@jif-oai](https://github.com/jif-oai) in [#7256](https://github.com/openai/codex/pull/7256)
  + fix: don't store early exit sessions by [@jif-oai](https://github.com/jif-oai) in [#7263](https://github.com/openai/codex/pull/7263)
  + fix: Correct the stream error message by [@CSRessel](https://github.com/CSRessel) in [#7266](https://github.com/openai/codex/pull/7266)
  + [app-server-test-client] add send-followup-v2 by [@celia-oai](https://github.com/celia-oai) in [#7271](https://github.com/openai/codex/pull/7271)
  + feat[app-serve]: config management by [@jif-oai](https://github.com/jif-oai) in [#7241](https://github.com/openai/codex/pull/7241)
  + feat: add custom env for unified exec process by [@jif-oai](https://github.com/jif-oai) in [#7286](https://github.com/openai/codex/pull/7286)
  + [app-server] feat: add thread\_id and turn\_id to item and error notifications by [@owenlin0](https://github.com/owenlin0) in [#7124](https://github.com/openai/codex/pull/7124)
  + feat: add compaction event by [@jif-oai](https://github.com/jif-oai) in [#7289](https://github.com/openai/codex/pull/7289)
  + [app-server] feat: add turn/diff/updated event by [@owenlin0](https://github.com/owenlin0) in [#7279](https://github.com/openai/codex/pull/7279)
  + fix: Drop MacOS 13 by [@jif-oai](https://github.com/jif-oai) in [#7295](https://github.com/openai/codex/pull/7295)
  + fix: drop conversation when /new by [@jif-oai](https://github.com/jif-oai) in [#7297](https://github.com/openai/codex/pull/7297)
  + chore: proper client extraction by [@jif-oai](https://github.com/jif-oai) in [#6996](https://github.com/openai/codex/pull/6996)
  + tmp: drop flaky ubuntu by [@jif-oai](https://github.com/jif-oai) in [#7300](https://github.com/openai/codex/pull/7300)
  + [app-server] add thread/tokenUsage/updated v2 event by [@celia-oai](https://github.com/celia-oai) in [#7268](https://github.com/openai/codex/pull/7268)
  + correctly recognize WorkspaceWrite policy on /approvals by [@iceweasel-oai](https://github.com/iceweasel-oai) in [#7301](https://github.com/openai/codex/pull/7301)
  + feat: update process ID for event handling by [@jif-oai](https://github.com/jif-oai) in [#7261](https://github.com/openai/codex/pull/7261)
  + Fixed regression in experimental "sandbox command assessment" feature by [@etraut-openai](https://github.com/etraut-openai) in [#7308](https://github.com/openai/codex/pull/7308)
  + nit: drop file by [@jif-oai](https://github.com/jif-oai) in [#7314](https://github.com/openai/codex/pull/7314)
  + doc: fix relative links and add tips by [@lionel-oai](https://github.com/lionel-oai) in [#7319](https://github.com/openai/codex/pull/7319)
  + Fixes two bugs in example-config.md documentation by [@etraut-openai](https://github.com/etraut-openai) in [#7324](https://github.com/openai/codex/pull/7324)
  + chore: improve rollout session init errors by [@jobchong](https://github.com/jobchong) in [#7336](https://github.com/openai/codex/pull/7336)
  + feat: detached review by [@jif-oai](https://github.com/jif-oai) in [#7292](https://github.com/openai/codex/pull/7292)
  + fix: other flaky tests by [@jif-oai](https://github.com/jif-oai) in [#7372](https://github.com/openai/codex/pull/7372)
  + chore: better session recycling by [@jif-oai](https://github.com/jif-oai) in [#7368](https://github.com/openai/codex/pull/7368)
  + chore(deps): bump arboard from 3.6.0 to 3.6.1 in /codex-rs by [@dependabot](https://github.com/dependabot)[bot] in [#7426](https://github.com/openai/codex/pull/7426)
  + chore(deps): bump serde\_with from 3.14.0 to 3.16.1 in /codex-rs by [@dependabot](https://github.com/dependabot)[bot] in [#7422](https://github.com/openai/codex/pull/7422)
  + chore(deps): bump reqwest from 0.12.23 to 0.12.24 in /codex-rs by [@dependabot](https://github.com/dependabot)[bot] in [#7424](https://github.com/openai/codex/pull/7424)
  + chore(deps): bump tracing from 0.1.41 to 0.1.43 in /codex-rs by [@dependabot](https://github.com/dependabot)[bot] in [#7428](https://github.com/openai/codex/pull/7428)
  + Fixed CLA action to properly exempt dependabot by [@etraut-openai](https://github.com/etraut-openai) in [#7429](https://github.com/openai/codex/pull/7429)
  + chore(deps): bump image from 0.25.8 to 0.25.9 in /codex-rs by [@dependabot](https://github.com/dependabot)[bot] in [#7421](https://github.com/openai/codex/pull/7421)
  + [app-server] add turn/plan/updated event by [@celia-oai](https://github.com/celia-oai) in [#7329](https://github.com/openai/codex/pull/7329)
  + fix: disable review rollout filtering by [@jif-oai](https://github.com/jif-oai) in [#7371](https://github.com/openai/codex/pull/7371)
  + [app-server] fix: ensure thread\_id and turn\_id are on all events by [@owenlin0](https://github.com/owenlin0) in [#7408](https://github.com/openai/codex/pull/7408)
  + [app-server] fix: emit item/fileChange/outputDelta for file change items by [@owenlin0](https://github.com/owenlin0) in [#7399](https://github.com/openai/codex/pull/7399)
  + Fix recent\_commits(limit=0) returning 1 commit instead of 0 by [@Towaiji](https://github.com/Towaiji) in [#7334](https://github.com/openai/codex/pull/7334)
  + fix: nix build missing rmcp output hash by [@Alb-O](https://github.com/Alb-O) in [#7436](https://github.com/openai/codex/pull/7436)
  + docs: clarify codex max defaults and xhigh availability by [@kgruiz](https://github.com/kgruiz) in [#7449](https://github.com/openai/codex/pull/7449)
  + fix: prevent MCP startup failure on missing 'type' field by [@linuxmetel](https://github.com/linuxmetel) in [#7417](https://github.com/openai/codex/pull/7417)
  + chore: update to rmcp@0.10.0 to pick up support for custom client notifications by [@bolinfest](https://github.com/bolinfest) in [#7462](https://github.com/openai/codex/pull/7462)
  + fix(apply\_patch) tests for shell\_command by [@dylan-hurd-oai](https://github.com/dylan-hurd-oai) in [#7307](https://github.com/openai/codex/pull/7307)
  + [app-server] Add ImageView item by [@celia-oai](https://github.com/celia-oai) in [#7468](https://github.com/openai/codex/pull/7468)
  + fix(core): enable history lookup on windows by [@stevemostovoy-openai](https://github.com/stevemostovoy-openai) in [#7457](https://github.com/openai/codex/pull/7457)
  + fix(tui): handle WSL clipboard image paths by [@manoelcalixto](https://github.com/manoelcalixto) in [#3990](https://github.com/openai/codex/pull/3990)

  **Full Changelog**: [rust-v0.63.0...rust-v0.64.0](https://github.com/openai/codex/compare/rust-v0.63.0...rust-v0.64.0)

  [Full release on Github](https://github.com/openai/codex/releases/tag/rust-v0.64.0)

## November 2025

* 2025-11-24

  ### Usage and credits fixes

  Minor updates to address a few issues with Codex usage and credits:

  + Adjusted all usage dashboards to show "limits remaining" for consistency. The CLI previously displayed "limits used."
  + Fixed an issue preventing users from buying credits if their ChatGPT subscription was purchased via iOS or Google Play.
  + Fixed an issue where the CLI could display stale usage information; it now refreshes without needing to send a message first.
  + Optimized the backend to help smooth out usage throughout the day, irrespective of overall Codex load or how traffic is routed. Before, users could get unlucky and hit a few cache misses in a row, leading to much less usage.
* 2025-11-21

  ### Codex CLI 0.63.0

  ```
  $ npm install -g @openai/codex@0.63.0
  ```

    View details    

  ## Bug fixes

  + Fixes the bug where enabling web search can lead to `Invalid value: 'other'.` errors.

  ## PRs Merged

  + [app-server] feat: add Declined status for command exec by [@owenlin0](https://github.com/owenlin0) in [#7101](https://github.com/openai/codex/pull/7101)
  + chore: drop model\_max\_output\_tokens by [@jif-oai](https://github.com/jif-oai) in [#7100](https://github.com/openai/codex/pull/7100)
  + fix: clear out duplicate entries for `bash` in the GitHub release by [@bolinfest](https://github.com/bolinfest) in [#7103](https://github.com/openai/codex/pull/7103)

  **Full Changelog**: [rust-v0.62.0...rust-v0.63.0](https://github.com/openai/codex/compare/rust-v0.62.0...rust-v0.63.0)

  [Full release on Github](https://github.com/openai/codex/releases/tag/rust-v0.63.0)
* 2025-11-20

  ### Codex CLI 0.61.0

  ```
  $ npm install -g @openai/codex@0.61.0
  ```

    View details    

  ### Highlights

  + ExecPolicy2 integration and exec-server prep: core now integrates ExecPolicy2 with exec-server refactors and cutover groundwork, plus quickstart docs to help teams adopt the new policy engine.
  + Improved truncation and error reporting: single-pass truncation reduces duplicate work, and error events can now carry optional status codes for clearer observability.
  + Shell reliability and sandbox warnings: fallback shell selection is hardened and world-writable directory warnings are less noisy, including improved messaging on Windows.
  + UX fixes: corrected reasoning display, preserved review footer context after `/review`, and the model migration screen now shows only once.

  ### PRs Merged

  + fix(app-server) move windows world writable warning ([#6916](https://github.com/openai/codex/pull/6916)) — [@dylan-hurd-oai](https://github.com/dylan-hurd-oai)
  + [core] add optional status\_code to error events ([#6865](https://github.com/openai/codex/pull/6865)) — [@celia-oai](https://github.com/celia-oai)
  + fix: prepare ExecPolicy in exec-server for execpolicy2 cutover ([#6888](https://github.com/openai/codex/pull/6888)) — [@bolinfest](https://github.com/bolinfest)
  + stop over-reporting world-writable directories ([#6936](https://github.com/openai/codex/pull/6936)) — [@iceweasel-oai](https://github.com/iceweasel-oai)
  + fix(context left after review): review footer context after `/review` ([#5610](https://github.com/openai/codex/pull/5610)) — [@guidedways](https://github.com/guidedways)
  + Fix/correct reasoning display ([#6749](https://github.com/openai/codex/pull/6749)) — [@lionelchg](https://github.com/lionelchg)
  + chore: refactor exec-server to prepare it for standalone MCP use ([#6944](https://github.com/openai/codex/pull/6944)) — [@bolinfest](https://github.com/bolinfest)
  + fix(shell) fallback shells ([#6948](https://github.com/openai/codex/pull/6948)) — [@dylan-hurd-oai](https://github.com/dylan-hurd-oai)
  + execpolicy2 core integration ([#6641](https://github.com/openai/codex/pull/6641)) — [@zhao-oai](https://github.com/zhao-oai)
  + Single pass truncation ([#6914](https://github.com/openai/codex/pull/6914)) — [@pakrym-oai](https://github.com/pakrym-oai)
  + update execpolicy quickstart readme ([#6952](https://github.com/openai/codex/pull/6952)) — [@zhao-oai](https://github.com/zhao-oai)
  + stop model migration screen after first time. ([#6954](https://github.com/openai/codex/pull/6954)) — [@aibrahim-oai](https://github.com/aibrahim-oai)

  [Full release on Github](https://github.com/openai/codex/releases/tag/rust-v0.61.0)
* 2025-11-19

  ### Codex CLI 0.60.1

  ```
  $ npm install -g @openai/codex@0.60.1
  ```

    View details    

  Bug fix release, most of the new important changes are in <https://github.com/openai/codex/releases/tag/rust-v0.59.0>

  ## Bug fix:

  + Default model for API users is now `gpt-5.1-codex`

  [Full release on Github](https://github.com/openai/codex/releases/tag/rust-v0.60.1)
* 2025-11-19

  ### Codex CLI 0.59.0

  ```
  $ npm install -g @openai/codex@0.59.0
  ```

    View details    

  ### Highlights

  + GPT-5.1-Codex-Max: introducing our newest frontier agentic coding model. GPT-5.1-Codex-Max delivers higher reliability, faster iteration, and support for long-running, project-scale workflows. Learn more at <https://www.openai.com/index/gpt-5-1-codex-max>
  + Native Compaction Support: added first-class support for Compaction, improving performance across extended coding sessions.
  + Expanded Tool Token Limits: codex models now support up to 10,000 tool output tokens. Configure this via `tool_output_token_limit` in `config.toml`.
  + Windows Agent mode: Introduced Agent mode for native Windows. Codex can read files, write files, and run commands in your working folder with fewer approvals. Agent mode uses a new experimental Windows sandbox to limit filesystem and network access. Learn more at <https://developers.openai.com/codex/windows>
  + TUI and UX Improvements
    - Eliminated ghost snapshot notifications when no `git` repository is present.
    - Codex Resume now displays branches and respects the current working directory for filtering.
    - Added placeholder icons for images.
    - Credits are now visible in `/status`.

  ### PRs Merged

  + fix: don't truncate at new lines ([#6907](https://github.com/openai/codex/pull/6907)) — [@aibrahim](https://github.com/aibrahim)
  + feat: arcticfox in the wild ([#6906](https://github.com/openai/codex/pull/6906)) — [@aibrahim](https://github.com/aibrahim)
  + [app-server] populate thread>turns>items on thread/resume ([#6848](https://github.com/openai/codex/pull/6848)) — [@owenlin0](https://github.com/owenlin0)
  + nit: useless log to debug ([#6898](https://github.com/openai/codex/pull/6898)) — [@jif](https://github.com/jif)
  + fix(core) Support changing /approvals before conversation ([#6836](https://github.com/openai/codex/pull/6836)) — @dylan.hurd
  + chore: consolidate compaction token usage ([#6894](https://github.com/openai/codex/pull/6894)) — [@jif](https://github.com/jif)
  + chore(app-server) world-writable windows notification ([#6880](https://github.com/openai/codex/pull/6880)) — @dylan.hurd
  + fix: parallel tool call instruction injection ([#6893](https://github.com/openai/codex/pull/6893)) — [@jif](https://github.com/jif)
  + nit: stable ([#6895](https://github.com/openai/codex/pull/6895)) — [@jif](https://github.com/jif)
  + feat: warning large commits ([#6838](https://github.com/openai/codex/pull/6838)) — [@jif](https://github.com/jif)
  + fix label ([#6892](https://github.com/openai/codex/pull/6892)) — [@tibo](https://github.com/tibo)
  + Move shell to use `truncate_text` ([#6842](https://github.com/openai/codex/pull/6842)) — [@aibrahim](https://github.com/aibrahim)
  + Run remote auto compaction ([#6879](https://github.com/openai/codex/pull/6879)) — [@pakrym](https://github.com/pakrym)
  + flaky-unified\_exec\_formats\_large\_output\_summary ([#6884](https://github.com/openai/codex/pull/6884)) — [@aibrahim](https://github.com/aibrahim)
  + shell\_command returns freeform output ([#6860](https://github.com/openai/codex/pull/6860)) — [@pakrym](https://github.com/pakrym)
  + chore(core) arcticfox ([#6876](https://github.com/openai/codex/pull/6876)) — @dylan.hurd
  + fix(tui) ghost snapshot notifications ([#6881](https://github.com/openai/codex/pull/6881)) — @dylan.hurd
  + fix: typos in model picker ([#6859](https://github.com/openai/codex/pull/6859)) — [@aibrahim](https://github.com/aibrahim)
  + chore: update windows docs url ([#6877](https://github.com/openai/codex/pull/6877)) — [@AE](https://github.com/AE)
  + feat: tweak windows sandbox strings ([#6875](https://github.com/openai/codex/pull/6875)) — [@AE](https://github.com/AE)
  + fix: add more fields to ThreadStartResponse and ThreadResumeResponse ([#6847](https://github.com/openai/codex/pull/6847)) — [@mbolin](https://github.com/mbolin)
  + chore: update windows sandbox docs ([#6872](https://github.com/openai/codex/pull/6872)) — [@AE](https://github.com/AE)
  + Remote compaction on by-default ([#6866](https://github.com/openai/codex/pull/6866)) — [@pakrym](https://github.com/pakrym)
  + [app-server] introduce `turn/completed` v2 event ([#6800](https://github.com/openai/codex/pull/6800)) — [@celia](https://github.com/celia)
  + update credit status details ([#6862](https://github.com/openai/codex/pull/6862)) — [@zhao](https://github.com/zhao)
  + tui: add branch to 'codex resume', filter by cwd ([#6232](https://github.com/openai/codex/pull/6232)) — @172423086+nornagon-openai
  + smoketest for browser vuln, rough draft of Windows security doc ([#6822](https://github.com/openai/codex/pull/6822)) — [@iceweasel](https://github.com/iceweasel)
  + windows sandbox: support multiple workspace roots ([#6854](https://github.com/openai/codex/pull/6854)) — [@iceweasel](https://github.com/iceweasel)
  + updating codex backend models ([#6855](https://github.com/openai/codex/pull/6855)) — [@zhao](https://github.com/zhao)
  + exec-server ([#6630](https://github.com/openai/codex/pull/6630)) — @172423086+nornagon-openai
  + Fix tests so they don't emit an extraneous `config.toml` in the source tree ([#6853](https://github.com/openai/codex/pull/6853)) — [@etraut](https://github.com/etraut)
  + [app-server-test-client] feat: auto approve command ([#6852](https://github.com/openai/codex/pull/6852)) — [@owenlin0](https://github.com/owenlin0)
  + Improved runtime of `generated_ts_has_no_optional_nullable_fields` test ([#6851](https://github.com/openai/codex/pull/6851)) — [@etraut](https://github.com/etraut)
  + fix: local compaction ([#6844](https://github.com/openai/codex/pull/6844)) — [@jif](https://github.com/jif)
  + Fix typo in config.md for MCP server ([#6845](https://github.com/openai/codex/pull/6845)) — @simcoea
  + [codex][otel] support mtls configuration ([#6228](https://github.com/openai/codex/pull/6228)) — [@apanasenko](https://github.com/apanasenko)
  + feat: review in app server ([#6613](https://github.com/openai/codex/pull/6613)) — [@jif](https://github.com/jif)
  + chore(config) enable shell\_command ([#6843](https://github.com/openai/codex/pull/6843)) — @dylan.hurd
  + Prompt to turn on windows sandbox when auto mode selected. ([#6618](https://github.com/openai/codex/pull/6618)) — [@iceweasel](https://github.com/iceweasel)
  + Add the utility to truncate by tokens ([#6746](https://github.com/openai/codex/pull/6746)) — [@aibrahim](https://github.com/aibrahim)
  + Update faq.md section on supported models ([#6832](https://github.com/openai/codex/pull/6832)) — [@adpena](https://github.com/adpena)
  + fixing localshell tool calls ([#6823](https://github.com/openai/codex/pull/6823)) — [@zhao](https://github.com/zhao)
  + feat: enable parallel tool calls ([#6796](https://github.com/openai/codex/pull/6796)) — [@jif](https://github.com/jif)
  + feat: remote compaction ([#6795](https://github.com/openai/codex/pull/6795)) — [@jif](https://github.com/jif)
  + nit: app server ([#6830](https://github.com/openai/codex/pull/6830)) — [@jif](https://github.com/jif)
  + nit: mark ghost commit as stable ([#6833](https://github.com/openai/codex/pull/6833)) — [@jif](https://github.com/jif)
  + feat: git branch tooling ([#6831](https://github.com/openai/codex/pull/6831)) — [@jif](https://github.com/jif)
  + 🐛 fix(rmcp-client): refresh OAuth tokens using expires\_at ([#6574](https://github.com/openai/codex/pull/6574)) — [@LaelLuo](https://github.com/LaelLuo)
  + fix(windows) shell\_command on windows, minor parsing ([#6811](https://github.com/openai/codex/pull/6811)) — @dylan.hurd
  + chore(core) Add shell\_serialization coverage ([#6810](https://github.com/openai/codex/pull/6810)) — @dylan.hurd
  + Update defaults to gpt-5.1 ([#6652](https://github.com/openai/codex/pull/6652)) — [@aibrahim](https://github.com/aibrahim)
  + Demote function call payload log to debug to avoid noisy error-level stderr ([#6808](https://github.com/openai/codex/pull/6808)) — [@Cassirer](https://github.com/Cassirer)
  + execpolicy2 extension ([#6627](https://github.com/openai/codex/pull/6627)) — [@zhao](https://github.com/zhao)
  + [app-server] feat: add v2 command execution approval flow ([#6758](https://github.com/openai/codex/pull/6758)) — [@owenlin0](https://github.com/owenlin0)
  + background rate limits fetch ([#6789](https://github.com/openai/codex/pull/6789)) — [@zhao](https://github.com/zhao)
  + move cap\_sid file into ~/.codex so the sandbox cannot overwrite it ([#6798](https://github.com/openai/codex/pull/6798)) — [@iceweasel](https://github.com/iceweasel)
  + Fix TUI issues with Alt-Gr on Windows ([#6799](https://github.com/openai/codex/pull/6799)) — [@etraut](https://github.com/etraut)
  + core: add a feature to disable the shell tool ([#6481](https://github.com/openai/codex/pull/6481)) — @172423086+nornagon-openai
  + chore(core) Update shell instructions ([#6679](https://github.com/openai/codex/pull/6679)) — @dylan.hurd
  + fix: annotate all app server v2 types with camelCase ([#6791](https://github.com/openai/codex/pull/6791)) — [@owenlin0](https://github.com/owenlin0)
  + LM Studio OSS Support ([#2312](https://github.com/openai/codex/pull/2312)) — [@Rugved](https://github.com/Rugved)
  + [app-server] add events to readme ([#6690](https://github.com/openai/codex/pull/6690)) — [@celia](https://github.com/celia)
  + core/tui: non-blocking MCP startup ([#6334](https://github.com/openai/codex/pull/6334)) — @172423086+nornagon-openai
  + chore: delete chatwidget::tests::binary\_size\_transcript\_snapshot tui test ([#6759](https://github.com/openai/codex/pull/6759)) — [@owenlin0](https://github.com/owenlin0)
  + feat: execpolicy v2 ([#6467](https://github.com/openai/codex/pull/6467)) — [@zhao](https://github.com/zhao)
  + nit: personal git ignore ([#6787](https://github.com/openai/codex/pull/6787)) — [@jif](https://github.com/jif)
  + tmp: drop sccache for windows 2 ([#6775](https://github.com/openai/codex/pull/6775)) — [@jif](https://github.com/jif)
  + feat: placeholder for image that can't be decoded to prevent 400 ([#6773](https://github.com/openai/codex/pull/6773)) — [@jif](https://github.com/jif)
  + fix(core) serialize shell\_command ([#6744](https://github.com/openai/codex/pull/6744)) — @dylan.hurd
  + Fix FreeBSD/OpenBSD builds: target-specific keyring features and BSD hardening ([#6680](https://github.com/openai/codex/pull/6680)) — [@jinxiaoyong](https://github.com/jinxiaoyong)
  + Exempt the "codex" github user from signing the CLA ([#6724](https://github.com/openai/codex/pull/6724)) — [@etraut](https://github.com/etraut)
  + chore(deps): bump actions/github-script from 7 to 8 ([#6755](https://github.com/openai/codex/pull/6755)) — @49699333+dependabot[bot]
  + Fix: Claude models return incomplete responses due to empty finish\_reason handling ([#6728](https://github.com/openai/codex/pull/6728)) — [@dulikaifazr](https://github.com/dulikaifazr)
  + Fix AltGr/backslash input on Windows Codex terminal ([#6720](https://github.com/openai/codex/pull/6720)) — @pornotato
  + Revert "tmp: drop sccache for windows ([#6673](https://github.com/openai/codex/pull/6673))" ([#6751](https://github.com/openai/codex/pull/6751)) — [@etraut](https://github.com/etraut)
  + fix: resolve Windows MCP server execution for script-based tools ([#3828](https://github.com/openai/codex/pull/3828)) — @jlee14281
  + Fix documentation errors for Custom Prompts named arguments and add canonical examples ([#5910](https://github.com/openai/codex/pull/5910)) — @169171880+Sayeem3051
  + Tighten panic on double truncation ([#6701](https://github.com/openai/codex/pull/6701)) — [@aibrahim](https://github.com/aibrahim)
  + Improve compact ([#6692](https://github.com/openai/codex/pull/6692)) — [@aibrahim](https://github.com/aibrahim)
  + Refactor truncation helpers into its own file ([#6683](https://github.com/openai/codex/pull/6683)) — [@aibrahim](https://github.com/aibrahim)
  + Revert "templates and build step for validating/submitting winget package" ([#6696](https://github.com/openai/codex/pull/6696)) — [@aibrahim](https://github.com/aibrahim)
  + ci: only run CLA assistant for openai org repos ([#6687](https://github.com/openai/codex/pull/6687)) — [@joshka](https://github.com/joshka)
  + Handle "Don't Trust" directory selection in onboarding ([#4941](https://github.com/openai/codex/pull/4941)) — @viniciusmotta8
  + Ignore unified\_exec\_respects\_workdir\_override ([#6693](https://github.com/openai/codex/pull/6693)) — [@pakrym](https://github.com/pakrym)
  + Order outputs before inputs ([#6691](https://github.com/openai/codex/pull/6691)) — [@pakrym](https://github.com/pakrym)
  + feat: add app-server-test-client crate for internal use ([#5391](https://github.com/openai/codex/pull/5391)) — [@owenlin0](https://github.com/owenlin0)
  + fix codex detection, add new security-focused smoketests. ([#6682](https://github.com/openai/codex/pull/6682)) — [@iceweasel](https://github.com/iceweasel)
  + feat(ts-sdk): allow overriding CLI environment ([#6648](https://github.com/openai/codex/pull/6648)) — [@lopopolo](https://github.com/lopopolo)
  + templates and build step for validating/submitting winget package ([#6485](https://github.com/openai/codex/pull/6485)) — [@iceweasel](https://github.com/iceweasel)
  + Add test timeout ([#6612](https://github.com/openai/codex/pull/6612)) — [@pakrym](https://github.com/pakrym)
  + Enable TUI notifications by default ([#6633](https://github.com/openai/codex/pull/6633)) — @172423086+nornagon-openai
  + tmp: drop sccache for windows ([#6673](https://github.com/openai/codex/pull/6673)) — [@jif](https://github.com/jif)
  + [App server] add mcp tool call item started/completed events ([#6642](https://github.com/openai/codex/pull/6642)) — [@celia](https://github.com/celia)
  + feat: cache tokenizer ([#6609](https://github.com/openai/codex/pull/6609)) — [@jif](https://github.com/jif)
  + feat: better UI for unified\_exec ([#6515](https://github.com/openai/codex/pull/6515)) — [@jif](https://github.com/jif)
  + feat: add resume logs when doing /new ([#6660](https://github.com/openai/codex/pull/6660)) — [@jif](https://github.com/jif)
  + tests: replace mount\_sse\_once\_match with mount\_sse\_once for SSE mocking ([#6640](https://github.com/openai/codex/pull/6640)) — [@pakrym](https://github.com/pakrym)
  + Promote shared helpers for suite tests ([#6460](https://github.com/openai/codex/pull/6460)) — [@aibrahim](https://github.com/aibrahim)
  + Use shared network gating helper in chat completion tests ([#6461](https://github.com/openai/codex/pull/6461)) — [@aibrahim](https://github.com/aibrahim)
  + Avoid double truncation ([#6631](https://github.com/openai/codex/pull/6631)) — [@aibrahim](https://github.com/aibrahim)
  + Revert "Revert "Overhaul shell detection and centralize command generation for unified exec"" ([#6607](https://github.com/openai/codex/pull/6607)) — [@pakrym](https://github.com/pakrym)
  + [app-server] small fixes for JSON schema export and one-of types ([#6614](https://github.com/openai/codex/pull/6614)) — [@owenlin0](https://github.com/owenlin0)
  + [App-server] add new v2 events:`item/reasoning/delta`, `item/agentMessage/delta` & `item/reasoning/summaryPartAdded` ([#6559](https://github.com/openai/codex/pull/6559)) — [@celia](https://github.com/celia)
  + chore(core) Consolidate apply\_patch tests ([#6545](https://github.com/openai/codex/pull/6545)) — @dylan.hurd
  + Only list failed tests ([#6619](https://github.com/openai/codex/pull/6619)) — [@pakrym](https://github.com/pakrym)
  + feat: Add support for --add-dir to exec and TypeScript SDK ([#6565](https://github.com/openai/codex/pull/6565)) — @33551757+danfhernandez
  + Add AbortSignal support to TypeScript SDK ([#6378](https://github.com/openai/codex/pull/6378)) — @33551757+danfhernandez
  + Enable close-stale-contributor-prs.yml workflow ([#6615](https://github.com/openai/codex/pull/6615)) — [@pakrym](https://github.com/pakrym)
  + Update default yield time ([#6610](https://github.com/openai/codex/pull/6610)) — [@pakrym](https://github.com/pakrym)
  + Close stale PRs workflow ([#6594](https://github.com/openai/codex/pull/6594)) — [@pakrym](https://github.com/pakrym)
  + Migrate prompt caching tests to test\_codex ([#6605](https://github.com/openai/codex/pull/6605)) — [@pakrym](https://github.com/pakrym)
  + Revert "Overhaul shell detection and centralize command generation for unified exec" ([#6606](https://github.com/openai/codex/pull/6606)) — [@pakrym](https://github.com/pakrym)
  + Overhaul shell detection and centralize command generation for unified exec ([#6577](https://github.com/openai/codex/pull/6577)) — [@pakrym](https://github.com/pakrym)

  [Full release on Github](https://github.com/openai/codex/releases/tag/rust-v0.59.0)
* 2025-11-18

  ### Introducing GPT-5.1-Codex-Max

  [Today we are releasing GPT-5.1-Codex-Max](http://www.openai.com/index/gpt-5-1-codex-max), our new frontier agentic coding model.

  GPT‑5.1-Codex-Max is built on an update to our foundational reasoning model, which is trained on agentic tasks across software engineering, math, research, and more. GPT‑5.1-Codex-Max is faster, more intelligent, and more token-efficient at every stage of the development cycle–and a new step towards becoming a reliable coding partner.

  Starting today, the CLI and IDE Extension will default to `gpt-5.1-codex-max` for users that are signed in with ChatGPT. API access for the model will come soon.

  For non-latency-sensitive tasks, we've also added a new Extra High (`xhigh`) reasoning effort, which lets the model think for an even longer period of time for a better answer. We still recommend medium as your daily driver for most tasks.

  If you have a model specified in your [`config.toml` configuration file](/codex/local-config), you can instead try out `gpt-5.1-codex-max` for a new Codex CLI session using:

  ```
  codex --model gpt-5.1-codex-max
  ```

  You can also use the `/model` slash command in the CLI. In the Codex IDE Extension you can select GPT-5.1-Codex from the dropdown menu.

  If you want to switch for all sessions, you can change your default model to `gpt-5.1-codex-max` by updating your `config.toml` [configuration file](/codex/local-config):

  ```
  model = "gpt-5.1-codex-max"
  ```
* 2025-11-13

  ### Introducing GPT-5.1-Codex and GPT-5.1-Codex-Mini

  Along with the [GPT-5.1 launch in the API](https://openai.com/index/gpt-5-1-for-developers/), we are introducing new `gpt-5.1-codex-mini` and `gpt-5.1-codex` model options in Codex, a version of GPT-5.1 optimized for long-running, agentic coding tasks and use in coding agent harnesses in Codex or Codex-like harnesses.

  Starting today, the CLI and IDE Extension will default to `gpt-5.1-codex` on macOS and Linux and `gpt-5.1` on Windows.

  If you have a model specified in your [`config.toml` configuration file](/codex/local-config), you can instead try out `gpt-5.1-codex` for a new Codex CLI session using:

  ```
  codex --model gpt-5.1-codex
  ```

  You can also use the `/model` slash command in the CLI. In the Codex IDE Extension you can select GPT-5.1-Codex from the dropdown menu.

  If you want to switch for all sessions, you can change your default model to `gpt-5.1-codex` by updating your `config.toml` [configuration file](/codex/local-config):

  ```
  model = "gpt-5.1-codex"
  ```
* 2025-11-13

  ### Codex CLI 0.58.0

  ```
  $ npm install -g @openai/codex@0.58.0
  ```

    View details    

  ### Highlights

  + Support for gpt5.1 models family. [Read more](/openai/codex/blob/rust-v0.58.0/www.openai.com/index/gpt-5-1)
  + App server enhancements: new JSON schema generator command, item started/completed events, macro cleanup, reduced boilerplate, and tightened duplicate-code hygiene ([#6406](https://github.com/openai/codex/pull/6406) [#6517](https://github.com/openai/codex/pull/6517) [#6470](https://github.com/openai/codex/pull/6470) [#6488](https://github.com/openai/codex/pull/6488)).
  + Quality of life fixes: doc updates (web\_search, SDK, config), TUI shortcuts inline, seatbelt/Wayland/brew/compaction/cloud-tasks bugfixes, clearer warnings, auth-aware status output, and OTEL test stabilization ([#5889](https://github.com/openai/codex/pull/5889) [#6424](https://github.com/openai/codex/pull/6424) [#6425](https://github.com/openai/codex/pull/6425) [#6376](https://github.com/openai/codex/pull/6376) [#6421](https://github.com/openai/codex/pull/6421) [#4824](https://github.com/openai/codex/pull/4824) [#6238](https://github.com/openai/codex/pull/6238) [#5856](https://github.com/openai/codex/pull/5856) [#6446](https://github.com/openai/codex/pull/6446) [#6529](https://github.com/openai/codex/pull/6529) [#6541](https://github.com/openai/codex/pull/6541)).

  ### PRs Merged

  + [#6381](https://github.com/openai/codex/pull/6381) — Improve world-writable scan (`917f39ec1`)
  + [#5889](https://github.com/openai/codex/pull/5889) — feat(tui): Display keyboard shortcuts inline for approval options (`5beb6167c`)
  + [#6389](https://github.com/openai/codex/pull/6389) — more world-writable warning improvements (`a47181e47`)
  + [#6425](https://github.com/openai/codex/pull/6425) — Fix SDK documentation: replace "file diffs" with "file change notifications" (`8b80a0a26`)
  + [#6421](https://github.com/openai/codex/pull/6421) — fix(seatbelt): Allow reading hw.physicalcpu (`c07461e6f`)
  + [#5856](https://github.com/openai/codex/pull/5856) — fix(cloud-tasks): respect `cli_auth_credentials_store` config (`5f1fab0e7`)
  + [#6387](https://github.com/openai/codex/pull/6387) — For npm upgrade on Windows, go through cmd.exe to get path traversal working (`625f2208c`)
  + [#6437](https://github.com/openai/codex/pull/6437) — chore(deps): bump codespell-project/actions-codespell from 2.1 to 2.2 (`7c7c7567d`)
  + [#6438](https://github.com/openai/codex/pull/6438) — chore(deps): bump taiki-e/install-action from 2.60.0 to 2.62.49 (`082d2fa19`)
  + [#6443](https://github.com/openai/codex/pull/6443) — chore(deps): bump askama from 0.12.1 to 0.14.0 in /codex-rs (`78b2aeea5`)
  + [#6444](https://github.com/openai/codex/pull/6444) — chore(deps): bump zeroize from 1.8.1 to 1.8.2 in /codex-rs (`e2598f509`)
  + [#6446](https://github.com/openai/codex/pull/6446) — Fix warning message phrasing (`131c38436`)
  + [#6424](https://github.com/openai/codex/pull/6424) — Fix config documentation: correct TOML parsing description (`557ac6309`)
  + [#6454](https://github.com/openai/codex/pull/6454) — Move compact (`50a77dc13`)
  + [#6376](https://github.com/openai/codex/pull/6376) — Updated docs to reflect recent changes in `web_search` configuration (`65cb1a1b7`)
  + [#6407](https://github.com/openai/codex/pull/6407) — fix: use generate\_ts from app\_server\_protocol (`42683dadf`)
  + [#6419](https://github.com/openai/codex/pull/6419) — Support exiting from the login menu (`b46012e48`)
  + [#6422](https://github.com/openai/codex/pull/6422) — Don't lock PRs that have been closed without merging (`591615315`)
  + [#6406](https://github.com/openai/codex/pull/6406) — [app-server] feat: add command to generate json schema (`fbdedd9a0`)
  + [#6238](https://github.com/openai/codex/pull/6238) — fix: update brew auto update version check (`788badd22`)
  + [#6433](https://github.com/openai/codex/pull/6433) — Add opt-out for rate limit model nudge (`e743d251a`)
  + [#6246](https://github.com/openai/codex/pull/6246) — Add user command event types (`980886498`)
  + [#6466](https://github.com/openai/codex/pull/6466) — feat: add workdir to unified\_exec (`f01f2ec9e`)
  + [#6468](https://github.com/openai/codex/pull/6468) — [app-server] chore: move initialize out of deprecated API section (`2ac49fea5`)
  + [#4824](https://github.com/openai/codex/pull/4824) — Fix wayland image paste error (`52e97b9b6`)
  + [#4098](https://github.com/openai/codex/pull/4098) — add codex debug seatbelt --log-denials (`0271c20d8`)
  + [#6477](https://github.com/openai/codex/pull/6477) — refactor(tui): job-control for Ctrl-Z handling (`60deb6773`)
  + [#6470](https://github.com/openai/codex/pull/6470) — [app-server] update macro to make renaming methods less boilerplate-y (`3838d6739`)
  + [#6478](https://github.com/openai/codex/pull/6478) — upload Windows .exe file artifacts for CLI releases (`9aff64e01`)
  + [#6482](https://github.com/openai/codex/pull/6482) — flip rate limit status bar (`930f81a17`)
  + [#6480](https://github.com/openai/codex/pull/6480) — Use codex-linux-sandbox in unified exec (`6c36318bd`)
  + [#6489](https://github.com/openai/codex/pull/6489) — Colocate more of bash parsing (`bb7b0213a`)
  + [#6488](https://github.com/openai/codex/pull/6488) — [hygiene][app-server] have a helper function for duplicate code in turn APIs (`695187277`)
  + [#6041](https://github.com/openai/codex/pull/6041) — Enable ghost\_commit feature by default (`052b05283`)
  + [#6503](https://github.com/openai/codex/pull/6503) — nit: logs to trace (`ad279eacd`)
  + [#6492](https://github.com/openai/codex/pull/6492) — Add unified exec escalation handling and tests (`807e2c27f`)
  + [#6517](https://github.com/openai/codex/pull/6517) — [app-server] add item started/completed events for turn items (`e357fc723`)
  + [#6523](https://github.com/openai/codex/pull/6523) — Update full-auto description with on-request (`eb1c651c0`)
  + [#6528](https://github.com/openai/codex/pull/6528) — Re-add prettier log-level=warn to generate-ts (`424bfecd0`)
  + [#6507](https://github.com/openai/codex/pull/6507) — feat: warning switch model on resume (`530db0ad7`)
  + [#6510](https://github.com/openai/codex/pull/6510) — feat: shell\_command tool (`29364f3a9`)
  + [#6516](https://github.com/openai/codex/pull/6516) — chore: verify boolean values can be parsed as config overrides (`c3a710ee1`)
  + [#6541](https://github.com/openai/codex/pull/6541) — Fix otel tests (`7d9ad3eff`)
  + [#6534](https://github.com/openai/codex/pull/6534) — feat: only wait for mutating tools for ghost commit (`e00eb50db`)
  + [#6529](https://github.com/openai/codex/pull/6529) — Fixed status output to use auth information from AuthManager (`ad09c138b`)
  + [#6551](https://github.com/openai/codex/pull/6551) — Add gpt-5.1 model definitions (`ec69a4a81`)
  + [#6558](https://github.com/openai/codex/pull/6558) — Do not double encode request bodies in logging (`2f58e6999`)
  + [#6483](https://github.com/openai/codex/pull/6483) — [app-server] feat: thread/resume supports history, path, and overrides (`964220ac9`)
  + [#6561](https://github.com/openai/codex/pull/6561) — NUX for gpt5.1 (`e63ab0dd6`)
  + [#6568](https://github.com/openai/codex/pull/6568) — Set verbosity to low for 5.1 (`f97874093`)
  + [#6567](https://github.com/openai/codex/pull/6567) — Update subtitle of model picker as part of the nux (`966d71c02`)
  + [#6569](https://github.com/openai/codex/pull/6569) — Change model picker to include gpt5.1 (`ad7eaa80f`)
  + [#6575](https://github.com/openai/codex/pull/6575) — Avoid hang when tool's process spawns grandchild that shares stderr/stdout (`73ed30d7e`)
  + [#6580](https://github.com/openai/codex/pull/6580) — remove porcupine model slug (`b1979b70a`)
  + [#6583](https://github.com/openai/codex/pull/6583) — feat: show gpt mini (`e3aaee00c`)
  + [#6585](https://github.com/openai/codex/pull/6585) — copy for model migration nudge (`305fe73d8`)
  + [#6586](https://github.com/openai/codex/pull/6586) — Reasoning level update (`e3dd362c9`)
  + [#6593](https://github.com/openai/codex/pull/6593) — Default to explicit medium reasoning for 5.1 (`34621166d`)
  + [#6588](https://github.com/openai/codex/pull/6588) — chore(core) Update prompt for gpt-5.1 (`8dcbd29ed`)
  + [#6597](https://github.com/openai/codex/pull/6597) — feat: proxy context left after compaction (`2a417c47a`)
  + [#6589](https://github.com/openai/codex/pull/6589) — fix model picker wrapping (`ba74cee6f`)

  [Full release on Github](https://github.com/openai/codex/releases/tag/rust-v0.58.0)
* 2025-11-09

  ### Codex CLI 0.57.0

  ```
  $ npm install -g @openai/codex@0.57.0
  ```

    View details    

  ### Highlights

  + TUI quality-of-life: ctrl-n/p navigation for slash command lists and backtracking skips the /status noise.
  + Improve timeout on long running commasnds

  ### PRs Merged

  + [#6233](https://github.com/openai/codex/pull/6233) – Freeform unified exec output formatting
  + [#6342](https://github.com/openai/codex/pull/6342) – Make `generate_ts` prettier output warn-only
  + [#6335](https://github.com/openai/codex/pull/6335) – TUI: fix backtracking past `/status`
  + [#1994](https://github.com/openai/codex/pull/1994) – Enable CTRL-n/CTRL-p for navigating slash commands, files, history
  + [#6340](https://github.com/openai/codex/pull/6340) – Skip retries on `insufficient_quota` errors
  + [#6345](https://github.com/openai/codex/pull/6345) – Remove shell tool when unified exec is enabled
  + [#6347](https://github.com/openai/codex/pull/6347) – Refresh AI labeler rules to match issue tracker labels
  + [#6346](https://github.com/openai/codex/pull/6346) – Prefer `wait_for_event` over `wait_for_event_with_timeout` (initial update)
  + [#5486](https://github.com/openai/codex/pull/5486) – Fix `apply_patch` rename/move path resolution
  + [#6349](https://github.com/openai/codex/pull/6349) – Prefer `wait_for_event` over `wait_for_event_with_timeout` (follow-up)
  + [#6336](https://github.com/openai/codex/pull/6336) – App-server: implement `account/read` endpoint
  + [#6338](https://github.com/openai/codex/pull/6338) – App-server: expose additional fields on `Thread`
  + [#6353](https://github.com/openai/codex/pull/6353) – App-server: add auth v2 doc & update Codex MCP interface section
  + [#6368](https://github.com/openai/codex/pull/6368) – App-server: README updates for threads and turns
  + [#6351](https://github.com/openai/codex/pull/6351) – Promote shell config tool to model family config
  + [#6369](https://github.com/openai/codex/pull/6369) – TUI: add inline comments to `tui.rs`
  + [#6370](https://github.com/openai/codex/pull/6370) – Add `--promote-alpha` option to `create_github_release` script
  + [#6367](https://github.com/openai/codex/pull/6367) – SDK: add `network_access` and `web_search` options to TypeScript SDK
  + [#6097](https://github.com/openai/codex/pull/6097) (includes work from [#6086](https://github.com/openai/codex/issues/6086)) – WSL: normalize Windows paths during update
  + [#6377](https://github.com/openai/codex/pull/6377) – App-server docs: add initialization section
  + [#6373](https://github.com/openai/codex/pull/6373) – Terminal refactor: remove deprecated flush logic
  + [#6252](https://github.com/openai/codex/pull/6252) – Core: replace Cloudflare 403 HTML with friendly message
  + [#6380](https://github.com/openai/codex/pull/6380) – Unified exec: allow safe commands without approval
  + [#5258](https://github.com/openai/codex/pull/5258) – Kill shell tool process groups on timeout

  [Full release on Github](https://github.com/openai/codex/releases/tag/rust-v0.57.0)
* 2025-11-07

  ### Introducing GPT-5-Codex-Mini

  Today we are introducing a new `gpt-5-codex-mini` model option to Codex CLI and the IDE Extension. The model is a smaller, more cost-effective, but less capable version of `gpt-5-codex` that provides approximately 4x more usage as part of your ChatGPT subscription.

  Starting today, the CLI and IDE Extension will automatically suggest switching to `gpt-5-codex-mini` when you reach 90% of your 5-hour usage limit, to help you work longer without interruptions.

  You can try the model for a new Codex CLI session using:

  ```
  codex --model gpt-5-codex-mini
  ```

  You can also use the `/model` slash command in the CLI. In the Codex IDE Extension you can select GPT-5-Codex-Mini from the dropdown menu.

  Alternatively, you can change your default model to `gpt-5-codex-mini` by updating your `config.toml` [configuration file](/codex/local-config):

  ```
  model = "gpt-5-codex-mini"
  ```
* 2025-11-07

  ### Codex CLI 0.56.0

  ```
  $ npm install -g @openai/codex@0.56.0
  ```

    View details    

  ### Highlights

  + Introducing our new model GPT-5-Codex-Mini — a more compact and cost-efficient version of GPT-5-Codex

  ### PRs merged

  + [#6211](https://github.com/openai/codex/pull/6211) fix: Update the deprecation message to link to the docs
  + [#6212](https://github.com/openai/codex/pull/6212) [app-server] feat: export.rs supports a v2 namespace, initial v2  
    notifications
  + [#6230](https://github.com/openai/codex/pull/6230) Fix nix build
  + [#3643](https://github.com/openai/codex/pull/3643) fix(core): load custom prompts from symlinked Markdown files
  + [#4200](https://github.com/openai/codex/pull/4200) allow codex to be run from pid 1
  + [#6234](https://github.com/openai/codex/pull/6234) Upgrade rmcp to 0.8.4
  + [#6237](https://github.com/openai/codex/pull/6237) Add modelReasoningEffort option to TypeScript SDK
  + [#5565](https://github.com/openai/codex/pull/5565) tui: refactor ChatWidget and BottomPane to use Renderables
  + [#6229](https://github.com/openai/codex/pull/6229) refactor Conversation history file into its own directory
  + [#6231](https://github.com/openai/codex/pull/6231) Improved token refresh handling to address "Re-connecting" behavior
  + [#6261](https://github.com/openai/codex/pull/6261) Update rmcp to 0.8.5
  + [#6214](https://github.com/openai/codex/pull/6214) [app-server] feat: v2 Thread APIs
  + [#6282](https://github.com/openai/codex/pull/6282) Fixes intermittent test failures in CI
  + [#6249](https://github.com/openai/codex/pull/6249) stop capturing r when environment selection modal is open
  + [#6183](https://github.com/openai/codex/pull/6183) [App-server] Implement v2 for account/login/start and account/login/completed
  + [#6285](https://github.com/openai/codex/pull/6285) Prevent dismissal of login menu in TUI
  + [#4388](https://github.com/openai/codex/pull/4388) fix: ToC so it doesn't include itself or duplicate the end marker
  + [#6288](https://github.com/openai/codex/pull/6288) [App-server] Add account/login/cancel v2 endpoint
  + [#6286](https://github.com/openai/codex/pull/6286) feat: add model nudge for queries
  + [#6300](https://github.com/openai/codex/pull/6300) feat: support models with single reasoning effort
  + [#6319](https://github.com/openai/codex/pull/6319) chore: rename for clarity
  + [#6216](https://github.com/openai/codex/pull/6216) [app-server] feat: v2 Turn APIs
  + [#6295](https://github.com/openai/codex/pull/6295) docs: Fix code fence and typo in advanced guide
  + [#6326](https://github.com/openai/codex/pull/6326) chore: fix grammar mistakes
  + [#6283](https://github.com/openai/codex/pull/6283) Windows Sandbox: Show Everyone-writable directory warning
  + [#6289](https://github.com/openai/codex/pull/6289) chore: move relevant tests to app-server/tests/suite/v2
  + [#6333](https://github.com/openai/codex/pull/6333) feat: clarify that gpt-5-codex should not amend commits unless requested
  + [#6332](https://github.com/openai/codex/pull/6332) Updated contributing guidelines and PR template to request link to bug report  
    in PR notes
  + [#5980](https://github.com/openai/codex/pull/5980) core: widen sandbox to allow certificate ops when network is enabled
  + [#6337](https://github.com/openai/codex/pull/6337) [App Server] Add more session metadata to listConversations

  [Full release on Github](https://github.com/openai/codex/releases/tag/rust-v0.56.0)
* 2025-11-06

  ### GPT-5-Codex model update

  We've shipped a minor update to GPT-5-Codex:

  + More reliable file edits with `apply_patch`.
  + Fewer destructive actions such as `git reset`.
  + More collaborative behavior when encountering user edits in files.
  + 3% more efficient in time and usage.

## October 2025

* 2025-10-30

  ### Credits on ChatGPT Pro and Plus

  Codex users on ChatGPT Plus and Pro can now use on-demand credits for more Codex usage beyond what's included in your plan. [Learn more.](https://developers.openai.com/codex/pricing)
* 2025-10-22

  ### Tag @Codex on GitHub Issues and PRs

  You can now tag `@codex` on a teammate's pull request to ask clarifying questions, request a follow-up, or ask Codex to make changes. GitHub Issues now also support `@codex` mentions, so you can kick off tasks from any issue, without leaving your workflow.

  ![Codex responding to a GitHub pull request and issue after an @Codex mention.](/images/codex/integrations/github-example.png)
* 2025-10-06

  ### Codex is now GA

  Codex is now generally available with 3 new features — @Codex in Slack, Codex SDK, and new admin tools.

  #### @Codex in Slack

  ![](/images/codex/integrations/slack-example.png)

  You can now questions and assign tasks to Codex directly from Slack. See the [Slack guide](/codex/integrations/slack) to get started.

  #### Codex SDK

  Integrate the same agent that powers the Codex CLI inside your own tools and workflows with the Codex SDK in Typescript. With the new Codex GitHub Action, you can easily add Codex to CI/CD workflows. See the [Codex SDK guide](/codex/sdk) to get started.

  ```
  import { Codex } from "@openai/codex-sdk";

  const agent = new Codex();
  const thread = await agent.startThread();

  const result = await thread.run("Explore this repo");
  console.log(result);

  const result2 = await thread.run("Propose changes");
  console.log(result2);
  ```

  #### New admin controls and analytics

  ![](/images/codex/enterprise/analytics.png)

  ChatGPT workspace admins can now edit or delete Codex Cloud environments. With managed config files, they can set safe defaults for CLI and IDE usage and monitor how Codex uses commands locally. New analytics dashboards help you track Codex usage and code review feedback. Learn more in the [enterprise admin guide.](/codex/enterprise)

  #### Availability and pricing updates

  The Slack integration and Codex SDK are available to developers on ChatGPT Plus, Pro, Business, Edu, and Enterprise plans starting today, while the new admin features will be available to Business, Edu, and Enterprise.
  Beginning October 20, Codex Cloud tasks will count toward your Codex usage. Review the [Codex pricing guide](/codex/pricing) for plan-specific details.

## September 2025

* 2025-09-23

  ### GPT-5-Codex in the API

  GPT-5-Codex is now available in the Responses API, and you can also use it with your API Key in the Codex CLI.
  We plan on regularly updating this model snapshot.
  It is available at the same price as GPT-5. You can learn more about pricing and rate limits for this model on our [model page](http://platform.openai.com/docs/models/gpt-5-codex).
* 2025-09-15

  ### Introducing GPT-5-Codex

  #### New model: GPT-5-Codex

  ![codex-switch-model](https://cdn.openai.com/devhub/docs/codex-switch-model.png)

  GPT-5-Codex is a version of GPT-5 further optimized for agentic coding in Codex.
  It's available in the IDE extension and CLI when you sign in with your ChatGPT account.
  It also powers the cloud agent and Code Review in GitHub.

  To learn more about GPT-5-Codex and how it performs compared to GPT-5 on software engineering tasks, see our [announcement blog post](https://openai.com/index/introducing-upgrades-to-codex/).

  #### Image outputs

  ![codex-image-outputs](https://cdn.openai.com/devhub/docs/codex-image-output.png)

  When working in the cloud on front-end engineering tasks, GPT-5-Codex can now display screenshots of the UI in Codex web for you to review. With image output, you can iterate on the design without needing to check out the branch locally.

  #### New in Codex CLI

  + You can now resume sessions where you left off with `codex resume`.
  + Context compaction automatically summarizes the session as it approaches the context window limit.

  Learn more in the [latest release notes](https://github.com/openai/codex/releases/tag/rust-v0.36.0)

## August 2025

* 2025-08-27

  ### Late August update

  #### IDE extension (Compatible with VS Code, Cursor, Windsurf)

  ![](/images/codex/changelog/local_task.gif)

  Codex now runs in your IDE with an interactive UI for fast local iteration. Easily switch between modes and reasoning efforts.

  #### Sign in with ChatGPT (IDE & CLI)

  ![](/images/codex/changelog/sign-in-with-chat.gif)

  One-click authentication that removes API keys and uses ChatGPT Enterprise credits.

  #### Move work between local ↔ cloud

  ![](/images/codex/changelog/cloud_task.gif)

  Hand off tasks to Codex web from the IDE with the ability to apply changes locally so you can delegate jobs without leaving your editor.

  #### Code Reviews

  ![](/images/codex/changelog/codex_review.gif)

  Codex goes beyond static analysis. It checks a PR against its intent, reasons across the codebase and dependencies, and can run code to validate the behavior of changes.
* 2025-08-21

  ### Mid August update

  #### Image inputs

  ![](/images/codex/changelog/image_input.png)

  You can now attach images to your prompts in Codex web. This is great for asking Codex to implement frontend changes or follow up on whiteboarding sessions.

  #### Container caching

  ![](/images/codex/changelog/container_caching.png)

  Codex now caches containers to start new tasks and followups 90% faster, dropping the median start time from 48 seconds to 5 seconds. You can optionally configure a maintenance script to update the environment from its cached state to prepare for new tasks. See the docs for more.

  #### Automatic environment setup

  Now, environments without manual setup scripts automatically run the standard installation commands for common package managers like yarn, pnpm, npm, go mod, gradle, pip, poetry, uv, and cargo. This reduces test failures for new environments by 40%.

## June 2025

* 2025-06-13

  ### Best of N

  ![](/images/codex/changelog/best-of-n.png)

  Codex can now generate multiple responses simultaneously for a single task, helping you quickly explore possible solutions to pick the best approach.

  #### Fixes & improvements

  + Added some keyboard shortcuts and a page to explore them. Open it by pressing ⌘-/ on macOS and Ctrl+/ on other platforms.
  + Added a "branch" query parameter in addition to the existing "environment", "prompt" and "tab=archived" parameters.
  + Added a loading indicator when downloading a repo during container setup.
  + Added support for cancelling tasks.
  + Fixed issues causing tasks to fail during setup.
  + Fixed issues running followups in environments where the setup script changes files that are gitignored.
  + Improved how the agent understands and reacts to network access restrictions.
  + Increased the update rate of text describing what Codex is doing.
  + Increased the limit for setup script duration to 20 minutes for Pro and Business users.
  + Polished code diffs: You can now option-click a code diff header to expand/collapse all of them.
* 2025-06-03

  ### June update

  #### Agent internet access

  ![](/images/codex/changelog/internet_access.png)

  Now you can give Codex access to the internet during task execution to install dependencies, upgrade packages, run tests that need external resources, and more.

  Internet access is off by default. Plus, Pro, and Business users can enable it for specific environments, with granular control of which domains and HTTP methods Codex can access. Internet access for Enterprise users is coming soon.

  Learn more about usage and risks in the [docs](/codex/cloud/agent-internet).

  #### Update existing PRs

  ![](/images/codex/changelog/update_prs.png)

  Now you can update existing pull requests when following up on a task.

  #### Voice dictation

  ![](/images/codex/changelog/voice_dictation.gif)

  Now you can dictate tasks to Codex.

  #### Fixes & improvements

  + Added a link to this changelog from the profile menu.
  + Added support for binary files: When applying patches, all file operations are supported. When using PRs, only deleting or renaming binary files is supported for now.
  + Fixed an issue on iOS where follow up tasks where shown duplicated in the task list.
  + Fixed an issue on iOS where pull request statuses were out of date.
  + Fixed an issue with follow ups where the environments were incorrectly started with the state from the first turn, rather than the most recent state.
  + Fixed internationalization of task events and logs.
  + Improved error messages for setup scripts.
  + Increased the limit on task diffs from 1 MB to 5 MB.
  + Increased the limit for setup script duration from 5 to 10 minutes.
  + Polished GitHub connection flow.
  + Re-enabled Live Activities on iOS after resolving an issue with missed notifications.
  + Removed the mandatory two-factor authentication requirement for users using SSO or social logins.

## May 2025

* 2025-05-22

  ### Reworked environment page

  It's now easier and faster to set up code execution.

  ![](/images/codex/changelog/environment_setup.png)

  #### Fixes & improvements

  + Added a button to retry failed tasks
  + Added indicators to show that the agent runs without network access after setup
  + Added options to copy git patches after pushing a PR
  + Added support for unicode branch names
  + Fixed a bug where secrets were not piped to the setup script
  + Fixed creating branches when there's a branch name conflict.
  + Fixed rendering diffs with multi-character emojis.
  + Improved error messages when starting tasks, running setup scripts, pushing PRs, or disconnected from GitHub to be more specific and indicate how to resolve the error.
  + Improved onboarding for teams.
  + Polished how new tasks look while loading.
  + Polished the followup composer.
  + Reduced GitHub disconnects by 90%.
  + Reduced PR creation latency by 35%.
  + Reduced tool call latency by 50%.
  + Reduced task completion latency by 20%.
  + Started setting page titles to task names so Codex tabs are easier to tell apart.
  + Tweaked the system prompt so that agent knows it's working without network, and can suggest that the user set up dependencies.
  + Updated the docs.
* 2025-05-19

  ### Codex in the ChatGPT iOS app

  Start tasks, view diffs, and push PRs—while you're away from your desk.

  ![](/images/codex/changelog/mobile_support.png)
