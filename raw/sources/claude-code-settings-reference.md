<!--
source: https://code.claude.com/docs/en/settings-reference
type: blog
fetched: 2026-11-10
-->

# SettingsAll settings
 page pageComplete reference for every Claude Code settings.json key: where each one goes, its type and default, and a paste-ready example, with an index of every key.
##  page page
This reference page lists each key Claude Code reads from a settings file, plus the [short group of keys](#global-config-settings) it keeps in ~/.claude.json instead. To pick a file, or check precedence, start with [Settings files and precedence](/docs/en/settings).

[​](#settings-index)Settings index

| Key | Description | Topic | Scope |
| --- | --- | --- | --- |
| advisorModel | Pick which model answers when Claude asks the advisor tool | Model and responses | Any file |
| agent | Start every session as a named subagent with its prompt, tools, and model | Agents, sessions, and worktrees | Any file |
| agentPushNotifEnabled | Let Claude send a push notification to your phone when it decides to | Remote, desktop, and notifications | Any file |
| allowAllClaudeAiMcps | Load the claude.ai connectors Claude Code fetches itself alongside a deployed managed-mcp.json | MCP | Managed |
| allowClaudeInChromeWithManagedMcp | Let the built-in Claude in Chrome server run alongside a deployed managed-mcp.json | MCP | Managed |
| allowedChannelPlugins | Replace the default allowlist of channel plugins that can push messages | Plugins and skills | Managed |
| allowedHttpHookUrls | Limit which URLs HTTP hooks can target | Hooks and automation | Any file |
| allowedMcpServers | Allowlist which MCP servers users can add | MCP | Any file |
| allowedProviders | Limit which API providers a machine may use | Authentication and providers | Managed |
| allowManagedHooksOnly | Run only the hooks your organization deploys | Hooks and automation | Managed |
| allowManagedMcpServersOnly | Make the managed MCP allowlist the only one that applies | MCP | Managed |
| allowManagedPermissionRulesOnly | Make managed settings the only settings source of permission rules | Permission settings | Managed |
| alwaysThinkingEnabled | Turn extended thinking off for every session | Model and responses | Any file |
| apiKeyHelper | Generate the API credential with your own command | Authentication and providers | Any file |
| askUserQuestionTimeout | Let an unanswered question auto-continue after idle time | Interface and terminal | User or managed |
| appendPlugins | Run your organization’s mods after every mod a user installs | Plugins and skills | User or managed |
| attribution | Customize the attribution Claude Code adds to commits and pull requests | Git and attribution | Any file |
| attribution.commit | Change or hide the trailer Claude Code adds to commits | Git and attribution | Any file |
| attribution.pr | Change or hide the attribution line in pull request descriptions | Git and attribution | Any file |
| attribution.sessionUrl | Omit the claude.ai session link from cloud and Remote Control commits | Git and attribution | Any file |
| autoCompactEnabled | Turn automatic compaction off or on | Memory and context | Any file |
| autoCompactWindow | Set how full the context gets before Claude Code compacts | Memory and context | Any file |
| autoConnectIde | Connect to a running VS Code or JetBrains IDE automatically from an external terminal | Global config settings | Global config |
| autoContinueAtUsageLimit | Wait in the open session and continue the task automatically after a claude.ai usage limit resets | Interface and terminal | User or managed |
| autoInstallIdeExtension | Let /ide install the IDE extension from an external terminal | Global config settings | Global config |
| autoMemoryDirectory | Store auto memory in a directory you choose | Memory and context | Any file |
| autoMemoryEnabled | Turn auto memory off or on | Memory and context | Any file |
| autoMode | Add your own allow and deny rules to the auto mode classifier | Permission settings | User or managed |
| autoMode.classifyAllShell | Send every shell command through the auto mode classifier, even ones a narrow allow rule matches | Permission settings | User or managed |
| autoScrollEnabled | Follow new output to the bottom in fullscreen rendering | Interface and terminal | Any file |
| autoUpdatesChannel | Follow the stable release channel instead of latest | Updates and versioning | Any file |
| availableModels | Restrict which models people can pick | Model and responses | Any file |
| availableModelsMatch | Make each availableModels model ID entry permit only the version it names | Model and responses | Managed |
| awaySummaryEnabled | Turn off the session recap shown when you come back to the terminal | Remote, desktop, and notifications | Any file |
| awsAuthRefresh | Refresh expired Bedrock credentials in .aws with your own command | Authentication and providers | Any file |
| awsCredentialExport | Supply Bedrock credentials as JSON from your own command | Authentication and providers | Any file |
| axScreenReader | Render screen-reader friendly output | Interface and terminal | User or managed |
| bashEditDiffEnabled | Record the files that changed while a Bash command ran in every permission mode | Interface and terminal | User or managed |
| bashOutputMaxChars | Set how much of a successful command’s output Claude receives inline | Memory and context | Any file |
| blockedMarketplaces | Block plugin marketplace sources for your organization | Plugins and skills | Managed |
| browserExternalPageTools | Keep Claude’s tools off external pages in the desktop Browser pane | Tools | Managed |
| channelsEnabled | Allow channels for your organization | Plugins and skills | Managed |
| claudeInChromeDefaultEnabled | Turn on Chrome integration when a session starts, in the interactive CLI and the VS Code extension | Global config settings | Global config |
| claudeMd | Inject organization-wide CLAUDE.md instructions from managed settings | Memory and context | Managed |
| claudeMdExcludes | Skip specific CLAUDE.md files when memory loads | Memory and context | Any file |
| cleanupPeriodDays | Choose how many days Claude Code keeps transcripts before deleting them | Privacy and telemetry | Any file |
| companyAnnouncements | Show your organization’s announcements at startup | Interface and terminal | Any file |
| copyFullResponse | Make /copy copy the full response without showing the picker | Global config settings | Global config |
| copyOnSelect | Turn off automatic copying of text you select with the mouse in fullscreen rendering and agent view | Global config settings | Global config |
| crossSessionInbound | Choose whether Claude Code delivers messages from your other sessions, shows a notice without delivering them, or refuses them | Agents, sessions, and worktrees | Any file |
| defaultShell | Choose whether Bash or PowerShell runs the shell commands you type with the ! prefix | Interface and terminal | Any file |
| defaultToAgentsView | Open agent view instead of a new conversation when you run claude with no arguments | Global config settings | Global config |
| deniedMcpServers | Block specific MCP servers by URL, command, or name | MCP | Any file |
| deniedModels | Block specific models, even ones availableModels permits | Model and responses | Managed |
| desktopSessionCleanupPeriodDays | Set an age limit in days for Claude Desktop and Cowork transcripts | Privacy and telemetry | User or managed |
| dialogExpiry | Set how long Claude Code waits for Remote Control or an SDK host to answer a forwarded dialog before it cancels the dialog | Interface and terminal | User or managed |
| diffTool | Choose whether Claude’s proposed file changes open in the VS Code or JetBrains diff viewer or stay in the terminal | Global config settings | Global config |
| disableAgentView | Turn off background agents and agent view | Agents, sessions, and worktrees | Any file |
| disableAllHooks | Turn off hooks, a custom status line, and a custom @ file suggestion command at once | Hooks and automation | Any file |
| disableArtifact | Deprecated; use enableArtifact to turn the Artifact tool off | Remote, desktop, and notifications | Any file |
| disableAutoMode | Remove auto mode from the permission mode cycle | Permission settings | Any file |
| disableBrowserExternalNavigation | Limit the desktop Browser pane to localhost for people and Claude | Tools | Managed |
| disableBundledSkills | Turn off the skills and workflows included with Claude Code | Plugins and skills | Any file |
| disableClaudeAiConnectors | Turn off claude.ai connectors so Claude Code doesn’t fetch them | MCP | Any file |
| disableCommandPluginSources | Block plugins that install by running a marketplace-declared command | Plugins and skills | Managed |
| disableDeepLinkRegistration | Stop Claude Code from registering the claude-cli:// handler | Remote, desktop, and notifications | Any file |
| disableDesktopLocalSessions | Turn off Desktop Code sessions that run on the device, leaving SSH to other hosts and cloud | Remote, desktop, and notifications | Managed |
| disabledMcpjsonServers | Reject specific servers from a project’s .mcp.json | MCP | Any file |
| disableMobileSimulatorTools | Block Claude’s tools in the desktop iOS Simulator pane | Tools | Managed |
| disableRemoteControl | Turn off Remote Control everywhere it can start | Remote, desktop, and notifications | Any file |
| disableSideloadFlags | Reject the CLI flags that sideload plugins, subagents, and MCP servers | Enterprise and managed settings | Managed |
| disableSkillShellExecution | Stop skills and custom commands from running inline shell | Plugins and skills | Any file |
| disableWorkflows | Turn dynamic workflows off for everyone; use enableWorkflows for yourself | Hooks and automation | Any file |
| editorMode | Use vim key bindings in the input prompt | Interface and terminal | Any file |
| effortLevel | Set a default effort level for models without a saved level of their own | Model and responses | Any file |
| emojiCompletionEnabled | Turn off :shortcode: emoji suggestions and replacement in the prompt input | Interface and terminal | Any file |
| enableAllProjectMcpServers | Approve every server in project .mcp.json files without a prompt | MCP | Any file |
| enableArtifact | Turn the Artifact tool off with a false in any file; no file can turn it back on | Remote, desktop, and notifications | Any file |
| enabledMcpjsonServers | Approve specific servers from a project’s .mcp.json | MCP | Any file |
| enabledPlugins | Turn individual plugins on or off per scope | Plugins and skills | Any file |
| enableWorkflows | Turn dynamic workflows on or off against your plan’s default | Hooks and automation | Any file |
| enforceAvailableModels | Keep the /model Default choice inside your availableModels allowlist | Model and responses | Any file |
| env | Set environment variables for every session and its subprocesses | Memory and context | Any file |
| externalEditorContext | Show Claude’s last response as comments when you press Ctrl+G to edit | Global config settings | Global config |
| extraKnownMarketplaces | Register marketplaces for a repository or an organization | Plugins and skills | Any file |
| fallbackModel | Name backup models for when the primary is overloaded | Model and responses | Any file |
| fastMode | Turn fast mode on for sessions where it’s available | Model and responses | Any file |
| fastModePerSessionOptIn | Require people to turn fast mode on each session | Model and responses | Any file |
| feedbackDrafts | Control whether Claude queues feedback drafts for you to review | Privacy and telemetry | User or managed |
| feedbackSurveyRate | Change how often the session quality survey appears | Privacy and telemetry | Any file |
| fileCheckpointingEnabled | Turn off or on the file snapshots that /rewind restores | Memory and context | Any file |
| fileSuggestion | Supply @ file autocomplete from your own command | Interface and terminal | Any file |
| footerLinksRegexes | Make issue or review IDs in output into clickable links below the input box | Interface and terminal | User or managed |
| forceLoginGatewayUrl | Set the gateway URL the login screen connects to | Authentication and providers | User or managed |
| forceLoginMethod | Restrict login to claude.ai, Claude Console, or a cloud gateway | Authentication and providers | Any file |
| forceLoginOrgUUID | Pin claude.ai logins to your organization; only managed settings enforce it | Authentication and providers | Any file |
| forceRemoteSettingsRefresh | Block startup until server-managed settings are freshly fetched | Enterprise and managed settings | Managed |
| gatewayInternalNetworks | Let /login reach a cloud gateway on public IPv4 space your organization uses internally | Authentication and providers | Managed |
| gcpAuthRefresh | Refresh Google Cloud credentials with your own command | Authentication and providers | Any file |
| hooks | Run your own commands as hooks at points in Claude Code’s lifecycle | Hooks and automation | Any file |
| httpHookAllowedEnvVars | Limit which env vars HTTP hooks can put in headers | Hooks and automation | Any file |
| idleCompaction | Stop Claude Code from compacting a long conversation that you’ve stepped away from | Memory and context | Any file |
| includeCoAuthoredBy | Deprecated; use attribution to hide or change commit and PR attribution | Git and attribution | Any file |
| includeGitInstructions | Remove the built-in commit and PR instructions from Claude’s context | Git and attribution | Any file |
| inputNeededNotifEnabled | Get a push notification when Claude is waiting on you | Remote, desktop, and notifications | Any file |
| isolatePeerMachines | Ask you before Claude messages one of your sessions on another machine | Agents, sessions, and worktrees | Any file |
| keybindingFlavor | Deprecated and has no effect; the word-editing shortcuts always follow readline conventions | Interface and terminal | Any file |
| language | Have Claude respond in a language other than English | Model and responses | Any file |
| leftArrowOpensAgents | Turn off the ← shortcut that backgrounds the session and opens agent view | Global config settings | Global config |
| managedMcpServers | Provide remote MCP servers to every user alongside the ones they add | MCP | Managed |
| managedSourcesBehavior | Compose every managed source you deploy instead of using the highest-priority one alone | Enterprise and managed settings | Managed |
| maxEffortLevel | Cap the effort level for every model or per model, on every provider | Model and responses | Any file |
| maxProseWidth | Cap how wide the prose in Claude’s responses runs in a wide terminal | Interface and terminal | Any file |
| minimumVersion | Keep auto-updates from installing anything below a version | Updates and versioning | Any file |
| model | Change the model Claude Code starts with | Model and responses | Any file |
| modelOverrides | Map model IDs to your provider’s IDs, such as Bedrock ARNs | Model and responses | Any file |
| modelPicker | Choose which models the /model picker lists, in your own order and with your own labels | Model and responses | User or managed |
| modelPricing | Report spend at your organization’s contracted rates instead of list price | Model and responses | Managed |
| modelSettings | Keep a saved effort level or auto-compact window per model, or cap one model’s effort | Model and responses | Any file |
| otelHeadersHelper | Generate rotating OpenTelemetry headers with your own command | Authentication and providers | Any file |
| outputStyle | Change Claude’s role, tone, and output format with an output style | Model and responses | Any file |
| parentSettingsBehavior | Apply or drop restrictions an SDK or IDE host passes when you deploy managed settings | Enterprise and managed settings | Managed |
| permissionExplainerEnabled | Removed in v2.1.257, together with the Ctrl+E command explanation on shell permission prompts | Global config settings | Global config |
| permissions | Set allow, ask, and deny rules and the default permission mode | Permission settings | Any file |
| permissions.additionalDirectories | Give Claude file access to directories outside the current one | Permission settings | Any file |
| permissions.allow | Approve listed tool uses without a prompt | Permission settings | Any file |
| permissions.ask | Always prompt before listed tool uses | Permission settings | Any file |
| permissions.blockReadsOutsideWorkingDirectories | Make the file tools refuse reads outside the working directories in every permission mode | Permission settings | Any file |
| permissions.blockWritesOutsideWorkingDirectories | Make the Write, Edit, and NotebookEdit tools refuse paths outside the working directories in every permission mode, apart from some of Claude Code’s own files | Permission settings | Any file |
| permissions.defaultMode | Set the default permission mode for new sessions | Permission settings | Any file |
| permissions.deny | Block listed tool uses, including reads of files that hold secrets | Permission settings | Any file |
| permissions.denyInsteadOfPrompting | Deny tool calls that would wait on a permission prompt, so a session nobody is watching keeps working | Permission settings | User or managed |
| permissions.disableBypassPermissionsMode | Prevent anyone from entering bypassPermissions mode | Permission settings | Any file |
| plansDirectory | Choose where plan mode writes plan files | Memory and context | Any file |
| pluginConfigs | Store the answers you gave a plugin’s configuration dialog | Plugins and skills | User or managed |
| pluginSuggestionMarketplaces | Choose which marketplaces can surface plugin install suggestions in /plugin | Plugins and skills | Managed |
| pluginTrustMessage | Add your own text to the plugin trust warning | Plugins and skills | Managed |
| policyHelper | Run an executable that computes managed settings at startup | Enterprise and managed settings | Managed |
| policyHelper.path | Name the helper executable Claude Code runs | Enterprise and managed settings | Managed |
| policyHelper.refreshIntervalMs | Re-run the helper in the background on an interval | Enterprise and managed settings | Managed |
| policyHelper.timeoutMs | Set how long Claude Code waits for the helper | Enterprise and managed settings | Managed |
| preferredNotifChannel | Choose a terminal bell or desktop notification for task completion | Remote, desktop, and notifications | Any file |
| prefersReducedMotion | Reduce or turn off spinner, shimmer, and flash animations | Interface and terminal | Any file |
| prependPlugins | Run your organization’s mods before every mod a user installs | Plugins and skills | User or managed |
| processWrapper | Run Claude Code’s background processes through a corporate launcher on macOS and Linux | Agents, sessions, and worktrees | User or managed |
| promptCacheTtl | Choose the prompt cache lifetime for the main conversation | Model and responses | Any file |
| promptSuggestionEnabled | Hide the grayed-out prompt suggestions in the input box | Interface and terminal | Any file |
| prStatusFooterEnabled | Turn off the prompt footer’s PR review status badge and the pull request check behind it | Global config settings | Global config |
| prUrlTemplate | Point PR links at an internal code-review tool instead of github.com | Git and attribution | Any file |
| remote.defaultEnvironmentId | Pick the default cloud environment for claude --cloud; a self-hosted ccpool_ ID is read only from user and managed settings and --settings | Remote, desktop, and notifications | Any file |
| remoteControlAtStartup | Connect Remote Control automatically when a session starts | Remote, desktop, and notifications | Any file |
| requiredMaximumVersion | Refuse to start on a version newer than your organization allows | Updates and versioning | Managed |
| requiredMinimumVersion | Refuse to start on a version older than your organization requires | Updates and versioning | Managed |
| respectGitignore | Keep gitignored files out of the @ file picker | Interface and terminal | Any file |
| respondToBashCommands | Stop Claude from responding after a ! shell command runs | Interface and terminal | Any file |
| sandbox | Isolate Bash commands from your filesystem and network on macOS, Linux, and WSL2 | Sandbox settings | Any file |
| sandbox.allowAppleEvents | Let sandboxed commands send Apple Events on macOS | Sandbox settings | User or managed |
| sandbox.allowNestedUserNamespaces | Let sandboxed commands create user namespaces on Linux and WSL2 | Sandbox settings | User or managed |
| sandbox.allowUnsandboxedCommands | Let Claude retry a blocked command outside the sandbox, or forbid it | Sandbox settings | Any file |
| sandbox.autoAllowBashIfSandboxed | Run sandboxed commands without a permission prompt | Sandbox settings | Any file |
| sandbox.bwrapPath | Point the sandbox at a bubblewrap binary outside PATH | Sandbox settings | Managed |
| sandbox.credentials | Hide or mask credential files and variables inside the sandbox | Sandbox settings | Any file |
| sandbox.credentials.allowPlaintextInject | Let masked credentials reach plain HTTP services on trusted test networks | Sandbox settings | User or managed |
| sandbox.credentials.awsPairs | Link custom-named AWS key variables into one credential for re-signing | Sandbox settings | User or managed |
| sandbox.credentials.envVars | Unset or mask an environment variable inside the sandbox | Sandbox settings | Any file |
| sandbox.credentials.files | Block or mask reads of a credential file inside the sandbox | Sandbox settings | Any file |
| sandbox.credentials.sigv4 | Choose whether streaming, presigned, or SigV4A AWS requests fail or pass through | Sandbox settings | User or managed |
| sandbox.enabled | Turn on Bash sandboxing on macOS, Linux, and WSL2 | Sandbox settings | Any file |
| sandbox.enableWeakerNestedSandbox | Run the Linux sandbox inside an unprivileged container | Sandbox settings | Any file |
| sandbox.enableWeakerNetworkIsolation | Let gh, gcloud, and terraform verify TLS behind a MITM proxy inside the sandbox on macOS | Sandbox settings | Any file |
| sandbox.excludedCommands | Name commands Claude Code can run outside the sandbox | Sandbox settings | Any file |
| sandbox.failIfUnavailable | Refuse to start when the sandbox can’t, instead of running unsandboxed | Sandbox settings | Any file |
| sandbox.filesystem | Control which paths sandboxed commands can read and write | Sandbox settings | Any file |
| sandbox.filesystem.allowManagedReadPathsOnly | Stop developers from re-opening read paths your organization blocked | Sandbox settings | Managed |
| sandbox.filesystem.allowRead | Re-open reading inside a region denyRead blocks | Sandbox settings | Any file |
| sandbox.filesystem.allowWrite | Add paths sandboxed commands can write to | Sandbox settings | Any file |
| sandbox.filesystem.denyRead | Block sandboxed commands from reading specific paths | Sandbox settings | Any file |
| sandbox.filesystem.denyWrite | Block sandboxed commands from writing to specific paths | Sandbox settings | Any file |
| sandbox.filesystem.disabled | Turn off filesystem isolation while keeping network isolation | Sandbox settings | User or managed |
| sandbox.ignoreViolations | Silence violation reports for paths a command is expected to probe | Sandbox settings | Any file |
| sandbox.network | Control which hosts, ports, and sockets sandboxed commands reach | Sandbox settings | Any file |
| sandbox.network.allowAllUnixSockets | Let sandboxed commands connect to every Unix socket | Sandbox settings | Any file |
| sandbox.network.allowedDomains | Pre-allow domains so sandboxed commands don’t prompt for them | Sandbox settings | Any file |
| sandbox.network.allowLocalBinding | Let sandboxed commands listen on network ports and connect to localhost on macOS | Sandbox settings | Any file |
| sandbox.network.allowMachLookup | Let macOS sandboxed tools like the iOS Simulator or Playwright reach their XPC services | Sandbox settings | Any file |
| sandbox.network.allowManagedDomainsOnly | Lock the network allowlist to managed settings | Sandbox settings | Managed |
| sandbox.network.allowUnixSockets | List Unix socket paths sandboxed commands can use on macOS | Sandbox settings | Any file |
| sandbox.network.deniedDomains | Block domains for sandboxed commands, even inside an allowed wildcard | Sandbox settings | Any file |
| sandbox.network.httpProxyPort | Route sandbox HTTP traffic through your own proxy | Sandbox settings | Any file |
| sandbox.network.socksProxyPort | Route sandbox SOCKS traffic through your own proxy | Sandbox settings | Any file |
| sandbox.network.strictAllowlist | Deny hosts outside the allowlist instead of prompting | Sandbox settings | User or managed |
| sandbox.network.tlsTerminate | Have the sandbox proxy terminate TLS so it can read HTTPS requests | Sandbox settings | User or managed |
| sandbox.ripgrep | Use your own ripgrep binary inside the sandbox | Sandbox settings | User or managed |
| sandbox.socatPath | Point the sandbox proxy at a socat binary outside PATH | Sandbox settings | Managed |
| showClearContextOnPlanAccept | Show a “clear context” option on the plan accept screen | Interface and terminal | Any file |
| showThinkingSummaries | See summaries of Claude’s thinking instead of a collapsed stub | Model and responses | Any file |
| showTurnDuration | Hide the “Cooked for” duration after each response | Interface and terminal | Any file |
| skillListingBudgetFraction | Reserve more or less context for the skill listing | Memory and context | Any file |
| skillListingMaxDescChars | Cap each skill’s description length in the skill listing | Memory and context | Any file |
| skillOverrides | Hide or collapse a skill without editing its SKILL.md | Plugins and skills | Any file |
| skipAutoPermissionPrompt | Skip the one-time notice Claude Code shows when you first enter auto mode yourself rather than through the built-in default | Permission settings | User or managed |
| skipDangerousModePermissionPrompt | Skip the confirmation dialog before bypassPermissions mode | Permission settings | User, local, or managed |
| skipWebFetchPreflight | Skip the WebFetch hostname check when Anthropic is unreachable | Privacy and telemetry | Any file |
| spellcheck | Underline misspelled words in the prompt input with a spell checker you install | Interface and terminal | User or managed |
| spinnerTipsEnabled | Hide tips in the spinner while Claude works | Interface and terminal | Any file |
| spinnerTipsOverride | Add your own tips to the spinner rotation, or replace the built-in tips | Interface and terminal | Any file |
| spinnerVerbs | Add or replace the verbs shown while a turn runs | Interface and terminal | Any file |
| sshConfigs | Add SSH connections to the Desktop environment selector | Remote, desktop, and notifications | User or managed |
| sshHostAllowlist | Limit which hosts Desktop SSH sessions can reach | Remote, desktop, and notifications | Managed |
| sshHostCommands | Add SSH connections whose host comes from a command to the Desktop environment selector | Remote, desktop, and notifications | User or managed |
| statusLine | Run your own command to render a status line below the prompt | Interface and terminal | Any file |
| strictKnownMarketplaces | Allowlist the marketplace sources users can add and install from | Plugins and skills | Managed |
| strictPluginOnlyCustomization | Block skills, agents, hooks, and MCP servers from user and project sources | Plugins and skills | Managed |
| strictPluginOnlyCustomization.agents | Lock agents to plugin and managed sources | Plugins and skills | Managed |
| strictPluginOnlyCustomization.hooks | Lock hooks to plugin and managed sources | Plugins and skills | Managed |
| strictPluginOnlyCustomization.mcp | Lock MCP servers to plugin and managed sources | Plugins and skills | Managed |
| strictPluginOnlyCustomization.skills | Lock skills to plugin and managed sources | Plugins and skills | Managed |
| subagentPromptCacheTtl | Choose the prompt cache lifetime for subagents and other requests outside the main conversation | Model and responses | Any file |
| subagentStatusLine | Rewrite rows in the subagent task display with your own command | Interface and terminal | Any file |
| switchModelsOnFlag | Switch models automatically or pause when a safety classifier flags a request | Model and responses | Any file |
| syncClaudeAiPlugins | Stop loading the plugins enabled on your claude.ai account and stop downloading new ones | Plugins and skills | User, local, or managed |
| syncClaudeAiSkills | Stop loading the skills enabled on your claude.ai account and stop downloading new ones | Plugins and skills | User, local, or managed |
| syntaxHighlightingDisabled | Turn off syntax highlighting in diffs and code blocks | Interface and terminal | Any file |
| taskOutputMaxChars | Removed in v2.1.277, together with the TaskOutput tool it sized | Memory and context | Any file |
| teammateDefaultModel | Removed in v2.1.234; see Specify teammates and models for how Claude Code picks a teammate’s model | Global config settings | Global config |
| teammateMode | Choose how agent team teammates display | Agents, sessions, and worktrees | Any file |
| terminalProgressBarEnabled | Hide the terminal progress bar in terminals that support it | Interface and terminal | Any file |
| terminalTitleFromRename | Stop /rename and --name from changing the terminal tab title | Interface and terminal | Any file |
| theme | Pick the interface color theme, built-in or custom | Interface and terminal | Any file |
| timeFormat | Show the times in the interface on a 12-hour or 24-hour clock, in UTC, or with a strftime pattern | Interface and terminal | Any file |
| timeZone | Show the times in the interface in a time zone other than your system’s | Interface and terminal | Any file |
| tui | Choose the fullscreen or classic terminal renderer | Interface and terminal | Any file |
| ultracode | Have Claude plan a workflow for each substantive task without being asked | Model and responses | Any file |
| useAutoModeDuringPlan | Let the auto mode classifier review shell commands in plan mode; set false to get prompts instead | Permission settings | User, local, or managed |
| verbose | Show full tool output instead of truncated summaries; viewMode takes precedence when both are set | Interface and terminal | Any file |
| viewMode | Start every session in default, verbose, or focus view | Interface and terminal | Any file |
| vimInsertModeRemaps | Map a two-key INSERT-mode sequence such as jj to Escape | Interface and terminal | User or managed |
| voice | Turn on voice dictation and pick hold or tap mode | Interface and terminal | Any file |
| voiceEnabled | Turn on voice dictation with the older single-key form | Interface and terminal | Any file |
| wheelScrollAccelerationEnabled | Turn off mouse-wheel acceleration in fullscreen rendering | Interface and terminal | Any file |
| workflowKeywordTriggerEnabled | Let the word ultracode in a prompt start a workflow; set false to type it without starting one | Hooks and automation | Any file |
| workflowSizeGuideline | Set the agent count Claude aims for in dynamic workflows | Hooks and automation | Any file |
| worktree | Configure how Claude Code creates git worktrees | Agents, sessions, and worktrees | Any file |
| worktree.baseRef | Branch new worktrees from the remote default branch or your local HEAD | Agents, sessions, and worktrees | Any file |
| worktree.bgIsolation | Let background sessions edit the working copy without a worktree | Agents, sessions, and worktrees | Any file |
| worktree.location | Choose where Desktop SSH sessions create their worktrees on a remote machine | Agents, sessions, and worktrees | User |
| worktree.sparsePaths | Check out only the directories you need in each worktree | Agents, sessions, and worktrees | Any file |
| worktree.symlinkDirectories | Symlink large directories into each worktree instead of duplicating them | Agents, sessions, and worktrees | Any file |
| wslInheritsWindowsSettings | Have WSL read managed settings from the Windows policy chain | Enterprise and managed settings | Managed |

## Every key below links to its entry. Scope lists the [files](/docs/en/settings#settings-files-and-who-they-affect) it can go in: User is ~/.claude/settings.json, Project is .claude/settings.json, Local is .claude/settings.local.json, and Managed is [what your organization deploys](/docs/en/managed-settings). Any file means all four, and Global config means [~/.claude.json](#global-config-settings).

````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````
[​](#model-and-responses)Model and responses
### Choose which models Claude Code uses and how it responds. For how these settings interact with the /model command and environment variables, see [Model configuration](/docs/en/model-config).
[​](#advisormodel)advisorModel`
- Scope: Any file
- Type: string, one of the aliases "fable", "opus", or "sonnet", which resolve to Claude Code’s current default version of that model family, or a full model ID such as "claude-opus-5-5"
- Default: unset, so the advisor is off
- Per-session overrides: --advisor takes precedence over this key for one session. CLAUDE_CODE_DISABLE_ADVISOR_TOOL turns the advisor off, and this key can’t turn it back on

```
{
  "advisorModel": "opus"
}

```
### Pick which model answers when Claude calls the server-side [advisor tool](/docs/en/advisor). Unset it to turn the advisor off. The advisor must be at least as capable as your main model. See [Choose an advisor model](/docs/en/advisor#choose-an-advisor-model) for the accepted pairings and what happens when you pick one that isn’t accepted.
You don’t usually edit this key by hand. Run /advisor to open a picker that shows the current choice, the models that can advise, and **No advisor**. Claude Code saves your pick to this key in ~/.claude/settings.json. If you pick from a [Remote Control](/docs/en/remote-control) client or in a session attached to a remote worker, the pick applies to that session only and doesn’t change this key.
If your account requires the [usage-credits consent](/docs/en/advisor#fable-advisor-and-usage-credits), accept it first by running /model fable. Until you do, picking Fable in /advisor saves nothing and Claude Code tells you to run /model fable first.

****``
****````````
****
****````

settings.json
The key has no effect on providers where the advisor [isn’t available](/docs/en/advisor#requirements), such as Amazon Bedrock and Claude Platform on AWS. "fable" requires [Fable access](/docs/en/advisor#choose-an-advisor-model).
[​](#alwaysthinkingenabled)alwaysThinkingEnabled`
- Scope: Any file
  - true: no effect; thinking is already on
  - false: Claude Code turns extended thinking off for every session
- Default: unset, so thinking is on for models that support it
- Per-session overrides: MAX_THINKING_TOKENS takes precedence over this key for one session: 0 turns thinking off, under the same model and provider limits as false, and a positive value turns thinking on even when this key is false. On adaptive-reasoning models the number itself is ignored

```
{
  "alwaysThinkingEnabled": false
}

```
### Turn [extended thinking](/docs/en/model-config#extended-thinking) off for every session by setting this to false. Thinking is on by default, so true changes nothing. Most people set this through /config rather than by editing the file.
On models that always think, such as Opus 5.5, Sonnet 5.5, Haiku 5.5, and the Fable models, false has no effect. On [third-party providers](/docs/en/third-party-integrations) Claude Code omits the thinking parameter instead of turning thinking off, so adaptive-reasoning models may still think. With thinking turned off on the Anthropic API, Claude Code sends effort high instead of a higher level to models it knows [don’t accept that combination](/docs/en/errors#effort-isnt-available-with-thinking-turned-off), such as Opus 5.

****``
****``
``

****
****````````

settings.json
[​](#availablemodels)availableModels`
- Scope: Any file. Deploy it in managed settings to enforce it for an organization.
- Type: array of model aliases or IDs
- Default: unset, so every model is available

```
{
  "availableModels": ["sonnet", "haiku"]
}

```
### Restrict which models people can select for the main session, [subagents](/docs/en/sub-agents), [skills](/docs/en/skills), and the [advisor](/docs/en/advisor). A managed list constrains /model, --model, and the model key in a developer’s own files; a model outside it can’t be selected. With the default prefix matching, this doesn’t touch the Default option on its own; pair it with [enforceAvailableModels](#enforceavailablemodels) for that.

****``
****
****

This example lets people select only Sonnet and Haiku models:
settings.json
A model ID entry such as "claude-opus-5" also permits later versions that extend it, such as Opus 5.5. To block one of those versions, use [deniedModels](#deniedmodels). To make each model ID entry permit only the version it names, use [availableModelsMatch](#availablemodelsmatch). See [Restrict model selection](/docs/en/model-config#restrict-model-selection). For third-party provider IDs, see [Pin models for third-party deployments](/docs/en/model-config#pin-models-for-third-party-deployments).
[​](#availablemodelsmatch)availableModelsMatch`
- Scope: Managed. Claude Code ignores the key in user, project, and local settings and in --settings, with a warning
  - "prefix": a model ID entry permits its version and any model ID that extends it with another segment
  - "exact": a model ID entry permits only the version it names, so "claude-opus-5" permits Opus 5 but not claude-opus-5-5. An entry such as "claude-opus-4-5" also permits its dated Anthropic model ID claude-opus-4-5-20251101. A family alias such as "opus" still permits the whole family, and best, opusplan, and default entries are ignored
- Default: "prefix"

```
{
  "availableModels": ["claude-opus-5", "claude-sonnet-5"],
  "availableModelsMatch": "exact"
}

```
### Choose how [availableModels](#availablemodels) entries match model IDs. By default a model ID entry also permits later versions that extend it, so "claude-opus-5" permits Opus 5.5. With "exact", each model ID entry permits only the version it names, so a newer version of that model stays blocked until you list it. Requires Claude Code v2.1.283 or later.

****````
****``
``````````````````

****``

This example permits Opus 5 and Sonnet 5 and no later release of either:
managed-settings.json
With "exact", the Default option is also limited to the listed models whenever the list names at least one model or family. See [Block specific models or versions](/docs/en/model-config#block-specific-models-or-versions).
[​](#deniedmodels)deniedModels`
- Scope: Managed. Claude Code ignores the key in user, project, and local settings and in --settings, with a warning
  - A family alias such as "opus" blocks every model in that family
  - A model ID such as "claude-opus-5-5" blocks that version in every spelling, including dated and provider-specific IDs
  - A model ID with no minor version, such as "claude-opus-5", also blocks later minor versions such as Opus 5.5. Write "claude-opus-5-0" to block Opus 5 alone
  - best, opusplan, and default entries are ignored
- Default: unset, so no model is blocked

```
{
  "availableModels": ["opus", "sonnet"],
  "deniedModels": ["claude-opus-5-5"]
}

```
### Block specific models, with or without an [availableModels](#availablemodels) allowlist and even when that list permits them. Claude Code hides a blocked model from the /model picker, and the model can’t be selected anywhere availableModels is enforced. A session on the Default option doesn’t run a blocked model either, as [Block specific models or versions](/docs/en/model-config#block-specific-models-or-versions) describes. Requires Claude Code v2.1.283 or later.

****````
****``
``
````
``````

****

This example permits Opus and Sonnet models and blocks Opus 5.5:
managed-settings.json
See [Block specific models or versions](/docs/en/model-config#block-specific-models-or-versions).
[​](#effortlevel)effortLevel`
- Scope: Any file
  - "low": the least reasoning, for short, scoped, latency-sensitive tasks that aren’t intelligence-sensitive
  - "medium": reduces token usage for cost-sensitive work that can trade off some intelligence
  - "high": balances token usage and intelligence
  - "xhigh": deeper reasoning at higher token spend
- Default: unset
- Per-session overrides: --effort takes precedence over this key for one session, and CLAUDE_CODE_EFFORT_LEVEL takes precedence over both

```
{
  "effortLevel": "xhigh"
}

```
### Set a default [effort level](/docs/en/model-config#adjust-effort-level) for models you haven’t saved a level for. Lower levels are faster and cheaper on straightforward tasks, and higher levels reason more deeply on complex problems.
When you run /effort low, medium, high, or xhigh in an interactive session on your machine, Claude Code saves the level for the active model under [modelSettings](#modelsettings) rather than writing this key. Before v2.1.251, /effort wrote this key.
Within the same settings file, Claude Code uses a model’s saved level rather than this key. [modelSettings](#modelsettings) states the cross-file precedence.
In a session attached to a remote worker, in a -p run, and in the Agent SDK, /effort applies to that session only. [Adjust effort level](/docs/en/model-config#adjust-effort-level) lists the interactive picks that also apply to that session only. The message that /effort prints says which happened.

****``
****``
``
``
``

****
****````

settings.json
In your user settings file, ~/.claude/settings.json, this key is the older form /effort wrote before it saved levels per model, and it keeps applying where it applied before, on Opus 5, Fable 5.1, and earlier models. Opus 5.5 and models released after it ignore it and start at their own default until you save a level for them, which /effort writes under [modelSettings](#modelsettings). In project, local, and managed settings, and with --settings, this key applies to every model.
[​](#enforceavailablemodels)enforceAvailableModels`
- Scope: Any file
  - true: when Default would resolve to a model outside availableModels, Claude Code resolves it to the first available model in the list
  - false: this key doesn’t change how Default resolves
- Default: false

```
{
  "availableModels": ["sonnet", "haiku"],
  "enforceAvailableModels": true
}

```
### The /model picker has a **Default** option, and [default model setting](/docs/en/model-config#default-model-setting) describes the model it resolves to. An [availableModels](#availablemodels) allowlist limits the models you can name, but with the default [prefix matching](#availablemodelsmatch) it doesn’t remap your account type’s default, so **Default** can still resolve to a model outside the list. This key closes that gap. Requires Claude Code v2.1.175 or later.
When your organization deploys any managed settings, Claude Code reads this key from the managed source alone and ignores it in your other files.
For how this key applies to the startup model checks, see [Amazon Bedrock](/docs/en/amazon-bedrock#when-your-organization-enforces-a-model-allowlist) and [Google Cloud’s Agent Platform](/docs/en/google-vertex-ai#when-your-organization-enforces-a-model-allowlist).

****``
``
****

****``

This example restricts named selections to Sonnet and Haiku models and makes **Default** resolve to the first of them that is available:
settings.json
This key has no effect when availableModels is unset or empty. See [Enforce the allowlist for the Default model](/docs/en/model-config#enforce-the-allowlist-for-the-default-model). Requires Claude Code v2.1.175 or later.
[​](#fallbackmodel)fallbackModel`
- Scope: Any file
- Type: array of model aliases or IDs; "default" expands to the default model
- Default: unset, so a failed request isn’t retried on another model
- Per-session overrides: --fallback-model takes precedence over this key for one session

```
{
  "fallbackModel": ["claude-sonnet-5", "claude-haiku-4-5"]
}

```
### Name backup models for Claude Code to try, in order, when your primary model is overloaded or unavailable. Claude Code switches to the next available model in the chain for the rest of the turn and shows a notice. Without a chain, Claude Code retries the same model and then surfaces the server’s error, and you retry or switch models yourself.
A switch means one turn with a cold [prompt cache](/docs/en/prompt-caching#switching-models) on the fallback model; your next message tries the primary model first again.

****``
****``
****
****``

This example tries Sonnet 5 first, then Haiku 4.5, when your primary model fails:
settings.json
Unlike most array settings, this key doesn’t merge across settings files: the highest-precedence file that defines it supplies the whole chain. If your project file sets ["claude-sonnet-5"] and your user file sets ["claude-haiku-4-5"], the chain is ["claude-sonnet-5"] only. Claude Code keeps at most three distinct allowed models from the list and ignores the rest. See [Fallback model chains](/docs/en/model-config#fallback-model-chains).
[​](#fastmode)fastMode`
- Scope: Any file
  - true: Claude Code turns fast mode on for sessions where it’s available. On Fable 5.2, you must also run /fast while using Fable 5.2
  - false: fast mode stays off
- Default: unset, so fast mode is off
- Per-session overrides: CLAUDE_CODE_DISABLE_FAST_MODE turns fast mode off for one session, and this key can’t turn it back on

```
{
  "fastMode": true
}

```
### Turn [fast mode](/docs/en/fast-mode) on for sessions where it’s available, for interactive work such as rapid iteration or live debugging where you want speed at a higher cost per token. You don’t usually edit this key yourself. Running /fast writes fastMode: true to ~/.claude/settings.json, and running it again to turn fast mode off removes the key.
Only Fable 5.2, Opus 5.5, Opus 5, and Opus 4.8 support fast mode. Running /fast from another model switches you to Opus, and switching to an unsupported model turns fast mode off. See [Switch models while fast mode is on](/docs/en/fast-mode#switch-models-while-fast-mode-is-on).

****``
****````
``

****
****``

settings.json
[​](#fastmodepersessionoptin)fastModePerSessionOptIn`
- Scope: Any file
  - true: a saved fastMode: true no longer turns fast mode on at session start, so each person runs /fast in each session they want it; a fastMode: true passed with --settings still counts for that session unless managed settings set this key
  - false: a saved fastMode: true works as fastMode describes
- Default: false

```
{
  "fastModePerSessionOptIn": true
}

```
### Normally, running /fast saves [fastMode](#fastmode) to a person’s user settings, so new sessions on a supported model start with fast mode on. On Fable 5.2, that happens only if they [turned it on while using Fable 5.2](/docs/en/fast-mode#switch-models-while-fast-mode-is-on). To make each person run /fast in each session they want it, set this key to true. Claude Code leaves fastMode in their file, so turning this key off restores the old behavior.
Owners on Team or Enterprise plans can deploy it organization-wide through [server-managed settings](/docs/en/server-managed-settings). When managed settings set the key, /fast on is refused outside interactive terminal sessions and reports that your organization has disabled fast mode. That covers [non-interactive mode](/docs/en/headless), the [VS Code extension](/docs/en/vs-code), and [cloud sessions](/docs/en/claude-code-on-the-web).

****``
****``````````
``````

****``

settings.json
See [Require per-session opt-in](/docs/en/fast-mode#require-per-session-opt-in).
[​](#language)language`
- Scope: Any file
- Type: string, any language name, such as "japanese", "spanish", or "french"; Claude Code doesn’t validate it
- Default: unset; session titles then match the language of your conversation

```
{
  "language": "japanese"
}

```
### Have Claude respond in a language other than English by default. There is no fixed list for responses: Claude Code passes the value verbatim to Claude as an instruction to always respond in that language, so any language name Claude can read works. Claude Code doesn’t check the value, so a misspelled name reaches Claude as written rather than producing an error. The same value sets the language for [voice dictation](/docs/en/voice-dictation#change-the-dictation-language), which does have a fixed list of [supported dictation languages](/docs/en/voice-dictation#change-the-dictation-language), and for auto-generated session titles.

****``
****``````
****

settings.json
[​](#maxeffortlevel)maxEffortLevel`
- Scope: Any file. Deploy it in managed settings to enforce it for an organization. When several scopes set a cap, the lowest applies, so a cap set in one scope can’t be raised from another
- Type: string, one of "low", "medium", "high", "xhigh", or "max". A "max" value sets no cap
- Default: unset, so no cap applies
- Per-model caps: add maxEffortLevel to a model’s modelSettings entry. That entry replaces this key for the model only within the settings source that sets both, such as your user settings or one managed source. Set "max" there to exempt the model from that source’s cap; Claude Code still applies caps from other sources

```
{
  "maxEffortLevel": "medium",
  "modelSettings": {
    "claude-sonnet-4-6": {
      "maxEffortLevel": "max"
    }
  }
}

```
### Cap the [effort level](/docs/en/model-config#adjust-effort-level) a session can use, leaving lower levels available. Any higher level runs at the cap instead, including one from /effort, the /model picker, --effort, [CLAUDE_CODE_EFFORT_LEVEL](/docs/en/env-vars), a skill’s or subagent’s effort frontmatter, or the model’s own default. Claude Code applies the cap itself before each request, so it holds on every provider, including Amazon Bedrock, Google Cloud’s Agent Platform, and Microsoft Foundry. Requires Claude Code v2.1.267 or later.

****``
****````````````
****
****``````

This example caps every model at medium and exempts Sonnet 4.6:
settings.json
When your organization also sets an [effort limit](/docs/en/model-config#organization-effort-limits) for a model, the lower of the two caps applies.
[​](#model)model`
- Scope: Any file
- Type: string, a model alias or full model ID
- Default: unset, so Claude Code uses your account’s default model
- Per-session overrides: --model takes precedence over ANTHROPIC_MODEL, and both take precedence over this key for one session, including over a managed model; an availableModels list still applies to the pick

```
{
  "model": "claude-sonnet-5"
}

```
### Set the model every new session uses, so you don’t have to pick one with /model each time. Setting it here doesn’t stop you from switching mid-session. If your admin set an [organization default model](/docs/en/model-config#organization-default-model) to override user selection, you get that model even when you set this key in user, project, or local settings.

****``
****
****
****````````

settings.json
A value here outranks [ANTHROPIC_DEFAULT_MODEL](/docs/en/model-config#set-a-default-model-for-new-sessions), which Claude Code uses only when nothing else selects a model.
[​](#modeloverrides)modelOverrides`
- Scope: Any file
- Type: object mapping model ID to provider model ID
- Default: unset

```
{
  "modelOverrides": {
    "claude-opus-4-6": "arn:aws:bedrock:us-east-1:123456789012:inference-profile/example"
  }
}

```
### Map Anthropic model IDs to provider-specific model IDs, such as Amazon Bedrock inference profile ARNs. Each model picker entry then uses its mapped value when calling the provider API. Administrators use this on [Amazon Bedrock, Google Cloud’s Agent Platform, and Microsoft Foundry](/docs/en/model-config#override-model-ids-per-version) to route each model version to a specific inference profile, version name, or deployment for governance, cost allocation, or regional routing.

****``
****
****

This example routes every call for Opus 4.6 to the named Bedrock inference profile:
settings.json
See [Override model IDs per version](/docs/en/model-config#override-model-ids-per-version).
[​](#modelpicker)modelPicker`
- Scope: User or managed. Claude Code reads the key from managed settings, --settings, and user settings, and ignores it in project and local settings so a repository you clone can’t relabel the picker. The highest of those three that sets the key supplies the whole lineup, and Claude Code never combines lineups from two sources.
- Type: object with an options array of rows and an optional replaceBuiltInOptions Boolean
- Default: unset, so the picker shows the built-in lineup

```
{
  "modelPicker": {
    "options": [
      { "model": "us.anthropic.claude-opus-4-8", "label": "Opus (production)" },
      {
        "model": "us.anthropic.claude-sonnet-4-6",
        "label": "Sonnet (production)",
        "description": "Day-to-day work"
      }
    ]
  }
}

```
#### List the models the /model picker offers, in the order you write them and under labels you choose, so the picker lists the models your organization runs, after the built-in lineup or instead of it. Each row’s model is taken verbatim, so it accepts anything --model accepts: an alias such as opus, an Anthropic model ID, or a provider-format ID for Amazon Bedrock, Google Cloud’s Agent Platform, Microsoft Foundry, or an LLM gateway. Requires Claude Code v2.1.242 or later.

****````
****````
****

This example adds two Bedrock deployments after the built-in lineup, under names your team recognizes:
managed-settings.json

[​](#fields-for-modelpicker)Fields for modelPicker`

| Field | Type | What it does |
| --- | --- | --- |
| options | array of rows, each with a required model and optional label, description, and behavesAs | The rows the picker shows, in this order, except that a grayed-out row moves to the bottom. Without a label, Claude Code titles the row with the built-in name for a model it knows, or the model ID otherwise, and without a description it writes a generic second line |
| replaceBuiltInOptions | Boolean, default false | Set it to true to show only these rows, Default, and a row for the model the session is already using. Leave it unset to add these rows after the built-in lineup |

- Dropped: a row Claude Code can’t serve, such as a retired model or a model your organization has no access to
- Grayed out: a row you can’t select yet, shown with the reason
- No row survives: Claude Code keeps the built-in lineup, filtered by the allowlist as usual
### The key takes two fields, one for the rows themselves and one for whether they replace the built-in lineup or add to it.
****
An entry in options can also carry an optional behavesAs string beside its model, which requires v2.1.257 or later. Set it to the ID of a model your Claude Code version already knows, such as claude-opus-4-8, on an entry whose model is newer than your version. Claude Code then applies that known model’s capabilities and effort defaults to the entry instead of treating its model as unknown. The entry’s label and the model ID Claude Code sends in requests don’t change.
With replaceBuiltInOptions on, Claude Code hides every other row: the built-in lineup, the rows it adds for [availableModels](#availablemodels) entries, the models [gateway discovery](/docs/en/llm-gateway-protocol#model-discovery) found, and [ANTHROPIC_CUSTOM_MODEL_OPTION](/docs/en/model-config#add-a-custom-model-option). With it off, Claude Code skips a listed model that the built-in lineup already covers. A label changes what the picker shows, not which model Claude Code runs.
An [availableModels](#availablemodels) allowlist still applies to these rows. Before you add a listed model to the allowlist, read [Merge behavior](/docs/en/model-config#merge-behavior): a specific model ID narrows its family’s wildcard entry. Claude Code also checks each row against the session before it shows the picker:

****
****
****

Claude Code drops a row it can’t parse and keeps the rest. See [Fix a broken settings file](/docs/en/settings#fix-a-broken-settings-file).
[​](#modelpricing)modelPricing`
- Scope: Managed. Deploy the key through server-managed settings, an MDM policy, a managed-settings.json file, or a policy helper. Claude Code ignores it in user, project, and local settings, in --settings, and on Windows in the user-writable HKCU registry. With server-managed settings, each session reports costs at list price until that session’s settings fetch has confirmed the setting. A host application that embeds Claude Code and sets CLAUDE_CODE_PROVIDER_MANAGED_BY_HOST can supply a table of its own through the SDK managedSettings option, which Claude Code uses only when no managed source sets the key and only in Claude Code v2.1.246 or later.
- Type: object with an optional multiplier and an optional overrides map
- Default: unset, so Claude Code reports list price unless a host application supplies a table

```
{
  "modelPricing": {
    "multiplier": 0.85,
    "overrides": {
      "claude-sonnet-4-6": {
        "input": 2.4,
        "output": 12,
        "cacheRead": 0.24,
        "cacheWrite": 3
      }
    }
  }
}

```
#### Report spend at the rates your organization pays instead of list price. Set it when your organization has contracted rates, so the dollar figures developers see match your bill. Claude Code applies the rates in /usage, the [status line](/docs/en/statusline), the Agent SDK’s total_cost_usd, the [--max-budget-usd](/docs/en/cli-reference) limit, and the [OpenTelemetry](/docs/en/monitoring-usage) cost metric and events. You supply the rates: Claude Code doesn’t read them from your contract or the Claude Console. Requires Claude Code v2.1.242 or later.

****``````````
****````
****

Set multiplier alone for a flat discount or markup, overrides alone for per-model rates, or both.
This example sets contracted rates for Sonnet 4.6 and then reduces every figure, the Sonnet row included, by 15%:
managed-settings.json
Set multiplier above 1, up to 10, to mark every figure up. A markup requires Claude Code v2.1.271 or later. Earlier versions ignore a multiplier above 1 with a warning and keep the rest of the setting.
For the steps, including how to confirm the rates are in effect, see [Report spend at your contracted rates](/docs/en/costs#report-spend-at-your-contracted-rates).

[​](#fields-for-modelpricing)Fields for modelPricing`

| Field | Type | What it does |
| --- | --- | --- |
| multiplier | number greater than 0 and at most 10 | Scales every cost Claude Code computes, whether or not an overrides row covers it. Below 1 is a discount, above 1 a markup |
| overrides | map of model ID to a rate object with input, output, cacheRead, and cacheWrite, each 0 to 10000 | The USD-per-million-token rates for that model, all four required. cacheWrite covers both five-minute and one-hour cache writes. See Which models a row applies to |

#### ````````````````
Claude Code uses a row’s rates exactly as you wrote them, without adding the fast-mode surcharge or the [US-only-inference rate](https://platform.claude.com/docs/en/about-claude/pricing). If you also set multiplier, Claude Code applies it on top of the row’s rates. Claude Code drops a row with a rate it can’t parse, or a multiplier it can’t parse, and keeps the rest; see [Fix a broken settings file](/docs/en/settings#fix-a-broken-settings-file).
[​](#which-models-a-modelpricing-row-applies-to)Which models a modelPricing row applies to
- A built-in model’s ID: a key Claude Code itself uses for a built-in model, whether that key is the model’s own ID, such as claude-sonnet-4-6, or its Bedrock, Agent Platform, or Foundry ID. Claude Code applies the row to every dated snapshot ID and provider-specific ID of that model.
- Any other key: a key that isn’t a built-in model’s ID, such as a gateway model alias. Claude Code applies the row to that one ID only. When a model ID matches one of your keys exactly and also falls under a row keyed by a built-in model’s ID, Claude Code uses the exact match.
- A Bedrock application inference profile: once Claude Code has resolved the profile to the model it routes to, through your modelOverrides map or the bedrock:GetInferenceProfile lookup, Claude Code applies that model’s row to the profile.
### Claude Code decides which models a row applies to from the row’s key:

****``
****
****````

[​](#modelsettings)modelSettings`
- Scope: Any file
  - effortLevel: one of "low", "medium", "high", or "xhigh"
  - maxEffortLevel: the highest effort level the model may run at
  - autoCompactWindow: a number of tokens from 100000 to 1000000, or "auto" for the window tuned for the model. /autocompact saves here. For that model, the value takes precedence over a top-level autoCompactWindow in the same settings file. Requires Claude Code v2.1.288 or later
- Default: unset

```
{
  "modelSettings": {
    "claude-opus-5-5": {
      "effortLevel": "high"
    }
  }
}

```
### Save an [effort level](/docs/en/model-config#adjust-effort-level) for each model you use. Requires Claude Code v2.1.251 or later.
In an interactive session on your machine, when you save low, medium, high, or xhigh as your default with /effort or the /model picker’s effort slider, Claude Code writes that level here under the model you’re using, so you rarely edit this key yourself. When you pick one of those levels in the [VS Code extension’s model picker](/docs/en/vs-code#use-the-prompt-box), Claude Code saves it here the same way. The [effortLevel](#effortlevel) entry lists the sessions where /effort applies to that session only.
Edit the key by hand to change or remove a level you saved.
A model’s effortLevel here takes precedence over the top-level [effortLevel](#effortlevel) in the same settings file. Across files, Claude Code resolves each model separately: the highest-precedence [settings file](/docs/en/settings#settings-precedence) that sets either an effortLevel for that model or a top-level effortLevel that [applies to that model](#effortlevel) decides, so an effortLevel in managed settings outranks a level you saved in user settings. [Adjust effort level](/docs/en/model-config#adjust-effort-level) lists what else can override a saved level, such as --effort at launch.
To cap one model’s effort rather than set its level, add a [maxEffortLevel](#maxeffortlevel) field to that model’s entry. The field requires Claude Code v2.1.267 or later.

****``
****``````````
``
````````````

****

Claude Code writes each entry under the model’s canonical name, such as claude-opus-5-5, and matches that model’s alias, date-suffixed, [1m], and recognized provider-specific IDs to the same entry.
This example keeps Opus 5.5 at high while other models use their own saved or default levels:
settings.json
Run /effort auto to clear your saved level for the model you’re using. Claude Code leaves the other entries and any top-level effortLevel in place.
[​](#outputstyle)outputStyle`
- Scope: Any file
- Type: string, the name of a built-in or custom output style
- Default: unset, so Claude Code uses the default style

```
{
  "outputStyle": "Explanatory"
}

```
### Select an [output style](/docs/en/output-styles) by name. An output style is a saved set of instructions that changes Claude’s role, tone, and output format, such as the built-in Explanatory and Learning styles or one you wrote yourself.
If you change this key during a session, Claude uses the new style starting with your next message. For what that message costs in prompt caching, see [Changing output style](/docs/en/prompt-caching#changing-output-style). Before v2.1.251, the edit applied only after you ran /clear or started a new session.

****``
****
****

This example selects the built-in Explanatory style, which adds educational insights between tasks:
settings.json
[​](#promptcachettl)promptCacheTtl`
- Scope: Any file
  - "5m": the cache holds for five minutes
  - "1h": the cache holds for an hour
- Default: unset, so each main-conversation request gets its default lifetime
- Per-session overrides: FORCE_PROMPT_CACHING_5M takes precedence over everything else, then CLAUDE_CODE_PROMPT_CACHE_TTL, then this key, and last ENABLE_PROMPT_CACHING_1H

```
{
  "promptCacheTtl": "1h",
  "subagentPromptCacheTtl": "5m"
}

```
### Choose how long the [prompt cache](/docs/en/prompt-caching) holds the main conversation. This key applies to your interactive, -p, and Agent SDK turns, together with the helpers Claude Code runs inline with them. The one-hour lifetime keeps the cache warm across longer breaks, and the API [bills each cache write at a higher rate](https://platform.claude.com/docs/en/build-with-claude/prompt-caching#pricing) than at the five-minute lifetime. Requires Claude Code v2.1.242 or later.

****``
****``
``

****
****``````

This example keeps the main conversation on the one-hour lifetime and leaves subagents on five minutes:
settings.json
For what each lifetime costs, see [Cache lifetime](/docs/en/prompt-caching#cache-lifetime).
[​](#showthinkingsummaries)showThinkingSummaries`
- Scope: Any file
  - true: you see full thinking summaries when you expand thinking with Ctrl+O
  - false: the Anthropic API redacts thinking blocks and Claude Code shows a collapsed stub
- Default: false

```
{
  "showThinkingSummaries": true
}

```
### See summaries of Claude’s [extended thinking](/docs/en/model-config#extended-thinking) in interactive sessions. Set it if you want the full summaries when you expand thinking with Ctrl+O. When unset or false, the Anthropic API redacts thinking blocks and Claude Code shows a collapsed stub.

****``
****````
``

****``

settings.json
Redaction changes only what you see, not what the model generates. To reduce thinking spend, [lower the budget or disable thinking](/docs/en/model-config#extended-thinking) instead.
[​](#subagentpromptcachettl)subagentPromptCacheTtl`
- Scope: Any file
  - "5m": the cache holds for five minutes
  - "1h": the cache holds for an hour
- Default: unset, so each of these requests gets its default lifetime
- Per-session overrides: FORCE_PROMPT_CACHING_5M takes precedence over everything else, then CLAUDE_CODE_SUBAGENT_PROMPT_CACHE_TTL, then this key, then ENABLE_PROMPT_CACHING_1H, which asks for the one-hour lifetime on every request. For where a subagent’s own frontmatter value ranks, see Choose the TTL yourself

```
{
  "subagentPromptCacheTtl": "1h"
}

```
### Choose how long the [prompt cache](/docs/en/prompt-caching) holds the requests Claude Code makes outside the main conversation. This key applies to [subagents](/docs/en/sub-agents), [workflows](/docs/en/workflows), and Claude Code’s own background and helper requests, such as compaction and session titles. The one-hour lifetime keeps the cache warm across longer breaks, and the API [bills each cache write at a higher rate](https://platform.claude.com/docs/en/build-with-claude/prompt-caching#pricing) than at the five-minute lifetime. Requires Claude Code v2.1.242 or later.

****``
****``
``

****
****``````

This example gives subagents and the other requests outside the main conversation the one-hour lifetime:
settings.json
This key covers the requests [promptCacheTtl](#promptcachettl) doesn’t, so set both to choose a lifetime for every request Claude Code makes. For how a subagent’s cache differs from the main conversation’s, see [Subagents and the cache](/docs/en/prompt-caching#subagents-and-the-cache).
[​](#switchmodelsonflag)switchModelsOnFlag`
- Scope: Any file. Appears in /config as Switch models when a message is flagged, with the options Switch automatically and Ask each time.
  - true: Claude Code switches to the fallback model and continues
  - false: in an interactive session Claude Code pauses so you can choose between switching and editing the prompt; where no dialog can show, such as a -p run, the flagged request ends as an error
- Default: unset. Claude Code switches automatically, though it may ask first in an interactive session

```
{
  "switchModelsOnFlag": false
}

```
### Choose what happens when a [safety classifier flags a request](/docs/en/model-config#automatic-model-fallback): switch to the fallback model and continue, or pause so you can choose between switching and editing the prompt.

****``
````

****

settings.json
See [Ask before switching](/docs/en/model-config#ask-before-switching).
[​](#ultracode)ultracode`
- Scope: Any file
  - true: sessions start with ultracode on when dynamic workflows are enabled for you and your model supports xhigh
  - false: sessions start with ultracode off
- Default: unset, so ultracode is off
- Per-session overrides: /effort ultracode turns ultracode on for one session without this key, and /effort ultracode off turns it off for one session when this key is true. The --effort ultracode flag also turns it on for one session, at xhigh effort

```
{
  "ultracode": true
}

```
## Start sessions with [ultracode](/docs/en/workflows#let-claude-decide-with-ultracode) on. With it on, Claude plans a workflow for each substantive task instead of waiting for you to ask. Claude plans workflows only when [dynamic workflows](/docs/en/workflows) are enabled for you and your model supports xhigh effort. The key doesn’t change the session’s effort level: ultracode runs at whichever level the session uses. Claude Code reads this key but never writes it: /effort ultracode turns ultracode on for the current session only.

****``
****````
``

****
****``````````

settings.json
The session’s effort level comes from [effortLevel](#effortlevel), [modelSettings](#modelsettings), and the other [effort sources](/docs/en/model-config#adjust-effort-level), and an [effort cap](/docs/en/model-config#organization-effort-limits) such as [maxEffortLevel](#maxeffortlevel) lowers that level without turning ultracode off. This and the /effort ultracode off form require Claude Code v2.1.284 or later. Before v2.1.284, ultracode: true ran the session at xhigh effort, and an effort cap below xhigh kept ultracode off. An Agent SDK apply_flag_settings control request also accepts the key.
[​](#permission-settings)Permission settings
### Decide what Claude can do without asking, the default permission mode for new sessions, and what auto mode’s classifier allows. For rule syntax and the permission model, see [Configure permissions](/docs/en/permissions).
[​](#allowmanagedpermissionrulesonly)allowManagedPermissionRulesOnly`
- A repository’s .claude/ directory
- Your ~/.claude/skills/ and ~/.claude/commands/ directories, including skills synced from claude.ai
- An --add-dir directory
- Plugins declared with a .claude-plugin manifest inside ~/.claude/skills/ or the project’s .claude/skills/
  - The session is a Code session or Cowork session, other than a cloud session, for which the Claude Desktop app itself starts Claude Code
  - Your managed settings set the key, not only an embedding host’s parent settings
  - The session runs Claude Code v2.1.305 or later
- Scope: Managed
  - true: managed settings become the only settings source of permission rules
  - false: Claude Code applies permission rules from user, project, local, and --settings files in addition to the managed ones
- Default: unset, so Claude Code applies permission rules from user, project, and local settings and from --settings, in addition to the managed ones

```
{
  "allowManagedPermissionRulesOnly": true
}

```
### Make managed settings the only settings source of permission rules. Claude Code then ignores allow, ask, and deny rules in user, project, local, and --settings files, ignores --allowedTools, hides the always-allow choices in permission prompts, and stops saving new rules.
When [parent settings from an embedding host](/docs/en/managed-settings#let-an-embedding-host-add-policy) apply, Claude Code treats them as part of the managed tier. It drops their allow rules and additionalDirectories, and keeps their deny and ask rules except Read and Edit rules whose pattern starts with !. A host can’t carve paths out of the managed rules with a ! rule, whether or not you set this key.
--disallowedTools rules and the current session’s deny and ask rules still apply, including after Claude Code reloads settings mid-session. They only restrict, so they can’t widen what the managed rules grant. Before v2.1.257, Claude Code dropped those command-line and session rules at the first settings reload.
For what a ! pattern in a --disallowedTools or session rule can carve out, see [Read and Edit rules](/docs/en/permissions#read-and-edit).
When you set this key, Claude Code v2.1.282 or later also ignores the [allowed-tools](/docs/en/skills#pre-approve-tools-for-a-skill) frontmatter in skills and .claude/commands/ files from these sources:

``
````
``
``````
``

Skills from managed settings and bundled skills keep their allowed-tools. @inline plugins outside those Desktop sessions keep theirs too, except one named [anthropic-skills](/docs/en/skills#names-reserved-for-synced-skills). A skill’s disallowed-tools still applies. For what a developer sees when Claude Code ignores the field, see [When only managed permission rules apply](/docs/en/skills#when-only-managed-permission-rules-apply).

****``
****``
````

****``

managed-settings.json
This key doesn’t lock down the MCP server allowlist; for that, set [allowManagedMcpServersOnly](#allowmanagedmcpserversonly). See [Managed-only settings](/docs/en/managed-settings#managed-only-settings).
[​](#automode)autoMode`
- Scope: User or managed
- Type: object with environment, allow, soft_deny, and hard_deny arrays of prose rules, plus the classifyAllShell Boolean
- Default: unset, so the classifier uses only its built-in rules

```
{
  "autoMode": {
    "soft_deny": ["$defaults", "Never run terraform apply"]
  }
}

```
### Add your own rules to what the [auto mode](/docs/en/permission-modes#eliminate-prompts-with-auto-mode) classifier blocks and allows. Use it to tell the classifier which repos, buckets, and domains your organization trusts, so it stops blocking routine internal operations. The classifier ships with [built-in allow and deny rules](/docs/en/auto-mode-config#inspect-the-defaults-and-your-effective-config). Include the literal string "$defaults" in an array to keep those built-in rules at that position and add yours around them; leave it out to replace them with yours.

****``
****``````````
****

This example keeps the built-in soft_deny rules, through "$defaults", and adds one more that blocks terraform apply:
settings.json
When more than one of those files sets the same array, Claude Code concatenates the entries. For the rule format and how each array is applied, see [Configure auto mode](/docs/en/auto-mode-config).
[​](#automode-classifyallshell)autoMode.classifyAllShell`
- Scope: User or managed. Read wherever autoMode is read.
  - true: while auto mode is active, Claude Code sends every Bash and PowerShell command through the classifier and suspends your shell allow rules; outside auto mode the rules still apply
  - false: auto mode suspends only allow rules that could run arbitrary code, such as Bash(*) and Bash(python *); a command that any other allow rule matches skips the classifier unless it carries per-command allowed domains, and every other shell command goes through it
- Default: false

```
{
  "autoMode": {
    "classifyAllShell": true
  }
}

```
### Send every Bash and PowerShell command through the auto mode classifier while auto mode is active. By default, auto mode suspends only allow rules that could run arbitrary code: tool-wide and wildcard rules such as Bash(*), and interpreter or shell-wrapper prefixes such as Bash(python *). A command that any other allow rule matches, such as Bash(npm test), skips the classifier unless it carries [per-command allowed domains](/docs/en/sandboxing#per-command-allowed-domains-in-auto-mode). When it skips, a destructive argument the rule’s prefix didn’t anticipate can get through unseen. Setting this key suspends every shell allow rule for the session so the classifier sees every command. Requires Claude Code v2.1.193 or later.

****````
****``
``````

****``

settings.json
See [Route all shell commands through the classifier](/docs/en/auto-mode-config#route-all-shell-commands-through-the-classifier).
[​](#disableautomode)disableAutoMode`
- Scope: Any file. Most useful in managed settings, where users can’t override it. Also accepted under permissions as permissions.disableAutoMode.
- Type: the string "disable"
- Default: unset

```
{
  "disableAutoMode": "disable"
}

```
### Remove [auto mode](/docs/en/permission-modes#eliminate-prompts-with-auto-mode) from the Shift+Tab cycle. Any session that would otherwise [start in auto mode](/docs/en/permission-modes#which-mode-a-session-starts-in), whether from --permission-mode auto, a settings file, or the built-in default, starts in default instead. Administrators set it in managed settings to prevent developers in their organization from using auto mode.

****``````
****``
****

settings.json
[​](#permissions)permissions`
- Scope: Any file
- Type: object with allow, ask, deny, additionalDirectories, blockReadsOutsideWorkingDirectories, blockWritesOutsideWorkingDirectories, defaultMode, denyInsteadOfPrompting, disableBypassPermissionsMode, and disableAutoMode
- Default: unset

```
{
  "permissions": {
    "allow": ["Bash(npm run *)"],
    "ask": ["Bash(git push *)"],
    "deny": ["Read(./.env)"],
    "defaultMode": "acceptEdits"
  }
}

```
### Control which tools Claude can use without asking, which ones prompt, and which ones are blocked. Also set the default [permission mode](/docs/en/permission-modes) for new sessions. Every permissions.* key below nests under this object.

****``
****````````````````````
****

This example approves npm run commands without asking, prompts before git push, blocks reads of .env, and starts sessions in acceptEdits:
settings.json
The three rule arrays share one syntax; see [Permission rule syntax](#permission-rule-syntax) under permissions.allow. For how permission rules from different files combine, see [how permission rules merge across scopes](/docs/en/permissions#settings-precedence); for how settings keys in general combine, see [Settings precedence](/docs/en/settings#settings-precedence) on the settings guide.
[​](#useautomodeduringplan)useAutoModeDuringPlan`
  - A false in any of these files or in --settings turns it off, unless you leave that user or local file out with an option such as --setting-sources. Ignoring a left-out file requires Claude Code v2.1.314 or later
  - true: the same as unset; when auto mode is available, the classifier reviews shell commands during planning
  - false: you get a permission prompt for every command outside the built-in read-only set
- Default: true

```
{
  "useAutoModeDuringPlan": false
}

```
### Choose whether Claude Code uses the auto mode classifier to review shell commands in plan mode. With the default true, the classifier reviews each command during planning when auto mode is available and you see no prompt, except for [critical-path removals](/docs/en/permission-modes#critical-paths). Set false to get a permission prompt for every command outside the built-in read-only set. Appears in /config as **Use auto mode during plan**.

****````````

****``
``

****``

settings.json
[​](#permissions-allow)permissions.allow`
- Scope: Any file
- Type: array of permission rule strings
- Default: unset
- Per-session overrides: --allowedTools adds allow rules for one session, and a deny rule from any settings file still blocks a tool it names

```
{
  "permissions": {
    "allow": ["Bash(git diff *)", "Read(~/.zshrc)"]
  }
}

```
#### List the tool uses Claude Code approves without asking you. In an MCP rule, * can appear only in the tool name after the mcp__<server>__ prefix, such as mcp__github__get_*; it can’t appear in the server name.

****``
****
****
****``

This example approves git diff and lets Claude Code read your .zshrc without asking:
settings.json
Claude Code applies allow rules from a project’s .claude/settings.json only after you accept the [workspace trust dialog](/docs/en/permissions#project-allow-rules-and-workspace-trust) for that folder.
[​](#permission-rule-syntax)Permission rule syntax

| Rule | What it matches |
| --- | --- |
| Bash | Every Bash command |
| Bash(npm run *) | Commands starting with npm run |
| Read(./.env) | Reads of the .env file |
| WebFetch(domain:example.com) | Fetch requests to example.com |

### Permission rules follow the format Tool or Tool(specifier). Claude Code evaluates deny rules first, then ask, then allow, and the first match decides regardless of how specific each rule is; see the [permission rule evaluation order](/docs/en/permissions#manage-permissions).
Each row shows one rule shape and what it matches.
````````````
For the complete rule syntax, including wildcard behavior, tool-specific patterns for Read, Edit, WebFetch, MCP, and Agent rules, and the security limitations of Bash patterns, see [Permission rule syntax](/docs/en/permissions#permission-rule-syntax).
[​](#permissions-ask)permissions.ask`
- Scope: Any file
- Type: array of permission rule strings
- Default: unset

```
{
  "permissions": {
    "ask": ["Bash(git push *)"]
  }
}

```
### List the tool uses that prompt you for confirmation even in a permission mode that would otherwise approve them, such as acceptEdits or bypassPermissions. In dontAsk mode Claude Code denies a matching tool use instead of prompting.

****``
****
****

settings.json

[​](#permissions-deny)permissions.deny`
- Scope: Any file
- Type: array of permission rule strings
- Default: unset
- Per-session overrides: --disallowedTools adds deny rules for one session alongside this key

```
{
  "permissions": {
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)",
      "Read(./config/credentials.json)",
      "Bash(curl *)"
    ]
  }
}

```
### List the tool uses Claude Code blocks. Use it for files that hold API keys, secrets, or environment values: Claude Code excludes matching files from file discovery and search results, denies reads of them, and blocks the [Edit and Write tools](/docs/en/permissions#read-and-edit) on the matching paths.
Read and Edit deny rules apply to Claude’s built-in file tools, to file commands Claude Code recognizes in Bash, such as cat, head, tail, sed, and tee, and to the targets of Bash [redirections](/docs/en/permissions#redirections) such as > file and < file; they don’t apply to a command that reads files without naming them, such as grep -r pattern ., or to arbitrary subprocesses, so for OS-level enforcement [enable the sandbox](/docs/en/sandboxing).

****``
****
****
****``

This example denies reads of .env files, the secrets directory, and a credentials file, and blocks curl commands:
settings.json
Tool names accept glob patterns, so "*" denies every tool and "mcp__*" denies every MCP tool. Claude Code ignores a deny rule for the [EndConversation](/docs/en/tools-reference#endconversation-tool-behavior) tool as long as any other tool is still available to Claude. A Bash deny rule matches the command as Claude writes it, so Bash(curl *) doesn’t stop /usr/bin/curl or sh -c 'curl …'; see [what a Bash rule doesn’t match](/docs/en/permissions#bash-rule-limits). This key replaces the deprecated ignorePatterns configuration.
[​](#permissions-additionaldirectories)permissions.additionalDirectories`
- Scope: Any file, with limits on the sandbox write access that project and local entries give
- Type: array of directory paths
- Default: unset
- Per-session overrides: --add-dir and /add-dir add directories for one session alongside this key

```
{
  "permissions": {
    "additionalDirectories": ["../docs/"]
  }
}

```
### Give Claude file access to directories outside the one you started in, as additional [working directories](/docs/en/permissions#working-directories). Most .claude/ configuration is [not discovered](/docs/en/permissions#additional-directories-grant-file-access-not-configuration) from these directories.

****``
****
****
****````

settings.json
Like allow rules, entries in a project’s .claude/settings.json take effect only after you accept the [workspace trust dialog](/docs/en/permissions#project-allow-rules-and-workspace-trust) for that folder.
[​](#permissions-blockreadsoutsideworkingdirectories)permissions.blockReadsOutsideWorkingDirectories`
- Actions no mode auto-approves covers when a shell command that reads such a path prompts you
- Sandboxed commands under the block covers what a sandboxed command can read
- Scope: Any file. A true in any file applies, so a repository can turn the block on for itself but can’t lift yours.
  - true: Claude’s file tools refuse reads outside the working directories
  - false: the same as unset; the block still applies if another file sets true
- Default: unset, so reads outside the working directories follow your permission mode

```
{
  "permissions": {
    "blockReadsOutsideWorkingDirectories": true
  }
}

```
#### Make Claude’s file tools refuse reads outside your [working directories](/docs/en/permissions#working-directories) in every permission mode, including bypassPermissions. Claude Code denies Read, Grep, Glob, and LSP calls on those paths and tells Claude to ask you to add the directory with /add-dir. Files Claude Code itself needs stay readable, such as your skills, plugins, rules, agents, commands, and the CLAUDE.md memory file under ~/.claude/. Requires Claude Code v2.1.257 or later.
Claude Code doesn’t refuse shell commands the same way:

A Bash command the shell parser can’t trace, such as one that changes directory more than once or runs a subshell, prompts you even in auto mode and bypassPermissions mode. The prompt appears even when the command names no path outside the working directories. This prompt doesn’t apply when the command runs in the [sandbox](/docs/en/sandboxing) and the sandbox enforces the block.
Claude Code also writes true here when you choose to block such reads on [auto mode’s prompt before the first read outside the working directories](/docs/en/permission-modes#first-read-outside-the-working-directories).

****````
****``
````

****

settings.json
To lift the block, remove the key from every settings file that sets it, then restart each running session.
Directories you add with --add-dir, /add-dir, or additionalDirectories in your user or managed settings count as working directories for the block. Directories added only in repository settings don’t count: those in .claude/settings.json, and those in .claude/settings.local.json unless git reports that file as untracked. In a directory that isn’t a git repository, or when git tracks the file, Claude Code treats .claude/settings.local.json as repository settings, so put directories you want to keep readable in your user settings instead.
When [autoMemoryDirectory](#automemorydirectory) comes from the project’s .claude/settings.json, or from a .claude/settings.local.json [treated as repository-supplied](/docs/en/permissions#when-your-local-settings-file-needs-trust), Claude Code loads no [auto memory](/docs/en/memory#storage-location) from that directory and saves none to it.
[​](#sandboxed-commands-under-the-block)Sandboxed commands under the block
- Filesystem isolation is off through sandbox.filesystem.disabled
- allowManagedReadPathsOnly is set
- The path of the directory you started Claude Code in contains a glob character such as *, ?, or [
- ~/.gitconfig
- The config, ignore, and attributes files under $XDG_CONFIG_HOME/git, which defaults to ~/.config/git
- Files your global git configuration names through [include], [includeIf], core.excludesFile, or core.attributesFile
### When [sandboxing](/docs/en/sandboxing) is on, the block also covers sandboxed commands. Claude Code denies them read access to your home directory and to the other roots that hold user files: /Users, /home, /root, /Volumes, /mnt, /media, /run/media, and /srv. It then re-opens the working directories, [worktrees](/docs/en/worktrees) Claude Code creates in the session, the session temp directory, and the parts of ~/.claude that commands need, such as skills and plugins. While the block is in force, allowRead and allowWrite entries from repository settings don’t count.
When the session’s working directory is a linked [git worktree](/docs/en/worktrees), including one Claude Code entered mid-session, the repository’s common .git directory stays readable and writable to sandboxed commands, so git keeps working there.
In these cases the block doesn’t reach sandboxed commands, while Claude’s file tools keep enforcing it:

``
``
``````

Under the block, Claude Code re-opens your global git configuration files to sandboxed commands so git keeps your identity and settings:

``
``````````
````````

Claude Code judges each file separately. When a file lies where a sandboxed command can write, directly or through a symlink, Claude Code doesn’t re-open the files it names.
On Linux and WSL2, a configuration file that is a symlink can stay unreadable at its own path, and git then runs without it. ~/.git-credentials and $XDG_CONFIG_HOME/git/credentials stay blocked.
If a re-opened file holds a secret, such as an http.extraHeader token, add its path to [sandbox.filesystem.denyRead](#sandbox-filesystem-denyread). A denyRead entry that covers a file always takes precedence over this re-open.
[​](#permissions-blockwritesoutsideworkingdirectories)permissions.blockWritesOutsideWorkingDirectories`
- Scope: Any file. A true in any file the session loads applies, so a repository can turn the block on for itself but can’t lift yours. In a cloud session, Claude Code might not apply the key, because the file tools run in a container that is itself the boundary.
  - true: turns the block on
  - false: the same as unset; the block still applies if another file sets true
- Default: unset, so writes outside the working directories follow your permission mode. The block is also on while Claude Code can’t read the permissions object in your managed settings.

```
{
  "permissions": {
    "blockWritesOutsideWorkingDirectories": true
  }
}

```
#### Make the Write, Edit, and NotebookEdit tools refuse paths outside your [working directories](/docs/en/permissions#working-directories) in every permission mode, including bypassPermissions, apart from [some of Claude Code’s own files](#what-the-write-block-refuses-and-what-stays-writable). The key doesn’t limit shell commands, MCP tools, or the programs hooks run. To limit where shell commands write, turn on [sandboxing](/docs/en/sandboxing). Requires Claude Code v2.1.314 or later.
Once the key is on, Claude Code also removes the EnterWorktree and ExitWorktree tools or refuses calls to them. To keep working in worktrees, follow [Claude has no EnterWorktree tool](/docs/en/worktrees#claude-has-no-enterworktree-tool).

****````
****``
````

****``

settings.json
To test the block, ask Claude to use the Write tool to create a file outside your working directories, such as ~/block-test.txt if your home directory isn’t one of them. Claude Code refuses the call, and the refusal says the [setting blocks writes outside the working directories](/docs/en/errors#setting-blocks-writes-outside-the-working-directories).
To lift the block, remove the key from every settings file that sets it, then restart Claude Code.
[​](#what-the-write-block-refuses-and-what-stays-writable)What the write block refuses and what stays writable
- Claude Code settings files: Claude Code refuses these writes inside the working directories too, because a settings file can lift the block. Edit settings files yourself.
- A directory that only repository settings add: one that additionalDirectories lists only in .claude/settings.json, or in .claude/settings.local.json unless git reports that file as untracked
- A subagent’s worktree: an isolation: worktree subagent’s file edits are refused when its worktree sits outside the working directories
- Auto memory in a directory the repository chose: a directory that autoMemoryDirectory names in repository settings
#### Some of Claude Code’s own files stay writable, such as plan files, the [scratchpad](/docs/en/claude-directory#session-scratchpad-directory), a [background session](/docs/en/agent-view)’s tmp directory, and .md files in this project’s [auto memory](/docs/en/memory#storage-location).
Along with your own files outside the working directories, the block refuses writes to:

****
****``````
****``
****``

Settings files stay refused whatever you add. To let a write through in any of the other cases, [add a working directory](#let-one-directory-through-the-read-or-write-block). /add-dir needs a directory that exists, so name the .claude/worktrees directory at the repository root for subagent worktrees.
[​](#let-one-directory-through-the-read-or-write-block)Let one directory through the read or write block
### To let Claude reach one directory outside the project while blockReadsOutsideWorkingDirectories or blockWritesOutsideWorkingDirectories is true, add it as a working directory. Run /add-dir <directory> in the session, pass --add-dir <directory> when you start Claude Code, or list it under additionalDirectories in your user or managed settings. No [allow rule](/docs/en/permissions#read-and-edit) lets Claude’s file tools through either block.
[​](#permissions-defaultmode)permissions.defaultMode`
- Scope: Any file. auto and bypassPermissions don’t take effect from project or local settings, so set them in ~/.claude/settings.json instead. Before v2.1.257, bypassPermissions took effect from any file. For conversations the VS Code extension starts, Claude Code reads only user, managed, and --settings values.
  - "default": Claude Code runs only reads without asking
  - "acceptEdits": Claude Code also runs file edits and common filesystem commands such as mkdir and mv without asking
  - "plan": Claude Code reads and plans but blocks edits until you approve a plan
  - "auto": Claude Code runs without routine prompts; before actions such as shell commands and network requests run, a background classifier checks that they align with your request
  - "dontAsk": Claude Code auto-denies every call that would otherwise prompt, though a mod you installed can still approve some of those calls. File reads inside your working directories, other actions that need no approval, and pre-approved tools still run, apart from reads from network paths
  - "bypassPermissions": Claude Code runs everything without asking
  - "manual": an alias for "default"
- Default: unset
- Per-session overrides: --permission-mode, and its equivalent --dangerously-skip-permissions for bypassPermissions, take precedence over this key for one session

```
{
  "permissions": {
    "defaultMode": "acceptEdits"
  }
}

```
### Set the default [permission mode](/docs/en/permission-modes) for new sessions. When you leave it unset, the [built-in default](/docs/en/permission-modes#which-mode-a-session-starts-in) for your surface applies.

****````````````
****``
``````
``
``
``
``
````

****
****``````

settings.json
Permission rules layer on top of every mode: deny rules block in every mode, including bypassPermissions. See [Permission modes](/docs/en/permission-modes). In cloud sessions, Claude Code honors only acceptEdits, plan, default, and auto from this key. For conversations the VS Code extension starts, see [which setting the extension reads for the starting permission mode](/docs/en/permission-modes#switch-permission-modes).
[​](#permissions-denyinsteadofprompting)permissions.denyInsteadOfPrompting`
- Scope: User or managed, and --settings. A repository can’t set it for you.
  - true: Claude Code denies calls that would otherwise prompt
  - false: the same as unset; calls are still denied if another of these sources sets true
- Default: unset, so a call that needs approval prompts you

```
{
  "permissions": {
    "defaultMode": "auto",
    "denyInsteadOfPrompting": true
  }
}

```
#### Set this to true to keep a session running when nobody is there to answer a permission prompt. Claude Code denies a tool call that would otherwise wait on a prompt, and the turn continues. Requires Claude Code v2.1.319 or later.
A call goes ahead if an allow rule, your [permission mode](/docs/en/permission-modes), or auto mode’s classifier approves it. To allow most calls that would otherwise prompt, answer from a [PermissionRequest hook](/docs/en/hooks#permissionrequest).

****````
****``
````

****

In ~/.claude/settings.json, this example starts sessions in auto mode and denies whatever would still fall back to a prompt:
settings.json
The key applies in -p runs, interactive terminal sessions, the [VS Code extension](/docs/en/vs-code), local sessions in the [Desktop app](/docs/en/desktop), [subagents](/docs/en/sub-agents), and [agent teams](/docs/en/agent-teams). To deny what would prompt in a single [non-interactive](/docs/en/headless) run instead, pass [--permission-prompts none](/docs/en/headless#turn-off-permission-prompts-in-unattended-runs) with -p.
[​](#what-else-denyinsteadofprompting-stops)What else denyInsteadOfPrompting stops
- Question and plan tools: Claude Code leaves out AskUserQuestion, EnterPlanMode, and ExitPlanMode, so a session in plan mode can’t leave it on its own. A teammate in an agent team keeps EnterPlanMode and ExitPlanMode
- MCP elicitation: Claude Code cancels an elicitation request unless an Elicitation hook answers it
- Permission hosts: Claude Code doesn’t ask your canUseTool callback or --permission-prompt-tool. To approve calls from code, answer from a PermissionRequest hook. Some calls are denied before any hook is asked, such as a critical-path removal in auto mode that no ask rule covers.
- Classifier billing notice: where the notice about billed classifier requests would open a dialog, Claude Code doesn’t show it and denies the actions that need those requests
#### With the setting on, Claude Code also stops these requests for an answer:

****``````````
****``
****````````
****

A session can still wait on the [workspace trust dialog](/docs/en/permissions#project-allow-rules-and-workspace-trust) and on [project MCP server approval](/docs/en/mcp#project-server-approvals-and-workspace-trust). Answer both before you leave the session running.
[​](#messages-from-denyinsteadofprompting)Messages from denyInsteadOfPrompting`

```
Permission for this tool use was denied. It requires approval, and this session has no approval surface

```

```
no approval surface in this session; permission request denied automatically

```

```
20 actions were refused and no work went ahead in between, so Claude stopped.

```
### These messages report refused calls. They aren’t prompts, so nothing waits for your answer.
The denial Claude reads can open with this text:

In stream-json output, [the runs that emit a permission_denied message](/docs/en/agent-sdk/typescript#sdkpermissiondeniedmessage) report this decision_reason:

In auto mode with the setting on, the turn ends after 20 calls in a row that the classifier blocked or a [safety check refused](/docs/en/errors#auto-mode-cannot-determine-the-safety-of-an-action), and you see this message:

A -p run reports that turn as error_during_execution.
[​](#permissions-disablebypasspermissionsmode)permissions.disableBypassPermissionsMode`
- Scope: Any file. Typically set in managed settings to enforce organizational policy.
- Type: the string "disable"
- Default: unset
- Per-session overrides: this key takes precedence over --dangerously-skip-permissions, which Claude Code rejects while the key is set

```
{
  "permissions": {
    "disableBypassPermissionsMode": "disable"
  }
}

```
### Prevent anyone from entering bypassPermissions mode. Claude Code then rejects the --dangerously-skip-permissions flag, and ignores an [agent definition’s](/docs/en/sub-agents#permission-modes) permissionMode: bypassPermissions, so the subagent runs with the parent session’s permission mode.

****``
****``
****
****``

settings.json
Before v2.1.223, Claude Code applied the frontmatter permission mode even with bypass disabled.
[​](#skipautopermissionprompt)skipAutoPermissionPrompt`
- Scope: User or managed. A repository can’t set it for you.
  - true: Claude Code skips the notice
  - false: the same as unset; the notice appears once unless another of these files sets true
- Default: unset, so the notice appears once

```
{
  "skipAutoPermissionPrompt": true
}

```
### Skip the one-time notice describing [auto mode](/docs/en/permission-modes#eliminate-prompts-with-auto-mode) that Claude Code shows when you first enter auto mode yourself, for example through your own settings or the mode selector, rather than when the built-in default starts a session in it. Claude Code shows that notice once and then records that it was shown, so this key only matters where the notice hasn’t appeared yet.

****``
****``
````

****

settings.json
[​](#skipdangerousmodepermissionprompt)skipDangerousModePermissionPrompt`
- Scope: User, local, or managed. An untrusted repository can’t skip the dialog for you.
  - true: Claude Code skips the confirmation dialog before a session enters bypassPermissions mode
  - false: the same as unset; the dialog appears unless another of these files sets true
- Default: unset, so the dialog appears

```
{
  "skipDangerousModePermissionPrompt": true
}

```
## Skip the confirmation dialog Claude Code shows before a session enters bypassPermissions mode, whether from --dangerously-skip-permissions or from defaultMode: "bypassPermissions". Claude Code writes true here in your user settings when you accept that dialog once.

****``
****````
````

****

settings.json
[​](#sandbox-settings)Sandbox settings
### Isolate the commands Claude runs from your filesystem, your network, and your credentials. For how sandboxing works and platform requirements, see [Sandboxing](/docs/en/sandboxing).
[​](#sandbox)sandbox`
- Scope: Any file
- Type: object with enabled, failIfUnavailable, autoAllowBashIfSandboxed, excludedCommands, allowUnsandboxedCommands, enableWeakerNestedSandbox, enableWeakerNetworkIsolation, allowAppleEvents, allowNestedUserNamespaces, bwrapPath, socatPath, ignoreViolations, and ripgrep, plus the filesystem, network, and credentials objects
- Default: unset, so Claude Code runs commands without a sandbox

```
{
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": true,
    "excludedCommands": ["docker *"],
    "filesystem": {
      "allowWrite": ["/tmp/build", "~/.kube"],
      "denyRead": ["~/.aws/credentials"]
    },
    "network": {
      "allowedDomains": ["github.com", "*.npmjs.org"]
    }
  }
}

```
### Isolate the Bash commands Claude runs from your filesystem and network with [sandboxing](/docs/en/sandboxing). Turn the sandbox on with enabled, then narrow or widen what sandboxed commands can touch with the filesystem, network, and credentials sub-objects. The sandbox runs on macOS, Linux, and WSL2.

****``
****````````````````````````````````
****

This turns the sandbox on, skips permission prompts for sandboxed commands, runs docker outside the sandbox, opens two extra write paths, hides your AWS credentials file, and pre-allows GitHub and npm:
settings.json
When managed settings set a Boolean key such as enabled or failIfUnavailable, that value overrides anything a developer sets. Claude Code merges array keys across the settings scopes the session loads, so a developer can append entries; see [Keep developers from widening the policy](/docs/en/sandboxing#keep-developers-from-widening-the-policy) for the managed-only locks. To require the sandbox for an organization, see [Enforce sandboxing with managed settings](/docs/en/sandboxing#enforce-sandboxing-with-managed-settings).
[​](#sandbox-enabled)sandbox.enabled`
- Scope: Any file, with limits on project and local settings
  - true: Claude Code sandboxes Bash commands
  - false: Bash commands run unsandboxed
- Default: false

```
{
  "sandbox": {
    "enabled": true
  }
}

```
### Turn on [sandboxing](/docs/en/sandboxing) for Bash commands. When you pick a mode in the /sandbox panel, Claude Code writes this key to .claude/settings.local.json for the current project; set it in ~/.claude/settings.json to sandbox every project.

****``
****``
``

****``

settings.json
On Linux and WSL2 the sandbox needs bubblewrap and socat; see [Set up Linux and WSL2](/docs/en/sandboxing#set-up-linux-and-wsl2). When the sandbox can’t start, Claude Code runs commands unsandboxed unless you also set [failIfUnavailable](#sandbox-failifunavailable).
[​](#sandbox-failifunavailable)sandbox.failIfUnavailable`
- Scope: Any file, with limits on project and local settings
  - true: Claude Code exits with an error at startup when sandbox.enabled is true but the sandbox can’t start. If the sandbox passes that check and then fails to initialize, the session keeps running and Claude Code refuses each sandboxed command
  - false: Claude Code runs commands unsandboxed when the sandbox can’t start
- Default: false

```
{
  "sandbox": {
    "enabled": true,
    "failIfUnavailable": true
  }
}

```
### Make Claude Code exit with an error at startup when sandbox.enabled is true but the sandbox can’t start because the platform doesn’t support it or the dependency check fails. Without this key, Claude Code runs commands unsandboxed. Managed deployments that require sandboxing as a security gate can use this setting.
On a platform the sandbox doesn’t support, Claude Code doesn’t start with this key on. See [Enforce sandboxing with managed settings](/docs/en/sandboxing#enforce-sandboxing-with-managed-settings).

****``
****``````
``

****``

This turns the sandbox on for managed machines and sets failIfUnavailable to true:
managed-settings.json
See [Enforce sandboxing with managed settings](/docs/en/sandboxing#enforce-sandboxing-with-managed-settings).
[​](#sandbox-autoallowbashifsandboxed)sandbox.autoAllowBashIfSandboxed`
- Scope: Any file
  - true: Claude Code runs sandboxed Bash commands without a permission prompt, except in the cases that Auto-allow mode describes; CLAUDE_CODE_SUBPROCESS_ENV_SCRUB turns auto-allow off
  - false: sandboxed commands go through the regular permission flow, so your allow rules and permission mode decide. The /sandbox Mode tab calls this regular permissions mode
- Default: true

```
{
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": false
  }
}

```
### Let Claude Code run sandboxed Bash commands without a permission prompt. Commands that can’t run in the sandbox still go through the regular permission flow, and deny rules and content-scoped ask rules such as Bash(git push *) still apply; a bare Bash ask rule is skipped for sandboxed commands. Set it to false to send sandboxed commands through the regular permission flow too, which the /sandbox **Mode** tab calls regular permissions mode.

****``
****````
****

****``

This keeps the sandbox on and sends sandboxed commands through the regular permission flow:
settings.json
See [Auto-allow mode](/docs/en/sandboxing#auto-allow-mode) for what auto-allow mode still prompts on and how it behaves in plan mode.
[​](#sandbox-excludedcommands)sandbox.excludedCommands`
- Scope: Any file, with limits on project and local settings
- Type: array of command patterns
- Default: unset, so no command is excluded

```
{
  "sandbox": {
    "excludedCommands": ["docker *"]
  }
}

```
- A command starting with sudo, eval, or xargs
- A cd, pushd, or popd, wherever it appears in the call
- A command substitution, a subshell, or a control-flow block such as if or for
- A redirection, such as docker build . > build.log or a <<EOF heredoc, other than one that only duplicates a file descriptor, as 2>&1 does
- A command name that comes from a variable
- A git clone, git init, git worktree add, git worktree move, or git bundle create with a path argument that is absolute, starts with ~, or contains a .. segment
### Name commands that Claude Code runs outside the sandbox, such as tools that don’t work under it. Each entry uses the same syntax as the content of a Bash(...) [permission rule](/docs/en/permissions#permission-rule-syntax): an exact command, a prefix such as docker *, or a wildcard pattern. A pattern with no wildcard is an exact match, so docker matches only docker with no arguments.
Your entries take a Bash call out of the sandbox only when they cover every command in it, and some call shapes stay sandboxed even then. A docker * entry alone doesn’t take npm ci && docker build . out of the sandbox.

****``
****
****

settings.json
Claude Code keeps a Bash call sandboxed when it has one of these shapes, among others:

``````
``````
````
``````

``````````````

For example, cd build && docker compose up stays sandboxed under a docker * entry, and adding a cd entry doesn’t change that. Under a git * entry, git clone <url> vendor/lib runs outside the sandbox, but git clone <url> ~/tools stays sandboxed. A clone writes a whole tree of files, possibly executable ones, wherever its destination path points.
Excluded commands still go through the regular permission flow. Exclusion is a convenience, not a security boundary: when a tool only needs to write somewhere specific, [filesystem.allowWrite](#sandbox-filesystem-allowwrite) keeps it sandboxed.
Entries from the settings scopes the session loads combine into one list unless the sandbox is [admin-required](/docs/en/sandboxing#repository-settings-under-an-admin-required-sandbox). While it is, Claude Code ignores entries in .claude/settings.json and .claude/settings.local.json, so a cloned repository can’t take commands out of the sandbox. Entries in managed settings, --settings, and your ~/.claude/settings.json still apply, and no managed-only lock covers this list.
[​](#sandbox-allowunsandboxedcommands)sandbox.allowUnsandboxedCommands`
- Scope: Any file, with a limit on project and local settings
  - true: Claude can retry a command outside the sandbox with the dangerouslyDisableSandbox parameter after the sandbox blocks it
  - false: Claude Code ignores that parameter, so while the sandbox is running, commands Claude runs are sandboxed unless they match an excludedCommands entry
- Default: true

```
{
  "sandbox": {
    "enabled": true,
    "allowUnsandboxedCommands": false
  }
}

```
### Let Claude retry a command outside the sandbox with the dangerouslyDisableSandbox parameter after the sandbox blocks it. When it’s false, Claude Code ignores that parameter. While the sandbox is running, commands Claude runs are then sandboxed unless they match an [excludedCommands](#sandbox-excludedcommands) entry. The /sandbox **Overrides** tab shows that state as **Strict sandbox mode**. A false in managed settings turns on strict sandbox mode for the developers it covers.

****``
****````
````

****``

This enforces strict sandbox mode for everyone the managed settings cover:
managed-settings.json
A false from managed settings or --settings also makes the sandbox [admin-required](/docs/en/sandboxing#repository-settings-under-an-admin-required-sandbox). A false in your user settings holds against a project’s true but doesn’t make the sandbox admin-required. Holding against a project’s value requires Claude Code v2.1.285 or later.
Who approves an unsandboxed retry depends on your permission mode and allow rules. See [The unsandboxed retry escape hatch](/docs/en/sandboxing#the-unsandboxed-retry-escape-hatch).
To see when commands you type yourself at the [! shell-mode prompt](/docs/en/interactive-mode#shell-mode-with-prefix) run sandboxed, see [strict sandbox mode](/docs/en/sandboxing#turn-off-the-retry-with-strict-sandbox-mode).
[​](#sandbox-filesystem)sandbox.filesystem`
- Scope: Any file
- Type: object with allowWrite, denyWrite, denyRead, and allowRead arrays, plus the allowManagedReadPathsOnly and disabled Booleans
- Default: unset, so the default read and write boundaries apply

```
{
  "sandbox": {
    "filesystem": {
      "allowWrite": ["/tmp/build", "~/.kube"],
      "denyRead": ["~/.aws/credentials"]
    }
  }
}

```
#### Control which paths sandboxed commands can read and write. By default they can write to the working directory, the per-user temp directory, and directories you add with --add-dir, /add-dir, or permissions.additionalDirectories, and can read the rest of the filesystem, including credential files. Widen or narrow that with the four path lists, or switch the filesystem layer off with disabled. See [Filesystem isolation](/docs/en/sandboxing#filesystem-isolation) for the default boundaries.

****``
****````````````
****

This lets sandboxed commands write to a build directory and your kubeconfig, and hides your AWS credentials file:
settings.json
Claude Code enforces these lists at the OS sandbox boundary, so they apply to every subprocess a sandboxed command starts, such as kubectl, terraform, or npm. Claude Code adds your [permission rules](/docs/en/sandboxing#permission-rules) to the same lists: Edit allow and deny rules to allowWrite and denyWrite, Read deny rules to denyRead, and WebFetch(domain:...) allow and deny rules to the [network](#sandbox-network) domain lists.
Unless a lock applies, Claude Code merges these lists across the settings files the session loads. [allowManagedReadPathsOnly](#sandbox-filesystem-allowmanagedreadpathsonly) limits allowRead to entries from managed settings, and [allowManagedDomainsOnly](#sandbox-network-allowmanageddomainsonly) does the same for allowed domains. [Repository locks](/docs/en/sandboxing#repository-settings-under-an-admin-required-sandbox) leave out entries from a repository’s settings files.
[Configure sandboxing](/docs/en/sandboxing#configure-sandboxing) covers sources you exclude with --setting-sources. When you edit a list during a session, Claude Code [applies the change to the running session](/docs/en/settings#when-edits-take-effect).
[​](#sandbox-path-prefixes)Sandbox path prefixes

| Prefix | Meaning | Example |
| --- | --- | --- |
| / | Absolute path from filesystem root | /tmp/build stays /tmp/build |
| ~/ | Relative to home directory | ~/.kube becomes $HOME/.kube |
| ./ or no prefix | Relative to the project root for project settings, or to ~/.claude for user settings | ./output in .claude/settings.json resolves to <project-root>/output |

##### Paths in allowWrite, denyWrite, denyRead, allowRead, and [credentials.files](#sandbox-credentials-files) resolve by their prefix:
``````````````````````
The //path prefix for absolute paths also works. If you use single-slash /path expecting project-relative resolution, switch to ./path. This syntax differs from [Read and Edit permission rules](/docs/en/permissions#read-and-edit), which use //path for absolute and /path for project-relative: sandbox filesystem paths use standard conventions, so /tmp/build is an absolute path.
Claude Code strips a trailing slash from a directory path, so ~/.aws and ~/.aws/ match the same directory. Before v2.1.224, Claude Code passed the trailing slash through to the sandbox, and Claude could still read or write paths under a denyRead or denyWrite entry written with one.
Where wildcards work in sandbox paths

| sandbox.filesystem list | What works on Linux and WSL2 | Example that doesn’t work on Linux and WSL2 | What to write instead |
| --- | --- | --- | --- |
| denyRead, allowRead | A trailing /** works, so ~/build/** covers the same directory as ~/build. Any other wildcard works only after the first directory name of the entry’s full path. | /**/*.pem in denyRead covers nothing, so it blocks no reads | /srv/**/*.pem, with one entry for each top-level directory |
| allowWrite, denyWrite | Only a trailing /** works, so ~/build/** covers the same directory as ~/build | ./src/* covers only a file or directory in src that is itself named *, and nothing when there is none | ./src, which covers everything under src, or one entry for each path |

```
~/keys/*.pem              the entry
/home/alice/keys/*.pem    its full path
 ^^^^                     the first directory name, home

```
##### The wildcards *, ?, and ** work in all four sandbox.filesystem path lists on macOS and in fewer places on Linux and WSL2:
``````````````````````````````````````
In ~/keys/*.pem, the wildcard comes after the first directory name, which is home for a home directory of /home/alice:

On Linux and WSL2, the **Config** tab of /sandbox in a session warns about Edit permission rules that contain a wildcard other than a trailing /**. Those wildcards don’t work for sandboxed commands. Add each path the rule should cover, or the directory that holds them, to allowWrite for an allow rule or denyWrite for a deny rule.
Directory names with brackets, braces, or parentheses

```
app/
└── [slug]/
    └── page.tsx

```
- Brackets such as [slug]: in every list on macOS, and in denyRead and allowRead on Linux and WSL2, the brackets in ./app/[slug] are also a pattern. The entry then also matches any path under app named with one character from slug, such as app/s or app/g. With that entry in allowRead, or in allowWrite on macOS, sandboxed commands can reach those paths as well. Rename any they shouldn’t reach.
- Brackets such as [user-id] or [post-id], where the hyphen’s left character sorts after its right: ./app/[user-id] covers only the directory with exactly that name, in every list on every platform. Before v2.1.304, sandboxed commands on Linux and WSL2 failed to start while denyRead or allowRead held such an entry.
- Braces and parentheses: these are ordinary characters, so ~/data/{keys,tokens} covers one directory named {keys,tokens}, not two alternatives. To cover ~/data/keys and ~/data/tokens, add each as its own entry.
### To allow or block a directory whose name contains brackets, write the name as it is, such as ./app/[slug]. In that entry, [slug] is the directory’s real name, brackets included:

That entry covers everything under the directory, so leave off a trailing /**. On macOS and on Linux and WSL2, the app/[slug] directory has to exist when the sandboxed command starts.

``````````````````
``````
****````````

[​](#sandbox-filesystem-allowwrite)sandbox.filesystem.allowWrite`
- Scope: Any file, with limits on project and local settings
- Type: array of path strings, using the sandbox path prefixes
- Default: unset, so sandboxed commands can write to the working directory, the per-user temp directory, directories you’ve added with --add-dir or /add-dir, and directories in permissions.additionalDirectories

```
{
  "sandbox": {
    "filesystem": {
      "allowWrite": ["/tmp/build", "~/.kube"]
    }
  }
}

```
### Add paths where sandboxed commands can write, beyond the working directory, the per-user temp directory, and the directories you’ve added with --add-dir, /add-dir, or permissions.additionalDirectories. Use it when a subprocess such as kubectl or a build tool needs to write outside the project.

****``
****
****``````

This lets a build write under /tmp/build and lets kubectl update your kubeconfig:
settings.json
Claude Code merges allowWrite entries and the paths from your Edit(...) allow permission rules across the settings scopes the session loads, leaving out the ones from repository settings while [permissions.blockReadsOutsideWorkingDirectories](#sandboxed-commands-under-the-block) is on. [Repository locks](/docs/en/sandboxing#repository-settings-under-an-admin-required-sandbox) can leave out a repository’s entries too. An allowWrite entry can’t lift a [protected path](/docs/en/sandboxing#protected-paths).
[​](#sandbox-filesystem-denywrite)sandbox.filesystem.denyWrite`
- Scope: Any file
- Type: array of path strings, using the sandbox path prefixes
- Default: unset

```
{
  "sandbox": {
    "filesystem": {
      "denyWrite": ["/etc", "/usr/local/bin"]
    }
  }
}

```
### Block sandboxed commands from writing to specific paths, including paths inside a directory that is otherwise writable.

****``
****
****

This keeps sandboxed commands from changing system configuration or installing binaries:
settings.json
Claude Code merges entries across every settings scope the session loads, and adds the paths from your Edit(...) deny permission rules.
[​](#sandbox-filesystem-denyread)sandbox.filesystem.denyRead`
- Scope: Any file
- Type: array of path strings, using the sandbox path prefixes
- Default: unset, so sandboxed commands keep the default read access, which includes credential files such as ~/.aws/credentials

```
{
  "sandbox": {
    "filesystem": {
      "denyRead": ["~/.aws/credentials"]
    }
  }
}

```
### Block sandboxed commands from reading specific paths, such as credential files that the default read policy would otherwise expose. To protect a credential file and keep it usable through the sandbox proxy, see [sandbox.credentials](#sandbox-credentials) instead.

****``
****
****``

settings.json
Claude Code merges entries across every settings scope the session loads, and adds the paths from your Read(...) deny permission rules. When [filesystem.disabled](#sandbox-filesystem-disabled) is true, Claude Code doesn’t enforce these entries.
[​](#sandbox-filesystem-allowread)sandbox.filesystem.allowRead`
- Scope: Any file, with limits on project and local settings
- Type: array of path strings, using the sandbox path prefixes
- Default: unset

```
{
  "sandbox": {
    "filesystem": {
      "denyRead": ["~/"],
      "allowRead": ["."]
    }
  }
}

```
### Re-open reading for specific paths inside a region that [denyRead](#sandbox-filesystem-denyread) blocks, to build workspace-only read access. An exact or wildcard denyRead entry stays blocked inside a broader allowRead, as the [overlap table](/docs/en/sandboxing#configure-sandboxing) shows. When a wildcard denyRead entry such as ~/**/.env matches a directory, Claude Code blocks reads of its contents as well. Before v2.1.236 on macOS, Claude Code re-opened the paths a wildcard denyRead entry matched wherever a broader allowRead entry covered them, and left a matched directory’s contents readable.

****``
****
****

This blocks reads of your home directory except the project itself:
settings.json
Claude Code resolves a . entry to the project root in project settings and to ~/.claude in user settings. Claude Code merges entries across the settings files the session loads unless [allowManagedReadPathsOnly](#sandbox-filesystem-allowmanagedreadpathsonly) is set, and leaves out entries from repository settings while [permissions.blockReadsOutsideWorkingDirectories](#sandboxed-commands-under-the-block) is on. [Repository locks](/docs/en/sandboxing#repository-settings-under-an-admin-required-sandbox) can leave out a repository’s entries too.
[​](#sandbox-filesystem-allowmanagedreadpathsonly)sandbox.filesystem.allowManagedReadPathsOnly`
- Scope: Managed
  - true: Claude Code honors only the allowRead entries from managed settings
  - false: allowRead entries from other settings files can merge in
- Default: false

```
{
  "sandbox": {
    "filesystem": {
      "denyRead": ["~/"],
      "allowRead": ["~/work"],
      "allowManagedReadPathsOnly": true
    }
  }
}

```
### Honor only the [allowRead](#sandbox-filesystem-allowread) entries that come from managed settings, so developers can’t re-open read access to paths your organization blocked. Claude Code still merges denyRead entries from every settings scope the session loads.

****``
****````
````

****``

This blocks reads of the home directory, re-opens ~/work, and stops developers from re-opening anything else:
managed-settings.json
See [Keep developers from widening the policy](/docs/en/sandboxing#keep-developers-from-widening-the-policy).
[​](#sandbox-filesystem-disabled)sandbox.filesystem.disabled`
- Scope: User or managed. When managed settings configure sandbox.filesystem at all, or list a sandbox.credentials.files entry with "mode": "deny", only managed settings can set it.
  - true: Claude Code skips filesystem isolation and keeps network isolation
  - false: filesystem isolation stays on
- Default: false, so filesystem isolation stays on

```
{
  "sandbox": {
    "enabled": true,
    "filesystem": {
      "disabled": true
    },
    "network": {
      "allowedDomains": ["github.com", "*.npmjs.org"]
    }
  }
}

```
### Skip filesystem isolation while keeping network isolation. Sandboxed commands get unrestricted read and write access to the host filesystem, and their network egress stays confined to [network.allowedDomains](#sandbox-network-alloweddomains). Use it when you sandbox to control where commands connect rather than what they write.

****````````
****``
``

****``

This leaves the filesystem open and confines network egress to GitHub and npm:
settings.json
With the layer off, Claude Code doesn’t enforce denyRead or credentials.files deny entries, while credentials.envVars entries and applied mask entries keep working. [autoAllowBashIfSandboxed](#sandbox-autoallowbashifsandboxed) still defaults to true, so set it to false to keep prompting. See [Disable filesystem isolation](/docs/en/sandboxing#disable-filesystem-isolation) for the full list of sources that can set it and what changes when isolation is off.
[​](#sandbox-ignoreviolations)sandbox.ignoreViolations`
- Scope: Any file, with limits on project and local settings
- Type: object mapping a command substring to an array of violation substrings, usually paths
- Default: unset, so every violation is reported

```
{
  "sandbox": {
    "ignoreViolations": {
      "*": ["/etc/hosts"]
    }
  }
}

```
### Silence sandbox violation reports for paths you expect a command to probe and be refused, such as a tool that checks /etc/hosts on startup, so those denials don’t show up as violations or in what Claude sees. The sandbox still blocks the access; only the report is suppressed. Keys are substrings to match against the command, with * matching every command, and values are substrings of the violation to ignore for that command, such as a filesystem path.

****``
****
****

settings.json
[​](#sandbox-enableweakernestedsandbox)sandbox.enableWeakerNestedSandbox`
- Scope: Any file, with limits on project and local settings
  - true: the inner sandbox bind-mounts the container’s existing /proc instead of mounting a fresh one
  - false: the sandbox mounts a fresh /proc, which doesn’t work in an unprivileged Docker container
- Default: false

```
{
  "sandbox": {
    "enabled": true,
    "enableWeakerNestedSandbox": true
  }
}

```
### Run the Linux sandbox inside an unprivileged Docker container, where bubblewrap can’t mount a fresh /proc. Instead the inner sandbox bind-mounts the container’s existing /proc, which exposes process information that a fresh mount would hide. This reduces security; use it only when the outer container already provides the isolation you need.

****``
****````
````

****``

settings.json
Linux and WSL2 only. See [Bubblewrap fails to start inside a container](/docs/en/sandboxing#bubblewrap-fails-to-start-inside-a-container).
[​](#sandbox-enableweakernetworkisolation)sandbox.enableWeakerNetworkIsolation`
- Scope: Any file, with limits on project and local settings
  - true: sandboxed commands on macOS can reach com.apple.trustd.agent
  - false: sandboxed commands on macOS can’t reach the system TLS trust service
- Default: false

```
{
  "sandbox": {
    "enabled": true,
    "enableWeakerNetworkIsolation": true
  }
}

```
### Let sandboxed commands on macOS reach the system TLS trust service, com.apple.trustd.agent. Go-based tools such as gh, gcloud, and terraform need it to verify TLS certificates when you use [network.httpProxyPort](#sandbox-network-httpproxyport) with a MITM proxy and a custom CA. This reduces security by opening a potential data exfiltration path through the trust service.

****``
****````
``

****``

settings.json
If you don’t use a MITM proxy, list the failing tools in [excludedCommands](#sandbox-excludedcommands) instead; see [Go-based CLIs fail TLS verification on macOS](/docs/en/sandboxing#go-based-clis-fail-tls-verification-on-macos).
[​](#sandbox-allowappleevents)sandbox.allowAppleEvents`
- Scope: User or managed
  - true: sandboxed commands on macOS can send Apple Events
  - false: sandboxed commands on macOS can’t send Apple Events, so open and osascript fail with error -600
- Default: false

```
{
  "sandbox": {
    "enabled": true,
    "allowAppleEvents": true
  }
}

```
### Let sandboxed commands on macOS send Apple Events, which open, osascript, and tools that open URLs in a browser need; without it they fail with error -600. This removes code-execution isolation: sandboxed commands can launch other applications unsandboxed with no user prompt, and can send AppleScript commands to running applications such as Terminal, subject to the per-app macOS automation-consent prompt (TCC).

****``
****``
````````

****``

settings.json
To keep isolation and still run one such tool, add it to [excludedCommands](#sandbox-excludedcommands) instead. See [Apple Events on macOS](/docs/en/sandboxing#security-limitations).
[​](#sandbox-allownestedusernamespaces)sandbox.allowNestedUserNamespaces`
- Scope: User or managed. A true counts from ~/.claude/settings.json, JSON passed with --settings, or managed settings. Claude Code ignores a true in a project’s .claude/settings.json or .claude/settings.local.json. In a session with CLAUDE_CODE_SUBPROCESS_ENV_SCRUB set to 1, Claude Code ignores a true from every source. A false counts from any file, by settings precedence.
  - true: sandboxed commands can create user namespaces
  - false: this key allows nothing extra, and the sandbox’s default applies
- Default: false

```
{
  "sandbox": {
    "enabled": true,
    "allowNestedUserNamespaces": true
  }
}

```
### Let sandboxed commands on Linux and WSL2 create user namespaces, which Chromium’s and Electron’s own sandbox, a nested bubblewrap, and unshare need. If you set this key to true, you turn off a security boundary: code from a sandboxed command can end up running outside the sandbox. For rootless Podman or Buildah, use [excludedCommands](#sandbox-excludedcommands) instead, because the sandbox stops them in other ways too. Requires Claude Code v2.1.305 or later.

****``````````````````````
****``
``

****``

settings.json
With this key on, don’t rely on any of the sandbox’s restrictions, including [protected paths](/docs/en/sandboxing#protected-paths) and [credentials.files](#sandbox-credentials-files) entries, to stop a malicious command. In [auto-allow mode](/docs/en/sandboxing#auto-allow-mode), that command can run without a permission prompt. If your organization has a security team, check with them before you turn the key on.
To find the fix for your tool, see [Chromium or rootless Podman fails inside the sandbox on Linux](/docs/en/sandboxing#chromium-or-rootless-podman-fails-inside-the-sandbox-on-linux).
[​](#sandbox-ripgrep)sandbox.ripgrep`
- Scope: User or managed
- Type: object with command, the path to the ripgrep binary, and optional args, an array of arguments to prepend
- Default: unset, so the sandbox uses the same ripgrep binary as Claude Code. That is the bundled binary unless you set USE_BUILTIN_RIPGREP to 0

```
{
  "sandbox": {
    "ripgrep": {
      "command": "/usr/local/bin/rg"
    }
  }
}

```
### Point the sandbox at a ripgrep binary of your own instead of the one Claude Code uses, for example when your platform needs a differently built rg.

****``
****````
****````

settings.json
[​](#sandbox-bwrappath)sandbox.bwrapPath`
- Scope: Managed. Claude Code reads it only from managed settings so that a user, project, or local file can’t point the sandbox at a different binary.
- Type: string, an absolute path; Claude Code drops a relative path and falls back to PATH lookup
- Default: unset, so Claude Code finds bwrap on PATH

```
{
  "sandbox": {
    "enabled": true,
    "bwrapPath": "/opt/admin/bwrap"
  }
}

```
### Point the sandbox at a bubblewrap binary installed outside PATH, such as a vendored copy on an air-gapped host. Claude Code uses the path both for the startup dependency check and when it wraps each sandboxed command.

****``
****``
****````

managed-settings.json
Linux and WSL2 only.
[​](#sandbox-socatpath)sandbox.socatPath`
- Scope: Managed
- Type: string, an absolute path; Claude Code drops a relative path and falls back to PATH lookup
- Default: unset, so Claude Code finds socat on PATH

```
{
  "sandbox": {
    "enabled": true,
    "socatPath": "/opt/admin/socat"
  }
}

```
### Point the sandbox network proxy at a socat binary installed outside PATH.

****``
****``
****````

managed-settings.json
Linux and WSL2 only.
[​](#sandbox-credentials)sandbox.credentials`
- Scope: Any file. Claude Code honors mask entries, allowPlaintextInject, awsPairs, and sigv4 only from user settings, managed settings, and the --settings flag.
- Type: object with files, envVars, allowPlaintextInject, awsPairs, and sigv4
- Default: unset, so no credentials are protected

```
{
  "sandbox": {
    "credentials": {
      "files": [{ "path": "~/.aws/credentials", "mode": "deny" }],
      "envVars": [{ "name": "GITHUB_TOKEN", "mode": "deny" }]
    }
  }
}

```
#### Declare the credential files and environment variables to [protect from sandboxed commands](/docs/en/sandboxing#protect-credentials). Each entry names a file path or a variable name and a mode: deny hides the credential inside the sandbox, and mask shows sandboxed commands a placeholder while the [sandbox proxy](/docs/en/sandboxing#mask-credentials) substitutes the real value on outbound requests. Claude Code protects only the entries you list; there is no built-in credential deny list.

****````````````
****``````````
****

This hides your AWS credentials file and removes GITHUB_TOKEN from sandboxed commands:
settings.json
The deny file protection is part of the filesystem layer, so it doesn’t apply when you [disable filesystem isolation](/docs/en/sandboxing#disable-filesystem-isolation); the environment variable protection still does.
[​](#invalid-credential-entries-in-managed-settings)Invalid credential entries in managed settings
- An entry in files or envVars that still has a valid path or name and a mode of mask or deny, such as one whose extract pattern has no capturing group, is degraded to mode: "deny" with a warning, so the credential stays blocked, not masked, until you fix the entry. A degraded files entry pins filesystem.disabled like an explicit deny entry, and the warning notes that its read block isn’t enforced if managed settings turn filesystem isolation off.
- An entry with an unknown mode or an invalid path or name is stripped.
- Each case warns; whether an entry is degraded or stripped, the remaining valid entries are still enforced.
### When a managed sandbox.credentials entry fails validation, Claude Code keeps protecting the credential where it can:

````````````````````````
``````

Applies in v2.1.191 and later; before v2.1.221, every invalid entry was stripped. For the other managed keys with per-field handling, see [Invalid entries in managed settings](/docs/en/managed-settings#invalid-entries-in-managed-settings).
[​](#sandbox-credentials-files)sandbox.credentials.files`
- Scope: Any file. Claude Code drops mask entries from project .claude/settings.json and local .claude/settings.local.json.
- Type: array of objects, each with path and a mode of "deny" or "mask", plus the optional mask fields for files
- Default: unset, so no credential files are protected

```
{
  "sandbox": {
    "credentials": {
      "files": [
        { "path": "~/.aws/credentials", "mode": "deny" },
        { "path": "~/.config/gh/hosts.yml", "mode": "mask", "injectHosts": ["api.github.com"] }
      ]
    }
  }
}

```
#### Protect credential files or directories from sandboxed commands. With "mode": "deny", Claude Code blocks reads of the path inside the sandbox, the same read block as [sandbox.filesystem.denyRead](#sandbox-filesystem-denyread). With "mode": "mask", sandboxed commands on Linux and WSL2 read a sentinel copy of the file, and the sandbox proxy substitutes the real value on outbound requests to that entry’s injectHosts; on macOS the file is unreadable inside the sandbox instead. "mode": "mask" requires Claude Code v2.1.221 or later.

****````````
****````````
****

This hides your AWS credentials file and masks the gh hosts file, substituting the real value only on requests to api.github.com:
settings.json
Paths use the same [prefixes](#sandbox-path-prefixes) as the sandbox.filesystem.* settings, and Claude Code merges the arrays from every settings scope the session loads. [Protect credentials](/docs/en/sandboxing#protect-credentials) covers what still applies from sources you exclude with --setting-sources. mask entries require Claude Code v2.1.221 or later.
mask substitution runs only through the sandbox proxy, so set [sandbox.network.tlsTerminate](#sandbox-network-tlsterminate), or [allowPlaintextInject](#sandbox-credentials-allowplaintextinject) for plain-HTTP test networks. mask applies to a single file, so list each credential file individually. Claude Code accepts but ignores the mask fields on a deny entry. [Mask credentials](/docs/en/sandboxing#mask-credentials) covers which settings sources are honored, and [Mask credential files](/docs/en/sandboxing#mask-credential-files) covers when an entry falls back to deny.

[​](#mask-fields-for-files)Mask fields for files

| Field | Type | What it does |
| --- | --- | --- |
| extract | string, a regular expression with at least one capturing group | Mask only the text captured by group 1 of each match, so the rest of the file stays parseable. With decode also set, Claude Code checks each capture as a possible JWT instead of replacing it outright. Requires v2.1.221 or later |
| onExtractNoMatch | "warn", "deny", or "error"; default "warn" | What happens when extract or decode finds nothing to mask. warn leaves the file readable as-is inside the sandbox, deny makes it unreadable, and error stops sandbox setup until you fix the configuration. Claude Code treats deny as error when the read block wouldn’t be enforced, because you disable filesystem isolation or a sandbox.filesystem.allowRead entry re-opens the path. Requires v2.1.221 or later; the decode case requires v2.1.224 or later |
| decode | the string "jwt" | Find JSON Web Tokens (JWTs) in the file, with a built-in pattern or with extract when set, verify each candidate, and replace it with a structurally valid fake token, so code inside the sandbox that decodes the token keeps working. When no candidate verifies, onExtractNoMatch governs the outcome. Requires v2.1.224 or later |
| maskClaims | array of strings, at least one claim name; requires decode | Mask only the named top-level payload claims inside each verified JWT and rebuild the token around the modified payload, so the other claims stay readable. When no named claim matches, onExtractNoMatch governs the outcome. Requires v2.1.224 or later |
| maskDuplicates | Boolean, default false | Also replace verbatim copies of each masked value elsewhere in the file, such as a secret pasted into a comment. Claude Code matches raw substrings, so reserve it for long, high-entropy secrets. Consulted only when extract or decode is set. Requires v2.1.221 or later |
| injectHosts | array of strings, each a host that sandbox.network.allowedDomains also admits | Narrow the hosts where the sandbox proxy substitutes the real value. When unset, the proxy substitutes it on requests to every host in sandbox.network.allowedDomains. Requires v2.1.221 or later |

```
{
  "sandbox": {
    "credentials": {
      "files": [
        {
          "path": "~/.config/gh/hosts.yml",
          "mode": "mask",
          "extract": "oauth_token:\\s*(\\S+)",
          "maskDuplicates": true,
          "onExtractNoMatch": "deny",
          "injectHosts": ["api.github.com"]
        }
      ]
    }
  }
}

```
### A mask entry accepts these optional fields. Without extract or decode, Claude Code replaces the entire file content with one sentinel. On macOS with filesystem isolation on, Claude Code applies a mask entry as deny before extract or decode runs; see [Mask credential files](/docs/en/sandboxing#mask-credential-files).
````````````````````````````````````````````````````````````
This masks only the oauth_token value in the gh hosts file, replaces every other copy of it in the file, makes the file unreadable if the pattern matches nothing, and substitutes the real token only on requests to api.github.com:
settings.json
[​](#sandbox-credentials-envvars)sandbox.credentials.envVars`
- Scope: Any file. Claude Code drops mask entries from project .claude/settings.json and local .claude/settings.local.json.
- Type: array of objects, each with name and a mode of "deny" or "mask", plus the optional mask fields for environment variables
- Default: unset, so no environment variables are protected

```
{
  "sandbox": {
    "credentials": {
      "envVars": [
        { "name": "NPM_TOKEN", "mode": "deny" },
        { "name": "GITHUB_TOKEN", "mode": "mask", "injectHosts": ["api.github.com"] }
      ]
    }
  }
}

```
#### Protect environment variables from sandboxed commands. With "mode": "deny", Claude Code removes the variable from the environment of sandboxed commands. With "mode": "mask", sandboxed commands see a per-session sentinel value, and the sandbox proxy substitutes the real value on outbound requests to that entry’s injectHosts, so tools such as gh and npm keep authenticating without ever holding the real credential.

****````````
****````````
****

This removes NPM_TOKEN from sandboxed commands and masks GITHUB_TOKEN, substituting the real value only on requests to api.github.com:
settings.json
The name must start with a letter or underscore and contain only letters, digits, and underscores. Claude Code merges the arrays from every settings scope the session loads, and applies deny when the same variable appears with both modes. [Protect credentials](/docs/en/sandboxing#protect-credentials) covers what still applies from sources you exclude with --setting-sources.
mask substitution runs only through the sandbox proxy, so set [sandbox.network.tlsTerminate](#sandbox-network-tlsterminate), or [allowPlaintextInject](#sandbox-credentials-allowplaintextinject) for plain-HTTP test networks; see [Mask credentials](/docs/en/sandboxing#mask-credentials). Claude Code accepts but ignores the mask fields on a deny entry.

[​](#mask-fields-for-environment-variables)Mask fields for environment variables

| Field | Type | What it does |
| --- | --- | --- |
| extract | string, a regular expression with at least one capturing group | Mask only the text captured by group 1 of each match, such as the password inside a DATABASE_URL connection string, so the rest of the value stays parseable. Requires v2.1.224 or later |
| onExtractNoMatch | "warn", "deny", or "error"; default "warn". On an entry with decode, only "warn" is accepted | What happens when extract matches nothing. warn passes the variable through unmasked, deny unsets it inside the sandbox, and error stops sandbox setup until you fix the configuration. Requires v2.1.224 or later |
| decode | the string "jwt" | Verify the whole value is a JWT and replace it with a structurally valid fake token, so code inside the sandbox that decodes the token keeps working; the proxy substitutes the whole real token on egress. A value that doesn’t verify passes through unmasked with a warning. Requires v2.1.224 or later |
| maskClaims | array of strings, at least one claim name; requires decode | Mask only the named top-level payload claims inside the decoded JWT and rebuild the token around the modified payload, so the other claims stay readable. When no named claim matches, the variable passes through unmasked with a warning. Requires v2.1.224 or later |
| injectHosts | array of strings, each a host that sandbox.network.allowedDomains also admits | Narrow the hosts where the sandbox proxy substitutes the real value. When unset, the proxy substitutes it on requests to every host in sandbox.network.allowedDomains. Write an IPv6 destination as the bare compressed address, such as "::1", not the bracketed form; see IPv6 destinations in injectHosts |

```
{
  "sandbox": {
    "credentials": {
      "envVars": [
        {
          "name": "DATABASE_URL",
          "mode": "mask",
          "extract": "://[^:]+:([^@]+)@",
          "onExtractNoMatch": "deny"
        },
        {
          "name": "SERVICE_JWT",
          "mode": "mask",
          "decode": "jwt",
          "maskClaims": ["api_key"]
        }
      ]
    }
  }
}

```
### A mask entry accepts these optional fields. Without extract or decode, Claude Code replaces the entire value with one sentinel. extract and decode can’t be combined on the same entry.
````````````````````````````````````````````
This masks only the password inside DATABASE_URL, unsets the variable if the pattern matches nothing, and masks a JWT in SERVICE_JWT while leaving every claim except api_key readable:
settings.json
[​](#sandbox-credentials-allowplaintextinject)sandbox.credentials.allowPlaintextInject`
- Scope: User or managed
  - true: Claude Code allows mask substitution on plain HTTP requests as well as TLS-terminated HTTPS
  - false: Claude Code allows mask substitution only on TLS-terminated HTTPS
- Default: false

```
{
  "sandbox": {
    "credentials": {
      "allowPlaintextInject": true
    }
  }
}

```
### Allow mask substitution on plain HTTP requests as well as TLS-terminated HTTPS. On plain HTTP the upstream identity is unverified and the credential travels in cleartext, so leave this off outside trusted test networks.

****``
****````
````

****``

settings.json
[​](#sandbox-credentials-awspairs)sandbox.credentials.awsPairs`
- Scope: User or managed
- Type: array of objects, each with accessKeyIdVar, secretAccessKeyVar, and optionally sessionTokenVar, naming sandbox.credentials.envVars entries
- Default: unset, so only the conventional trio is paired

```
{
  "sandbox": {
    "credentials": {
      "awsPairs": [
        {
          "accessKeyIdVar": "MY_KEY_ID",
          "secretAccessKeyVar": "MY_SECRET_KEY",
          "sessionTokenVar": "MY_SESSION_TOKEN"
        }
      ]
    }
  }
}

```
- The proxy re-signs requests on the hosts listed in the access key ID entry’s injectHosts
- When sessionTokenVar is set, the proxy sends the real token as x-amz-security-token on re-signed requests
- Naming any of the conventional variables in a pair replaces the automatic pairing
### Group masked environment variables that form one AWS credential for [SigV4 re-signing](/docs/en/sandboxing#re-sign-aws-requests) when your credential lives in variables with non-standard names. Claude Code links the conventional AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and AWS_SESSION_TOKEN trio automatically when you mask their whole values, so you need this key only for other names. Requires Claude Code v2.1.224 or later.

****``
****````````
****

This links three custom-named variables into one AWS credential for re-signing:
settings.json
Each named variable must be a whole-value mask entry in [sandbox.credentials.envVars](#sandbox-credentials-envvars), without extract or decode, and can fill only one slot across all pairs. These rules also apply:

``
````

[​](#sandbox-credentials-sigv4)sandbox.credentials.sigv4`
- Scope: User or managed
  - "deny": the proxy fails the request
  - "passthrough": the proxy forwards the request signed with the masked placeholder, so the tool receives AWS’s own rejection
- Default: unset, so every form is "deny"

```
{
  "sandbox": {
    "credentials": {
      "sigv4": {
        "streaming": "passthrough"
      }
    }
  }
}

```
### Choose what the sandbox proxy does with AWS request forms it [can’t re-sign](/docs/en/sandboxing#re-sign-aws-requests): streaming for aws-chunked streaming uploads, presigned for presigned URLs, and sigv4a for SigV4A asymmetric signatures. This applies only to requests signed with a masked pair’s placeholder access key ID. Requires Claude Code v2.1.224 or later.

****``
****````````
``

****``

This forwards streaming uploads instead of failing them at the proxy:
settings.json
With deny, the proxy fails the request. With passthrough, the proxy forwards the request with its signature computed from the masked placeholder, so AWS rejects it and the calling tool receives AWS’s own response instead of a proxy error.
[​](#sandbox-network)sandbox.network`
- Scope: Any file. strictAllowlist, allowManagedDomainsOnly, and tlsTerminate are read from fewer sources, as their entries say.
- Type: object with the sub-keys below
- Default: unset, so no domains are pre-allowed and your permission mode decides what happens to each new host

```
{
  "sandbox": {
    "network": {
      "allowedDomains": ["github.com", "*.npmjs.org"],
      "deniedDomains": ["uploads.github.com"],
      "allowLocalBinding": true
    }
  }
}

```
### Control which hosts, ports, and sockets sandboxed commands can reach. The sandbox routes outbound traffic through a proxy that enforces these lists; see [Network isolation](/docs/en/sandboxing#network-isolation) for how the proxy decides and when it prompts.

****````````
****
****

This pre-allows GitHub and npm, blocks uploads.github.com, and lets commands bind to localhost:
settings.json
Claude Code merges the array sub-keys across settings scopes, so a project can add domains to your user list unless a [repository lock](/docs/en/sandboxing#repository-settings-under-an-admin-required-sandbox) applies. WebFetch(domain:...) allow and deny [permission rules](/docs/en/sandboxing#permission-rules) feed the same allow and deny lists.
[​](#sandbox-network-allowunixsockets)sandbox.network.allowUnixSockets`
- Scope: Any file, with limits on project and local settings
- Type: array of strings, each a socket path
- Default: unset, so the macOS sandbox blocks every Unix socket

```
{
  "sandbox": {
    "network": {
      "allowUnixSockets": ["~/.ssh/agent-socket"]
    }
  }
}

```
### List the Unix socket paths sandboxed commands can connect to on macOS. Claude Code ignores this list on Linux and WSL2, where the seccomp filter can’t inspect socket paths; use [allowAllUnixSockets](#sandbox-network-allowallunixsockets) there instead.

****``
****
****

settings.json
A socket path can grant broad access: allowing /var/run/docker.sock, for example, lets a sandboxed command control the Docker daemon. See [Security limitations](/docs/en/sandboxing#security-limitations).
[​](#sandbox-network-allowallunixsockets)sandbox.network.allowAllUnixSockets`
- Scope: Any file, with limits on project and local settings
  - true: sandboxed commands can connect to every Unix socket. On Linux and WSL2 they can also connect to VM sockets, the AF_VSOCK address family
  - false: the sandbox blocks Unix-socket connections: on macOS except the paths in allowUnixSockets, and on Linux and WSL2 through the seccomp filter when it’s present
- Default: false

```
{
  "sandbox": {
    "network": {
      "allowAllUnixSockets": true
    }
  }
}

```
### Let sandboxed commands connect to every Unix socket. On Linux and WSL2, the sandbox’s [seccomp filter](/docs/en/sandboxing#set-up-linux-and-wsl2) blocks socket(AF_UNIX, ...) calls, so this is the only way to permit Unix sockets there. When the filter is missing, which /sandbox reports on its Dependencies tab, the sandbox doesn’t block Unix-socket calls. See [Set up Linux and WSL2](/docs/en/sandboxing#set-up-linux-and-wsl2) for where the filter comes from.

****``
****````
````

****``

settings.json
On WSL2, true also reopens the interop socket that launches Windows binaries such as cmd.exe and powershell.exe.
[​](#sandbox-network-allowlocalbinding)sandbox.network.allowLocalBinding`
- Scope: Any file, with limits on project and local settings
  - true: sandboxed commands on macOS can listen on any local address and connect to any port on localhost
  - false: sandboxed commands on macOS can’t listen on a port or connect directly to servers on localhost
- Default: false

```
{
  "sandbox": {
    "network": {
      "allowLocalBinding": true
    }
  }
}

```
### Let sandboxed commands on macOS listen on network ports, for example to start a dev server, and connect to any port on localhost. A command that listens on a non-loopback address accepts connections from other machines. The key has no effect on Linux and WSL2, where each sandboxed command has its own loopback interface. To reach a server on the host from Linux or WSL2, see [A command fails to reach a server on localhost](/docs/en/sandboxing#a-command-fails-to-reach-a-server-on-localhost).

****``
****``
``

****``

settings.json
[​](#sandbox-network-allowmachlookup)sandbox.network.allowMachLookup`
- Scope: Any file, with limits on project and local settings
- Type: array of strings, each a service name; a single trailing * matches a prefix, and "*" alone matches every service
- Default: unset

```
{
  "sandbox": {
    "network": {
      "allowMachLookup": ["com.apple.CoreSimulator.*"]
    }
  }
}

```
### List additional XPC and Mach service names the macOS sandbox may look up. Tools that communicate over XPC, such as the iOS Simulator or Playwright, need their services listed here. Sandboxed commands can reach outside the sandbox to each service that you list, and the sandbox [doesn’t confine what those services do for those commands](/docs/en/sandboxing#security-limitations).

****``
****````
****

This allows every service under the com.apple.CoreSimulator. prefix:
settings.json
[​](#sandbox-network-alloweddomains)sandbox.network.allowedDomains`
- Scope: Any file, with limits on project and local settings. Only managed settings when allowManagedDomainsOnly is set.
- Type: array of strings, each a domain, wildcard pattern, or IP literal, with an optional :port suffix
- Default: unset, so your permission mode decides what happens to each new host

```
{
  "sandbox": {
    "network": {
      "allowedDomains": ["github.com", "*.npmjs.org", "api.example.com:443"]
    }
  }
}

```
### Pre-allow domains for outbound traffic from sandboxed commands, so the sandbox doesn’t prompt for them. Wildcards such as *.example.com match subdomains, and an optional :port suffix limits an entry to one port; an entry without a port matches every port.

****````
****``
****

This pre-allows GitHub on every port, every npm subdomain, and one API host on port 443 only:
settings.json
Write IPv6 literals bracketed, with an optional port: "[::1]" allows every port and "[::1]:443" one port. The bracketed form requires Claude Code v2.1.229 or later. See [IPv6 addresses in domain lists](/docs/en/sandboxing#ipv6-addresses-in-domain-lists).
[​](#sandbox-network-denieddomains)sandbox.network.deniedDomains`
- Scope: Any file
- Type: array of strings, each a domain, wildcard pattern, or IP literal, with an optional :port suffix
- Default: unset

```
{
  "sandbox": {
    "network": {
      "deniedDomains": ["sensitive.cloud.example.com"]
    }
  }
}

```
### Block domains for outbound traffic from sandboxed commands, using the same wildcard, port, and IPv6 syntax as [allowedDomains](#sandbox-network-alloweddomains). A denied domain stays blocked even when an allowedDomains entry matches it too.

****``
****``
****

settings.json
Claude Code merges this list from every settings source the session loads even when allowManagedDomainsOnly is set, so a developer can always tighten the deny list. For IPv6 literals, see [IPv6 addresses in domain lists](/docs/en/sandboxing#ipv6-addresses-in-domain-lists).
An entry written with the trailing dot that marks a fully qualified domain name, such as example.com., blocks the same connections as example.com.
[​](#sandbox-network-strictallowlist)sandbox.network.strictAllowlist`
- Scope: User or managed. A repository can’t turn it on or off.
  - true: Claude Code denies sandboxed commands access to hosts outside the allowlist
  - false: unless another trusted settings file sets true, Claude Code decides a host outside the allowlist by permission mode instead of denying it outright: in auto mode it checks the host against the command’s per-command allowed domains, in dontAsk mode it denies, in bypassPermissions mode and in interactive terminal plan-mode sessions where bypass is available it allows, and otherwise it asks you
- Default: false

```
{
  "sandbox": {
    "network": {
      "strictAllowlist": true
    }
  }
}

```
### Deny sandboxed commands access to hosts outside the allowlist instead of prompting for approval. The allowlist is [allowedDomains](#sandbox-network-alloweddomains) plus domains from WebFetch(domain:...) allow rules, or only the managed settings entries when [allowManagedDomainsOnly](#sandbox-network-allowmanageddomainsonly) is set. [Locks that apply without an admin-required sandbox](/docs/en/sandboxing#locks-that-apply-without-an-admin-required-sandbox) covers a repository’s entries. Requires Claude Code v2.1.219 or later.

****``
****``
````````

****``

settings.json
Claude Code enforces this for sandboxed commands only; in-process tools such as WebFetch still follow their [permission rules](/docs/en/sandboxing#permission-rules). When any of the honored sources sets it to true, it stays on. See [Network isolation](/docs/en/sandboxing#network-isolation). Requires Claude Code v2.1.219 or later.
[​](#sandbox-network-allowmanageddomainsonly)sandbox.network.allowManagedDomainsOnly`
- Scope: Managed
  - true: Claude Code honors only allowedDomains and WebFetch(domain:...) allow rules from managed settings and blocks a non-allowed domain instead of prompting
  - false: domains from other settings files can merge into the allowlist
- Default: false

```
{
  "sandbox": {
    "network": {
      "allowManagedDomainsOnly": true,
      "allowedDomains": ["github.com", "*.npmjs.org"]
    }
  }
}

```
### Lock the network allowlist to what managed settings define. Claude Code then honors only allowedDomains and WebFetch(domain:...) allow rules from managed settings, ignores domains from user, project, local, and --settings settings, and blocks a non-allowed domain automatically instead of prompting.

****``
****``````
``

****``

This locks the allowlist to GitHub and npm and ignores any domains developers add:
managed-settings.json
While the key is true, the sandbox is [admin-required](/docs/en/sandboxing#repository-settings-under-an-admin-required-sandbox), and only managed settings can set a [proxy port](#sandbox-network-httpproxyport).
Denied domains still merge from every source the session loads. See [Keep developers from widening the policy](/docs/en/sandboxing#keep-developers-from-widening-the-policy).
[​](#sandbox-network-httpproxyport)sandbox.network.httpProxyPort`
- Scope: Any file, unless other sandbox settings limit which files can set a port
- Type: number, a local TCP port
- Default: unset, so Claude Code runs its own proxy

```
{
  "sandbox": {
    "network": {
      "httpProxyPort": 8080
    }
  }
}

```
### Point the sandbox at your own HTTP proxy instead of the one Claude Code runs. Organizations do this to inspect HTTPS traffic, apply their own filtering rules, or log requests. Your proxy takes over filtering, and Claude Code stops applying its domain lists and network prompts to traffic sent there. When unset, Claude Code starts its own proxy for HTTP traffic.

****``
****
****

settings.json
Set [socksProxyPort](#sandbox-network-socksproxyport) too if your proxy should carry SOCKS traffic as well; with only one of the two set, Claude Code still runs its own proxy for the other protocol. See [Custom proxy configuration](/docs/en/sandboxing#custom-proxy-configuration).
[​](#sandbox-network-socksproxyport)sandbox.network.socksProxyPort`
- Scope: Any file, unless other sandbox settings limit which files can set a port
- Type: number, a local TCP port
- Default: unset, so Claude Code runs its own proxy

```
{
  "sandbox": {
    "network": {
      "socksProxyPort": 8081
    }
  }
}

```
### Point the sandbox at your own SOCKS5 proxy instead of the one Claude Code runs. Your proxy takes over filtering, and Claude Code stops applying its domain lists and network prompts to traffic sent there. When unset, Claude Code starts its own proxy for SOCKS traffic.

****``
****
****

settings.json
See [Custom proxy configuration](/docs/en/sandboxing#custom-proxy-configuration).
[​](#sandbox-network-tlsterminate)sandbox.network.tlsTerminate`
- Scope: User or managed. A repository can’t switch it on or supply a certificate authority.
- Type: object with optional caCertPath and caKeyPath strings, each a file path
- Default: unset, so the proxy doesn’t terminate or inspect TLS

```
{
  "sandbox": {
    "network": {
      "tlsTerminate": {}
    }
  }
}

```
## Make the sandbox proxy terminate TLS so it can read the contents of HTTPS requests. This is experimental, and mask [credential substitution](/docs/en/sandboxing#mask-credentials) requires it. Set {} to generate an ephemeral certificate authority for the session, or set caCertPath and caKeyPath to use your own.

****``
****````
****

settings.json
When more than one honored source sets it, Claude Code uses the value from the highest-precedence source: managed settings, then the --settings flag, then user settings.

[​](#memory-and-context)Memory and context
### Control what Claude Code loads into context, how it compacts, and where it keeps memory and plans. See [Manage context](/docs/en/context-window) and [Memory](/docs/en/memory).
[​](#autocompactenabled)autoCompactEnabled`
- Scope: Any file
  - true: Claude Code compacts the conversation automatically when context approaches the limit
  - false: Claude Code doesn’t compact automatically
- Default: true
- Per-session overrides: DISABLE_AUTO_COMPACT turns auto-compact off for one session; whichever of the two turns it off, the other can’t turn it back on

```
{
  "autoCompactEnabled": false
}

```
### Have Claude Code [compact the conversation automatically](/docs/en/context-window#when-your-context-fills-up) when context approaches the limit. Appears in /config as **Auto-compact**, and toggling it there writes this key to your user settings.

****``
****``
``

****``
****``

settings.json
The manual /compact command keeps working while auto-compact is off. If you turn auto-compact off, [idle compaction](#idlecompaction) turns off too.
[​](#autocompactwindow)autoCompactWindow`
- Scope: Any file
- Type: number of tokens, from 100000 to 1000000. Claude Code caps the value at your model’s context window; the models overview lists each model’s window
- Default: unset, so Claude Code picks a window tuned for your model
- Per-session overrides: --autocompact takes precedence over this key for one session, and CLAUDE_CODE_AUTO_COMPACT_WINDOW takes precedence over both unless Claude Code ignores the variable’s value

```
{
  "autoCompactWindow": 500000
}

```
### Set how full the context window gets before Claude Code [compacts automatically](/docs/en/context-window#when-your-context-fills-up).

****``
****````
****
****````

settings.json
The [/autocompact](/docs/en/commands#all-commands) command saves a window for the current model under [modelSettings](#modelsettings), which takes precedence over this key in the same file for that model. [Set the auto-compact window](/docs/en/model-config#set-the-auto-compact-window) covers how the command, flag, variable, and setting interact.
[​](#automemorydirectory)autoMemoryDirectory`
- Scope: Any file
- Type: string, an absolute or ~/-prefixed directory path
- Default: unset, so Claude Code uses ~/.claude/projects/<project>/memory/

```
{
  "autoMemoryDirectory": "~/my-memory-dir"
}

```
### Store [auto memory](/docs/en/memory#storage-location) in a directory of your choice instead of the per-project default.

****``
****``
****``

settings.json
From project or local settings, Claude Code honors this key under the same [workspace trust rule as hooks](/docs/en/permissions#what-runs-before-you-trust-a-folder), since a cloned repository can supply those files.
[​](#automemoryenabled)autoMemoryEnabled`
- Scope: Any file
  - true: the same as unset; auto memory stays on unless something that outranks this key turns it off for the session, such as --bare, safe mode, or CLAUDE_CODE_DISABLE_AUTO_MEMORY
  - false: Claude doesn’t read from or write to the auto memory directory
- Default: true
- Per-session overrides: CLAUDE_CODE_DISABLE_AUTO_MEMORY takes precedence over this key for one session, in either direction

```
{
  "autoMemoryEnabled": false
}

```
### Turn [auto memory](/docs/en/memory#enable-or-disable-auto-memory) on or off. When false, Claude doesn’t read from or write to the auto memory directory. You can also toggle it with /memory during a session, which writes this key to your user settings.

****``
****``````
``

****``
****``

settings.json
[​](#bashoutputmaxchars)bashOutputMaxChars`
- Scope: Any file
- Type: number of characters, a positive integer. Claude Code clamps the value into the range 4000 to 128000
- Default: unset, so Claude receives up to 30,000 characters inline

```
{
  "bashOutputMaxChars": 100000
}

```
### Set how many characters of a successful Bash or PowerShell command’s [output Claude receives inline](/docs/en/tools-reference#output-limits). When output passes the limit, Claude Code saves it to a file and Claude receives a short preview plus the file’s path. Raise the limit when command output, such as a verbose build or a full test-suite log, routinely overflows the default and you want Claude to read it without opening the file. Requires Claude Code v2.1.261 or later.

****``
****````
****

settings.json
When you set this key, Claude Code ignores the [BASH_MAX_OUTPUT_LENGTH](/docs/en/env-vars) environment variable.
[​](#claudemd)claudeMd`
- Scope: Managed
- Type: string, the text of a CLAUDE.md file; write it as you would the file, Markdown included, with line breaks as \n
- Default: unset

```
{
  "claudeMd": "# Engineering rules\n\n- Always run make lint before committing.\n- Never push directly to main."
}

```
### Inject CLAUDE.md-style instructions as organization-managed memory without deploying a separate file. Claude Code loads the text as a managed memory entry ahead of user and project CLAUDE.md files.

****``
****``
****

This example deploys two rules as a short Markdown list:
managed-settings.json
See [Deploy organization-wide CLAUDE.md](/docs/en/memory#deploy-organization-wide-claude-md).
[​](#claudemdexcludes)claudeMdExcludes`
- Scope: Any file
- Type: array of strings, each a glob pattern or absolute path
- Default: unset, so Claude Code loads every CLAUDE.md it finds

```
{
  "claudeMdExcludes": ["**/vendor/**/CLAUDE.md"]
}

```
### Skip specific CLAUDE.md files when Claude Code loads [memory](/docs/en/memory#exclude-specific-claude-md-files). In a large monorepo, use it to skip CLAUDE.md files from other teams that aren’t relevant to your work; [Exclude irrelevant CLAUDE.md files](/docs/en/large-codebases#exclude-irrelevant-claude-md-files) in the large-codebases guide walks through that case. Patterns match against absolute file paths.

****``
****
****

settings.json
Exclusions apply only to user, project, and local memory files; managed policy CLAUDE.md files can’t be excluded.

[​](#env)env`
- Scope: Any file
- Type: object mapping variable names to string values
- Default: unset

```
{
  "env": {
    "DISABLE_AUTO_COMPACT": "1",
    "ANTHROPIC_BASE_URL": "https://proxy.example.com"
  }
}

```
#### Set environment variables for every session and for the subprocesses Claude Code starts from it. Most variables in the [environment variables reference](/docs/en/env-vars) can go here, which is how you apply one to every session or roll it out to your team. Project and local settings can’t set [some of them](#variables-claude-code-ignores-in-env).

****``
****
****

This example turns off automatic compaction and routes API requests through a proxy:
settings.json
[​](#how-env-values-interact-with-your-shell)How env values interact with your shell
- A value here overwrites the same variable exported in your shell, and when more than one settings file sets a variable, the highest-precedence one applies. Variables Claude Code ignores in env lists the exceptions for project and local settings.
- When the Claude Desktop app or a self-hosted environment runner starts the session, the launch environment it builds takes precedence instead: Claude Code ignores an env value from any settings file for a variable the launch environment already sets. The debug log names each ignored variable.
- To cancel a shell export, set the variable to "". Claude Code treats an empty value as unset for provider selection, and subprocesses inherit the empty value.
- NO_COLOR and FORCE_COLOR set here reach only subprocesses. To change Claude Code’s own interface colors, set them in your shell before launching claude.
- Values here are plain text in the settings file and reach every subprocess Claude Code starts. For an OTLP bearer token that rotates, use otelHeadersHelper; for API credentials, use apiKeyHelper.
#### ``
``
``
``````
````

[​](#when-claude-code-applies-env-values)When Claude Code applies env values
- From user settings, --settings, and managed settings: at startup, and again in the running session when a saved change alters the merged env.
- From project and local settings: after you trust the workspace, or at startup in -p mode, which never shows the trust dialog, and again when a saved change alters the merged env.
- Variables Claude Code classifies as safe, such as model selection, timeouts and limits, and feature toggles: at startup from every settings file, apart from the variables project and local settings can’t set.
- After you move the session with /cd on v2.1.246 or later: the new directory’s project and local env values, on top of the previous directory’s.
#### ````
````

````

[​](#variables-claude-code-ignores-in-env)Variables Claude Code ignores in env`
  - Variables that choose where Claude Code stores or writes its own files: CLAUDE_CONFIG_DIR, CLAUDE_CODE_TMPDIR, and the operating-system directory variables such as HOME, TMPDIR, TMP, TEMP, and the XDG_* family.
  - Windows variables that pick the programs and machine-wide configuration for the processes Claude Code starts, such as SystemRoot, ComSpec, ProgramData, LOCALAPPDATA, PATHEXT, PSModulePath, and the ProgramFiles family.
  - Variables that export session content: OTEL_LOG_RAW_API_BODIES and the detailed beta tracing pair ENABLE_BETA_TRACING_DETAILED and BETA_TRACING_ENDPOINT.
    - CLAUDE_CODE_ENABLE_TELEMETRY, plus the enhanced telemetry beta pair CLAUDE_CODE_ENHANCED_TELEMETRY_BETA and ENABLE_ENHANCED_TELEMETRY_BETA
    - The exporter selectors OTEL_LOGS_EXPORTER, OTEL_METRICS_EXPORTER, and OTEL_TRACES_EXPORTER
    - The content variables OTEL_LOG_USER_PROMPTS, OTEL_LOG_ASSISTANT_RESPONSES, OTEL_LOG_TOOL_CONTENT, and OTEL_LOG_TOOL_DETAILS
    - OTEL_EXPORTER_OTLP_* variables whose names end in _ENDPOINT, _HEADERS, _PROTOCOL, _CERTIFICATE, _CLIENT_KEY, or _INSECURE, in the generic and per-signal forms, such as OTEL_EXPORTER_OTLP_ENDPOINT and OTEL_EXPORTER_OTLP_METRICS_HEADERS
    - OTEL_EXPORTER_PROMETHEUS_HOST and OTEL_EXPORTER_PROMETHEUS_PORT
  - Variables that change how Claude Code starts or syncs, such as CLAUDE_CODE_PROCESS_WRAPPER, CLAUDE_CODE_SYNC_SKILLS, CLAUDE_CODE_SYNC_PLUGINS, CLAUDE_CODE_PLUGIN_CACHE_DIR, and CLAUDE_CODE_PLUGIN_SEED_DIR.
  - Variables that set your claude.ai sign-in, such as CLAUDE_CODE_OAUTH_TOKEN, CLAUDE_CODE_OAUTH_REFRESH_TOKEN, and CLAUDE_CODE_OAUTH_SCOPES.
  - The screen reader mode variable CLAUDE_AX_SCREEN_READER and the other variables whose names start with CLAUDE_AX_, such as CLAUDE_AX_STARTUP_QUIET_MS.
  - CLAUDE_CODE_USER_DIALOG_TIMEOUT_MS, which sets the timer on an unanswered dialog.
  - CLAUDE_CODE_DISABLE_ATTACHMENTS, which turns off attachment processing.
  - CLAUDE_CODE_DISABLE_FILE_MENTIONS, which stops Claude Code from expanding @ mentions of files and directories.
- Identity variables that Claude Code’s hosting environments own, such as CLAUDE_CODE_REMOTE and CLAUDE_CODE_ACCOUNT_UUID, are ignored from every file.
- CLAUDE_CODE_MESSAGING_SOCKET and CLAUDE_CODE_MESSAGING_TOKEN, which Claude Code exports itself, are ignored from every file. Ignoring the socket variable requires Claude Code v2.1.224 or later, and ignoring the token requires v2.1.228 or later.
- CLAUDE_CODE_PROJECT_DIR_NAME, which Claude Code reads from the launch environment only, is ignored from every file; requires v2.1.234 or later.
- CLAUDE_CODE_RESTRICTED, which Claude Code reads from the launch environment only, is ignored from every file.
- CLAUDE_CODE_DISABLE_POWERSHELL_CMD_RM_DENY, which Claude Code reads from the launch environment only, is ignored from every file. The variable requires Claude Code v2.1.283 or later.
- CLAUDE_CODE_DISABLE_DANGEROUS_RM_TIMEOUT, CLAUDE_CODE_DISABLE_SUBSTITUTION_RM_PROMPT, CLAUDE_CODE_DISABLE_INLINE_SHELL_RM_PROMPT, and CLAUDE_CODE_DISABLE_MOUNTED_DRIVE_RM_PROMPT, which Claude Code reads from the launch environment only, are ignored from every file.
- CLAUDE_CODE_EVEN_MORE_DANGEROUSLY_SKIP_PERMISSIONS, which Claude Code reads from the launch environment only, is ignored from every file.
- CLAUDE_CODE_WARN_DISK_FREE_GIB and CLAUDE_CODE_WARN_MEMORY_FREE_GIB, which Claude Code reads from the launch environment only, are ignored from every file. The variables require Claude Code v2.1.304 or later.
### ````````````````
``````````````
``````
``````
``````
````````
``````````````````
````

Only these values still apply from project and local settings, because they turn something off: none for the three exporter selectors, and an off value such as 0 for OTEL_LOG_USER_PROMPTS, OTEL_LOG_TOOL_CONTENT, and OTEL_LOG_TOOL_DETAILS. Such a value overrides the same variable in your user settings, but not one that the environment you start Claude Code from, a --settings file, or managed settings sets.
When a project or local settings file sets a variable in this group, a local interactive session shows a notice at startup. Run /status or claude doctor to see which ones Claude Code ignored and which turned telemetry off; both list names, never values. A non-interactive run with -p or an Agent SDK session shows no notice, so check that your collector still receives data after you upgrade. If it doesn’t, set the variables in your user settings, managed settings, the job’s environment, or a file you pass with --settings.
Ignoring this group in project and local settings requires Claude Code v2.1.282 or later.

``````````
``````
``````
``
``
````

Before v2.1.251, project and local settings could also set the variables in this list that choose where Claude Code writes its files or that export session content, except HOME and XDG_CONFIG_HOME. Before v2.1.290, they could also set the dialog timer variables and CLAUDE_CODE_DISABLE_ATTACHMENTS.

````
````
``
``
``
````````
``
````

[​](#filecheckpointingenabled)fileCheckpointingEnabled`
- Scope: Any file
  - true: Claude Code snapshots files before each edit so /rewind can restore them
  - false: Claude Code doesn’t snapshot files, so /rewind can’t restore them
- Default: true
- Per-session overrides: CLAUDE_CODE_DISABLE_FILE_CHECKPOINTING turns checkpointing off for one session; whichever of the two turns it off, the other can’t turn it back on

```
{
  "fileCheckpointingEnabled": false
}

```
### Have Claude Code snapshot files before each edit so [/rewind](/docs/en/checkpointing) can restore them. Appears in /config as **Rewind code (checkpoints)**, and toggling it there writes this key to your user settings.

****``
****````
````

****``
****``

settings.json
In a -p run or an Agent SDK session, Claude Code ignores this key. The SDK turns checkpointing on with its enableFileCheckpointing option, and a bare -p run needs CLAUDE_CODE_ENABLE_SDK_FILE_CHECKPOINTING=true. See [File checkpointing in the Agent SDK](/docs/en/agent-sdk/file-checkpointing).
[​](#idlecompaction)idleCompaction`
- Terminal: a line that starts with Compacted while idle, before the prompt cache expired
- VS Code chat panel: a notice that includes a summary written while you were away
- Desktop app: the same notice, inside a row whose label includes Claude Code notice. If you don’t see that row or its text, switch to the Verbose view mode.
- Session: you’re in an interactive terminal session, in the VS Code extension’s chat panel, or in the desktop app’s Code tab when the session runs on your machine or over SSH
- Auto-compaction: autoCompactEnabled is on
- Prompt cache: the conversation is on the one-hour prompt cache TTL
- Size: the conversation’s context has reached the token threshold, which you can change from its default of 200,000
- Idle time: about an hour has passed since the last request, and your computer stays awake until then
- Scope: Any file
  - true: Claude Code compacts idle conversations that meet the conditions
  - false: Claude Code doesn’t compact while your session is idle
- Default: true
- Per-session overrides: DISABLE_AUTO_COMPACT turns idle compaction off along with auto-compaction

```
{
  "idleCompaction": false
}

```
- Another settings source sets the key: a value in managed settings, the --settings flag, or a project or local settings file overrides your user settings. Change the key in that source instead
- Feature flags are unavailable on a version before v2.1.314: where Claude Code can’t fetch feature flags from Anthropic, idle compaction doesn’t run, so there is nothing to turn off
#### Idle compaction [compacts](/docs/en/context-window#what-survives-compaction) a long conversation that you’ve stepped away from. Your next message then sends a summary instead of the whole conversation. Once compacted, the conversation shows a notice:

****``
****``
****``

Idle compaction is on by default for conversations that meet all of these conditions:

****
****``
****
****
****

To turn idle compaction off, set this key to false.

****``
****``
``

****``
****``

settings.json
To turn idle compaction off or on from inside a terminal session, run /config and change the **Idle compaction** row. Your choice is saved to your user settings and applies right away. The row requires Claude Code v2.1.302 or later. If you run one of those versions and /config doesn’t show the row, check for these causes:

****``
****

The key requires Claude Code v2.1.290 or later. On an earlier version, which ignores this key, turn off [autoCompactEnabled](#autocompactenabled) to stop idle compaction.
[​](#change-the-idle-compaction-threshold)Change the idle compaction threshold

```
{
  "env": {
    "CLAUDE_CODE_IDLE_COMPACT_MIN_TOKENS": "150000"
  }
}

```
#### Set [CLAUDE_CODE_IDLE_COMPACT_MIN_TOKENS](/docs/en/env-vars) to the number of tokens a conversation’s context must reach before idle compaction applies to it. Use a positive whole number. Values below 100000 are raised to 100000, the lowest threshold.
At the default, a conversation on a 200K context window auto-compacts before it reaches 200,000 tokens. This example lowers the threshold to 150,000 so that those conversations qualify:
settings.json
[​](#idle-compaction-in-vs-code-and-the-desktop-app)Idle compaction in VS Code and the desktop app

```
Compacted using a summary written while you were away · turn off with "idleCompaction": false in settings.json

```
### A notice like this one means Claude Code [replaced your earlier conversation with a summary](/docs/en/context-window#what-survives-compaction) that Claude now works from:

You don’t need to do anything. To turn idle compaction off, set idleCompaction to false in ~/.claude/settings.json on the machine or WSL distribution where the session runs, or in another [settings file](/docs/en/settings#settings-files-and-who-they-affect).
[​](#plansdirectory)plansDirectory`
- Scope: Any file
- Type: string, a path relative to the project root
- Default: unset, so Claude Code uses ~/.claude/plans

```
{
  "plansDirectory": "./plans"
}

```
- Outside the project root: the path resolves outside the project root, as "../plans" does.
- Backslash on macOS, Linux, and WSL: the resolved path contains a backslash, as the Windows-style "docs\\plans" does. Write "docs/plans", which works on Windows too.
### Choose where Claude Code stores the plan files it writes in [plan mode](/docs/en/permission-modes#analyze-before-you-edit-with-plan-mode). Claude Code resolves the path relative to the project root.

****``
****
****``

settings.json
Claude Code stores plans in ~/.claude/plans instead of the directory you set in cases such as these:

****``
****````

[​](#skilllistingbudgetfraction)skillListingBudgetFraction`
- Scope: Any file
- Type: number, a fraction greater than 0 and at most 1
- Default: 0.01, which reserves 1% of the context window

```
{
  "skillListingBudgetFraction": 0.02
}

```
### Each turn, Claude sees a [listing of your skills](/docs/en/skills#skill-descriptions-are-cut-short) with their descriptions, and Claude Code caps that listing at a share of the context window. When the listing is over the cap, Claude Code keeps every skill’s name but drops the descriptions of the least-used skills, so Claude can still invoke those skills but is less likely to choose one on its own. Raise this key to keep more descriptions visible at the cost of more context per turn.

****``
****````
****``

settings.json
To see how much context the listing uses and which skills contribute most, run /doctor.
[​](#skilllistingmaxdescchars)skillListingMaxDescChars`
- Scope: Any file
- Type: number of characters, a positive integer
- Default: 1536

```
{
  "skillListingMaxDescChars": 2048
}

```
### Each turn, Claude sees a [listing of your skills](/docs/en/skills#skill-descriptions-are-cut-short) that shows each skill’s description and when_to_use text. This key caps how many characters of that text Claude Code shows per skill; longer text is cut at the cap.

****``
****
****``

settings.json
Raise it to keep long descriptions intact at the cost of more context per turn; lower it to fit more skills under [skillListingBudgetFraction](#skilllistingbudgetfraction).
[​](#taskoutputmaxchars)taskOutputMaxChars`
## Removed in v2.1.277, together with the TaskOutput tool it sized. Setting it has no effect on current versions. Claude reads a background task’s [output file](/docs/en/tools-reference#background-commands) with Read instead.
Through v2.1.276, you set this key to the number of characters of a [background task’s](/docs/en/tools-reference#background-commands) output that Claude received inline when it read the task with the TaskOutput tool.
[​](#interface-and-terminal)Interface and terminal
### Change how Claude Code looks and behaves in your terminal: theme, editor mode, status line, spinner, notifications inside the session, and accessibility. See [Terminal configuration](/docs/en/terminal-config).
[​](#askuserquestiontimeout)askUserQuestionTimeout`
- Scope: User or managed
- Type: string, one of "60s", "5m", "10m", or "never"
- Default: "never"

```
{
  "askUserQuestionTimeout": "5m"
}

```
### Let an unanswered [AskUserQuestion](/docs/en/tools-reference) dialog auto-continue after a period of idle time, submitting whatever options you had already selected. Set it when you step away and want Claude to continue without you. With the default, questions wait until you answer them. For when the timer pauses or never starts, see [Question auto-continue timeout](/docs/en/tools-reference#question-auto-continue-timeout).

****``
****````````
****``

settings.json
Appears in /config as **Question auto-continue timeout**, which writes this key to user settings; Claude Code hides the row while managed settings or the --settings flag set the key.
[​](#autocontinueatusagelimit)autoContinueAtUsageLimit`
- Scope: User or managed. Read from user settings, --settings, and managed settings only. When none of those sets the key, a project or local settings file that sets it turns the feature off rather than being ignored.
  - true: after a claude.ai usage limit stops your session, Claude Code waits in the open session and continues the task automatically after the reset
  - false: Claude Code doesn’t start the wait on its own. You can still start a wait yourself from the usage-limit options menu
- Default: true

```
{
  "autoContinueAtUsageLimit": false
}

```
### After a claude.ai usage limit stops your session, wait in the open session and continue the task automatically after the reset. See [Turn automatic continue off](/docs/en/interactive-mode#turn-automatic-continue-off). Requires Claude Code v2.1.234 or later.

****````
****``
``

****``

settings.json
Appears in /config as **Continue automatically at usage limit**, which writes this key to user settings; Claude Code hides the row while managed settings or the --settings flag set the key.
[​](#autoscrollenabled)autoScrollEnabled`
- Scope: Any file
  - true: the conversation follows new output to the bottom
  - false: you stay where you scrolled while Claude keeps working; permission prompts still appear below the transcript
- Default: true

```
{
  "autoScrollEnabled": false
}

```
### Follow new output to the bottom of the conversation in [fullscreen rendering](/docs/en/fullscreen). Turn it off to stay where you scrolled while Claude keeps working; permission prompts still scroll into view.

****``
****``
``

****``

settings.json
Appears in /config as **Auto-scroll** when fullscreen rendering is on, which writes this key to user settings.
[​](#axscreenreader)axScreenReader`
- Scope: User or managed. You can also set the key in a file you pass with --settings. Claude Code ignores the key in project and local settings, so neither a repository nor your own .claude/settings.local.json can turn screen-reader mode on or off.
  - true: Claude Code renders flat text without decorative borders or animations, using the classic renderer
  - false: Claude Code renders normally
- Default: unset, so screen-reader mode is off
- Per-session overrides: --ax-screen-reader takes precedence over CLAUDE_AX_SCREEN_READER, and both take precedence over this key for one session

```
{
  "axScreenReader": true
}

```
### Render screen-reader friendly output: flat text without decorative borders or animations. Screen-reader mode uses the classic renderer, so the tui setting has no effect while it is active; attached [background sessions](/docs/en/agent-view) still render fullscreen.

****``````
****``
``

****
****````

settings.json
[​](#basheditdiffenabled)bashEditDiffEnabled`
- Scope: User or managed. A true counts only from your user settings, JSON passed with --settings, or managed settings, so a true in a repository’s .claude/settings.json or .claude/settings.local.json can’t turn the recording on. A false in either repository file still turns it off unless a higher-precedence file sets true.
- Type: Boolean
- Default: unset, so Claude Code records changes in auto mode and bypassPermissions mode when it directs Claude to edit files through Bash
- Per-session overrides: CLAUDE_CODE_BASH_EDIT_DIFF takes precedence over this key for one session

```
{
  "bashEditDiffEnabled": true
}

```
### Choose whether Claude Code records which files changed in a Git repository while a Bash command runs. When it records them, you see their diff in the terminal after the command, and your [PostToolUse Bash hooks](/docs/en/hooks#bash) receive the changed-file list.
A listed file isn’t always one the command changed. A change that another program or another Bash call made while the command ran can appear there too.
Set the key to true to record them in every permission mode. Requires Claude Code v2.1.269 or later.

****````````````````
****
****``
****``

settings.json
[​](#companyannouncements)companyAnnouncements`
- Scope: Any file
- Type: array of strings
- Default: unset, so no announcement shows

```
{
  "companyAnnouncements": [
    "Welcome to Acme Corp! Review our code guidelines at docs.example.com"
  ]
}

```
### Show your organization’s announcements to users at startup. When you list more than one, Claude Code picks one at random for each session; on a person’s very first launch it shows the first entry.

****``
****
****

settings.json
[​](#defaultshell)defaultShell`
- Scope: Any file
  - "bash": Claude Code runs your ! commands in Bash
  - "powershell": Claude Code runs your ! commands in PowerShell
- Default: "bash", or "powershell" on Windows when Bash isn’t available

```
{
  "defaultShell": "powershell"
}

```
### Choose whether Bash or PowerShell runs the shell commands you type with the [! prefix](/docs/en/interactive-mode#shell-mode-with-prefix) in the input box, the ones Claude Code runs directly and adds to the session.
"powershell" works only while the [PowerShell tool](/docs/en/tools-reference#powershell-tool) is on. The tool is on by default on Windows without Git Bash, and on Windows with Git Bash for claude.ai and Console accounts. In Amazon Bedrock, Google Cloud’s Agent Platform, and Microsoft Foundry sessions, and on macOS, Linux, and WSL, set CLAUDE_CODE_USE_POWERSHELL_TOOL=1 to turn the tool on. Set that variable to 0 to turn the tool off.

****``
****````
````

****````

settings.json
If the shell you name isn’t available, Claude Code uses the other one: "powershell" falls back to Bash when the PowerShell tool is off, and "bash" falls back to PowerShell when Bash isn’t installed.
[​](#dialogexpiry)dialogExpiry`
- Scope: User or managed
- Type: string, one of "60s", "5m", "10m", or "never", which disables the deadline
- Default: "5m"
- Per-session overrides: CLAUDE_CODE_USER_DIALOG_TIMEOUT_MS takes precedence over this key for one session

```
{
  "dialogExpiry": "10m"
}

```
### Set the deadline for dialogs Claude Code [forwards to a remote client](/docs/en/remote-control#limitations), such as a Remote Control or SDK host, and for the approval dialog for a [held cross-session message](/docs/en/cross-session-messaging#control-inbound-messages). On Claude Code v2.1.236 or later, the same deadline bounds the mid-session [Fable usage-credits consent prompt](/docs/en/model-config#fable-and-usage-credits) in a session that may have nobody at the terminal. When no answer arrives before the deadline, Claude Code cancels the dialog and continues with its no-action default. Requires Claude Code v2.1.224 or later.

****``
****````````
****``
****``

settings.json
Permission prompts and [AskUserQuestion](/docs/en/tools-reference#askuserquestion-tool-behavior) questions use their own flows and aren’t governed by this deadline. Appears in /config as **Dialog expiry**, which writes this key to user settings; the row requires Claude Code v2.1.232 or later, and Claude Code hides it while managed settings or the --settings flag set the key.
[​](#editormode)editorMode`
- Scope: Any file
  - "normal": standard key bindings in the prompt input
  - "vim": vim-style editing with NORMAL, INSERT, and VISUAL modes
- Default: "normal"

```
{
  "editorMode": "vim"
}

```
### Choose the key binding mode for the input prompt.

****``
****``
``

****``

settings.json
Appears in /config as **Editor mode**, which writes this key to user settings.
[​](#emojicompletionenabled)emojiCompletionEnabled`
- Scope: Any file
  - true: Claude Code shows emoji suggestions after : and replaces a completed shortcode with its emoji
  - false: Claude Code neither suggests emoji nor replaces shortcodes
- Default: true

```
{
  "emojiCompletionEnabled": false
}

```
### Show emoji suggestions when you type : plus a shortcode in the prompt input, and replace a completed shortcode such as :heart: with its emoji. Set it to false to turn off both.

****``
****````
``

****``

settings.json
See [Emoji shortcodes](/docs/en/interactive-mode#emoji-shortcodes).

[​](#filesuggestion)fileSuggestion`
- Scope: Any file. Under the status line and file suggestion gates, Claude Code turns the command off or runs only a managed value, and skips yours without warning.
- Type: object with type, always "command", and command, the shell command to run
- Default: unset, so Claude Code uses the built-in file suggestion

```
{
  "fileSuggestion": {
    "type": "command",
    "command": "~/.claude/file-suggestion.sh"
  }
}

```
#### Run your own command to supply @ file path autocomplete instead of the built-in file suggestion. The built-in suggestion uses fast filesystem traversal; a large monorepo may do better with project-specific indexing such as a pre-built file index.

****``
****``````
****

settings.json
After you save this, type @ followed by part of a path in the prompt: the suggestions come from your command’s output.
[​](#command-input-and-output)Command input and output

```
{"query": "src/comp"}

```

```
src/components/Button.tsx
src/components/Modal.tsx
src/components/Form.tsx

```

```
#!/bin/bash
query=$(cat | jq -r '.query')
# Replace your-repo-file-index with your own file search command
your-repo-file-index --query "$query" | head -20

```
### Claude Code runs the command with the same environment variables as [hooks](/docs/en/hooks), including CLAUDE_PROJECT_DIR, and stops waiting after five seconds. The command receives JSON on stdin with a query field holding what you’ve typed so far:

Print newline-separated file paths to stdout. Claude Code shows at most 15:

The following script reads the query and hands it to a repository file index:

[​](#footerlinksregexes)footerLinksRegexes`
- Scope: User or managed
- Type: array of objects, each with type set to "regex", a pattern regex, a url template, and an optional label; {name} placeholders in url and label are filled from named capture groups in pattern
- Default: unset, so no badges render

```
{
  "footerLinksRegexes": [
    {
      "type": "regex",
      "pattern": "\\b(?<key>PROJ-\\d+)\\b",
      "url": "https://issues.example.com/browse/{key}",
      "label": "{key}"
    }
  ]
}

```
#### Render extra clickable badges in the footer below the input box when a regex matches turn output: tool results, including file contents and fetched pages, and Claude’s own responses. Use it to turn IDs printed by project CLIs, such as review tools and issue trackers, into session links.

****``
****``````````````````
****

This example matches issue keys such as PROJ-1234 and builds each link from the captured key:
settings.json
With this configured, when PROJ-1234 appears in a tool result or in Claude’s reply, a PROJ-1234 badge appears in the footer linking to https://issues.example.com/browse/PROJ-1234.
[​](#badge-constraints)Badge constraints

| Constraint | Behavior |
| --- | --- |
| URL origin | Captured values are URL-encoded and the constructed URL must share the template’s literal origin. A capture can fill a path segment or query value but can’t change where the link points |
| URL length | Constructed URLs longer than 2048 characters are dropped |
| URL scheme | Must be https, http, or a recognized editor or workspace deep-link scheme: vscode, vscode-insiders, cursor, windsurf, zed, jetbrains, idea, slack, linear, notion, figma |
| Label | Defaults to the matched text and is truncated to 28 display columns |
| Badge count | At most 5 badges render. The oldest is displaced by newer matches and /clear removes them |

### Each entry’s URL, label, and badge count are bounded as follows:
````````````````````````````
When a turn completes, Claude Code matches each entry’s pattern regex against the turn output on the main thread, so a slow regex blocks the UI until it finishes. Nested quantifiers such as (a+)+$ can take exponentially long against certain inputs and freeze the session, so keep each pattern linear and avoid nesting + or *.
Footer badges render alongside a [custom status line](/docs/en/statusline) when one is configured; neither replaces the other. Use a status line for a script-driven row that computes its own content from session data, and footer badges to turn IDs from the conversation into links without a script.
[​](#keybindingflavor)keybindingFlavor`
- Scope: Any file
- Type: string, "classic" or "readline"
- Default: unset
### Deprecated since v2.1.261 and has no effect. The prompt’s word-editing keys always [follow readline conventions](/docs/en/interactive-mode#make-ctrl-w-delete-back-to-whitespace), as in Bash. Claude Code still accepts keybindingFlavor, so a settings file that sets it stays valid.
In v2.1.238 through v2.1.260, setting it to "readline" made Ctrl+W delete back to the previous whitespace instead of only the previous word.

****``
****````
****

[​](#maxprosewidth)maxProseWidth`
- Scope: Any file
- Type: number of terminal columns, a whole number, minimum 40. Claude Code ignores any other value
- Default: unset, so prose wraps at the terminal edge

```
{
  "maxProseWidth": 80
}

```
### Cap the width of the prose in Claude’s responses so lines stay readable in a wide terminal. Paragraphs, headings, lists, and blockquotes wrap within this many columns, while tables and code blocks keep the full terminal width. Requires Claude Code v2.1.282 or later.

****``
****``
****

settings.json
[​](#prefersreducedmotion)prefersReducedMotion`
- Scope: Any file
  - true: Claude Code reduces or turns off interface animations such as the spinner, shimmer, and flash effects
  - false: the same as unset; Claude Code shows its animations
- Default: false

```
{
  "prefersReducedMotion": true
}

```
### Reduce or turn off interface animations such as the spinner, shimmer, and flash effects. Appears in /config as **Reduce motion**.

****``
****``
``

****``

settings.json
[​](#promptsuggestionenabled)promptSuggestionEnabled`
- Scope: Any file
  - true: you see prompt suggestions in your prompt input
  - false: Claude Code hides prompt suggestions
- Default: true
- Per-session overrides: CLAUDE_CODE_ENABLE_PROMPT_SUGGESTION takes precedence over this key for one session

```
{
  "promptSuggestionEnabled": false
}

```
### Show or hide [prompt suggestions](/docs/en/interactive-mode#prompt-suggestions), the grayed-out predictions that appear in your prompt input. Set it to false, or turn off **Prompt suggestions** in /config, to hide them.

****``
****``
``

****``
****``

settings.json
Prompt suggestions need a claude.ai or Console account with telemetry on. On Amazon Bedrock, Google Cloud’s Agent Platform, and Microsoft Foundry, or with telemetry turned off, such as by [DISABLE_TELEMETRY](/docs/en/env-vars), this key has no effect and only CLAUDE_CODE_ENABLE_PROMPT_SUGGESTION=1 turns them on.
[​](#respectgitignore)respectGitignore`
- Scope: Any file. When no settings file sets it, Claude Code falls back to respectGitignore in ~/.claude.json, which the /config toggle writes.
  - true: the @ file picker leaves out files that match .gitignore patterns
  - false: the @ file picker includes files that match .gitignore patterns
- Default: true

```
{
  "respectGitignore": false
}

```
### Control whether the @ file picker leaves out files that match .gitignore patterns. Appears in /config as **Respect .gitignore in file picker**.

****````````
****``````
``````

****``

settings.json
[​](#respondtobashcommands)respondToBashCommands`
- Scope: Any file
  - true: Claude Code adds the command’s output to the conversation and Claude replies to it
  - false: Claude Code adds the output to context without a reply
- Default: true

```
{
  "respondToBashCommands": false
}

```
### Choose whether Claude responds after you run a shell command with the [! prefix](/docs/en/interactive-mode#shell-mode-with-prefix) in the input box. By default, Claude Code adds the command’s output to the conversation and Claude replies to it. Set this key to false to add the output to context without a reply, so you can run several commands and ask about them together.

****``
****``
``

****``

settings.json
See [Shell mode with ! prefix](/docs/en/interactive-mode#shell-mode-with-prefix).
[​](#showclearcontextonplanaccept)showClearContextOnPlanAccept`
- Scope: Any file
  - true: the plan approval menu gets a first option, Yes, clear context and …, that approves the plan and clears the conversation context
  - false: the plan approval menu shows no clear-context option
- Default: false

```
{
  "showClearContextOnPlanAccept": true
}

```
### When Claude finishes a plan in [plan mode](/docs/en/permission-modes#review-and-approve-a-plan), it shows an approval menu. Planning can use a lot of context, so this key adds a first option to that menu, **Yes, clear context and …**, that approves the plan, clears the conversation context, and starts implementing from the plan alone. The rest of the label names the permission mode the session continues in, and shows how much of your context the planning used.

****``

``

****``

settings.json
[​](#showturnduration)showTurnDuration`
- Scope: Any file. A value in ~/.claude.json from an older version applies when no settings file sets it.
  - true: you see the turn duration message after each response
  - false: Claude Code hides the turn duration message
- Default: true

```
{
  "showTurnDuration": false
}

```
### Show or hide the turn duration message after each response, such as “Cooked for 1m 6s · done 6:05 PM”. The clock after “done” shows when the turn finished; [timeFormat](#timeformat) and [timeZone](#timezone) control its format and zone. Appears in /config as **Show turn duration**.

****````
****``
``

****``

settings.json
[​](#spellcheck)spellcheck`
- Scope: User or managed. The block from the highest tier that sets it applies as a whole.
- Type: object with enabled (Boolean), checker ("aspell", "hunspell", "ispell", or "auto"), language (string, passed to the checker as its dictionary name), and color (string, a terminal color name, #rrggbb, rgb(r,g,b), ansi256(n), or ansi:<name>)
- Default: unset, so spell checking is off; checker defaults to "auto", the first of the three found on PATH; language defaults to the checker’s own dictionary; color defaults to the theme’s error color

```
{
  "spellcheck": { "enabled": true, "language": "en_GB" }
}

```
### Underline misspelled words in the prompt input as you type, using a spell checker you install. Claude Code checks only the text in the input box. [Check spelling as you type](/docs/en/interactive-mode#check-spelling-as-you-type) covers installing aspell, hunspell, or ispell and what the checker covers. Requires Claude Code v2.1.235 or later.

****``
****````````````````````````
****``````````

settings.json
[​](#spinnertipsenabled)spinnerTipsEnabled`
- Scope: Any file
  - true: you see tips in the spinner while Claude is working
  - false: Claude Code hides spinner tips
- Default: true

```
{
  "spinnerTipsEnabled": false
}

```
### While Claude works, the spinner line rotates through short tips about Claude Code features, such as “Use Plan Mode to prepare for a complex request before making changes. Press Shift+Tab twice to enable.” Set this key to false to hide them. Appears in /config as **Show tips**.

****``
****``
``

****``

settings.json
[​](#spinnertipsoverride)spinnerTipsOverride`
- Scope: Any file. Claude Code honors tip objects, tipsFile, label, and excludeDefault from user settings, the --settings flag, and managed settings; from project and local settings it reads plain string tips only.
- Type: object with tips, tipsFile, label, and excludeDefault fields, each optional
- Default: unset, so Claude Code shows only the built-in tips

| Field | Required | Description |
| --- | --- | --- |
| id | Yes | Up to 64 letters, digits, ., _, or -. Claude Code keys the tip’s show history on it, so the tip’s cooldown survives reordering the list. Of two entries with the same id, Claude Code uses the first |
| text | Yes | The tip, one line of up to 500 characters. Claude Code strips ANSI escapes and control characters and collapses whitespace |
| cooldownSessions | No | Sessions Claude Code waits before showing the tip again, 0 to 1000, default 0 |
| priority | No | Order among tips that have gone unshown equally long, higher first, -10 to 10, default 0 |

- tipsFile: an absolute or ~/ path to a local JSON file holding an array of the same entries, or an object with a tips array, up to 256 KB. Claude Code reads the file once per process, so it loads your edits at the next start. You can’t set it through server-managed settings; deploy inline tips there, or deploy the path in an on-disk managed-settings.json.
- label: the prefix Claude Code shows before tips from user, --settings, and managed settings, up to 40 characters. The default is Tip, the same prefix as the built-in tips, and tips from project and local settings always use it.
- excludeDefault: set it to true to hide the built-in tips and show only yours. When Claude Code can’t load any of your tips, for example because tipsFile doesn’t exist or every entry is invalid, it keeps the built-in rotation instead of an empty spinner.

```
{
  "spinnerTipsOverride": {
    "label": "Acme tip",
    "tips": [
      "Run /review before opening a PR",
      {
        "id": "gateway-errors",
        "text": "Seeing 5xx errors? Check the gateway status page first",
        "cooldownSessions": 5,
        "priority": 2
      }
    ]
  }
}

```
- label: Claude Code shows both tips as Acme tip: ... instead of Tip: ....
- The plain string: Claude Code gives it the defaults, so it can come up again in the very next session.
- id: Claude Code keys the second tip’s show history on gateway-errors, so its cooldown still applies after you add or reorder tips.
- cooldownSessions: after Claude Code shows the gateway-errors tip, it doesn’t show that tip again until five sessions later.
- priority: when the gateway-errors tip and another tip have gone unshown for the same number of sessions, for example when neither has been shown yet, Claude Code shows gateway-errors first. The plain string has the default priority, 0.
### Add your own tips to the [spinner tips](#spinnertipsenabled) that Claude Code shows while Claude works, or replace the built-in tips with yours. Claude Code puts your tips in the same rotation as the built-in ones.
If you set [spinnerTipsEnabled](#spinnertipsenabled) to false, Claude Code hides all tips, yours included.

****``````````
****````````
****

Tip objects, tipsFile, label, and the Scope line’s rule that project and local settings contribute plain strings only require Claude Code v2.1.247 or later.
Each tips entry is a plain string or an object with these fields:
``````````````````````````
Claude Code reads a plain string as a tip with those defaults and a position-based id, so its show history resets when you reorder the list. Give a tip an id to keep its history across edits.
Claude Code reads at most 200 tips across tips and tipsFile, and drops an invalid entry with a debug warning instead of rejecting the settings file.
Use the remaining fields to name a tips file, set the prefix, and hide the built-in tips:

``````````
``````
``````

When more than one settings file sets the key, Claude Code shows tips from all of them and takes tipsFile, label, and excludeDefault from whichever of managed settings, the --settings flag, and user settings is the highest-precedence one that sets each.
This example, in your user settings, adds a plain string tip and an object tip to the rotation under the Acme tip prefix:
settings.json
Each field in the example changes one thing about how Claude Code shows the tips:

``````

````
````
````````

While Claude works, Claude Code shows your tips in the spinner with your prefix, such as Acme tip: Run /review before opening a PR.
[​](#spinnerverbs)spinnerVerbs`
- Scope: Any file
  - "append": Claude Code adds your verbs to the built-in set
  - "replace": Claude Code shows only your verbs
- Default: unset, so Claude Code uses the built-in verbs

```
{
  "spinnerVerbs": {
    "mode": "append",
    "verbs": ["Pondering", "Crafting"]
  }
}

```
### While a turn is in progress, the spinner shows a rotating verb such as “Accomplishing”, “Architecting”, or “Baking”. Use this key to add your own verbs to that rotation or replace the built-in list with yours.

****``
****``````
``

****

This example adds two verbs to the built-in set:
settings.json
In "replace" mode with an empty verbs array, Claude Code keeps the built-in verbs.
[​](#statusline)statusLine`
- Scope: Any file. When allowManagedHooksOnly is on, or disableAllHooks is set outside managed settings, only the managed settings value runs.
- Type: object with type set to "command" and a command string, plus optional padding as a number of characters, refreshInterval as a number of seconds, minimum 1, and hideVimModeIndicator as a Boolean
- Default: unset, so no status line

```
{
  "statusLine": {
    "type": "command",
    "command": "jq -r '\"[\\(.model.display_name)] \\(.context_window.used_percentage // 0)% context\"'",
    "padding": 2
  }
}

```
### Run your own command to render a [status line](/docs/en/statusline) below the prompt with context such as the model, cost, or git branch. Optional fields adjust spacing, add periodic re-runs, and hide the built-in vim mode indicator when your script renders vim.mode itself.

****``````
****``````````````
****

This example prints the model name and context usage, and adds two characters of horizontal spacing:
settings.json
The example needs [jq](https://jqlang.org/) installed and runs in a shell. For PowerShell and Git Bash equivalents, see [Windows configuration](/docs/en/statusline#windows-configuration); for the full setup, see [Manually configure a status line](/docs/en/statusline#manually-configure-a-status-line).
[​](#subagentstatusline)subagentStatusLine`
- Scope: Any file. When allowManagedHooksOnly is on, or disableAllHooks is set outside managed settings, only the managed settings value runs.
- Type: object with type set to "command" and a command string
- Default: unset, so Claude Code renders the default rows

```
{
  "subagentStatusLine": {
    "type": "command",
    "command": "jq -c '.tasks[] | {id, content: \"\\(.name): \\(.tokenCount) tokens\"}'"
  }
}

```
### When Claude runs [subagents](/docs/en/sub-agents), Claude Code lists them in a task display below the prompt, one row per subagent showing name · description · token count. This key lets you run your own command to rewrite those rows, for example to show each subagent’s context usage as a percentage. On each refresh, Claude Code sends the visible rows as one JSON object on stdin, with a tasks array carrying each subagent’s id, name, status, model, tokenCount, and more, and replaces the row for each id you write back as a {"id", "content"} line. Rows you don’t write back keep the default rendering.

****``````
****``````
****

settings.json
See [Subagent status lines](/docs/en/statusline#subagent-status-lines).
[​](#syntaxhighlightingdisabled)syntaxHighlightingDisabled`
- Scope: Any file
  - true: Claude Code turns off syntax highlighting in diffs, code blocks, and file previews
  - false: Claude Code highlights syntax
- Default: false

```
{
  "syntaxHighlightingDisabled": true
}

```
### Claude Code colors code by language in the diffs, code blocks, and file previews it shows in the terminal, with its built-in highlighter; no plugin or language server is involved. Set this key to true to show them as plain text instead, for example if the colors clash with your terminal theme or slow a screen reader.

****``
****``
``

****``

settings.json
[​](#terminalprogressbarenabled)terminalProgressBarEnabled`
- Scope: Any file. A value in ~/.claude.json from an older version applies when no settings file sets it.
  - true: you see the terminal progress bar in terminals that support it
  - false: Claude Code hides the terminal progress bar
- Default: true

```
{
  "terminalProgressBarEnabled": false
}

```
### Some terminals can show a progress indicator on the tab or in the taskbar for the program running in them. While Claude is working, Claude Code reports an in-progress state to the terminal, so you can see from another tab or window whether the session is still busy. The indicator stays visible after the turn ends while [background subagents](/docs/en/sub-agents#run-subagents-in-foreground-or-background) or [dynamic workflows](/docs/en/workflows) are still running, and clears once the session is idle.
Claude Code reports it only in terminals that support the indicator: ConEmu, Ghostty 1.2.0 or later, and iTerm2 3.6.6 or later. Set this key to false to stop Claude Code from reporting it. Appears in /config as **Terminal progress bar**.

****````
****``
``

****``

settings.json
[​](#terminaltitlefromrename)terminalTitleFromRename`
- Scope: Any file
  - true: the terminal tab title shows the session name you set
  - false: the tab keeps the title Claude Code generates from your conversation
- Default: true

```
{
  "terminalTitleFromRename": false
}

```
### Claude Code sets your terminal tab’s title. By default it uses a title it generates from the conversation, and once you give the session a [name](/docs/en/sessions#name-your-sessions) with /rename or --name, the tab shows that name instead. Set this key to false to keep the generated title on the tab even after you name the session. The name itself still applies, so /resume <name> and the session picker find it.

****``
****``
``

****``

settings.json
To stop Claude Code from updating the terminal title at all, set [CLAUDE_CODE_DISABLE_TERMINAL_TITLE](/docs/en/env-vars) to 1 instead.
[​](#theme)theme`
- Scope: Any file. A value in ~/.claude.json from an older version applies when no settings file sets it.
  - "auto": matches your terminal’s light or dark background
  - "dark": the dark theme
  - "light": the light theme
  - "dark-daltonized": the dark theme with colorblind-friendly colors
  - "light-daltonized": the light theme with colorblind-friendly colors
  - "dark-ansi": the dark theme using only your terminal’s ANSI color palette
  - "light-ansi": the light theme using only your terminal’s ANSI color palette
  - "custom:<slug>" or "custom:<plugin-name>:<slug>": a custom theme from ~/.claude/themes/ or a plugin
- Default: "dark"

```
{
  "theme": "light-daltonized"
}

```
### Pick the color theme for the interface. Appears in /config as **Theme**.

****````
****``
``
``
``
``
``
``
``````

****``

settings.json
See [Create a custom theme](/docs/en/terminal-config#create-a-custom-theme).
[​](#timeformat)timeFormat`
- Scope: Any file
  - "auto": the same as unset; each time keeps its built-in format, which follows your locale on the turn duration message
  - "12-hour": a 12-hour clock
  - "24-hour": a 24-hour clock
  - "24-hour-utc": a 24-hour clock in UTC with Z after the minutes, such as 18:05Z; Claude Code ignores timeZone for this preset
  - A strftime pattern such as "%H:%M": Claude Code writes each time with the pattern. Any value that contains a % is a pattern, and any other value outside the presets counts as "auto"
- Default: "auto"

```
{
  "timeFormat": "24-hour"
}

```

```
{
  "timeFormat": "%H:%M"
}

```

```
{
  "timeFormat": "%Y-%m-%d %H:%M"
}

```
### Choose how Claude Code writes the times it shows in the interface, such as the done 6:05 PM at the end of each turn duration message and the timestamps in the [transcript viewer](/docs/en/interactive-mode#transcript-viewer). To pick a preset, run /config and set **Time format**. Requires Claude Code v2.1.257 or later.

****``
****``
``
``
````````
``````

****``

settings.json
/config offers only the presets, so to use a strftime pattern, add the key to a settings file. This example shows each time as a two-digit 24-hour clock:
settings.json
The turn duration message and the transcript viewer then show times such as 18:05. In the transcript viewer, the pattern is the whole timestamp, so add date directives when you want the date there. This example puts the date in front of the clock:
settings.json
The same surfaces then show times such as 2026-09-01 18:05.
[​](#timezone)timeZone`
- Scope: Any file
- Type: string, an IANA time zone name. When Claude Code doesn’t recognize the name, it uses your system time zone
- Default: unset, so times show in your system time zone

```
{
  "timeZone": "Europe/Dublin"
}

```
### Show the times in the interface in a time zone other than your system’s. Set it to an [IANA time zone name](https://www.iana.org/time-zones), such as "UTC" or "Europe/Dublin". The times that [timeFormat](#timeformat) controls then show in this zone. If timeFormat is "24-hour-utc", times stay in UTC and Claude Code ignores this key. /config has no row for this key, so set it in a settings file. Requires Claude Code v2.1.257 or later.

****``
****
****

settings.json
[​](#tui)tui`
- Scope: Any file
  - "default": the classic main-screen renderer
  - "fullscreen": the flicker-free alt-screen renderer with virtualized scrollback
- Default: unset, so Claude Code picks the renderer for you
- Per-session overrides: CLAUDE_CODE_NO_FLICKER and CLAUDE_CODE_DISABLE_ALTERNATE_SCREEN take precedence over this key for one session: CLAUDE_CODE_NO_FLICKER=1 turns fullscreen on, and CLAUDE_CODE_NO_FLICKER=0 or CLAUDE_CODE_DISABLE_ALTERNATE_SCREEN=1 turns it off; when both are set, Claude Code turns it off

```
{
  "tui": "fullscreen"
}

```
### Choose the terminal UI renderer. Use "fullscreen" for the flicker-free [alt-screen renderer](/docs/en/fullscreen) with virtualized scrollback, or "default" for the classic main-screen renderer. Running /tui fullscreen or /tui default writes this key for you.

****``
****``
``

****
****``````````

settings.json
Under tmux -CC or over SSH to Windows, Claude Code keeps the classic renderer unless you set CLAUDE_CODE_NO_FLICKER=1. Background sessions opened from [agent view](/docs/en/agent-view) always use the fullscreen renderer regardless of this setting.
[​](#verbose)verbose`
- Scope: Any file. A value in ~/.claude.json from an older version applies when no settings file sets it.
  - true: you see full tool output
  - false: you see truncated summaries of tool output
- Default: false
- Per-session overrides: --verbose takes precedence over this key for one session

```
{
  "verbose": true
}

```
### By default, the transcript collapses each tool call to a short summary, such as the command Claude ran and a line count of its output, and you press Ctrl+O to switch the whole transcript to the expanded view when you want the details. Set this key to true to show every tool call’s full input and output inline as it happens, which is useful when you’re debugging a hook, an MCP server, or a long shell command. Appears in /config as **Verbose output**.

****````
****``
``

****``
****``

settings.json
A [viewMode](#viewmode) value or a sticky /focus selection overrides this key every session.
[​](#viewmode)viewMode`
- Scope: Any file
  - "default": the normal transcript with truncated tool output
  - "verbose": the transcript with full tool output
  - "focus": only your last prompt, a one-line summary of tool calls with edit diffstats, and the final response. Focus view needs the fullscreen renderer
- Default: unset, so the verbose setting and your last /focus choice apply
- Per-session overrides: --verbose takes precedence over this key for one session

```
{
  "viewMode": "focus"
}

```
### Set the transcript view Claude Code starts in: "default", "verbose", or "focus". When set, it overrides both the sticky /focus selection and the [verbose](#verbose) setting.

****``
****``
``
``

****````
****``

settings.json
[​](#viminsertmoderemaps)vimInsertModeRemaps`
- Scope: User or managed. A repository can’t remap your keystrokes.
- Type: object mapping a two-character sequence to "<Esc>"
- Default: unset

```
{
  "vimInsertModeRemaps": {
    "jj": "<Esc>"
  }
}

```
### Map two-key INSERT-mode sequences to Escape in [vim editor mode](/docs/en/interactive-mode#vim-editor-mode). Each key is exactly two printable characters typed in sequence, and "<Esc>" is the only supported target; Claude Code ignores other entries.

****``
****``
****

settings.json
Has no effect unless editorMode is "vim". See [Remap INSERT-mode key sequences](/docs/en/interactive-mode#remap-insert-mode-key-sequences).
[​](#voice)voice`
- Scope: Any file
  - "hold": you hold the dictation key while speaking and release it to stop
  - "tap": you tap the key once to start recording and again to send
- Default: unset, so dictation is off; when enabled is true and mode is unset, Claude Code uses "hold"

```
{
  "voice": {
    "enabled": true,
    "mode": "tap"
  }
}

```
### Turn on [voice dictation](/docs/en/voice-dictation) and choose how the dictation key behaves. Claude Code writes this object for you when you run /voice.

****``
****````````
``

****````````

This example turns dictation on and makes the key tap once to start recording and again to send:
settings.json
autoSubmit sends the prompt when you release the key in hold mode. Voice dictation requires a claude.ai account.
[​](#voiceenabled)voiceEnabled`
- Scope: Any file
  - true: voice dictation is on when you’re logged in with a claude.ai account and your organization’s policy allows voice, unless voice.enabled is set
  - false: voice dictation is off, unless voice.enabled is set
- Default: unset

```
{
  "voiceEnabled": true
}

```
### Deprecated since v2.1.92, when the [voice](#voice) object replaced it. Claude Code still reads it so older settings files keep working, but new configurations should set voice.enabled.
Turn voice dictation on with the single Boolean form that predates the voice object. When both are set, voice.enabled applies.

****``
****````
````

****

settings.json
[​](#wheelscrollaccelerationenabled)wheelScrollAccelerationEnabled`
- Scope: Any file
  - true: Claude Code accelerates mouse-wheel scroll speed during fast scrolls
  - false: Claude Code scrolls at a constant rate per wheel notch
- Default: true

```
{
  "wheelScrollAccelerationEnabled": false
}

```
## Accelerate mouse-wheel scroll speed during fast scrolls in [fullscreen rendering](/docs/en/fullscreen#mouse-wheel-scrolling). Set it to false for a constant scroll rate per wheel notch.

****``
****``
``

****``

settings.json
[​](#git-and-attribution)Git and attribution
### Control the attribution Claude Code adds to commits and pull requests and how it works with git.

[​](#attribution)attribution`
- Scope: Any file
- Type: object with commit and pr strings and a sessionUrl Boolean, or false to hide all attribution. The false value requires Claude Code v2.1.281 or later; earlier versions reject it and skip the whole user, project, or local settings file that holds it
- Default: unset, so Claude Code uses the standard attribution shown under each sub-key

```
{
  "attribution": {
    "commit": "Generated with AI\n\nCo-Authored-By: AI <ai@example.com>",
    "pr": "",
    "sessionUrl": false
  }
}

```
### Customize the attribution Claude Code adds to git commits and pull requests. Commits get a [git trailer](https://git-scm.com/docs/git-interpret-trailers) such as Co-Authored-By by default; pull request descriptions get plain text. Set each part separately with the sub-keys below.

****``
****``````````
****

To hide all attribution, set attribution to false. In a settings file that earlier versions also read, set [commit](#attribution-commit) and [pr](#attribution-pr) to empty strings and [sessionUrl](#attribution-sessionurl) to false instead.
This example replaces the commit attribution, removes pull request attribution, and drops the session link:
settings.json
Once you set commit or pr, Claude Code ignores the deprecated includeCoAuthoredBy setting and uses its default text for whichever of the two you left unset.
Claude Code tells Claude that your own instructions about attribution, such as a CLAUDE.md or [memory](/docs/en/memory) rule, take precedence over these commit and PR lines, unless the line is set in [managed settings](/docs/en/managed-settings).
[​](#includecoauthoredby)includeCoAuthoredBy`
- Scope: Any file
  - true: the same as unset; Claude Code adds the commit trailer and the pull request attribution text
  - false: Claude Code omits both the commit trailer and the pull request attribution text, unless attribution sets commit or pr, in which case the attribution rules apply
- Default: true

```
{
  "includeCoAuthoredBy": false
}

```
### Deprecated since v2.0.62, when [attribution](#attribution) replaced it. Claude Code still reads it, but new configurations should set attribution.
Use [attribution](#attribution) instead, which replaces this key and lets you change or hide the commit trailer, the pull request text, and the session link separately. Claude Code still honors includeCoAuthoredBy: false from settings files that predate attribution, but ignores it once you set attribution.commit or attribution.pr.

****``
****``
``````````

****``

settings.json
To hide all attribution, see [attribution](#attribution).
[​](#includegitinstructions)includeGitInstructions`
- Scope: Any file
  - true: Claude Code includes its built-in commit and pull request workflow instructions and the git status snapshot. Cloud sessions never include the snapshot
  - false: Claude Code leaves both out
- Default: true
- Per-session overrides: CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS takes precedence over this key for one session

```
{
  "includeGitInstructions": false
}

```
- -p runs: you replace the prompt when you pass --system-prompt or --system-prompt-file. You also replace it when you run a custom agent with its own prompt, selected with --agent or the agent setting. Outside bare mode, to keep the snapshot, run without a custom agent and add your instructions with --append-system-prompt instead of replacing the prompt.
- Agent SDK: you replace the prompt with a custom system prompt or a custom main-thread agent. If you set no system prompt, the SDK uses its minimal default and the session starts without the snapshot too. Outside bare mode, to keep the snapshot, use the claude_code preset without a custom agent.
### Claude Code gives Claude two git-related pieces of context: its built-in instructions for how to write commits and pull requests, in the Bash tool’s description, and a git status snapshot of your repository. The snapshot holds the current branch, the main branch, git status output, and recent commits. Claude Code reads it when a conversation starts.
Set this key to false to leave both out, for example when you use your own git workflow skills.

****``
****``
``

****``
****``

settings.json
If you replace the system prompt in [non-interactive mode](/docs/en/headless) or the Agent SDK, the session starts without the snapshot even when this key is true:

``````````
****````

[​](#prurltemplate)prUrlTemplate`
- Scope: Any file
- Type: string, a URL template using any of the five placeholders
- Default: unset

```
{
  "prUrlTemplate": "https://reviews.example.com/{owner}/{repo}/pull/{number}"
}

```
### Point the PR links Claude Code renders, in the footer badge and in tool-result summaries, at an internal code-review tool instead of github.com. Claude Code substitutes {host}, {owner}, {repo}, {number}, and {url} from the PR URL. [GitLab merge request](/docs/en/interactive-mode#gitlab-merge-requests) links on both surfaces keep their GitLab URL.

****``
****
****

settings.json
Claude Code applies the template only to the links it renders itself; a PR number Claude writes in a message, such as #123, stays as Claude wrote it. A URL that doesn’t have the /pull/<number> shape is left unchanged.
[​](#attribution-commit)attribution.commit`
- Scope: Any file
- Type: string
  - When Claude Code recognizes the model as a Claude model but can’t confirm its exact version, it writes Claude alone.
  - When it can’t match the model ID to any Claude model, such as a third-party model served through a custom ANTHROPIC_BASE_URL, it writes Claude Code.

```
{
  "attribution": {
    "commit": "Generated with AI\n\nCo-Authored-By: AI <ai@example.com>"
  }
}

```
### Set the attribution text Claude Code adds to git commits, including any trailers. Set it to an empty string to hide commit attribution.

****``
****
****``````
````

This example replaces the default trailer with a custom line and a custom Co-Authored-By trailer:
settings.json
[​](#attribution-pr)attribution.pr`
- Scope: Any file
- Type: string
- Default: unset, so Claude Code adds 🤖 Generated with [Claude Code](https://claude.com/claude-code)

```
{
  "attribution": {
    "pr": ""
  }
}

```
### Set the attribution text Claude Code adds to pull request descriptions. Set it to an empty string to hide pull request attribution.

****``
****
****``

settings.json
[​](#attribution-sessionurl)attribution.sessionUrl`
- Scope: Any file
  - true: Claude Code appends the claude.ai session link when it commits or opens a pull request from a cloud or Remote Control session
  - false: Claude Code omits the link
- Default: true

```
{
  "attribution": {
    "sessionUrl": false
  }
}

```
## Choose whether Claude Code appends the claude.ai session link when it commits or opens a pull request from a [cloud](/docs/en/claude-code-on-the-web) or [Remote Control](/docs/en/remote-control) session. Claude Code adds the link as a Claude-Session trailer on commits and as a link in pull request descriptions. Set it to false to omit the link.

****``
****``
``

****``

settings.json

[​](#hooks-and-automation)Hooks and automation
### Register hooks, restrict which hooks run, and control workflows. For hook events and payloads, see the [hooks reference](/docs/en/hooks).
[​](#allowedhttphookurls)allowedHttpHookUrls`
- Scope: Any file. Arrays merge across settings files.
- Type: array of URL patterns, with * as a wildcard
- Default: unset, so any URL is allowed

```
{
  "allowedHttpHookUrls": ["https://hooks.example.com/*", "http://localhost:*"]
}

```
### Limit which URLs [HTTP hooks](/docs/en/hooks#http-hook-fields) can target. When you define this key, Claude Code runs an HTTP hook only if its URL matches one of the patterns and blocks the rest without running them; an empty array blocks every HTTP hook.

****``
****``
****

This example allows any URL under https://hooks.example.com/ and any http://localhost URL:
settings.json
Hostname matching is case-insensitive and treats hooks.example.com., with the trailing dot that marks a fully qualified domain name, the same as hooks.example.com, which is how DNS treats them. The allowlist applies to hooks from every source, including managed settings.
In the Agent SDK’s managedSettings option, Claude Code ignores a list with entries, so pass it in the SDK’s [settings option](/docs/en/agent-sdk/typescript#options) instead. See [what an empty list does in parent settings](/docs/en/claude-apps-gateway#how-hook-and-skill-keys-in-parent-settings-take-effect).
[​](#allowmanagedhooksonly)allowManagedHooksOnly`
- Scope: Managed
  - true: only managed hooks run, plus Agent SDK hooks and hooks from plugins your managed settings force-enable. See What runs under allowManagedHooksOnly
  - false: hooks from every settings scope and plugin run
- Default: unset, so hooks from every settings scope and plugin run

```
{
  "allowManagedHooksOnly": true
}

```
#### Restrict hook execution to hooks your organization deploys.

****``
****````
``

****

managed-settings.json
[​](#what-runs-under-allowmanagedhooksonly)What runs under allowManagedHooksOnly`
- Managed and SDK hooks run: hooks from managed settings and hooks the Agent SDK registers in process
- Force-enabled plugin hooks run: hooks from plugins your managed settings force-enable through enabledPlugins. Claude Code matches on the full plugin@marketplace ID, so a plugin with the same name from a different marketplace stays blocked. This lets you distribute vetted hooks through an organization marketplace while blocking everything else. A mod in such a plugin loads only when it counts as your organization’s
- Monitors from other plugins are blocked: a plugin’s monitors don’t start unless the plugin is force-enabled. Requires Claude Code v2.1.310 or later
- Everything else is blocked: user, project, and local hooks, hooks and mods from other installed plugins, and hooks declared in agent frontmatter. Mods built into Claude Code keep running. To block only users’ mods, set allowManagedModsOnly instead.
- Command-sourced plugins are disabled: Claude Code also disables plugins with a command source, including plugins force-enabled in managed enabledPlugins, unless you set disableCommandPluginSources to false explicitly
- Marketplace headersHelper commands are blocked: Claude Code also blocks marketplace headersHelper commands unless disableCommandPluginSources is explicitly set to false, except for a marketplace that managed settings themselves declare. Requires Claude Code v2.1.238 or later
- Status line and file suggestion narrow to managed settings: Claude Code reads statusLine, fileSuggestion, and subagentStatusLine from managed settings only, following the status line and file suggestion gates
### When you set it to true, Claude Code changes which hooks and hook-like commands load:

****
****````
****
****``
****````````
``````
****``````

The [/goal](/docs/en/goal) command can’t run while this key is set, because it depends on hooks.
[​](#disableallhooks)disableAllHooks`
- Scope: Any file. Only managed settings can disable managed hooks.
  - true: Claude Code turns off hooks, any custom status line, and any custom file suggestion command
  - false: hooks, the status line, and the file suggestion command run
- Default: unset, so hooks run

```
{
  "disableAllHooks": true
}

```
- In managed settings: Claude Code disables every configured hook, including managed ones, and keeps running the hooks the Agent SDK registers in process
- In the Agent SDK’s managedSettings option: on a machine where an administrator deploys managed settings, Claude Code ignores this key unless the administrator lets an embedding host add policy. Where the key takes effect, user, project, local, and plugin hooks stop, as do any in the SDK’s settings option. An administrator’s managed hooks, force-enabled plugins’ hooks, and your SDK hook callbacks keep running. Requires Claude Code v2.1.309 or later.
- In any other settings file: Claude Code disables user, project, local, and plugin hooks; managed hooks, Agent SDK hooks, and hooks from plugins force-enabled in managed enabledPlugins keep running
- In managed settings: the mods in every installed plugin stop, your organization’s included
- In any other settings file: the mods you installed stop, and your organization’s mods keep running
#### Turn off [hooks](/docs/en/hooks#disable-or-remove-hooks), any custom [status line](/docs/en/statusline), and any custom [file suggestion](#filesuggestion) command. Use it to turn all of these off temporarily without deleting them from your settings.

****``
****``
``

****

settings.json
The reach depends on which file carries the key:

****
``
****``

The key also stops [mods](/docs/en/plugins/mods/overview), which are plugins whose code registers hooks:

****
****

Mods built into Claude Code keep running in both cases. Each has [its own switch](/docs/en/plugins/mods/overview#mods-built-into-claude-code).
Keeping Agent SDK hooks running when managed settings set this key requires Claude Code v2.1.242 or later.
The [/goal](/docs/en/goal) command can’t run while hooks are disabled, and the /hooks menu shows a notice instead of your hooks.
[​](#status-line-and-file-suggestion-gates)Status line and file suggestion gates
- Off entirely: when managed settings set disableAllHooks, or when the folder isn’t trusted under the same workspace trust rule as hooks in settings files
- Narrowed to managed settings: when allowManagedHooksOnly is set, when disableAllHooks is true outside managed settings after settings precedence applies, or when you start Claude Code with --safe-mode
### Claude Code makes two decisions for statusLine, fileSuggestion, and subagentStatusLine, in this order:

****``
****````````

Under narrowing, Claude Code runs a managed value if one is deployed. Otherwise it skips your value without warning: the status line is disabled, and @ autocomplete falls back to the built-in file suggestion.
[​](#disableworkflows)disableWorkflows`
- Scope: Any file
  - true: Claude Code turns off dynamic workflows and the bundled workflow commands for everyone your settings reach
  - false: the same as unset; whether workflows are on then follows enableWorkflows and your plan’s default
- Default: false
- Per-session overrides: CLAUDE_CODE_DISABLE_WORKFLOWS turns workflows off for one session; whichever of the two turns them off, the other can’t turn them back on

```
{
  "disableWorkflows": true
}

```
### Turn off [dynamic workflows](/docs/en/workflows#turn-workflows-off) and the bundled workflow commands for everyone your settings reach, such as an organization through managed settings. To turn workflows on or off just for yourself, use [enableWorkflows](#enableworkflows) instead, which the **Dynamic workflows** toggle in /config writes to your user settings.

****``
****``
````

****``
****``

settings.json
[​](#enableworkflows)enableWorkflows`
- Scope: Any file
  - true: Claude Code turns dynamic workflows on for you
  - false: Claude Code turns dynamic workflows off for you
- Default: unset, so workflows are on unless you’re on the Pro plan, where they’re off
- Per-session overrides: CLAUDE_CODE_DISABLE_WORKFLOWS turns workflows off for one session, and true here can’t turn them back on while it’s set

```
{
  "enableWorkflows": true
}

```
### Turn [dynamic workflows](/docs/en/workflows) on or off for yourself when your plan’s default isn’t what you want. Appears in /config as **Dynamic workflows**, which writes this key to your user settings and removes it again when you toggle back to your plan’s default. To turn workflows off for everyone from managed settings, use [disableWorkflows](#disableworkflows) instead.

****``
****``
``

****
****````

settings.json
[disableWorkflows](#disableworkflows) and your organization’s workflows policy also take precedence: enableWorkflows: true can’t turn workflows back on while any source turns workflows off. Claude Code hides the /config row while a source other than your user settings sets enableWorkflows, or sets disableWorkflows to true.
[​](#hooks)hooks`
- Scope: Any file. Hooks merge across files rather than replacing each other, and hooks from managed settings can’t be removed from other files.
- Type: object keyed by hook event; each value is an array of { "matcher", "hooks" } groups whose hooks entries have a type of "command", "prompt", "agent", "http", or "mcp_tool"
- Default: unset, so no hooks run

```
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": "~/.claude/hooks/check-bash.sh" }
        ]
      }
    ]
  }
}

```
### Run your own commands, prompts, agents, HTTP requests, or MCP tools as [hooks](/docs/en/hooks) at points in Claude Code’s lifecycle, such as before a tool call or when a session starts; the [hooks reference](/docs/en/hooks#hook-events) lists every event, its payload, and its exit codes. Each event maps to a list of matcher groups, and each group lists the handlers to run when the matcher applies.

****``
****````````````````
****

This example runs a script before every Bash tool call:
settings.json
For every event, matcher pattern, and handler field, see the [hooks reference](/docs/en/hooks#configuration). To turn hooks off, see [disableAllHooks](#disableallhooks); to limit hooks to the ones your organization deploys, see [allowManagedHooksOnly](#allowmanagedhooksonly).
[​](#httphookallowedenvvars)httpHookAllowedEnvVars`
- Scope: Any file. Arrays merge across settings files.
- Type: array of environment variable names
- Default: unset, so each hook’s own allowedEnvVars list applies

```
{
  "httpHookAllowedEnvVars": ["MY_TOKEN", "HOOK_SECRET"]
}

```
### An [HTTP hook](/docs/en/hooks#http-hook-fields) can put the value of an environment variable into a request header, for example an Authorization: Bearer $HOOK_TOKEN header, but only for variables the hook lists in its own allowedEnvVars. This key sets an outer limit on that list for every HTTP hook: a hook can use a variable only if both its own allowedEnvVars and this key name it. Use it to stop a hook from reading a secret it shouldn’t, even when the hook’s definition asks for it.

****``
****
****``

This example limits header interpolation to MY_TOKEN and HOOK_SECRET:
settings.json
The allowlist applies to hooks from every source, including managed settings.
In the Agent SDK’s managedSettings option, Claude Code ignores a list with entries, so pass it in the SDK’s [settings option](/docs/en/agent-sdk/typescript#options) instead. See [what an empty list does in parent settings](/docs/en/claude-apps-gateway#how-hook-and-skill-keys-in-parent-settings-take-effect).
[​](#workflowkeywordtriggerenabled)workflowKeywordTriggerEnabled`
- Scope: Any file. Appears in /config as Ultracode keyword trigger.
  - true: typing ultracode in a prompt triggers a dynamic workflow
  - false: you can type the word without triggering one
- Default: true

```
{
  "workflowKeywordTriggerEnabled": false
}

```
### Choose whether typing the keyword ultracode in a prompt triggers a [dynamic workflow](/docs/en/workflows#ask-for-a-workflow-in-your-prompt). Set it to false to type the word without triggering one.

****````
``

****``

settings.json
The ultracode effort setting, /workflows, and saved workflow commands are unaffected.
[​](#workflowsizeguideline)workflowSizeGuideline`
- Scope: Any file. A value there takes precedence over the Dynamic workflow size choice in /config, which Claude Code stores in ~/.claude.json, and Claude Code hides that row while a settings file sets the key.
  - "unrestricted": no guideline, so Claude sizes the workflow to the task
  - "small": Claude aims for fewer than 5 agents
  - "medium": Claude aims for fewer than 10 agents
  - "large": Claude aims for fewer than 50 agents
- Default: "medium", or "small" when you’re signed in on a Pro plan with Claude Code v2.1.271 or later

```
{
  "workflowSizeGuideline": "small"
}

```
## Set the [agent count Claude aims for](/docs/en/workflows#set-a-size-guideline) in the dynamic workflows it writes. Claude Code sends the value to Claude as advice, not an enforced cap: "small" asks for fewer than 5 agents, "medium" fewer than 10, and "large" fewer than 50. Choose "small" when you want to bound what a workflow spends.

````
****``
``
``
``

****````

settings.json

[​](#plugins-and-skills)Plugins and skills
### Enable plugins, register marketplaces, restrict which plugin sources an organization allows, and control which skills load. For installing and building plugins, see [Plugins](/docs/en/plugins/overview).
[​](#disablebundledskills)disableBundledSkills`
- Scope: Any file
  - true: Claude Code removes bundled skills and workflows and hides built-in commands such as /init from the model
  - false: bundled skills load
- Default: unset, so bundled skills load
- Per-session overrides: CLAUDE_CODE_DISABLE_BUNDLED_SKILLS set to 1 turns bundled skills off for one session; whichever of the two turns them off, the other can’t turn them back on

```
{
  "disableBundledSkills": true
}

```
### Turn off the [skills](/docs/en/skills) and workflows included with Claude Code. Claude Code removes bundled skills and workflows entirely, while built-in commands such as /init stay typable but are hidden from the model.

****``
****````
``

****
****````

settings.json
Skills from plugins, .claude/skills/, and .claude/commands/ are unaffected. /doctor stays typable like the built-in commands; to hide it, set [DISABLE_DOCTOR_COMMAND](/docs/en/env-vars) instead.
[​](#disableskillshellexecution)disableSkillShellExecution`
- Scope: Any file. A true in managed settings can’t be overridden by false elsewhere.
  - true: Claude Code replaces each inline shell command with [shell command execution disabled by policy] instead of running it
  - false: inline shell runs
- Default: unset, so inline shell runs

```
{
  "disableSkillShellExecution": true
}

```
### Turn off inline shell execution for !... and ! blocks in [skills](/docs/en/skills) and custom commands from user, project, plugin, or additional-directory sources. Claude Code replaces each command with [shell command execution disabled by policy] instead of running it.

****``````
****````
``

****

settings.json
Bundled skills and skills deployed through managed settings are unaffected.
[​](#skilloverrides)skillOverrides`
- Scope: Any file. The /skills menu writes to .claude/settings.local.json.
  - "on": Claude sees the skill and you can type /name
  - "name-only": Claude sees the skill by name without its description
  - "user-invocable-only": Claude doesn’t see the skill, but you can still type /name
  - "off": Claude doesn’t see the skill and /name is hidden from autocomplete
- Default: unset, so every skill is "on"

```
{
  "skillOverrides": {
    "legacy-context": "name-only",
    "deploy": "off"
  }
}

```
### Hide or collapse a [skill](/docs/en/skills#override-skill-visibility-from-settings) without editing its SKILL.md. Claude Code applies the value under each skill’s name to the skill list Claude sees and to your / autocomplete.

****``````
****````
``
````
````

****``

This example lists legacy-context to Claude by name only and hides deploy from Claude and from / autocomplete:
settings.json
Overrides don’t apply to plugin skills, which you manage through /plugin.
In managed settings and files passed with --settings, a key on a bundled skill’s alias, such as checkup for /doctor, also applies to the skill; see [how alias keys combine with keys on the skill’s own name](/docs/en/skills#override-skill-visibility-from-settings).
[​](#syncclaudeaiskills)syncClaudeAiSkills`
- Scope: User, local, or managed, and files passed with --settings. A repository can’t turn it off for you.
  - false: Claude Code stops downloading synced skills and stops loading the ones already in ~/.claude/skills/synced/. In user or managed settings, it also moves them to ~/.claude/skills/.trash/
  - true: the same as unset
- Default: unset, so sessions signed in with your claude.ai account sync your skills

```
{
  "syncClaudeAiSkills": false
}

```
### Turn off the download of the [skills enabled for your claude.ai account](/docs/en/skills#how-synced-skills-behave). Claude Code downloads them into ~/.claude/skills/synced/ in [terminal sessions where you sign in with your claude.ai account](/docs/en/skills#where-synced-skills-load), interactive or non-interactive, and in Cowork and cloud sessions. Set false to stop that download and stop loading the skills it already synced. Claude Code honors only false: true is the same as unset and doesn’t turn syncing on where it’s otherwise off.

****````
****``````
``

****

This example keeps a machine from downloading the account’s skills in any session:
settings.json
[​](#syncclaudeaiplugins)syncClaudeAiPlugins`
- Scope: User, local, or managed, and files passed with --settings. A repository can’t turn it off for you.
  - false: Claude Code stops downloading synced plugins and stops loading the ones already in ~/.claude/plugins/synced/. In user or managed settings, it also moves them to ~/.claude/plugins/.trash/
  - true: the same as unset
- Default: unset, so sessions signed in with your claude.ai account sync your plugins

```
{
  "syncClaudeAiPlugins": false
}

```
### Turn off the download of the [plugins enabled for your claude.ai account](/docs/en/plugins/loading#synced-plugins). Claude Code downloads them into ~/.claude/plugins/synced/ at the start of terminal sessions where you sign in with your claude.ai account and in Cowork sessions, and loads each one as <name>@synced. Set false to stop that download and stop loading the plugins it already synced. Claude Code honors only false: true is the same as unset and doesn’t turn syncing on where it’s otherwise off. Requires Claude Code v2.1.273 or later.

****````
****``````
``

****

To turn off one synced plugin rather than all of them, set "<name>@synced": false in [enabledPlugins](#enabledplugins).
This example keeps a machine from downloading the account’s plugins in any session:
settings.json
[​](#allowedchannelplugins)allowedChannelPlugins`
- Scope: Managed
- Type: array of objects, each with marketplace and plugin strings. An entry can instead be a "plugin@marketplace" string such as "telegram@claude-plugins-official", which Claude Code treats as the equivalent object. The string form requires Claude Code v2.1.267 or later; earlier versions reject the whole allowedChannelPlugins value when it contains one
- Default: unset, so Claude Code uses the default Anthropic allowlist

```
{
  "channelsEnabled": true,
  "allowedChannelPlugins": [
    { "marketplace": "claude-plugins-official", "plugin": "telegram" }
  ]
}

```
### Choose which [channel](/docs/en/channels) plugins can push messages into sessions in your organization. When you set it, Claude Code uses your list in place of the default Anthropic allowlist; each entry names a plugin and the marketplace it comes from.

****``
****``````````
****

This example turns channels on and allows only the Telegram plugin from the official Anthropic marketplace:
managed-settings.json
An empty array blocks every channel plugin.
This key takes effect once channels pass the [channelsEnabled](#channelsenabled) gate for the account: on Team and Enterprise plans, and on Console accounts with managed settings, that means channelsEnabled: true. See [Restrict which channel plugins can run](/docs/en/channels#restrict-which-channel-plugins-can-run).
[​](#blockedmarketplaces)blockedMarketplaces`
- Scope: Managed
- Type: array of marketplace source objects, in the same forms as strictKnownMarketplaces
- Default: unset, so no marketplace is blocked

```
{
  "blockedMarketplaces": [
    { "source": "github", "repo": "untrusted/plugins" }
  ]
}

```
### Block plugin marketplace sources for your organization. Claude Code checks the blocklist on marketplace add and on plugin install, update, refresh, and auto-update, so a marketplace someone added before you set the policy can’t be used to fetch plugins either. Blocked sources are checked before download, so they never touch the filesystem.
If you set this key in the [claude.ai admin console](/docs/en/server-managed-settings), claude.ai also applies it when anyone in your organization adds a marketplace from a git repository on claude.ai, as [How restrictions work](/docs/en/plugins/org#restrict-what-users-can-install) describes.

****``
****``
****

This example blocks one GitHub repository as a marketplace source:
managed-settings.json
A github entry may use the [owner-wildcard form](#owner-wildcards) "owner/*" to block every repository under that GitHub owner, which requires Claude Code v2.1.223 or later. Add { "source": "skills-dir" } to stop Claude Code loading [@skills-dir plugins](/docs/en/plugins/loading#plugins-shared-through-a-repository) from both ~/.claude/skills/ and a project’s .claude/skills/, without restricting any marketplace. See [Managed marketplace restrictions](/docs/en/plugins/org#restrict-what-users-can-install).
[​](#channelsenabled)channelsEnabled`
- Scope: Managed
  - true: Claude Code allows channels for your organization
  - false: the same as unset; whether channels are blocked depends on your plan, as the Default says
- Default: unset; channels are blocked on Team and Enterprise plans and on Console accounts with managed settings, and allowed on Pro, Max, and Ultra plans and on Console accounts without managed settings

```
{
  "channelsEnabled": true
}

```
### Allow [channels](/docs/en/channels) for your organization. On claude.ai Team and Enterprise plans, Claude Code blocks channels until you set this to true. For [Anthropic Console](/docs/en/authentication#claude-console-authentication) accounts that authenticate with an API key, channels are allowed by default. If your organization deploys managed settings, Claude Code blocks channels on those accounts too until you set this key to true.

****``
****``
``

****

managed-settings.json
To restrict which plugins can register as channels once they’re enabled, set [allowedChannelPlugins](#allowedchannelplugins). See [Enterprise controls](/docs/en/channels#enterprise-controls).
[​](#disablecommandpluginsources)disableCommandPluginSources`
- Scope: Managed
  - true: Claude Code never runs the marketplace-declared command, doesn’t install or update command-sourced plugins, and stops loading the ones already installed
  - false: Claude Code allows command-sourced plugins explicitly
- Default: unset, so Claude Code follows allowManagedHooksOnly: an organization that restricts hook execution to managed settings gets command sources disabled too. An application that passes disableAllHooks: true in the Agent SDK’s managedSettings option doesn’t by itself disable command sources.

```
{
  "disableCommandPluginSources": true
}

```
### Block the [command plugin source](/docs/en/plugins/marketplace-reference#command-plugin-source), which installs a plugin by running a marketplace-declared command on the user’s machine. When you set it to true, Claude Code never runs the command, doesn’t install or update command-sourced plugins, and stops loading the ones already installed. Set it to false to allow them explicitly. Whenever it blocks command sources, whether you set it to true or leave it unset under [allowManagedHooksOnly](#allowmanagedhooksonly), it also blocks marketplace [headersHelper commands](/docs/en/plugins/host-marketplace#authenticate-archive-downloads), except for a marketplace that managed settings themselves declare. Requires Claude Code v2.1.229 or later, and the headersHelper block requires v2.1.238 or later.

****``
****``
``

****``````

managed-settings.json
Requires Claude Code v2.1.229 or later.
[​](#pluginsuggestionmarketplaces)pluginSuggestionMarketplaces`
- Scope: Managed
- Type: array of marketplace names
- Default: unset, so no marketplace-declared suggestions surface

```
{
  "pluginSuggestionMarketplaces": ["acme-corp-plugins"]
}

```
### Name the marketplaces whose plugins can appear as contextual install suggestions, in spinner tips and pinned at the top of the /plugin **Discover** tab. The built-in first-party frontend-design tip is unaffected. Suggestions come from each plugin’s relevance declaration in its marketplace entry.

****``
****
****

managed-settings.json
A name takes effect only when the marketplace is registered on the machine and its registered source is also declared in the same managed settings, either as the [extraKnownMarketplaces](#extraknownmarketplaces) entry for that name or as an entry of [strictKnownMarketplaces](#strictknownmarketplaces). Claude Code ignores a marketplace registered from a different source under an allowlisted name. The official marketplace is exempt from the source requirement: allowlisting its name alone suffices, since that name can only register from the official Anthropic source. See [Suggest plugins by context](/docs/en/plugins/relevance).
[​](#plugintrustmessage)pluginTrustMessage`
- Scope: Managed
- Type: string
- Default: unset, so Claude Code shows the standard warning alone

```
{
  "pluginTrustMessage": "All plugins from our marketplace are approved by IT"
}

```
### Add your organization’s own text to the plugin trust warning Claude Code shows before installation, for example to confirm that plugins from your internal marketplace are vetted.

****``
****
****

managed-settings.json
[​](#strictknownmarketplaces)strictKnownMarketplaces`
- Scope: Managed
- Type: array of marketplace source objects; see Allowed source types
- Default: unset, so users can add any marketplace. An empty array is a complete lockdown that blocks every marketplace source, including the official Anthropic marketplace

```
{
  "strictKnownMarketplaces": [
    { "source": "github", "repo": "acme-corp/approved-plugins" },
    { "source": "github", "repo": "acme-corp/security-tools", "ref": "v2.0" },
    { "source": "url", "url": "https://plugins.example.com/marketplace.json" }
  ]
}

```
#### Restrict which plugin marketplace sources people in your organization can add and install plugins from. Claude Code enforces the allowlist on marketplace add and on plugin install, update, refresh, and auto-update, before any network or filesystem operation, so a marketplace someone added before you set the policy can’t be used to fetch plugins once its source no longer matches. Blocked users see an error naming the managed policy.
If you set this key in the [claude.ai admin console](/docs/en/server-managed-settings), claude.ai also applies it when anyone in your organization adds a marketplace from a git repository on claude.ai, as [How restrictions work](/docs/en/plugins/org#restrict-what-users-can-install) describes.

****``
****
****

This example allows two GitHub repositories, one pinned to the v2.0 ref, and one hosted marketplace.json URL:
managed-settings.json
You can also write this key as allowedMarketplaces; [Marketplace key aliases](#marketplace-key-aliases) describes how Claude Code treats the alias and which version accepts it. This key is a policy gate: it controls what users may add but registers nothing. To restrict and pre-register in one file, see [Combine with extraKnownMarketplaces](#combine-with-extraknownmarketplaces). For the user-facing view, see [Managed marketplace restrictions](/docs/en/plugins/org#restrict-what-users-can-install).
[​](#allowed-source-types)Allowed source types

| Source | Example entry | Fields |
| --- | --- | --- |
| github | { "source": "github", "repo": "acme-corp/plugins", "ref": "main", "path": "marketplace" } | repo required; ref is a branch or tag; path is a subdirectory |
| git | { "source": "git", "url": "https://gitlab.example.com/tools/plugins.git", "ref": "production" } | url required; ref and path as for github |
| url | { "source": "url", "url": "https://plugins.example.com/marketplace.json", "headers": { "Authorization": "Bearer ${TOKEN}" } } | url required; headers adds HTTP headers for authenticated access |
| file | { "source": "file", "path": "/opt/acme-corp/plugins/marketplace.json" } | path required, the absolute path to a marketplace.json file |
| directory | { "source": "directory", "path": "/opt/acme-corp/approved-marketplaces" } | path required, the absolute path to a directory containing .claude-plugin/marketplace.json |
| hostPattern | { "source": "hostPattern", "hostPattern": "^github\\.example\\.com$" } | hostPattern required, a regex matched anywhere in the marketplace host; anchor it with ^ and $ to match the whole host |
| pathPattern | { "source": "pathPattern", "pathPattern": "^/opt/approved/" } | pathPattern required, a regex matched anywhere in the path of file and directory sources; start it with ^ to pin a prefix |
| skills-dir | { "source": "skills-dir" } | No fields |

- url: a URL marketplace downloads only the marketplace.json file, and Claude Code doesn’t fetch plugin files by relative path from that server, so its plugins must use a plugin source other than a relative path, such as an archive URL, which can be on the same host. For plugins with relative paths, use a Git-based marketplace instead. See Plugins with relative paths fail in URL-based marketplaces.
  - A URL with a scheme, such as https:// or ssh://: the hostname in the URL.
  - An SSH address without a scheme, in git’s user@host:path form, such as git@git.example.com:tools/plugins.git: the host between @ and :, which is the host git connects to.
  - Any other form without a scheme: no host, so no strictKnownMarketplaces hostPattern entry matches it. For a blockedMarketplaces hostPattern, Claude Code takes a host from a wider set of forms, so a blocklist entry can still match such a form. Before v2.1.234, a strictKnownMarketplaces hostPattern also matched some forms that git doesn’t treat as SSH addresses.
- pathPattern: use it to allow filesystem marketplaces alongside hostPattern entries for network sources. ".*" allows every local path; a narrower pattern such as "^/opt/approved/" restricts to a directory.
- skills-dir: any allowlist, even an empty one, stops Claude Code loading @skills-dir plugins from both ~/.claude/skills/ and a project’s .claude/skills/. To keep loading them, add the { "source": "skills-dir" } entry and leave strictPluginOnlyCustomization unset. The entry has no meaning outside this key and blockedMarketplaces.
#### Each entry below shows one allowlist entry per source type and the fields it accepts. Most types match exactly; hostPattern and pathPattern match by regex, and github entries can use an [owner wildcard](#owner-wildcards).
``````````````````````````````````````````````````````````````````````````
Some source types carry rules beyond the table:

``
````````````
````````
````````````

file and directory sources have no host and never match a hostPattern entry.

``````
````````````

[​](#owner-wildcards)Owner wildcards

```
{
  "strictKnownMarketplaces": [
    { "source": "github", "repo": "acme-corp/*" }
  ]
}

```

| Rule | strictKnownMarketplaces | blockedMarketplaces |
| --- | --- | --- |
| Matching source spellings | owner/repo form only. A git URL that clones the same repository doesn’t match | Any spelling, including git URLs that resolve to the same github.com repository |
| Owner case | Case-sensitive | Case-insensitive |
| ref | Follows the exact-entry rules: an entry with a ref matches only sources with that exact ref, and an entry without one matches only sources that don’t specify a ref | An entry without a ref blocks all refs of the repositories it matches |
| path | Looser than the exact-entry rules: an entry with a path requires that exact value, while an entry without one matches any path inside the repository | An entry without a path blocks all paths of the repositories it matches |

#### A github entry whose repo value is "<owner>/*" matches every repository under that GitHub owner. Owner wildcards require Claude Code v2.1.223 or later and work only in strictKnownMarketplaces and blockedMarketplaces. Everywhere else a github source appears, such as extraKnownMarketplaces or /plugin marketplace add, the repo value must name a single repository. Before v2.1.223, Claude Code compared the entry literally, so an allowlist entry matched no repository and a blocklist entry blocked nothing; single-repository entries are enforced on every version.
This entry allows any marketplace repository in the acme-corp organization:
managed-settings.json
Only the whole repository-name position can be a wildcard. Claude Code ignores entries such as *, */plugins, or acme-corp/tools-* as invalid, so they match no repository.
The matching rules differ between the two settings:
``````````````````
[​](#exact-matching)Exact matching
- The repo or url must match exactly
- The ref field must match exactly, or both must be undefined
- The path field must match exactly, or both must be undefined
- { "source": "github", "repo": "acme-corp/plugins" } and { "source": "github", "repo": "acme-corp/plugins", "ref": "main" }
- { "source": "github", "repo": "acme-corp/plugins", "path": "marketplace" } and { "source": "github", "repo": "acme-corp/plugins" }
#### For every source type except owner-wildcard github entries and the regex-matched hostPattern and pathPattern entries, Claude Code allows a user’s addition only when the marketplace source matches an entry exactly. For the git-based sources github and git, exact matching includes the optional fields:

````
``
``

For example, Claude Code treats each pair below as two different sources:

````
````

[​](#allow-only-the-official-marketplace)Allow only the official marketplace

```
{
  "strictKnownMarketplaces": [
    { "source": "github", "repo": "anthropics/claude-plugins-official" }
  ]
}

```
- Non-interactive environments that run before the machine’s first interactive terminal session.
- Machines where Claude Code has only run through the VS Code extension.
- Machines where Claude Code already ran an interactive terminal session under a policy that blocked the marketplace, such as the empty-array lockdown. Claude Code records the blocked attempt and doesn’t retry after the policy changes.
#### To allow the official Anthropic marketplace and nothing else, list its repository:
managed-settings.json
With this entry, Claude Code keeps an already-registered official marketplace available and, on a fresh machine, registers the marketplace automatically the first time you start an interactive terminal session. Automatic registration most commonly misses:

On these machines, add the marketplace to [extraKnownMarketplaces](#extraknownmarketplaces) in the same managed-settings.json so Claude Code registers it automatically, or run claude plugin marketplace add anthropics/claude-plugins-official.
[​](#combine-with-extraknownmarketplaces)Combine with extraKnownMarketplaces`

| Aspect | strictKnownMarketplaces | extraKnownMarketplaces |
| --- | --- | --- |
| Purpose | Organizational policy enforcement | Team convenience |
| Settings file | Managed settings only | Any settings file |
| Behavior | Blocks non-allowlisted additions | Registers missing marketplaces |
| When enforced | Before network and filesystem operations | Immediately from user or managed settings; after the workspace trust dialog for a repository’s files |
| Can be overridden | No, highest precedence | Yes, by higher-precedence settings |
| Source format | Direct source object | Named marketplace with a nested source object |

```
{
  "strictKnownMarketplaces": [
    { "source": "github", "repo": "acme-corp/plugins" }
  ],
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": { "source": "github", "repo": "acme-corp/plugins" }
    }
  }
}

```
### The two keys do different jobs. This table compares them:
``````
To both restrict and pre-register a marketplace for all users, set both in managed-settings.json:
managed-settings.json
With only strictKnownMarketplaces set, users can still add an allowed marketplace themselves with /plugin marketplace add. The official Anthropic marketplace is the only one Claude Code registers automatically, and only when the allowlist allows it. [Allow only the official marketplace](#allow-only-the-official-marketplace) lists the machines it misses.
[​](#strictpluginonlycustomization)strictPluginOnlyCustomization`
- Scope: Managed
- Type: true to lock all four kinds of customization, or an array naming the kinds to lock, from "skills", "agents", "hooks", and "mcp"
- Default: unset, so nothing is locked

```
{
  "strictPluginOnlyCustomization": ["skills", "hooks"]
}

```
### Block skills, agents, hooks, and MCP servers from user and project sources, so they can come only from plugins or managed settings. Combine it with [strictKnownMarketplaces](#strictknownmarketplaces) to control the full customization supply chain: the marketplace allowlist controls which plugins users can install.

****``
****``````````
****

This example locks skills and hooks and leaves agents and MCP servers unlocked:
managed-settings.json
If you lock any surface, Claude Code also stops loading [skills-directory plugins](/docs/en/plugins/loading#skills-directory-plugins-blocked-by-managed-settings), the plugin folders that users keep under ~/.claude/skills/ or .claude/skills/. Users place those folders themselves rather than installing them from a marketplace, so Claude Code treats them as user customization under this setting.
The four sub-key entries below list what else each surface blocks and what still loads. Claude Code ignores surface names it doesn’t recognize rather than failing the settings file, so you can add new surface names before every client has updated.
[​](#strictpluginonlycustomization-skills)strictPluginOnlyCustomization.skills`
- Scope: Managed
- Type: the string "skills" in the strictPluginOnlyCustomization array
- Default: not locked

```
{
  "strictPluginOnlyCustomization": ["skills"]
}

```
### Lock the skills surface. Claude Code stops loading skills from ~/.claude/skills/ and .claude/skills/, custom commands from ~/.claude/commands/ and .claude/commands/, skills and commands under --add-dir directories, and skills synced from your claude.ai account. It keeps loading bundled skills, skills in the managed policy directory, and skills from plugins other than [skills-directory plugins](/docs/en/plugins/loading#skills-directory-plugins-blocked-by-managed-settings).

****``
****````
****

managed-settings.json
[​](#strictpluginonlycustomization-agents)strictPluginOnlyCustomization.agents`
- Scope: Managed
- Type: the string "agents" in the strictPluginOnlyCustomization array
- Default: not locked

```
{
  "strictPluginOnlyCustomization": ["agents"]
}

```
### Lock the agents surface. Claude Code stops loading agents from ~/.claude/agents/, .claude/agents/, and --add-dir directories. It keeps loading built-in agents, agents in the managed policy directory, and agents from plugins other than [skills-directory plugins](/docs/en/plugins/loading#skills-directory-plugins-blocked-by-managed-settings).

****``
****````
****

managed-settings.json
[​](#strictpluginonlycustomization-hooks)strictPluginOnlyCustomization.hooks`
  - Hooks from user, project, and local settings.json
  - Frontmatter hooks in skills, custom commands, and agents, from the sources that a skills or agents lock would block
- Keeps running: hooks in managed settings, and hooks from plugins other than skills-directory plugins
- Scope: Managed
- Type: the string "hooks" in the strictPluginOnlyCustomization array
- Default: not locked

```
{
  "strictPluginOnlyCustomization": ["hooks"]
}

```
### Lock the hooks surface:

****``
````

****

Skills, custom commands, and agents whose frontmatter hooks stop running still load while their own surface isn’t locked.
A personal or project [skill](/docs/en/skills#where-skills-live) that declares hooks in its frontmatter also loses its [allowed-tools](/docs/en/skills#pre-approve-tools-for-a-skill) pre-approval, so your users get permission prompts for the tools that field lists. When such a skill runs in a subagent through [context: fork](/docs/en/skills#run-skills-in-a-subagent), it keeps the pre-approval. A skill that declares no hooks keeps its pre-approval too.

****``
****````
****

managed-settings.json
[​](#strictpluginonlycustomization-mcp)strictPluginOnlyCustomization.mcp`
- Scope: Managed
- Type: the string "mcp" in the strictPluginOnlyCustomization array
- Default: not locked

```
{
  "strictPluginOnlyCustomization": ["mcp"]
}

```
### Lock the mcp surface. Claude Code stops loading MCP servers from ~/.claude.json and .mcp.json. It keeps loading [managed-mcp.json](/docs/en/managed-mcp) servers, servers from [managedMcpServers](#managedmcpservers), and MCP servers from plugins other than [skills-directory plugins](/docs/en/plugins/loading#skills-directory-plugins-blocked-by-managed-settings).

****``
****````
****

managed-settings.json
[​](#enabledplugins)enabledPlugins`
- Scope: Any file
- Type: object mapping plugin-name@marketplace-name to a Boolean
- Default: unset, so each plugin follows its defaultEnabled value

```
{
  "enabledPlugins": {
    "code-formatter@team-tools": true,
    "deployment-tools@team-tools": true,
    "experimental-features@personal": false
  }
}

```
- User settings: your personal plugin preferences
- Project settings: plugins turned on for everyone in the repository. This doesn’t install them, so each user installs them.
- Local settings: per-machine overrides, gitignored when Claude Code saves a setting there
- Managed settings: organization-wide policy. A plugin set to false here is blocked from installation at every scope and hidden from the marketplace
### Turn individual [plugins](/docs/en/plugins/overview) on or off, keyed by plugin-name@marketplace-name. A plugin with no entry at any scope falls back to its [defaultEnabled](/docs/en/plugins/manifest-reference#fields) value. When you enable or disable a plugin with /plugin or claude plugin enable, Claude Code writes this key for you.

****``
****``
****``

This example enables two plugins from the team-tools marketplace and disables one from personal:
settings.json
Each scope serves a different purpose:

****
****
****
****``

Project settings take precedence over user settings, so setting a plugin to false in ~/.claude/settings.json doesn’t disable a plugin that the project’s .claude/settings.json enables. To opt out of a project-enabled plugin on your machine, set it to false in .claude/settings.local.json instead. Plugins force-enabled by managed settings can’t be disabled this way, since managed settings override local settings.
[​](#extraknownmarketplaces)extraKnownMarketplaces`
- Scope: Any file. Claude Code honors entries in a repository’s .claude/settings.json or .claude/settings.local.json only after you accept the workspace trust dialog for that folder; in a folder you haven’t trusted, including a -p run there, it ignores them without a message.
- Type: object mapping a marketplace name to an object with a source object and an optional autoUpdate Boolean
- Default: unset

```
{
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": {
        "source": "github",
        "repo": "acme-corp/claude-plugins"
      }
    },
    "security-plugins": {
      "source": {
        "source": "git",
        "url": "https://git.example.com/security/plugins.git"
      }
    }
  }
}

```
#### Register additional plugin marketplaces by name, so that people who open the repository, or everyone your managed settings reach, get the marketplace without adding it themselves. Claude Code registers each marketplace it doesn’t already know. Whether a plugin that [enabledPlugins](#enabledplugins) names from it installs depends on the plugin’s source and which file enables it; [Enabled in project settings but not installed](/docs/en/plugins/loading#enabled-in-project-settings-but-not-installed) has the rules.

****````````
****````
****

This example registers a GitHub marketplace and a marketplace from a self-hosted git URL:
settings.json
[What runs before you trust a folder](/docs/en/permissions#what-runs-before-you-trust-a-folder) compares the trust gate with the other content a repository can supply. You can also write this key as additionalMarketplaces; see [Marketplace key aliases](#marketplace-key-aliases).
Set "autoUpdate": true alongside source to make Claude Code refresh that marketplace and update its installed plugins in the background after startup. When omitted, claude-plugins-official and most other official Anthropic marketplaces default to true, and third-party marketplaces default to false. See [Configure auto-updates](/docs/en/plugins/install#keep-plugins-updated).
When more than one settings file defines a marketplace entry under the same name, Claude Code uses the entry from the [highest-precedence file](/docs/en/settings#settings-precedence) whole. That entry replaces the lower-precedence entry and inherits none of its fields, so a redefinition can’t combine one file’s source.headers credential with a URL another file controls. Before v2.1.228, Claude Code merged same-name entries field by field, so an entry in a higher-precedence file could inherit fields it didn’t set, including another file’s headers.
[​](#marketplace-source-types)Marketplace source types
- github: a GitHub repository, with repo
- git: any git URL, with url
- url: a direct URL to a marketplace.json file, with url and optional headers and headersHelper for authenticated access. headersHelper names a command that prints headers whose values are too short-lived to list in headers, and requires Claude Code v2.1.238 or later
- file: a local path to a marketplace.json file, with path
- directory: a local filesystem path, with path. Use it for development, or for a marketplace your organization deploys to each machine.
- settings: an inline marketplace declared directly in the settings file without a hosted repository, with name and plugins
- Before each fetch of that marketplace’s marketplace.json, including a later refresh. Claude Code sends the printed headers with that fetch.
- Before each plugin archive download on the marketplace URL’s origin, meaning the same scheme, host, and port. Claude Code sends the output with that download, and no other download gets the headers.

```
{
  "extraKnownMarketplaces": {
    "team-tools": {
      "source": {
        "source": "settings",
        "name": "team-tools",
        "plugins": [
          {
            "name": "code-formatter",
            "source": {
              "source": "github",
              "repo": "acme-corp/code-formatter"
            }
          }
        ]
      }
    }
  }
}

```
- strict: unlike an entry in a marketplace’s marketplace.json, an entry in settings doesn’t need "strict": false, because a settings file carries no manifest fields to inline. See Strict mode.
- Folder trust: for an entry in a project’s .claude/settings.json or .claude/settings.local.json, Claude Code runs the command only after the user has also trusted that folder.
- Header filter: Claude Code drops request-routing and client-identity header names from an entry in a project’s .claude/settings.json or .claude/settings.local.json, because a repository can supply those files. Claude Code applies the same filter to a catalog entry and to an entry in an --add-dir directory’s settings, and no filter to an entry in your user settings, a --settings file, or managed settings.
#### The source object takes one of these forms:

``
``
````````````
````
``
````

The git source type works with any git hosting service, including self-hosted GitLab and Bitbucket. Claude Code clones the repository with the same authentication that git clone would use on that machine: configured credential helpers or SSH keys. A provider token such as GITHUB_TOKEN takes effect through a credential helper that reads it. See [Private repositories](/docs/en/plugins/host-marketplace#grant-access-to-a-private-marketplace) for setup details.
For github and git sources, Claude Code never downloads [Git LFS](https://git-lfs.com) content when it clones the marketplace repository to add or update it. LFS-tracked files are checked out as pointer files, and the add or update output reports how many.
The skipLfs field inside the source object is accepted and has no effect. Before v2.1.274, Claude Code downloaded LFS content unless you set "skipLfs": true.
For a url source, set headersHelper inside the source object when the credential in headers expires and a command has to produce a fresh one. Requires Claude Code v2.1.238 or later. For what the command must print and where Claude Code runs it, see [Write the headersHelper command](/docs/en/plugins/host-marketplace#write-the-headershelper-command), and for the cases where Claude Code doesn’t run it, see [When Claude Code skips a headersHelper command](/docs/en/plugins/host-marketplace#when-claude-code-skips-a-headershelper-command-or-drops-its-output). Once you set headersHelper on an https:// marketplace URL, Claude Code runs the command at two points, reusing one run’s output for up to 60 seconds:

``

Claude Code ignores any headersHelper set in the .claude/settings.json or .claude/settings.local.json of a directory you add with [--add-dir](/docs/en/permissions#what-runs-before-you-trust-a-folder), on a url source and on an inline plugin entry alike, and sends only the fixed headers set in that file. [How users accept a headersHelper command](/docs/en/plugins/host-marketplace#how-users-accept-a-headershelper-command) covers the other settings files.
Plugins listed in a settings source must reference external sources such as GitHub or npm, and the name must match the marketplace key. You still enable each plugin separately in enabledPlugins. This example declares one plugin inline:
settings.json
A plugin entry under source: 'settings' whose own source is an [archive](/docs/en/plugins/marketplace-reference#archive-plugin-source) can set headers for the archive download. If the value you would put in headers is short-lived, such as a token your registry mints on request, set a headersHelper command instead. An entry may set both. Both fields require Claude Code v2.1.238 or later.
Claude Code sends the entry’s headers, and whatever the command prints, with that plugin’s archive download and with no other download. Claude Code runs the command only when a user [installs or updates that one plugin by itself](/docs/en/plugins/host-marketplace#how-users-accept-a-headershelper-command). Three further rules depend on which file holds the entry:

````
****````
****````````

[​](#marketplace-key-aliases)Marketplace key aliases
- Earlier versions ignore the alias, so keep the canonical spelling in a file that older versions also read, such as a managed settings file for a fleet with mixed Claude Code versions.
- In any settings file that accepts the canonical key, Claude Code reads the alias exactly as it reads the canonical key.
- Claude Code may rewrite additionalMarketplaces to extraKnownMarketplaces when it updates the file.
- If you set both spellings in one file, Claude Code uses the canonical value and ignores the alias.
### On Claude Code v2.1.232 or later, you can write extraKnownMarketplaces as additionalMarketplaces and strictKnownMarketplaces as allowedMarketplaces. Claude Code treats each alias as follows:

````

[​](#pluginconfigs)pluginConfigs`
- Scope: User or managed
- Type: object mapping a plugin ID to an object with an options field, mapping each option name to a string, number, Boolean, or array of strings, and an optional mcpServers field holding per-server user configuration values in the same shape
- Default: unset

```
{
  "pluginConfigs": {
    "deployer@acme-tools": {
      "options": {
        "api_endpoint": "https://api.example.com"
      }
    }
  }
}

```
### Store the non-sensitive answers you give a plugin’s [userConfig](/docs/en/plugins/manifest-reference#user-configuration) configuration dialog, keyed by plugin ID. Claude Code writes this key to your user settings when you fill in the dialog, so you don’t need to edit it by hand. Claude Code stores sensitive options in the macOS Keychain instead, falling back to ~/.claude/.credentials.json when the Keychain rejects the write; on platforms without a supported keychain, it stores them in ~/.claude/.credentials.json.

****``
****````
****

This example stores the api_endpoint option for the deployer plugin from acme-tools:
settings.json
Built-in plugins store their options under the same key with an @builtin suffix. For example, the ****[Project instructions](/docs/en/memory#choose-which-instruction-files-load) setting that controls whether Claude Code reads AGENTS.md files is pluginConfigs["cc-plugin-agents-md@builtin"].options.instructionFiles. Before v2.1.285, the plugin’s ID was agents-md@builtin. Later versions read an entry under either ID.
Claude Code ignores project and local entries because it substitutes these values into plugin hook, MCP, and LSP configurations, and a cloned repository must not be able to supply them.
[​](#prependplugins)prependPlugins`
- Scope: User or managed. Claude Code reads the key from managed settings. It reads the key from user settings only on a machine with no managed settings or managed-mcp.json file, in a session whose credential isn’t a Team or Enterprise /login. It ignores the key in project and local settings and in a --settings file.
- Type: array of plugin-name@marketplace-name strings
- Default: unset

```
{
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": { "source": "directory", "path": "/opt/acme/claude-plugins" }
    }
  },
  "enabledPlugins": { "acme-guard@acme-tools": true },
  "prependPlugins": ["acme-guard@acme-tools", "sec-default@builtin"]
}

```
### List the managed plugins whose [mods](/docs/en/plugins/mods/overview) run before every mod a user installs, in the listed order. When you set this key in managed settings, name sec-default@builtin in the list to keep the built-in guard. In managed settings, Claude Code skips an id whose plugin doesn’t count as your organization’s. See [Install your organization’s mods and set the order](/docs/en/plugins/mods/admin#install-your-organizations-mods) for those conditions and for how the two ordering keys work together.

****````````
****``
****

managed-settings.json
[​](#appendplugins)appendPlugins`
- Scope: User or managed. Claude Code reads the key from managed settings. It reads the key from user settings only on a machine with no managed settings or managed-mcp.json file, in a session whose credential isn’t a Team or Enterprise /login. It ignores the key in project and local settings and in a --settings file.
- Type: array of plugin-name@marketplace-name strings
- Default: unset

```
{
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": { "source": "directory", "path": "/opt/acme/claude-plugins" }
    }
  },
  "enabledPlugins": { "acme-audit@acme-tools": true },
  "appendPlugins": ["acme-audit@acme-tools"]
}

```
## List the managed plugins whose [mods](/docs/en/plugins/mods/overview) run after every mod a user installs, in the listed order. An id listed in both prependPlugins and appendPlugins is prepended. In managed settings, Claude Code skips an id whose plugin doesn’t [count as your organization’s](/docs/en/plugins/mods/admin#install-your-organizations-mods).

****````````
****``
****

managed-settings.json
[​](#mcp)MCP
### Control which MCP servers Claude Code connects to and which an organization allows. See [Connect to external tools with MCP](/docs/en/mcp) and [Managed MCP configuration](/docs/en/managed-mcp).
[​](#allowallclaudeaimcps)allowAllClaudeAiMcps`
- Scope: Managed. Users can’t re-enable connectors that exclusive control suppressed.
  - true: Claude Code loads the claude.ai connectors alongside a deployed managed-mcp.json
  - false: a deployed managed-mcp.json takes exclusive control of MCP servers and suppresses the claude.ai connectors Claude Code fetches itself
- Default: false, so a deployed managed-mcp.json suppresses the claude.ai connectors Claude Code fetches itself

```
{
  "allowAllClaudeAiMcps": true
}

```
### Load the [claude.ai connectors](/docs/en/mcp#use-mcp-servers-from-claude-ai) Claude Code fetches itself alongside a deployed managed-mcp.json. Without this key, managed-mcp.json takes exclusive control of MCP servers and suppresses those connectors.

****``
****````
````

****````

managed-settings.json
[allowedMcpServers](#allowedmcpservers) and [deniedMcpServers](#deniedmcpservers) still apply to the connectors this key loads. Connectors delivered to a [cloud session](/docs/en/claude-code-on-the-web) whose host carries a managed-mcp.json, such as a self-hosted runner, stay suppressed. See [Allow claude.ai connectors alongside the managed set](/docs/en/managed-mcp#allow-claude-ai-connectors-alongside-the-managed-set).
[​](#allowclaudeinchromewithmanagedmcp)allowClaudeInChromeWithManagedMcp`
- Scope: Managed, from the device’s own managed settings only: an MDM-deployed plist or HKLM registry key, or a system managed-settings.json file. Claude Code ignores it in server-managed settings, in the user-writable HKCU registry, and in user or project settings.
  - true: the built-in Claude in Chrome server can run alongside a deployed managed-mcp.json
  - false: a deployed managed-mcp.json blocks Claude in Chrome in terminal sessions
- Default: false, so a deployed managed-mcp.json blocks Claude in Chrome in terminal sessions

```
{
  "allowClaudeInChromeWithManagedMcp": true
}

```
### Let the built-in [Claude in Chrome](/docs/en/chrome) server run alongside a deployed managed-mcp.json. Without this key, a deployed managed-mcp.json blocks Claude in Chrome in terminal sessions. Requires Claude Code v2.1.282 or later.

****````
****````
````

****````

managed-settings.json
A [deniedMcpServers](#deniedmcpservers) entry for claude-in-chrome still blocks the server with this key on. See [Allow Claude in Chrome alongside the managed set](/docs/en/managed-mcp#allow-claude-in-chrome-alongside-the-managed-set).
[​](#allowedmcpservers)allowedMcpServers`
- Scope: Any file. Entries from every file merge into one allowlist unless allowManagedMcpServersOnly is set. Deploy it in managed settings to enforce it.
- Type: array of objects, each with exactly one key. Use serverName, a string limited to letters, numbers, hyphens, and underscores; serverCommand, an array of the command and its arguments matched exactly; or serverUrl, a URL pattern with * wildcards
- Default: unset, so every server is allowed; an empty array blocks every server users add

```
{
  "allowedMcpServers": [
    { "serverCommand": ["npx", "-y", "@modelcontextprotocol/server-filesystem"] }
  ]
}

```
### Allowlist the MCP servers people can add. Claude Code blocks any server that doesn’t match an entry wherever it’s defined, including plugin servers, servers a user passes with --mcp-config, and servers from claude.ai.
Built-in servers such as Claude in Chrome, the ide server Claude Code connects to in a running [VS Code](/docs/en/vs-code#the-built-in-ide-mcp-server) or [JetBrains](/docs/en/jetbrains#the-built-in-ide-mcp-server) IDE, and servers the CLI itself configures are exempt from the allowlist, and the denylist still applies to them. On Claude Code v2.1.268 or later, a [Claude Tag](/docs/en/claude-tag) session’s Slack tools are also exempt from the allowlist, and the denylist still applies to them. In-process type: "sdk" servers are exempt from both lists; the [app that started the session](/docs/en/mcp#how-connectors-reach-claude-code) registers them.
Servers your organization delivers are also exempt from the allowlist, and the denylist still applies to them. The exemption covers every [managedMcpServers](#managedmcpservers) entry, and any [managed-mcp.json](/docs/en/managed-mcp#exclusive-control-with-managed-mcp-json) entry whose values use [no ${VAR} expansion outside env](/docs/en/managed-mcp#how-allowlists-and-denylists-apply-to-the-managed-set). See [How a server is evaluated](/docs/en/managed-mcp#how-a-server-is-evaluated) for the full check order. Before v2.1.259, servers from managed-mcp.json had to match too.

****````
****````````
****

This example allows only the stdio server that the listed npx command starts:
settings.json
A [deniedMcpServers](#deniedmcpservers) entry takes precedence, so a server on both lists is blocked. Once the list contains any serverCommand entry, a stdio server must match a serverCommand entry, and once it contains any serverUrl entry, a remote server must match a serverUrl entry: a serverName match no longer admits that kind of server. See [Policy-based control with allowlists and denylists](/docs/en/managed-mcp#policy-based-control-with-allowlists-and-denylists).
[​](#allowmanagedmcpserversonly)allowManagedMcpServersOnly`
- Scope: Managed
  - true: Claude Code reads allowedMcpServers from managed settings alone and ignores allowlists in user, project, and local settings
  - false: allowlists from every settings scope merge
- Default: false, so allowlists from every settings scope merge

```
{
  "allowManagedMcpServersOnly": true,
  "allowedMcpServers": [
    { "serverName": "github" }
  ]
}

```
### Make the managed allowlist the only one that applies. Claude Code then reads [allowedMcpServers](#allowedmcpservers) from managed settings alone and ignores allowlists in user, project, and local settings; [deniedMcpServers](#deniedmcpservers) still merges from every settings scope, so users can still block servers for themselves. Administrators set it so a user’s own settings can’t broaden what the managed allowlist permits.

****``
****````
``

****``

This example locks the allowlist to managed settings and allows only the server named github:
managed-settings.json
Users can still add MCP servers of their own; only servers that match the managed allowlist load. See [Restrict the allowlist to managed settings only](/docs/en/managed-mcp#restrict-the-allowlist-to-managed-settings-only).
[​](#deniedmcpservers)deniedMcpServers`
- Scope: Any file. Entries from every file merge into one denylist, and allowManagedMcpServersOnly doesn’t change that. Deploy it in managed settings to enforce it.
- Type: array of objects, each with exactly one key: serverName, a string, so a claude.ai connector’s display name such as "claude.ai Slack" works; serverCommand, an array of the command and its arguments matched exactly; or serverUrl, a URL pattern with * wildcards
- Default: unset, so no server is blocked; an empty array also blocks nothing

```
{
  "deniedMcpServers": [
    { "serverName": "filesystem" }
  ]
}

```
### Block specific MCP servers. Claude Code refuses to load a matching server wherever it’s defined, including plugin servers, servers passed with --mcp-config, servers from managed-mcp.json, servers from [managedMcpServers](#managedmcpservers), and the claude.ai connectors [it fetches itself](/docs/en/mcp#how-connectors-reach-claude-code). In-process type: "sdk" servers are exempt; the app that started the session registers them.

****````
****``````````
****

settings.json
The denylist takes precedence over [allowedMcpServers](#allowedmcpservers), so a server on both lists is blocked. See [Policy-based control with allowlists and denylists](/docs/en/managed-mcp#policy-based-control-with-allowlists-and-denylists).
[​](#disableclaudeaiconnectors)disableClaudeAiConnectors`
- Scope: Any file
  - true: Claude Code neither fetches nor connects those connectors
  - false: the same as unset; Claude Code fetches your connectors unless another settings file or ENABLE_CLAUDEAI_MCP_SERVERS turns them off
- Default: false, so Claude Code fetches your connectors
- Per-session overrides: ENABLE_CLAUDEAI_MCP_SERVERS set to false turns connectors off for one session; whichever of the two turns them off, the other can’t turn them back on

```
{
  "disableClaudeAiConnectors": true
}

```
### Turn off the [claude.ai MCP connectors](/docs/en/mcp#use-mcp-servers-from-claude-ai) [Claude Code fetches itself](/docs/en/mcp#how-connectors-reach-claude-code), so it neither fetches nor connects them. A true in any settings file applies: a checked-in project .claude/settings.json can opt a repository out of those connectors, but a project-level false can’t override a user- or managed-level true.

****``
****``
````

****``
****````

settings.json
Servers you pass explicitly with --mcp-config are unaffected. To block individual connectors instead of all of them, use [deniedMcpServers](#deniedmcpservers). See [Disable claude.ai connectors](/docs/en/mcp#disable-claude-ai-connectors).
[​](#disabledmcpjsonservers)disabledMcpjsonServers`
- Scope: Any file
- Type: array of strings, the server names as they appear in .mcp.json
- Default: unset

```
{
  "disabledMcpjsonServers": ["filesystem"]
}

```
### Reject specific servers defined in a project’s .mcp.json file so Claude Code never connects them or asks you to approve them. A rejection in any settings file applies, including a project .claude/settings.json checked into the repository.

****``
****``
****

settings.json
Claude Code writes this key to .claude/settings.local.json when you reject a server in the approval dialog. claude mcp get <name> shows a rejected server as ✘ Rejected (see disabledMcpjsonServers in settings). Rejection takes precedence over [enabledMcpjsonServers](#enabledmcpjsonservers) and [enableAllProjectMcpServers](#enableallprojectmcpservers).
[​](#enableallprojectmcpservers)enableAllProjectMcpServers`
- Scope: Any file. In a folder whose trust dialog you haven’t accepted, Claude Code honors it from user settings, managed settings, and --settings and ignores it in the shared project file, both in the session and for claude mcp list and claude mcp get; Project server approvals and workspace trust says when an untracked .claude/settings.local.json counts too.
  - true: Claude Code approves every MCP server defined in project .mcp.json files without a prompt
  - false: Claude Code asks you to approve each server. In a trusted folder, a false in a higher-precedence file overrides a true in a lower one; in a folder you haven’t trusted, a true in any honored file is enough
- Default: unset, so Claude Code asks you to approve each server

```
{
  "enableAllProjectMcpServers": true
}

```
### Approve every MCP server defined in project .mcp.json files without a prompt. Claude Code writes this key to .claude/settings.local.json when you choose to approve all servers in the approval dialog.

****``````````
****````
````````

****

settings.json
A [disabledMcpjsonServers](#disabledmcpjsonservers) entry still rejects a server.
[​](#enabledmcpjsonservers)enabledMcpjsonServers`
- Scope: Any file. In a folder whose trust dialog you haven’t accepted, Claude Code honors it from user settings, managed settings, and --settings and ignores it in the shared project file, both in the session and for claude mcp list and claude mcp get; Project server approvals and workspace trust says when an untracked .claude/settings.local.json counts too.
- Type: array of strings, the server names as they appear in .mcp.json
- Default: unset

```
{
  "enabledMcpjsonServers": ["memory", "github"]
}

```
### Approve specific servers defined in project .mcp.json files so Claude Code connects them without asking. Claude Code writes this key to .claude/settings.local.json when you approve a server in the approval dialog.

****``````````
****``
****

This example approves the memory and github servers from the project’s .mcp.json:
settings.json
A [disabledMcpjsonServers](#disabledmcpjsonservers) entry still rejects a server.
[​](#managedmcpservers)managedMcpServers`
- Scope: Managed. Claude Code drops the key with a warning in user, project, and local settings, and doesn’t read it in the Claude Desktop app’s Code tab on a third-party deployment or in the app’s Cowork sessions, where Claude Desktop supplies and locks those sessions’ MCP servers itself.
- Type: object keyed by server name. Each entry has the .mcp.json shape for an http or sse server: a required https:// url, and optionally headers, oauth, and the other HTTP and SSE options. Claude Code drops entries that fail validation, and What an entry can contain lists the conditions
- Default: unset, so managed settings provide no servers

```
{
  "managedMcpServers": {
    "search": {
      "type": "http",
      "url": "https://search.example.com/mcp"
    }
  }
}

```
## Provide remote MCP servers to every user from managed settings. Users keep the servers they add themselves and can’t edit or remove the ones you provide. Requires Claude Code v2.1.259 or later.

****``
****``````````````
****

This example provides one HTTP server named search:
managed-settings.json
For precedence, how provided servers combine with managed-mcp.json and the allow and deny lists, and what users see, see [Provide servers through managed settings](/docs/en/managed-mcp#provide-servers-through-managed-settings).
[​](#agents-sessions-and-worktrees)Agents, sessions, and worktrees
### Set the default agent, control teammates and cross-session messaging, and configure worktrees. See [Subagents](/docs/en/sub-agents) and [Worktrees](/docs/en/worktrees).
[​](#agent)agent`
- Scope: Any file
- Type: string, the name of a built-in or custom agent
- Default: unset, so the main thread runs as Claude Code’s default agent
- Per-session overrides: --agent takes precedence over this key for one session

```
{
  "agent": "code-reviewer"
}

```
### Run the main thread as a named [subagent](/docs/en/sub-agents#invoke-subagents-explicitly), so Claude Code applies that subagent’s system prompt, tool restrictions, and model to your session. The same key sets the default agent for sessions you dispatch from claude agents.

****``
****
****
****``

settings.json
A plugin’s own settings.json can also supply this key; see [Ship default settings with your plugin](/docs/en/plugins/components#default-settings).
[​](#crosssessioninbound)crossSessionInbound`
- Scope: Any file. A project or local value applies only when it’s stricter than the value managed settings, the --settings flag, or user settings give.
  - "accept": Claude Code delivers the message to Claude
  - "hold": Claude Code shows a notice for the message without delivering it
  - "refuse": Claude Code drops the message
- Default: unset, so Claude Code decides per message

```
{
  "crossSessionInbound": "hold"
}

```
### Choose what this session does with [messages arriving from your other Claude Code sessions](/docs/en/cross-session-messaging#control-inbound-messages). When no value applies, Claude Code decides per message from the two sessions’ permission-mode classes.

****````
****``
``
``

****

settings.json
Claude Code reads managed settings first, then the --settings flag, then user settings, and applies the first value found. refuse is stricter than hold, and hold is stricter than accept. When none of the trusted sources sets a value, a project or local hold or refuse still applies, replacing the per-message default. In sessions with cross-session messaging, this key appears in /config as **Messages from your other sessions**, which writes it to user settings; the row requires Claude Code v2.1.232 or later, and Claude Code hides it while the --settings flag or managed settings set the key.
Claude Code [warns](/docs/en/errors#crosssessioninbound-must-be-one-of-accept-hold-refuse) when you set a value it doesn’t recognize. While that value is present in a user, project, local, or --settings file, Claude Code holds inbound messages, even when a source that takes precedence sets accept. A refuse that another source sets still applies. Fix or remove the value to clear the hold.
When the unrecognized value is in [managed settings](/docs/en/managed-settings), Claude Code instead treats it as refuse until an administrator fixes it. Before v2.1.248, Claude Code ignored an unrecognized value without warning.
[​](#disableagentview)disableAgentView`
- Scope: Any file
  - true: Claude Code turns off claude agents, --bg, /background, and the on-demand supervisor
  - false: agent view is available
- Default: unset, so agent view is available
- Per-session overrides: CLAUDE_CODE_DISABLE_AGENT_VIEW turns agent view off for one session; whichever of the two turns it off, the other can’t turn it back on

```
{
  "disableAgentView": true
}

```
### Turn off [background agents and agent view](/docs/en/agent-view): claude agents, --bg, /background, and the on-demand supervisor. Set it in [managed settings](/docs/en/managed-settings) to enforce it for an organization.

****``
****````````
``

****
****``

settings.json
[​](#isolatepeermachines)isolatePeerMachines`
- Scope: Any file. A true from any scope applies, so a checked-in project file can turn the requirement on but not off.
  - true: Claude Code asks for your approval before Claude’s SendMessage reaches one of your sessions beyond this machine
  - false: cross-machine messages don’t prompt
- Default: unset, so cross-machine messages don’t prompt

```
{
  "isolatePeerMachines": true
}

```
### Require your explicit approval before Claude’s SendMessage reaches one of your sessions beyond this machine; see [Require approval for cross-machine messages](/docs/en/cross-session-messaging#require-approval-for-cross-machine-messages). The approval prompt appears even in [bypassPermissions mode](/docs/en/permission-modes#skip-all-checks-with-bypasspermissions-mode).

****````
****````
``

****

settings.json
The cross-machine SendMessage approval requires Claude Code v2.1.224 or later.
[​](#processwrapper)processWrapper`
- Scope: User or managed
- Type: string, the launcher command as an argv prefix, such as an absolute path with optional arguments
- Default: unset, so background processes start unwrapped
- Per-session overrides: CLAUDE_CODE_PROCESS_WRAPPER takes precedence over this key for one session

```
{
  "processWrapper": "/opt/corp/launcher --profile claude"
}

```
### On macOS and Linux, place a corporate launcher command in front of the [background processes Claude Code starts](/docs/en/corporate-launcher#what-the-launcher-covers). Claude Code runs the launcher with its own command line appended, so the launcher must exec into Claude Code; see [Run Claude Code behind a corporate launcher](/docs/en/corporate-launcher) for the launcher contract. Requires Claude Code v2.1.210 or later.

****``
****
****
****``

settings.json
Claude Code ignores the launcher on Windows and starts every process unwrapped. Requires Claude Code v2.1.210 or later.
[​](#teammatemode)teammateMode`
- Scope: Any file. Claude Code also reads a value left in ~/.claude.json by older versions.
  - "in-process": teammates run inside your main terminal pane
  - "auto": split panes when you’re running inside tmux, or inside iTerm2 with it2 on your PATH or tmux installed; in-process otherwise
  - "tmux": split panes using tmux or iTerm2, detected from your terminal
  - "iterm2": iTerm2 native split panes through the it2 CLI
- Default: "in-process"
- Per-session overrides: --teammate-mode takes precedence over this key for one session

```
{
  "teammateMode": "auto"
}

```
### Choose where Claude Code shows [agent team](/docs/en/agent-teams) teammates: inside your main terminal pane, or in split panes when your terminal supports them. See [Choose a display mode](/docs/en/agent-teams#choose-a-display-mode).

****````
****``
``````
``
````

****``
****``

settings.json

[​](#worktree)worktree`
- Scope: Any file
- Type: object with baseRef, symlinkDirectories, sparsePaths, and bgIsolation
- Default: unset

```
{
  "worktree": {
    "baseRef": "head",
    "symlinkDirectories": ["node_modules"]
  }
}

```
### Configure how Claude Code creates and manages [git worktrees](/docs/en/worktrees) for --worktree, the EnterWorktree tool, and isolated subagents and background sessions.

****``
****````````
****

This example branches new worktrees from your current HEAD and symlinks node_modules into each one:
settings.json
To copy gitignored files like .env into new worktrees, add a [.worktreeinclude file](/docs/en/worktrees#copy-gitignored-files-into-worktrees) to your project root instead of a setting.
[​](#worktree-baseref)worktree.baseRef`
- Scope: Any file
  - "fresh": new worktrees branch from origin/<default-branch>
  - "head": new worktrees branch from your current local HEAD, including unpushed commits
- Default: "fresh"

```
{
  "worktree": {
    "baseRef": "head"
  }
}

```
### Choose which ref new worktrees branch from. "fresh" branches from origin/<default-branch> for a clean tree matching the remote; "head" branches from your current local HEAD, so unpushed commits and feature-branch state are present in the worktree.

****``
****````
````

****``

settings.json
Inside a linked worktree, "head" resolves to that worktree’s HEAD, not the main checkout’s.
[​](#worktree-symlinkdirectories)worktree.symlinkDirectories`
- Scope: Any file
- Type: array of strings, directory paths relative to the repository root
- Default: unset, so Claude Code symlinks no directories

```
{
  "worktree": {
    "symlinkDirectories": ["node_modules", ".cache"]
  }
}

```
### Symlink directories from the main repository into each worktree so you don’t duplicate large directories on disk.

****``
****
****

This example symlinks node_modules and .cache from the main repository into every new worktree:
settings.json
[​](#worktree-sparsepaths)worktree.sparsePaths`
- Scope: Any file
- Type: array of strings, directory paths relative to the repository root
- Default: unset, so each worktree checks out the whole tree

```
{
  "worktree": {
    "sparsePaths": [".claude", "packages/my-app", "shared/utils"]
  }
}

```
### Check out only the listed directories in each worktree through git sparse-checkout. Claude Code writes only those directories plus root-level files to disk, which is faster in large monorepos; see [Check out only the directories you need](/docs/en/large-codebases#check-out-only-the-directories-you-need).

****``
****
****

Include .claude in the list so that each worktree also has the repository’s .claude/settings.json and .claude/rules/. This example checks out only .claude, packages/my-app, and shared/utils, plus root-level files, in each worktree:
settings.json
While a sparse worktree exists, git enables extensions.worktreeConfig in the repository’s shared .git/config.
[​](#worktree-bgisolation)worktree.bgIsolation`
- Scope: Any file
  - "worktree": Claude Code blocks Edit and Write in the main checkout until the session calls EnterWorktree
  - "none": background jobs edit the working copy directly
- Default: "worktree"

```
{
  "worktree": {
    "bgIsolation": "none"
  }
}

```
### Choose how [background sessions](/docs/en/agent-view#how-file-edits-are-isolated) isolate their file edits. If you moved a session to the background with ← or /background, that session edits files in place whatever this key says. With "worktree", Claude Code blocks Edit and Write in the main checkout until the session calls EnterWorktree; with "none", background jobs edit the working copy directly. Set "none" for a repository where git worktrees are impractical.

****``
****````````
``

****``

settings.json
Outside a git repository, a [WorktreeCreate hook](/docs/en/worktrees#non-git-version-control) that fails releases the block so the session can edit the working directory in place.
[​](#worktree-location)worktree.location`
- Scope: User, in ~/.claude/settings.json on the remote machine
- Type: string, an absolute path or one that starts with ~/
- Default: unset, so worktrees go inside the project

```
{
  "worktree": {
    "location": "~/worktrees"
  }
}

```
## Choose the folder on a remote machine where [Desktop SSH sessions](/docs/en/desktop#choose-where-ssh-session-worktrees-go) create their worktrees, instead of <project-root>/.claude/worktrees/. Only the desktop app reads this key: --worktree, the EnterWorktree tool, isolated subagents, and background sessions ignore it. Requires Claude Desktop v1.44121.0 or later.

****````
****``
****

This example sets the folder to ~/worktrees:
settings.json
A **Worktree folder** set on the SSH connection in Desktop takes precedence. If your organization restricts which folders sessions may use, Desktop keeps worktrees inside the project.
[​](#remote-desktop-and-notifications)Remote, desktop, and notifications
### Configure Remote Control, cloud environments, the desktop app, and the notifications Claude Code sends when it needs you. See [Remote Control](/docs/en/remote-control).
[​](#agentpushnotifenabled)agentPushNotifEnabled`
- Scope: Any file. Claude Code also reads a value left in ~/.claude.json by older versions.
  - true: Claude can send a push notification to your phone when it decides one is worth sending
  - false: Claude doesn’t send those notifications
- Default: false

```
{
  "agentPushNotifEnabled": true
}

```
### Allow Claude to send a push notification to your phone when it decides one is worth sending, for example when a long task finishes. In a local session, Claude can send one while [Remote Control](/docs/en/remote-control) is connected. Appears in /config as **Push when Claude decides**. When you change it there, Claude Code also saves the value to your account.

****````
****``
``

****``

settings.json
If you run sessions under a [claude remote-control](/docs/en/remote-control#start-a-remote-control-session) server, they follow the value saved to your account rather than this key. To change that value, run /config in a Claude Code session in your terminal and turn **Push when Claude decides** on or off. If the toggle already shows the value you want, change it and change it back so that Claude Code saves that value to your account.
See [Mobile push notifications](/docs/en/remote-control#mobile-push-notifications).
[​](#awaysummaryenabled)awaySummaryEnabled`
- Scope: Any file
  - true: you see a one-line session recap when you return after a few minutes away
  - false: Claude Code shows no recap
- Default: unset, so the recap is on
- Per-session overrides: CLAUDE_CODE_ENABLE_AWAY_SUMMARY takes precedence over this key for one session, in either direction

```
{
  "awaySummaryEnabled": false
}

```
### Show a one-line session recap when you return to the terminal after a few minutes away. Set it to false, or turn off **Session recap** in /config, to stop the recap.

****``
****``
``

****
****``

settings.json
Claude Code never shows the recap in non-interactive mode.
[​](#disableartifact)disableArtifact`
- Scope: Any file
  - true: Claude Code turns the Artifact tool off for every session the file applies to, and no other file turns it back on
  - false: ignored; to leave the tool on, remove the key
- Default: unset, so the tool follows your account’s availability
- Per-session overrides: CLAUDE_CODE_DISABLE_ARTIFACT set to 1 turns the tool off for one session

```
{
  "disableArtifact": true
}

```
### Deprecated, and replaced by [enableArtifact](#enableartifact). Claude Code still honors disableArtifact: true as equivalent to enableArtifact: false, and ignores disableArtifact: false.
Use [enableArtifact](#enableartifact) instead to turn off the [Artifact](/docs/en/artifacts) tool, which publishes session output as a private web page on claude.ai. When you turn the **Artifacts** row off in /config, Claude Code writes enableArtifact to your user settings and clears this key.

****``
****``
``

****
****````

settings.json
[Disable artifacts](/docs/en/artifacts#disable-artifacts) lists every way to turn the tool off.
[​](#disabledeeplinkregistration)disableDeepLinkRegistration`
- Scope: Any file
- Type: the string "disable"
- Default: unset, so Claude Code registers the handler

```
{
  "disableDeepLinkRegistration": "disable"
}

```
### Stop Claude Code from registering the claude-cli:// protocol handler with the operating system. [Deep links](/docs/en/deep-links) let external tools open a Claude Code session with a pre-filled prompt. Set this in environments where protocol handler registration is restricted or managed separately.

****``
****``
****

settings.json
[​](#disabledesktoplocalsessions)disableDesktopLocalSessions`
- Environment selector: the entry for the user’s computer is grayed out and unselectable, with the tooltip Disabled by your organization. On Windows the WSL entry is grayed out the same way, though whether WSL sessions run on a managed device at all is governed separately.
- New sessions: default to the first SSH connection if one is configured
- Sessions on the device: the app refuses to start or resume a session on the device, including an SSH connection back to the same machine
- SSH sessions to other hosts and cloud sessions: unaffected
- Scope: Managed. By default, the desktop app reads the key from one managed source.
  - true: the desktop app offers no on-device Code sessions; existing local sessions stay listed but can’t continue
  - false: local sessions stay available
- Default: unset, so local sessions are available

```
{
  "disableDesktopLocalSessions": true
}

```
### Turn off Code sessions that run on the device in the [desktop app](/docs/en/desktop#local-sessions-on-managed-devices), for deployments where developers should work on remote machines over SSH. With the key set to true, users see this in the Code tab:

********
****
****
****

The desktop app reads this key; the terminal CLI ignores it. Requires Claude Desktop v1.37937.0 or later.

****``
****````
``

****

managed-settings.json
The desktop app ignores any other value, and a value that isn’t a Boolean, such as the string "true" or 1, also logs a warning. Pair it with [sshConfigs](#sshconfigs) so users land on a working connection, and with [sshHostAllowlist](#sshhostallowlist) to limit which hosts they can reach. See [Local sessions on managed devices](/docs/en/desktop#local-sessions-on-managed-devices).
Claude Desktop supplies Code sessions with policy derived from your desktop configuration, for example the egress allowlist, filesystem sandbox, and MCP restrictions in third-party deployments. Claude Code ignores those parent settings whenever an [admin source](/docs/en/managed-settings#how-claude-code-combines-managed-sources) is present: server-managed settings, an MDM or OS-level policy, or a managed settings file. Deploying this key through one of those on a device that had none before, as in third-party deployments, therefore stops the desktop-derived policies from applying. [Let an embedding host add policy](/docs/en/managed-settings#let-an-embedding-host-add-policy) covers when parent settings can still merge; this holds for any key you deploy that way, not only this one.
[​](#disableremotecontrol)disableRemoteControl`
- Scope: Any file
  - true: Claude Code refuses claude remote-control, the --remote-control flag, auto-start, and the in-session toggle
  - false: Remote Control stays available
- Default: false

```
{
  "disableRemoteControl": true
}

```
### Turn off [Remote Control](/docs/en/remote-control): Claude Code then refuses claude remote-control, the --remote-control flag, auto-start, and the in-session toggle, and reports that your organization’s policy disabled it. Place it in [managed settings](/docs/en/managed-settings) for per-device MDM enforcement.

****``
****``````
``

****``

settings.json
[​](#enableartifact)enableArtifact`
- Scope: Any file. Every file can turn the tool off, and none can turn it back on.
  - false: Claude Code turns the Artifact tool off for every session the file applies to
  - true: the same as leaving the key unset, because it never overrides a false from another file, from CLAUDE_CODE_DISABLE_ARTIFACT, or from your organization’s admin setting
- Default: unset, so the tool follows your account’s availability

```
{
  "enableArtifact": false
}

```
### Turn off the [Artifact](/docs/en/artifacts) tool, which publishes session output as a private web page on claude.ai. When you turn the **Artifacts** row off in /config, Claude Code writes this key to your user settings, so you don’t usually edit it by hand.

****``
****``
``````

****

settings.json
While a source other than your own user settings keeps the tool turned off, Claude Code hides the **Artifacts** row in /config, because turning it on there wouldn’t change anything. [Disable artifacts](/docs/en/artifacts#disable-artifacts) lists every way to turn the tool off.
[​](#inputneedednotifenabled)inputNeededNotifEnabled`
- Scope: Any file. Claude Code also reads a value left in ~/.claude.json by older versions.
- Type: Boolean
- Default: false

```
{
  "inputNeededNotifEnabled": true
}

```
### Get a push notification on your phone when a permission prompt or question is waiting for your input. In a local session, Claude Code sends these only while [Remote Control](/docs/en/remote-control) is connected. Appears in /config as **Push when actions required**.

****````
****
****``

settings.json
See [Mobile push notifications](/docs/en/remote-control#mobile-push-notifications).
[​](#preferrednotifchannel)preferredNotifChannel`
- Scope: Any file. Claude Code also reads a value left in ~/.claude.json by older versions.
  - "auto": Claude Code sends a desktop notification when it detects iTerm2, Ghostty, or Kitty, rings the bell in Terminal.app only when its audible bell is off, and does nothing elsewhere
  - "terminal_bell": Claude Code rings the bell character in any terminal
  - "iterm2": Claude Code sends an iTerm2 desktop notification
  - "iterm2_with_bell": Claude Code sends an iTerm2 desktop notification and rings the bell
  - "kitty": Claude Code sends a Kitty desktop notification
  - "ghostty": Claude Code sends a Ghostty desktop notification
  - "notifications_disabled": Claude Code sends no notification
- Default: "auto"

```
{
  "preferredNotifChannel": "terminal_bell"
}

```
### Choose how Claude Code notifies you when a task completes or a permission prompt is waiting. A [mod’s notifications](/docs/en/plugins/mods/api#show-something-without-starting-a-turn) use the same setting. Appears in /config as **Local notifications**.

****````
****``
``
``
``
``
``
``

****``

settings.json
With "auto", Claude Code sends a desktop notification when it detects iTerm2, Ghostty, or Kitty. In Terminal.app it rings the bell character only when you have turned Terminal’s audible bell off, and in other terminals it does nothing. Set "terminal_bell" to ring the bell character in any terminal. See [Get a terminal bell or notification](/docs/en/terminal-config#get-a-terminal-bell-or-notification).
[​](#remote-defaultenvironmentid)remote.defaultEnvironmentId`
- Scope: Any file. For a self-hosted environment ID, user or managed settings, or the --settings flag only.
- Type: string, an environment ID such as env_... or ccpool_...
- Default: unset, so Claude Code uses the Anthropic-hosted environment when your list has one, and otherwise the first environment in your list that isn’t a Remote Control bridge environment, or the first environment when every one is a bridge environment
- Per-session overrides: --environment takes precedence over this key for the one cloud session it creates

```
{
  "remote": {
    "defaultEnvironmentId": "env_0123abcd"
  }
}

```
### Pick the default [cloud environment](/docs/en/cloud-environments) for cloud sessions you create from the CLI, such as with claude --cloud. Claude Code writes this key to your user settings when you pick an environment with [/remote-env](/docs/en/cloud-environments#select-an-environment-from-the-cli).

****````
****````
****
****``

settings.json
An Anthropic-hosted environment ID, which starts with env_, follows the standard settings precedence, so a value in a repository’s project settings overrides your user-level pick. A [self-hosted environment](/docs/en/self-hosted-environments) ID, which starts with ccpool_, is honored only from user settings, managed settings, and the --settings flag; Claude Code ignores one in a repository’s project or local settings, and /remote-env shows which value it ignored, so a checked-in file can’t steer sessions onto a self-hosted environment you didn’t choose.
[​](#remotecontrolatstartup)remoteControlAtStartup`
- Scope: Any file. Claude Code also reads a value left in ~/.claude.json by older versions.
  - true: Claude Code connects Remote Control automatically when each interactive session starts
  - false: Claude Code waits for /remote-control
- Default: unset, so the auto-connect default applies
- Per-session overrides: --remote-control turns Remote Control on for one session even when this key is false, and no flag turns it off for one session

```
{
  "remoteControlAtStartup": true
}

```
### Connect [Remote Control](/docs/en/remote-control) automatically when each interactive session starts, instead of waiting for /remote-control. Set it to true to turn auto-connect on, false to turn it off. Appears in /config as **Enable Remote Control for all sessions**.

****````
****``
````

****
****````

settings.json
Claude Code ignores a true from project or local settings, so a repository can turn auto-connect off for its checkout but can’t turn it on. For the full per-scope behavior, see [Enable Remote Control for all sessions](/docs/en/remote-control#enable-remote-control-for-all-sessions) and the [security keys where the stricter value applies](/docs/en/settings#security-keys-where-the-stricter-value-applies).
[​](#sshconfigs)sshConfigs`
- Scope: User or managed. The desktop app reads this key. By default, it reads managed connections from one managed source.
- Type: array of objects, each with required id, name, and sshHost and optional sshPort and sshIdentityFile
- Default: unset

```
{
  "sshConfigs": [
    {
      "id": "dev-vm",
      "name": "Dev VM",
      "sshHost": "user@dev.example.com"
    }
  ]
}

```
### Add SSH connections to the [Desktop](/docs/en/desktop#pre-configure-ssh-connections-for-your-team) environment selector. Administrators use sshConfigs to distribute shared connections to a team. Users can select a managed connection and ****[set their own Worktree folder](/docs/en/desktop#set-the-worktree-folder-on-an-existing-connection) for it. They can’t edit its other fields or delete it in the app.

****``
****``````````
****

This example adds one connection named Dev VM that connects to user@dev.example.com:
settings.json
[​](#sshhostallowlist)sshHostAllowlist`
- Scope: Managed. By default, Desktop reads the key from one managed source.
- Type: array of hostname patterns
- Default: unset, so any host is allowed

```
{
  "sshHostAllowlist": ["*.devboxes.example.com", "bastion.example.com"]
}

```
### Limit the hosts a [Desktop SSH session](/docs/en/desktop#restrict-which-ssh-hosts-users-can-connect-to) can connect to. Only the Desktop app reads this key; the CLI doesn’t. Patterns are case-insensitive: * matches any host, *.example.com matches example.com and every subdomain, and anything else is an exact match against the hostname after ~/.ssh/config resolution. An empty array turns SSH sessions off.
With Claude Desktop v3.1623.0 or later, a session’s [jump hosts](/docs/en/desktop#allow-jump-hosts) have to match a pattern too.

****``
****
****

This example allows devboxes.example.com and its subdomains, plus the exact host bastion.example.com:
managed-settings.json
A value that Desktop can’t read as a list of hosts, such as true or an object, counts as an empty array until you correct it, except null, which counts as unset. Requires Claude Desktop v2.26454.0 or later.
If you set [managedSourcesBehavior](#managedsourcesbehavior) to "merge" in your highest-ranked source, Desktop combines the lists from every [admin source](/docs/en/managed-settings#how-claude-code-combines-managed-sources) and allows a host that matches any of them. If you set an empty array in one source, SSH sessions stay on for the hosts another source lists.
[​](#sshhostcommands)sshHostCommands`
- Scope: User or managed. Only the desktop app reads this key. It reads managed entries from one managed settings file or MDM policy on the computer, and ignores the key in server-managed settings.
- Type: array of objects, each with required id, name, and command and optional sshIdentityFile and startDirectory. Desktop doesn’t read command as shell syntax, so pipes and variables don’t work: write it as a program and its arguments.
- Default: unset

```
{
  "sshHostCommands": [
    {
      "id": "devbox",
      "name": "Dev box",
      "command": "acme-dev create"
    }
  ]
}

```
## Add SSH connections whose host comes from a command to the [Desktop](/docs/en/desktop#create-an-ssh-connection-from-a-command) environment selector. When you create a connection or create another machine for it, Desktop runs the entry’s command on your computer and connects to the host that the command prints.
Requires Claude Desktop v3.6556.0 or later on macOS or Linux, or v4.16336.0 or later on Windows, signed in with a Claude account. On Windows, Desktop also has to [connect through the OpenSSH client](/docs/en/desktop#use-your-ssh-configuration).

****``
****````````````
****

This example adds one connection named Dev box, where acme-dev create stands for your own tool:
settings.json
On Windows, a bare name such as acme-dev doesn’t work, so [start the command with the program’s full path](/docs/en/desktop#write-the-command-on-windows).
Before Claude Code v2.1.307, the Edit tool refused a change that added this key to a valid settings file, with the error Unrecognized field: sshHostCommands. On those versions, add the key in a text editor instead; Claude Code loads a file that holds the key. In Desktop, the version that counts is the [Code tab’s Claude Code version](/docs/en/desktop#claude-code-version-in-the-code-tab), not your terminal’s.

[​](#authentication-and-providers)Authentication and providers
### Supply credentials through helper scripts and, for organizations, force a login method or organization. See [Authentication](/docs/en/authentication).
[​](#allowedproviders)allowedProviders`
- Scope: Managed. A list that the machine’s own admin sources set, MDM policies and managed settings files, keeps applying when server-managed settings also deliver one: a session may then use only the providers on both lists, so a server-managed list can narrow what the machine allows but never widen it. Which machine source’s allowedProviders counts follows how Claude Code combines managed sources. A list delivered through server-managed settings alone reaches only the sessions that fetch server-managed settings.
  - "anthropic": the Anthropic API on Anthropic’s own host, through a claude.ai or Console sign-in or an API key. Pair it with forceLoginMethod or forceLoginOrgUUID to also restrict the sign-in
  - "bedrock": Amazon Bedrock
  - "vertex": Google Cloud’s Agent Platform, formerly Vertex AI
  - "foundry": Microsoft Foundry
  - "anthropicAws": Claude Platform on AWS
  - "mantle": the Amazon Bedrock Mantle endpoint. A session that runs Mantle alongside the Invoke API uses both providers, so list "bedrock" and "mantle" together for it
  - "customEndpoint": the Anthropic API or a cloud provider’s API sent to another host, such as an LLM gateway named by ANTHROPIC_BASE_URL or by a provider’s endpoint variable such as ANTHROPIC_BEDROCK_BASE_URL. Claude Code admits it only for the exact value a managed env block pins
  - "gateway": a Cloud gateway sign-in
- Default: unset, so any provider can be used

```
{
  "allowedProviders": ["anthropic", "bedrock"]
}

```
#### List the services a machine may reach Claude through, such as the Anthropic API, Amazon Bedrock, or an LLM gateway. A session on a provider that isn’t listed is refused at startup, at login, and when it next contacts the API, so switching to an unlisted provider mid-session is refused too. The [refusal message](/docs/en/errors#managed-settings-dont-allow-this-api-provider) names what selected the provider and the steps to continue. Requires Claude Code v2.1.285 or later.

****````
****``````
``
``
``
``
``````
````````
``

****

managed-settings.json
Each cloud provider’s entry means that provider’s own service, including its regional, FIPS, and private endpoints.
An entry Claude Code doesn’t recognize as a provider name is dropped and reported, and the rest of the list stays enforced. With an empty list, or one whose every entry is unrecognized, Claude Code refuses every provider and doesn’t start on the machine.
[​](#endpoints-that-need-a-pin-in-managed-env)Endpoints that need a pin in managed env`
- "customEndpoint" sessions: the variable that names the host, such as ANTHROPIC_BASE_URL
- Amazon Bedrock: the AWS SDK’s AWS_ENDPOINT_URL, AWS_ENDPOINT_URL_BEDROCK, and AWS_ENDPOINT_URL_BEDROCK_RUNTIME variables when they point outside Bedrock’s own service. The session stays under "bedrock" rather than "customEndpoint"
- A gateway sign-in’s URL: the session stays under "gateway", and forceLoginGatewayUrl also counts as the pin
- An administrator source on the machine sets a list: only the env blocks of the machine’s own administrator sources count
- Only server-managed settings set a list: an env value in those server-managed settings counts too
### A pin is an endpoint variable’s value set in a managed [env](#env) block. When a session sends a provider’s traffic somewhere other than that provider’s own service, Claude Code admits it only if the session’s value is the same as the pin. These endpoints need one:

``
****``````````
****````

Which env blocks count as pins depends on where the list is set:

****``
****``

The list doesn’t judge a cloud provider’s credential and tenancy variables or the network path, such as HTTPS_PROXY and certificate settings. Set those for the fleet in the managed env block.
[​](#apikeyhelper)apiKeyHelper`
- Scope: Any file
- Type: string, a shell command line
- Default: unset, so Claude Code doesn’t run a helper

```
{
  "apiKeyHelper": "/bin/generate_temp_api_key.sh"
}

```
- After the cache lifetime, five minutes by default or the interval you set with CLAUDE_CODE_API_KEY_HELPER_TTL_MS.
- When a request to the Anthropic API, directly or through an LLM gateway, fails with 401 or 403.
- When a request through an LLM gateway fails with 401, but not 403, and you set CLAUDE_CODE_SKIP_VERTEX_AUTH for Google Cloud’s Agent Platform, CLAUDE_CODE_SKIP_ANTHROPIC_AWS_AUTH for Claude Platform on AWS, or CLAUDE_CODE_SKIP_MANTLE_AUTH for Amazon Bedrock Mantle. Requires Claude Code v2.1.318 or later.
- Before sending a request to the Anthropic API, directly or through an LLM gateway, when the cached output is a JWT that expired after the helper produced it. Requires Claude Code v2.1.246 or later.
### Run your own command to produce the credential Claude Code sends with model requests. Claude Code runs the command through the system shell, /bin/sh on macOS and Linux and cmd on Windows, and sends its output as both the X-Api-Key and Authorization: Bearer headers. Use it for dynamic or rotating credentials, such as short-lived tokens fetched from a vault.

****``
****
****

settings.json
Claude Code caches the value and reruns the command in these cases:

``
````
``````````

The last three cases apply only when the helper’s output is the credential Claude Code sends and ANTHROPIC_AUTH_TOKEN isn’t set.
In interactive sessions, when the command comes from project or local settings, Claude Code doesn’t run it until you accept the workspace trust prompt. See [Credential management](/docs/en/authentication#credential-management).
[​](#awsauthrefresh)awsAuthRefresh`
- Scope: Any file
- Type: string, a shell command line
- Default: unset, so Claude Code doesn’t refresh AWS credentials for you

```
{
  "awsAuthRefresh": "aws sso login --profile myprofile"
}

```
### Run your own command, such as aws sso login, to refresh the credentials in your .aws directory when the ones Claude Code has for [Amazon Bedrock](/docs/en/amazon-bedrock) stop working. Claude Code checks the current credentials against STS first and runs the command only when that check fails, then reads the refreshed .aws directory.
When the check fails at the same time in several Claude Code processes that use the same command and credentials, such as separate terminals or IDE windows, one process runs the command and the rest wait for that run instead of starting their own. A process that has waited 60 seconds with a request pending runs the command itself. To turn this off, set [CLAUDE_CODE_DISABLE_AUTH_REFRESH_LOCK](/docs/en/env-vars) to 1.

****``
****
****

settings.json
Use this key when your refresh flow writes to .aws; use [awsCredentialExport](#awscredentialexport) when it prints credentials instead. See [advanced credential configuration](/docs/en/amazon-bedrock#advanced-credential-configuration).
[​](#awscredentialexport)awsCredentialExport`
- Scope: Any file
- Type: string, a shell command line
- Default: unset, so Claude Code uses the ambient AWS credential chain

```
{
  "awsCredentialExport": "/bin/generate_aws_grant.sh"
}

```
### Run your own command that prints AWS credentials as JSON, so Claude Code can call [Amazon Bedrock](/docs/en/amazon-bedrock) with credentials that don’t live in your .aws directory. Claude Code accepts the aws sts output shape and the flat aws configure export-credentials shape, and scopes the credentials to its own Bedrock client, so the shell commands Claude runs still see your ambient credentials.

****``
****
****

settings.json
Unlike [awsAuthRefresh](#awsauthrefresh), Claude Code always runs this command when it’s set, without checking the ambient credentials first. See [advanced credential configuration](/docs/en/amazon-bedrock#advanced-credential-configuration).
[​](#forceloginmethod)forceLoginMethod`
- Scope: Any file. Claude Code honors "gateway" from the same sources as forceLoginGatewayUrl and treats it as unset everywhere else.
  - "claudeai": only claude.ai accounts can log in
  - "console": only Claude Console accounts can log in
  - "gateway": Claude Code sends people to a cloud gateway instead of a first-party login
- Default: unset, so people pick a login method

```
{
  "forceLoginMethod": "claudeai"
}

```
### Restrict which kind of account people can log in with. Set "claudeai" to allow only claude.ai accounts, "console" to allow only Claude Console accounts, or "gateway" to send people to a [cloud gateway](/docs/en/claude-apps-gateway) instead of a first-party login. Administrators set it in managed settings and pair it with [forceLoginOrgUUID](#forceloginorguuid) to keep developers’ claude.ai logins inside one organization.
If you set it to "claudeai" in any settings file, Claude Code also stops offering the [keyless Console sign-in](/docs/en/authentication#sign-in-without-an-api-key) in the sessions that file applies to. With "console" alone, people can still reach the keyless sign-in after a failed login. To stop Claude Code offering it, see [Stop offering the keyless sign-in on managed machines](/docs/en/authentication#stop-offering-the-keyless-sign-in-on-managed-machines), which also lists what else forceLoginOrgUUID changes.

****``````
****``
``
``

****

settings.json
Every first-party login path applies the restriction, including the [VS Code extension](/docs/en/vs-code), the Agent SDK, claude setup-token, and /install-github-app, except the terminal’s interactive login screen, reached by /login or first-run onboarding, which pre-selects the method without enforcing it. Before v2.1.212, only terminal logins applied it. See [Restrict login to your organization](/docs/en/authentication#restrict-login-to-your-organization) for how each login path, environment credentials, and third-party providers are handled.
When a managed source on the machine sets "gateway", Claude Code doesn’t use a leftover login, API key, or apiKeyHelper credential. See [Administrator policy requires a Cloud gateway sign-in](/docs/en/errors#administrator-policy-requires-a-cloud-gateway-sign-in) for the message each one produces. If you select a cloud provider through CLAUDE_CODE_USE_BEDROCK or a similar environment variable, the session doesn’t need the gateway sign-in. Before v2.1.261, Claude Code used a leftover login on these machines.
[​](#forcelogingatewayurl)forceLoginGatewayUrl`
- Scope: User or managed. Read from a managed source on the machine: managed-settings.json, the macOS plist or Windows HKLM registry, or a policy helper. On a machine with none of those, Claude Code v2.1.295 or later also reads it from user settings. Claude Code ignores it in HKCU and server-managed settings.
- Type: string, a full URL including the scheme
- Default: unset, so the Cloud gateway screen shows an error telling people to contact their IT administrator

```
{
  "forceLoginGatewayUrl": "https://claude-gateway.example.com"
}

```
### Set the gateway URL the /login Cloud gateway screen connects to, so people reach your [cloud gateway](/docs/en/claude-apps-gateway) without typing its address. The screen has no URL field: with this key set, it shows your gateway URL and connects when the person presses Enter; without it, it tells them to contact their IT administrator.
In managed settings, either this key or forceLoginMethod: "gateway" makes the machine gateway-only, except for sessions that select a cloud provider with CLAUDE_CODE_USE_*. /login then opens on the Cloud gateway screen with no login-method picker. See [Administrator policy requires a Cloud gateway sign-in](/docs/en/errors#administrator-policy-requires-a-cloud-gateway-sign-in) for what happens to a leftover first-party login or API key. Set both keys so the screen connects instead of showing an error.

****````
****
****

managed-settings.json
If the value isn’t a valid URL, the sign-in screen reports it, and the rest of the managed settings file still applies. See [Set the gateway URL](/docs/en/claude-apps-gateway#set-the-gateway-url).
[​](#forceloginorguuid)forceLoginOrgUUID`
- Scope: Any file. In a settings file that isn’t a managed source, Claude Code doesn’t check which organization a login belongs to, and a single UUID pre-selects the organization during login.
- Type: string, one UUID, or array of strings, several UUIDs
- Default: unset, so any organization can log in

```
{
  "forceLoginOrgUUID": ["xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", "yyyyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy"]
}

```
### From a managed source, require claude.ai account logins to belong to one Anthropic organization, given as a single UUID, or to any of several organizations, given as an array. From any settings file, Claude Code also uses a single UUID to pre-select that organization during a claude.ai or Claude Console login, and pre-selects nothing for an array. If you set the key in any settings file, Claude Code also stops offering the [keyless Console sign-in](/docs/en/authentication#sign-in-without-an-api-key) in the sessions that file applies to and creates an API key instead.

****``
****
****

This example accepts logins from either of two organizations without pre-selecting one:
managed-settings.json
If a managed source sets an empty array, or a value that isn’t a string or an array of strings, users who sign in with an Anthropic account can’t start Claude Code or complete a login. They see a message that names forceLoginOrgUUID and tells them to contact their administrator. A [policyHelper](#policyhelper) that emits a value of the wrong type [fails its run](#helper-failures) instead.
See [Restrict login to your organization](/docs/en/authentication#restrict-login-to-your-organization) for how Claude Code treats Claude Console logins, the other login paths, and environment credentials.
[​](#gatewayinternalnetworks)gatewayInternalNetworks`
- Scope: Managed. Read only from a source on the machine: managed-settings.json, the macOS plist or Windows HKLM registry, or a policy helper. Claude Code ignores it in HKCU and server-managed settings.
- Type: array of strings, at most four IPv4 CIDR blocks, each /8 to /32, not overlapping one another, and none overlapping private space.
- Default: unset, so /login accepts only gateways on private addresses

```
{
  "gatewayInternalNetworks": ["203.0.113.0/24"]
}

```
### Declare the public IPv4 blocks that your organization numbers its internal network from, so /login accepts a [cloud gateway](/docs/en/claude-apps-gateway) there. Requires Claude Code v2.1.268 or later.
Without this key, /login connects to any gateway on a private address and nothing else. With it, /login also accepts a gateway inside a listed block, over a direct connection only. The machine’s own address on that connection must also be inside the same block.

****````
****````
****``

managed-settings.json
Replace the documentation range in the example with your own block. Claude Code refuses the documentation ranges, the ranges that VPN and NAT64 clients use locally, and reserved space that no network is numbered from, such as multicast.
If an entry is invalid, or the value isn’t a list of strings, /login names the problem and refuses every new gateway sign-in on the machine until you fix the value. Existing sign-ins keep working. See [Allow a gateway on public address space you own](/docs/en/claude-apps-gateway#allow-a-gateway-on-public-address-space-you-own) for the full rules and what developers see.
[​](#gcpauthrefresh)gcpAuthRefresh`
- Scope: Any file
- Type: string, a shell command line
- Default: unset, so Claude Code’s credential error tells you to run gcloud auth application-default login yourself

```
{
  "gcpAuthRefresh": "gcloud auth application-default login"
}

```
### Run your own command to refresh Google Cloud Application Default Credentials when Claude Code finds they’ve expired or can’t be loaded, so [Google Cloud’s Agent Platform](/docs/en/google-vertex-ai) requests keep working without you re-authenticating by hand.
When several Claude Code processes that use the same command and credentials, such as separate terminals or IDE windows, find them expired at the same time, one process runs the command and the rest wait for that run instead of starting their own. A process that has waited 60 seconds with a request pending runs the command itself. To turn this off, set [CLAUDE_CODE_DISABLE_AUTH_REFRESH_LOCK](/docs/en/env-vars) to 1.

****``
****
****``

settings.json
See [advanced credential configuration](/docs/en/google-vertex-ai#advanced-credential-configuration).
[​](#otelheadershelper)otelHeadersHelper`
- Scope: Any file
- Type: string, an executable path or a shell command line
- Default: unset, so Claude Code adds no helper-generated headers

```
{
  "otelHeadersHelper": "/bin/generate_otel_headers.sh"
}

```
## Run your own command to generate the headers Claude Code sends with OpenTelemetry exports, for backends whose tokens rotate. Claude Code runs it at startup and periodically after that, and expects a JSON object of string header values on stdout.

****``
****
****

settings.json
Set the refresh interval with [CLAUDE_CODE_OTEL_HEADERS_HELPER_DEBOUNCE_MS](/docs/en/env-vars). See [Dynamic headers](/docs/en/monitoring-usage#dynamic-headers) for the script requirements and what happens when the helper fails.
[​](#updates-and-versioning)Updates and versioning
### Choose an update channel and, for organizations, pin the versions people can run. See [Update Claude Code](/docs/en/setup#update-claude-code).
[​](#autoupdateschannel)autoUpdatesChannel`
- Scope: Any file. Set it in managed settings to enforce one channel across your organization.
  - "latest": updates follow the most recent release
  - "stable": updates follow a version that is typically about one week old and skips releases with major regressions
- Default: unset, so Claude Code follows "latest"

```
{
  "autoUpdatesChannel": "stable"
}

```
### Choose which [release channel](/docs/en/setup#configure-release-channel) background auto-updates and claude update follow. Set "stable" for a version that is typically about one week old and skips releases with major regressions, or "latest" for the most recent release.

****``
****``
``

****``

settings.json
Claude Code writes "stable" to your user settings when you pick it under **Auto-update channel** in /config, and removes the key when you switch back to latest there. claude install stable and claude install latest also save the channel you name. Switching from "latest" to "stable" in /config asks whether to allow a downgrade or stay on your current version; staying sets [minimumVersion](#minimumversion). Homebrew installs ignore this key: the claude-code cask tracks stable and claude-code@latest tracks latest, and claude update defers to brew upgrade. To turn auto-updates off entirely, set [DISABLE_AUTOUPDATER](/docs/en/setup#disable-auto-updates) in env.
[​](#minimumversion)minimumVersion`
- Scope: Any file. Set it in managed settings to pin an organization-wide minimum that user and project settings can’t lower.
- Type: string, a version number such as "2.1.100"; a value that isn’t a valid version is ignored
- Default: unset, so updates can install any version the channel offers

```
{
  "autoUpdatesChannel": "stable",
  "minimumVersion": "2.1.100"
}

```
### Keep background auto-updates and claude update from installing any version below this one, so moving to the "stable" channel doesn’t downgrade you from a newer "latest" build. Claude Code writes this key for you when you choose to stay on your current version while switching channels in /config, and clears it when you switch back to "latest".

****``
****``
****

This example follows the stable channel and refuses to install any version below 2.1.100:
settings.json
This key only constrains updates. To make Claude Code refuse to start below a version, use [requiredMinimumVersion](#requiredminimumversion) instead. See [Pin a minimum version](/docs/en/setup#pin-a-minimum-version).
[​](#requiredmaximumversion)requiredMaximumVersion`
- Scope: Managed. Claude Code gives no warning when it ignores the key elsewhere.
- Type: string, a version number such as "2.1.150"; a value that isn’t a valid version is ignored
- Default: unset, so no ceiling applies

```
{
  "requiredMaximumVersion": "2.1.150"
}

```
### Set the newest Claude Code version your organization allows to start. When the running version is newer, Claude Code exits at startup and tells the user to install an approved version through your organization’s approved method; claude install <version> may also work. Requires Claude Code v2.1.163 or later.

****``
****``
****

managed-settings.json
Background auto-updates and claude update skip versions above the ceiling, so an installation inside the range stays inside it. claude update, claude install, and claude doctor keep working above the ceiling so users can recover. Pair it with [requiredMinimumVersion](#requiredminimumversion) to enforce a range.
[​](#requiredminimumversion)requiredMinimumVersion`
- Scope: Managed. Claude Code gives no warning when it ignores the key elsewhere.
- Type: string, a version number such as "2.1.150"; a value that isn’t a valid version is ignored
- Default: unset, so no floor applies

```
{
  "requiredMinimumVersion": "2.1.150"
}

```
## Set the oldest Claude Code version your organization allows to start. When the running version is older, Claude Code exits at startup and tells the user to update through your organization’s approved method. The check runs at startup only, so a session that’s already running continues. Requires Claude Code v2.1.163 or later.

****``
****``
****

managed-settings.json
claude update, claude install, and claude doctor keep working below the floor so users can recover. Unlike [minimumVersion](#minimumversion), which only prevents downgrades, this key blocks startup. Pair it with [requiredMaximumVersion](#requiredmaximumversion) to enforce a range.
[​](#tools)Tools
### Turn off specific tools in the [Claude Code desktop app](/docs/en/desktop). The terminal CLI ignores these keys. For the tools themselves, see [Tools available to Claude](/docs/en/tools-reference).
[​](#browserexternalpagetools)browserExternalPageTools`
- Scope: Managed
- Type: string, "disabled"; the desktop app also accepts "disable", in either case
- Default: unset, so Claude’s tools work on external pages

```
{
  "browserExternalPageTools": "disabled"
}

```
### Stop Claude from using its tools to read or act on external pages in the desktop app’s [Browser pane](/docs/en/desktop#browse-external-sites). People in your organization can still open external sites themselves, and local dev server previews keep working with Claude’s tools. The desktop app reads this key; the terminal CLI ignores it.

****``
****````
****

managed-settings.json
Any other value leaves Claude’s tools on, and a non-empty string that isn’t one of the two accepted values logs a warning. To block external sites for people and Claude alike, set [disableBrowserExternalNavigation](#disablebrowserexternalnavigation) instead. See [Restrict external browsing for your organization](/docs/en/desktop#restrict-external-browsing-for-your-organization).
[​](#disablebrowserexternalnavigation)disableBrowserExternalNavigation`
- Scope: Managed
  - true: the desktop app turns off external browsing in the Browser pane for people and Claude alike; localhost previews keep working
  - false: external browsing stays on
- Default: unset, so external browsing is on

```
{
  "disableBrowserExternalNavigation": true
}

```
### Turn off external browsing in the desktop app’s [Browser pane](/docs/en/desktop#browse-external-sites) for people and Claude alike. Localhost dev server previews keep working. HTML previews in SSH and WSL sessions still open, but they [don’t run scripts](/docs/en/desktop#turn-off-scripts-in-ssh-and-wsl-previews-for-your-organization). The desktop app reads this key; the terminal CLI ignores it.

****``
****````
``

****

managed-settings.json
The desktop app ignores any other value, and a value that isn’t a Boolean, such as the string "true" or 1, also logs a warning. To leave external browsing on but keep Claude’s tools off external pages, set [browserExternalPageTools](#browserexternalpagetools) instead. See [Restrict external browsing for your organization](/docs/en/desktop#restrict-external-browsing-for-your-organization).
If the computer that runs the desktop app receives no other Claude Code managed settings, also set [parentSettingsBehavior](#parentsettingsbehavior) to "merge" in the managed settings that you create. On Windows, if you create a managed settings file, users also lose WSL sessions until you [allow them](/docs/en/admin-setup#wsl-sessions-in-claude-code-desktop). See [Turn off scripts in SSH and WSL previews for your organization](/docs/en/desktop#turn-off-scripts-in-ssh-and-wsl-previews-for-your-organization) for the reasons.
[​](#disablemobilesimulatortools)disableMobileSimulatorTools`
- Scope: Managed
  - true: the desktop app blocks Claude’s tools for the iOS Simulator pane
  - false: Claude’s simulator tools follow each person’s settings toggle in the desktop app
- Default: unset, so Claude’s simulator tools follow each person’s settings toggle in the desktop app

```
{
  "disableMobileSimulatorTools": true
}

```
## Block Claude’s tools for the desktop app’s [iOS Simulator pane](/docs/en/desktop-ios-simulator#turn-off-simulator-access). People keep manual use of the pane; only Claude’s access is removed, and nobody can turn it back on from inside the app. The desktop app reads this key; the terminal CLI ignores it.

****``
****````
``

****

managed-settings.json
The desktop app ignores any other value, and a value that isn’t a Boolean, such as the string "true" or 1, also logs a warning.

[​](#privacy-and-telemetry)Privacy and telemetry
### Control how long Claude Code keeps session data and what it sends. The switches that turn off usage metrics and error reports are environment variables, not settings keys: set DISABLE_TELEMETRY, DISABLE_ERROR_REPORTING, or CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC in the [env](#env) key or in the shell. [Telemetry services](/docs/en/data-usage#telemetry-services) says what each one stops. Two exceptions turn off from a settings file: [feedbackDrafts](#feedbackdrafts) below for Claude-drafted feedback, and [feedbackSurveyRate](#feedbacksurveyrate) below for the session survey.
[​](#cleanupperioddays)cleanupPeriodDays`
- Scope: Any file
- Type: number of days, a whole number, minimum 1
- Default: 30

```
{
  "cleanupPeriodDays": 20
}

```
### Set how many days Claude Code keeps [session transcripts and other application data](/docs/en/claude-directory#cleaned-up-automatically) before deleting them. Claude Code runs the deletion as a background sweep after a session starts, as long as it can safely determine the retention period. The sweep deletes transcripts without showing a message, so a session you haven’t used for longer than the retention period no longer appears in the [/resume](/docs/en/sessions#resume-a-session) picker.

****``
****``
****``

settings.json
Setting 0 fails validation, so pick a large value such as 3650 for long retention. To stop Claude Code from writing transcripts at all, see [Plaintext storage](/docs/en/claude-directory#plaintext-storage).
[​](#desktopsessioncleanupperioddays)desktopSessionCleanupPeriodDays`
- Scope: User or managed. Claude Code also reads the key from a file you pass with --settings, and ignores it in project and local settings.
- Type: number of days, a whole number, minimum 0
- Default: 0, which sets no age limit

```
{
  "desktopSessionCleanupPeriodDays": 90
}

```
### Set an age limit in days for the transcripts of sessions you started or most recently continued in Claude Desktop or Cowork. Without this key, Claude Code [keeps those transcripts at any age](/docs/en/claude-directory#cleaned-up-automatically). Claude Code deletes each one once it’s older than both this limit and [cleanupPeriodDays](#cleanupperioddays), so with cleanupPeriodDays at its default of 30, a value of 7 still keeps them 30 days. [Cleaned up automatically](/docs/en/claude-directory#cleaned-up-automatically) lists the cases where cleanupPeriodDays applies instead and Claude Code ignores this key. Requires Claude Code v2.1.248 or later.

****````
****``
****``

settings.json
[​](#feedbackdrafts)feedbackDrafts`
- Scope: User or managed
  - "notify": Claude Code shows a card above the prompt when Claude queues a draft, up to three cards in a session by default
  - "quiet": Claude drafts without a card. You see the count of queued drafts in the prompt footer and review them in /feedback
  - "off": Claude Code removes the SendFeedback tool, so Claude can’t queue drafts
- Default: "notify"
- Per-session overrides: CLAUDE_CODE_SEND_FEEDBACK set to 0 turns the feature off for one session

```
{
  "feedbackDrafts": "quiet"
}

```
### Control [Claude-drafted feedback](/docs/en/tools-reference#sendfeedback-tool-behavior): whether Claude can queue feedback drafts for you to review, and whether Claude Code shows a card when Claude queues one.

****``
****````````
````
``

****``
****````

settings.json
Appears in /config as **Claude-drafted feedback**, which writes this key to your user settings. You see the /config row only in sessions [where Claude can draft feedback](/docs/en/tools-reference#sessions-without-claude-drafted-feedback); setting "off" doesn’t hide it, so you can turn the feature back on from the same row. A value in managed settings takes precedence over your user setting, so when an administrator sets this key, the row shows the managed value and changing it has no effect. Claude Code ignores this key in project and local settings.
[​](#feedbacksurveyrate)feedbackSurveyRate`
- Scope: Any file
- Type: number between 0 and 1
- Default: unset, so Claude Code uses the rate Anthropic sets remotely, or its built-in rate of 0.005 on Amazon Bedrock, Google Cloud’s Agent Platform, and Microsoft Foundry, which don’t receive remote configuration
- Per-session overrides: CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY set to 1 turns the survey off for one session whatever rate this key sets

```
{
  "feedbackSurveyRate": 0.05
}

```
### Set the probability that the [session quality survey](/docs/en/data-usage#session-quality-surveys) appears when a session is eligible for it. Set 0 to keep the survey from appearing.

****``
****````
****``
****````

settings.json
The same rate applies to the survey in the VS Code extension.
[​](#skipwebfetchpreflight)skipWebFetchPreflight`
- Scope: Any file
  - true: Claude Code skips the WebFetch domain safety check
  - false: the check runs before the first fetch to each hostname in a session, and again for a hostname whose earlier check was blocked or failed
- Default: unset, so the check runs before the first fetch to each hostname in a session

```
{
  "skipWebFetchPreflight": true
}

```
## Skip the [WebFetch domain safety check](/docs/en/data-usage#webfetch-domain-safety-check), which sends each requested hostname to api.anthropic.com before fetching. Set true in environments that block traffic to Anthropic, such as Amazon Bedrock, Google Cloud’s Agent Platform, or Microsoft Foundry deployments with restrictive egress.

****``
****``
``

****

settings.json
With the check skipped, WebFetch attempts any URL without consulting the blocklist, so pair it with [WebFetch permission rules](/docs/en/permissions#webfetch) if you need to restrict which domains Claude can reach.

[​](#enterprise-and-managed-settings)Enterprise and managed settings
### Keys an organization uses to compute, refresh, and combine managed settings. See [Set up managed settings](/docs/en/admin-setup).
[​](#disablesideloadflags)disableSideloadFlags`
- Scope: Managed
  - true: Claude Code rejects --plugin-dir, --plugin-url, --agents, and --mcp-config at startup and exits with an error naming them. In cloud sessions, it instead starts the session and drops every server-delivered --mcp-config entry except in-process type: "sdk" entries and a Claude Tag session’s Slack tools
  - false: Claude Code accepts those flags
- Default: false

```
{
  "disableSideloadFlags": true
}

```
- The CLAUDE_CODE_PLUGIN_DIRS environment variable: when the variable names a plugin folder, Claude Code exits at startup with an error that names the variable and says to unset it. Requires Claude Code v2.1.280 or later
- The Agent SDK addPlugins option: when an application passes plugin folders to reloadPlugins() in addPlugins, that call fails with an error. The session keeps running with the plugins it already had. Requires Claude Code v2.1.301 or later
- Code sessions on the user’s machine: they also start without the skills enabled for the user’s claude.ai account. Plugins that Claude Code installs from marketplaces in your managed settings still load. In Claude Desktop on 3P, MCP servers from plugins you deploy to the device’s org-plugins directory stay available too, because the desktop app connects to them itself. Before Claude Desktop v1.37937.0, these sessions failed at startup instead.
- Cowork sessions on the user’s machine: the skills inside those plugins and the skills enabled for the user’s claude.ai account stay available. In Claude Desktop on 3P, MCP servers from plugins you deploy to the device’s org-plugins directory stay available too, because the desktop app connects to them itself. Before Claude Desktop v1.44121.0, these sessions failed at startup instead.
### Reject the --plugin-dir, --plugin-url, --agents, and --mcp-config CLI flags at startup, which users could otherwise pass to bypass [strictKnownMarketplaces](#strictknownmarketplaces) for a single run. Claude Code exits with an error naming the rejected flags. In [cloud sessions](/docs/en/claude-code-on-the-web), Claude Code instead starts the session and drops every server-delivered --mcp-config entry except in-process type: "sdk" entries and a [Claude Tag](/docs/en/claude-tag) session’s Slack tools. Requires Claude Code v2.1.193 or later.

****``
****``````````````
``

****``

managed-settings.json
Claude Code still accepts a --mcp-config whose servers are all in-process type: "sdk" entries, so the Agent SDK and VS Code extension keep working. Users can still add servers with claude mcp add or a .mcp.json file; for per-server control, set [allowedMcpServers](/docs/en/managed-mcp) as well. Requires Claude Code v2.1.193 or later.
disableSideloadFlags also rejects plugin folders from these sources:

````

In cloud sessions, Claude Code also ignores server-delivered mid-session MCP updates, the path behind cloud session configuration and SDK setMcpServers() calls that reach those sessions. In-process type: "sdk" entries and a Claude Tag session’s Slack tools stay exempt there too. Before v2.1.268, both this drop and the startup drop also removed a Claude Tag session’s Slack tools. Before v2.1.239, a server-delivered --mcp-config blocked a cloud session from starting.
The desktop app manages some plugins itself, including plugins synced from claude.ai and plugins your organization deploys through the app. If you deploy this key to a device through MDM, OS-level policy, or a managed settings file, the desktop app doesn’t pass those plugins to the following sessions on that device:

****``
****``

[​](#forceremotesettingsrefresh)forceRemoteSettingsRefresh`
- Scope: Managed. Claude Code honors a true from any admin-controlled managed source, even one that isn’t the highest-priority source.
  - true: Claude Code blocks startup until it has freshly fetched server-managed settings, and exits if the fetch fails
  - false: unless Anthropic requires the settings, Claude Code doesn’t block startup on the fetch, though at a sign-in startup it waits up to five seconds for the fetch
- Default: false

```
{
  "forceRemoteSettingsRefresh": true
}

```
### Block CLI startup until Claude Code has freshly fetched [server-managed settings](/docs/en/server-managed-settings). If the fetch fails, Claude Code exits instead of continuing with cached or no settings. Set it when your environment can’t accept even a brief window in which a session runs without its managed policy.
When the key is unset, Claude Code doesn’t block startup on the fetch, though when the developer signs in at startup it waits up to five seconds for the fetch. [Anthropic can require the settings](/docs/en/server-managed-settings#fetch-and-caching-behavior), which does block a start without them. A Cloud gateway session waits, and exits if the gateway can’t be reached.

****````
****``
``

****``

managed-settings.json
Set it in an MDM profile or the managed settings file to enforce fail-closed startup before the first server payload arrives. Claude Code applies the check only in sessions that fetch server-managed settings, so a session that [doesn’t fetch them](/docs/en/server-managed-settings#platform-availability) starts without waiting. The claude auth subcommands are exempt, so users can re-authenticate when expired credentials are why the fetch fails. See [Enforce fail-closed startup](/docs/en/server-managed-settings#enforce-fail-closed-startup).
[​](#managedsourcesbehavior)managedSourcesBehavior`
- Scope: Managed. Claude Code reads this key from the highest-priority source that carries either this key or a policy key, and ignores this key in every source ranked lower, so a lower source can’t opt itself into combining with the source above it. Neither the Windows HKCU registry nor parent settings from an embedding host take part in the merge.
  - "first-wins": the highest-priority source that carries a policy key supplies the policy, and lower sources contribute only the keys Claude Code reads from every admin source
  - "merge": every admin source you deliver contributes its keys, combined by the rules below
- Default: "first-wins"

```
{
  "managedSourcesBehavior": "merge"
}

```

| Kind of key | How Claude Code combines it | Keys |
| --- | --- | --- |
| Lists | Combines entries from every source | permissions.allow, sandbox.network.allowedDomains, and other list keys |
| Locks | Applies the strictest value any source sets. When no source sets a strict value, applies a looser value only from the highest source | allowManagedPermissionRulesOnly, permissions.disableBypassPermissionsMode, and other boolean or enum locks |
| Restriction allowlists | Takes the list whole from the highest source that sets it, without adding entries from lower sources. When the highest source doesn’t set one, takes it whole from the next source down | availableModels, allowedMcpServers, allowedProviders, strictKnownMarketplaces, allowedChannelPlugins, and the fallbackModel chain |
| Values taken whole | Takes the value whole from the highest source that sets it, without combining entries or fields from lower sources. When the highest source doesn’t set it, takes it whole from the next source down | sandbox.credentials.awsPairs, sandbox.ripgrep |
| Provided MCP servers | Combines the server names from every source. When two sources set the same name, applies the higher source’s whole entry | managedMcpServers |
| Read from the highest-priority source only | Reads the key only from the highest-priority source that carries a policy key, so a lower source’s value is ignored even when the highest source sets none | apiKeyHelper, awsAuthRefresh, awsCredentialExport, gcpAuthRefresh, otelHeadersHelper, proxyAuthHelper, parentSettingsBehavior, modelPicker, policyHelper, permissions.defaultMode |
| env | Merges per variable across admin sources, under both "first-wins" and "merge" | env |
| Every other key | Takes the value from the highest source that sets it | cleanupPeriodDays, model |

- policyHelper: Claude Code honors it only when the highest source that carries a policy key is an MDM policy or a managed settings file, so under server-managed settings it doesn’t apply.
- modelOverrides: pairs with availableModels. Claude Code takes modelOverrides from the highest source that sets it, unless a higher source sets availableModels without modelOverrides. In that case it ignores modelOverrides from every source.
- forceLoginGatewayUrl, gatewayInternalNetworks, and the "gateway" value of forceLoginMethod: Claude Code never reads any of them from server-managed settings, so a value there neither applies nor hides one set in an MDM policy or managed settings file. Among the admin sources on the machine, only the highest-ranked one that carries a policy key supplies them, whether or not server-managed settings are also present.
- forceLoginOrgUUID and the "claudeai" and "console" values of forceLoginMethod: look up which value applies in Which managed source supplies login keys rather than in the table.
- allowedProviders: after the table’s rule, the machine’s own list still limits the result, as its entry’s Scope note states.
### Choose whether Claude Code applies only the highest-priority [managed source](/docs/en/managed-settings#how-claude-code-combines-managed-sources) your organization delivers, or combines every admin source it delivers. By default Claude Code takes the highest-priority source that carries a [policy key](/docs/en/managed-settings#how-claude-code-combines-managed-sources) and ignores the rest. A policy key is any settings key other than this one and wslInheritsWindowsSettings. Under that default, once server-managed settings or an MDM policy deliver a policy key, a managed-settings.json file contributes only the [keys Claude Code reads from every admin source](/docs/en/managed-settings#keys-read-from-every-admin-source). With "merge", every admin source you deliver contributes its keys to one combined policy. Requires Claude Code v2.1.242 or later.
Set "merge" only where every source [ranked](/docs/en/managed-settings#how-claude-code-combines-managed-sources) below your highest one is under an administrator’s control, because Claude Code then adds entries from a lower source, such as permissions.allow rules, to the policy.

****``
****``
``

****``

Deliver the key in the highest-priority source you deploy. A machine that never receives server-managed settings needs the key in its MDM profile too, because Claude Code reads the key from the highest-priority source that carries it or a policy key. A managed-settings.json file is the lowest-ranked admin source, so "merge" set there has no source below it to combine with. In server-managed settings, the key looks like this:

Under "merge", Claude Code combines each key by its kind. This table gives the rule for each kind. The restriction allowlist, values-taken-whole, and highest-source-only rows name every key they cover, and the other rows give examples:
``````````````````````````````````````````````````````````
Taking sandbox.credentials.awsPairs and sandbox.ripgrep whole requires Claude Code v2.1.257 or later.
A few keys add a condition that the table doesn’t show:

``````````

To confirm which sources combined on a machine, run /status and [read the Setting sources line](/docs/en/managed-settings#read-the-source-in-/status).
[​](#parentsettingsbehavior)parentSettingsBehavior`
- Scope: Managed. Claude Code reads it from the highest-priority admin-controlled managed source.
  - "first-wins": Claude Code drops the host-supplied settings when an admin-deployed managed tier is present
  - "merge": Claude Code applies the host-supplied settings under the admin tier through a restrictive-only filter
- Default: "first-wins"

```
{
  "parentSettingsBehavior": "merge"
}

```
### Choose whether Claude Code applies managed settings supplied by an embedding host process, such as the Agent SDK or an IDE extension, when an admin-deployed managed tier is also present. With "first-wins", Claude Code drops the host-supplied settings; with "merge", it applies them under the admin tier through a restrictive-only filter. Set "merge" when a host needs to pass its own restrictions to the sessions it launches, for example Claude Desktop delivering a gateway’s egress allowlist.

****``
****``
``

****``

managed-settings.json
This key has no effect when no admin-deployed managed tier exists: the host’s settings then apply as the only managed tier, still filtered to restrictive values. For the filter’s limits and how the managed sources interact, see [Parent settings from embedding hosts](/docs/en/managed-settings#parent-settings-from-embedding-hosts) and [Restrict parent settings](/docs/en/claude-apps-gateway#restrict-parent-settings).

[​](#policyhelper)policyHelper`
- Scope: Managed. Read from the macOS plist, the Windows HKLM registry, or the managed settings file. Claude Code reads the key from the highest-priority managed source that carries a policy key and runs the helper only when that source is one of those three; it ignores the key in server-managed settings, the HKCU registry, and host-supplied parent settings.
- Type: object with path, timeoutMs, and refreshIntervalMs
- Default: unset, so no helper runs

```
{
  "policyHelper": {
    "path": "/usr/local/bin/claude-policy",
    "timeoutMs": 5000,
    "refreshIntervalMs": 300000
  }
}

```
#### Run an executable you deploy that computes managed settings at startup, so you can derive policy from device posture, identity, or a remote service instead of a static file. Claude Code runs the helper before it accepts the first prompt and treats the settings it emits as the managed settings for the session.

****``
****``````
****

When server-managed settings deliver the policy at launch, they take precedence over the helper’s source and the helper doesn’t run.
If a later settings fetch reports the server-managed settings removed, Claude Code runs the helper at that point rather than waiting for the next launch. Its output governs the rest of the session, and a run that fails ends the session with the same message as a [failed startup run](#helper-failures).
This example runs the helper with a 5-second timeout and re-runs it every five minutes:
managed-settings.json
[​](#write-the-helper-output)Write the helper output

```
{
  "managedSettings": {
    "permissions": { "deny": ["Read(//etc/secrets/**)"] }
  }
}

```
#### Claude Code runs the helper with no arguments, sets CLAUDE_CODE_VERSION in its environment, and reads a JSON envelope from stdout, capped at 1 MiB.
Put the settings under a managedSettings key. A bare settings object with no managedSettings key parses with managedSettings undefined and applies nothing, and Claude Code reports no error:

When the helper emits managedSettings, that object becomes the only managed settings source for the run: Claude Code ignores the MDM, file, and HKCU sources, reads the [cross-source keys](/docs/en/managed-settings#keys-read-from-every-admin-source) from the helper’s output alone, and never merges [parent settings](/docs/en/managed-settings#parent-settings-from-embedding-hosts).
The startup forceRemoteSettingsRefresh check runs before the helper and reads any admin source. A helper that exits 0 with an envelope that omits managedSettings contributes no managed settings, and the other sources apply as usual.
[​](#helper-failures)Helper failures
- path breaks the rules in policyHelper.path.
- No regular file is at path. Claude Code checks for the file before starting the helper, within the same timeoutMs budget, so an unresponsive network mount can cause the run to fail.
- The helper exits non-zero, is still running when timeoutMs elapses, or doesn’t start at all, for example because it isn’t executable.
- The helper writes more than 1 MiB to stdout or to stderr.
- stdout isn’t a single JSON object, or its managedSettings has a schema violation Claude Code can’t repair.
### A helper run fails when:

````
````
``

``

When the startup run fails, Claude Code prints the reason and refuses to start. After a non-zero exit, the reason includes the helper’s stderr, or its stdout when stderr is empty. After a timeout, the reason names the timeoutMs limit and includes none of the helper’s output. The refusal covers interactive sessions, claude -p, Agent SDK sessions, [background sessions](/docs/en/agent-view), and most subcommands.
The refusal is deliberate, so a helper that needs outage resilience should serve from its own cache and exit 0.
When a background refresh fails, Claude Code keeps the last successful policy in effect, and /status shows the failing refresh with its reason until a refresh succeeds. Each refresh runs under the same timeoutMs and failure rules as the startup run.
With --debug, Claude Code writes the helper’s stderr from every run to the [debug log](/docs/en/debug-your-config).
Claude Code reports an invalid policyHelper value as a [dropped entry](/docs/en/managed-settings#find-entries-claude-code-dropped) and starts the session on the remaining managed settings without running a helper. Invalid values include a bare path string and a timeoutMs below [its minimum](#policyhelper-timeoutms).
To turn a helper off, remove the key from the source that sets it.
[​](#policyhelper-path)policyHelper.path`
- Scope: Managed. Read from the macOS plist, the Windows HKLM registry, or the managed settings file, wherever policyHelper is read.
- Type: string, an absolute path in normalized form, without . or .. segments; on Windows, a drive-letter or UNC path that ends in .exe
- Default: none; required when policyHelper is set

```
{
  "policyHelper": {
    "path": "/usr/local/bin/claude-policy"
  }
}

```
### Name the helper executable Claude Code runs. For what happens when the path breaks the rules below, see [Helper failures](#helper-failures).

****````
****``````
****``

managed-settings.json
[​](#policyhelper-timeoutms)policyHelper.timeoutMs`
- Scope: Managed. Read from the macOS plist, the Windows HKLM registry, or the managed settings file, wherever policyHelper is read.
- Type: integer, milliseconds, minimum 1000
- Default: 10000

```
{
  "policyHelper": {
    "path": "/usr/local/bin/claude-policy",
    "timeoutMs": 5000
  }
}

```
### Set how long Claude Code waits for the helper before treating the run as failed. A timed-out run fails the same way as a non-zero exit, so at startup Claude Code refuses to start.

****````
****``
****``

managed-settings.json
[​](#policyhelper-refreshintervalms)policyHelper.refreshIntervalMs`
- Scope: Managed. Read from the macOS plist, the Windows HKLM registry, or the managed settings file, wherever policyHelper is read.
- Type: integer, milliseconds: 0 to disable refresh, otherwise at least 60000
- Default: unset, so Claude Code runs the helper once at startup

```
{
  "policyHelper": {
    "path": "/usr/local/bin/claude-policy",
    "refreshIntervalMs": 300000
  }
}

```
### Have Claude Code re-run the helper in the background on an interval so policy changes reach a running session. When a refresh succeeds, its output replaces the previous managed settings without a restart; when a refresh fails, Claude Code keeps the policy it already has.

****````
****````
****

This example re-runs the helper every five minutes:
managed-settings.json
[​](#wslinheritswindowssettings)wslInheritsWindowsSettings`
- Scope: Managed. In an admin-controlled Windows source.
  - true: Claude Code on WSL reads managed settings from the Windows policy chain, and reads /etc/claude-code only when no Windows admin document is present
  - false: WSL reads only /etc/claude-code
- Default: false, so WSL reads only /etc/claude-code

```
{
  "wslInheritsWindowsSettings": true
}

```
## Have Claude Code on WSL read managed settings from the Windows policy chain, with HKLM and the Windows managed settings file taking priority over /etc/claude-code and HKCU below it. While the chain is on, Claude Code reads /etc/claude-code only when [no Windows admin document is present](/docs/en/managed-settings#present-admin-documents) in the HKLM registry value or the C:\Program Files\ClaudeCode\ folder. Set it to extend the policy you already deploy on Windows to WSL sessions on the same machine, so they follow the same rules as host sessions. Claude Code honors it only when set in the HKLM registry key or in a managed settings file or drop-in under C:\Program Files\ClaudeCode\, both of which require Windows admin to write.

****``
****````
````

****````

managed-settings.json
Once an admin source turns the chain on, HKCU policy joins it on WSL only when HKCU also sets the key to true. That copy doesn’t turn the chain on by itself. A Windows source that contains only this key, set to true or false, doesn’t count as a policy source, so a lower-priority source still supplies the policy. This key has no effect on native Windows.
Claude Code reads true and false with or without quotes and reads null as removing the key. An admin-controlled Windows source that holds any other value counts as a [present admin document](/docs/en/managed-settings#present-admin-documents) with the chain turned on: neither /etc/claude-code nor HKCU applies, and a startup warning names the key. An HKLM value or Windows-folder file that exists but can’t be read also keeps /etc/claude-code from applying whether or not the chain is on. Requires Claude Code v2.1.282 or later.
[​](#global-config-settings)Global config settings
### Save these keys in ~/.claude.json, not in a settings file. Claude Code ignores them anywhere else. Claude Code and /config write most of them for you, and you can also edit them by hand.
[​](#autoconnectide)autoConnectIde`
- Scope: Global config
  - true: Claude Code connects to a running IDE automatically when you start it from an external terminal
  - false: Claude Code doesn’t connect automatically from an external terminal; inside a VS Code or JetBrains terminal, or with --ide, it still connects
- Default: false
- Per-session overrides: CLAUDE_CODE_AUTO_CONNECT_IDE takes precedence over this key for one session, in either direction

```
{
  "autoConnectIde": true
}

```
### Connect to a running IDE automatically when you start Claude Code from an external terminal. Appears in /config as **Auto-connect to IDE (external terminal)** when you run Claude Code outside a VS Code or JetBrains terminal.

****``
****``
````

****``
****``

~/.claude.json
Claude Code ignores this key in settings.json.
[​](#autoinstallideextension)autoInstallIdeExtension`
- Scope: Global config
  - true: /ide installs the extension
  - false: /ide doesn’t install the extension
- Default: true
- Per-session overrides: CLAUDE_CODE_IDE_SKIP_AUTO_INSTALL set to 1 skips the install for one session even when this key is true

```
{
  "autoInstallIdeExtension": false
}

```
### Let [/ide](/docs/en/commands) install the Claude Code IDE extension in a running VS Code, Cursor, or Devin Desktop when you run the command from an external terminal. Claude Code doesn’t install or update the extension when you start claude. Before v2.1.318, Claude Code installs or updates the extension when you start claude in one of those editors’ terminals, unless this key is false.
Appears in /config as **Auto-install IDE extension** when you run Claude Code inside a VS Code or JetBrains terminal.

****``
****````
````

****``
****``````

~/.claude.json
Claude Code ignores this key in settings.json.
[​](#claudeinchromedefaultenabled)claudeInChromeDefaultEnabled`
- Scope: Global config
  - true: Claude Code turns on Chrome integration when an interactive CLI session starts, as it does when you pass --chrome. In the VS Code extension, sessions connect to the browser as they start
  - false: interactive CLI sessions start with Chrome integration off, and Claude Code stops offering to set it up. Pass --chrome to turn it on for one interactive session. In the VS Code extension, a session connects when you type @browser, as when the key is unset
- Default: unset, so Chrome integration is off and Claude Code can still offer to set it up
- Per-session overrides: --chrome and --no-chrome take precedence over this key for one interactive session

```
{
  "claudeInChromeDefaultEnabled": true
}

```
### Start every interactive CLI session with [Chrome integration](/docs/en/chrome) on, without passing --chrome each time. If you run [claude remote-control](/docs/en/remote-control), a session it starts for one of your [project](/docs/en/claude-projects) threads follows this key too, except in bypassPermissions mode. With Claude Code v2.1.287 or later, this key also applies to sessions in the [VS Code extension](/docs/en/vs-code#automate-browser-tasks-with-chrome): see [Enable Chrome by default](/docs/en/chrome#enable-chrome-by-default).
Running /chrome and selecting **Enabled by default** sets this key for you, as does answering the [“Claude in Chrome extension detected” dialog](/docs/en/chrome#answer-the-startup-dialog). Appears in /config as **Claude in Chrome enabled by default**.

****``
****````
``````

****
****````

~/.claude.json
Claude Code ignores this key in settings.json.
[​](#copyfullresponse)copyFullResponse`
- Scope: Global config
  - true: /copy copies the full response without showing the picker
  - false: when the response contains code blocks or blockquotes, /copy shows a picker where you choose one block or the full response
- Default: false

```
{
  "copyFullResponse": true
}

```
### Make [/copy](/docs/en/commands) copy the full response every time, without showing the picker. Selecting **Always copy full response** in that picker sets this key to true. Appears in /config as **Skip the /copy picker**.

****``
****````
````

****``

~/.claude.json
Claude Code ignores this key in settings.json.
[​](#copyonselect)copyOnSelect`
- Scope: Global config
  - true: Claude Code copies text to your clipboard when you finish selecting it
  - false: selecting text leaves your clipboard unchanged, and you copy the selection with a keyboard shortcut instead
- Default: true

```
{
  "copyOnSelect": false
}

```
###  text to your clipboard automatically when you finish selecting it with the mouse in [fullscreen rendering](/docs/en/fullscreen#use-the-mouse) or [agent view](/docs/en/agent-view). Appears in /config as ** on select** while fullscreen rendering is on.

****``
****``
``

****``

~/.claude.json
Claude Code ignores this key in settings.json.
[​](#defaulttoagentsview)defaultToAgentsView`
- Scope: Global config
  - true: claude with no arguments opens agent view, unless agent view is turned off
  - false: claude with no arguments starts a new conversation
- Default: false

```
{
  "defaultToAgentsView": true
}

```
### Open [agent view](/docs/en/agent-view) instead of a new conversation when you run claude with no arguments. Appears in /config as **Open agents view by default** unless agent view is [turned off](#disableagentview).

****``
****````
````

****``

~/.claude.json
Claude Code ignores this key in settings.json.
[​](#difftool)diffTool`
- Scope: Global config
  - "auto": Claude Code opens the diff in the IDE’s diff viewer when a VS Code or JetBrains IDE is connected
  - "terminal": Claude Code keeps the diff in the terminal
- Default: "auto"

```
{
  "diffTool": "terminal"
}

```
### Choose where Claude Code shows the diff of an Edit or Write change it proposes when a [VS Code](/docs/en/vs-code) or [JetBrains](/docs/en/jetbrains#features) IDE is connected: "auto" opens it in the IDE’s diff viewer, "terminal" keeps it in the terminal. Appears in /config as **Diff tool** only while Claude Code is connected to a VS Code or JetBrains IDE.

****``
****``
``

****``

~/.claude.json
Claude Code ignores this key in settings.json.
[​](#externaleditorcontext)externalEditorContext`
- Scope: Global config
  - true: the editor buffer starts with Claude’s previous response as # comment lines, which Claude Code strips when you save
  - false: the editor buffer opens with only your prompt
- Default: false

```
{
  "externalEditorContext": true
}

```

```
# ─── Claude's last response (for reference; removed on save) ───
# I added the retry loop to fetchUser in src/api.ts and a test
# for the timeout case. Want me to wire the same retry into
# fetchOrders?
# ─── Write your reply below this line ──────────────────────────

Yes, and cap it at three attempts.

```
### When you press Ctrl+G, Claude Code opens the prompt you’re typing in your [external editor](/docs/en/interactive-mode#general-controls). With this key on, the editor buffer starts with Claude’s previous response as # comment lines, so you can read it while you write, and Claude Code strips those lines when you save. Appears in /config as **Show last response in external editor**.

****``
****````
``

****``

~/.claude.json
With it on, the buffer Claude Code opens looks like this, and only the text below the marker line is sent as your prompt:

Claude Code keeps the last 50 lines of the response and marks the cut with # … (earlier output truncated).
Claude Code ignores this key in settings.json.
[​](#leftarrowopensagents)leftArrowOpensAgents`
- Scope: Global config
  - true: pressing ← on an empty prompt in a session you started in the terminal backgrounds it and opens agent view
  - false: Claude Code turns the shortcut off; in a session you attached to from agent view, ← on an empty prompt still detaches
- Default: true

```
{
  "leftArrowOpensAgents": false
}

```
### Press ← on an empty prompt to [background the session and open agent view](/docs/en/agent-view#switch-sessions-without-leaving-the-terminal). Set this key to false to turn the shortcut off. Appears in /config as **← opens agents** when agent view is available.

****``
****````
````

****``

~/.claude.json
Claude Code ignores this key in settings.json.
[​](#permissionexplainerenabled)permissionExplainerEnabled`
- Scope: Global config. On v2.1.256 and earlier.
- Type: Boolean
- Default: true
### Removed in v2.1.257, together with the Ctrl+E command explanation on Bash and PowerShell permission prompts. Setting it has no effect on current versions.
Through v2.1.256, you could press Ctrl+E on a Bash or PowerShell permission prompt to see a model-generated explanation of the command, and set this key to false to turn that shortcut off.

****``
****
****``

[​](#prstatusfooterenabled)prStatusFooterEnabled`
- Scope: Global config
  - true: the footer shows the badge under the conditions in PR review status
  - false: Claude Code skips the footer’s pull request and merge request check and doesn’t show that badge. A session you attached to from agent view can still show a plain link to a pull request linked to it
- Default: true

```
{
  "prStatusFooterEnabled": false
}

```
### Show a badge in the prompt footer for the current branch’s open pull request or merge request, with a colored underline that shows its [status](/docs/en/interactive-mode#pr-review-status). Appears in /config as **Show PR status footer**.

****``
****``
``

****``

~/.claude.json
Claude Code ignores this key in settings.json.
[​](#teammatedefaultmodel)teammateDefaultModel`
- Scope: Global config. On v2.1.233 and earlier.
- Type: string, a model alias or full model ID, or null
- Default: unset
## Removed in v2.1.234, together with its /config row **Default teammate model**. Setting it has no effect on current versions.
Through v2.1.233, you set this key to the model for [agent team](/docs/en/agent-teams#specify-teammates-and-models) teammates your prompt didn’t name a model for: an alias such as "sonnet", or null to follow the lead’s model. For the model Claude Code picks for such teammates now, see [specify teammates and models](/docs/en/agent-teams#specify-teammates-and-models).

****``
****``
****

[​](#see-also)See also
- Configure permissions: rule syntax, permission modes, and workspace trust
- Environment variables: every CLAUDE_*, ANTHROPIC_*, and provider variable Claude Code reads
- Tools available to Claude: the built-in tools and which need approval
- Example settings files: a personal file, a team file, and an organization’s managed file
- Set up managed settings: how organizations decide what to enforce
- Deploy managed settings: delivery mechanisms, precedence within the managed tier, and invalid entries in managed settings
- Debug your configuration: claude doctor and the Settings Error dialog
````

``
Was this page helpful?
