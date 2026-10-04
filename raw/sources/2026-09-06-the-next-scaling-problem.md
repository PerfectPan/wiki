<!--
source: https://tetral.ai/blog/the-next-scaling-problem/
type: blog
author: Yang Li
published: 2026-09-06
fetched: 2026-10-02
note: body pre-fetched via in-session reader tool; direct fetch skipped
-->

# The Next Scaling Problem

## Scaling the wrong thing
At the end of last year, I started building cloud agents with one goal: to
scale them. By then I had spent months living in local coding agents, especially
[Claude Code](https://www.anthropic.com/news/claude-3-7-sonnet) from its early
research preview and later [Codex CLI](https://github.com/openai/codex). An agent
looked like a program installed on a computer, surrounded by that computer’s
files, shell, and tools.
[Manus’s article on context
engineering](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)
made a cloud version concrete: actions ran inside a virtual-machine sandbox,
with its filesystem serving as restorable context. For my first product, Anoma,
I took the most literal path and moved the local agent loop into
[E2B](https://e2b.dev/blog/how-manus-uses-e2b-to-provide-agents-with-virtual-computers).
The sandbox became the unit of agent capacity, so scaling agents meant scaling
sandboxes.
Using E2B did not remove the need to manage a sandbox fleet; more users still
meant more sandboxes to provision, reuse, and reclaim, within the provider’s
lifecycle constraints. Session history and traces stayed inside those sandboxes
until cleanup, making debugging depend on
[access to environments holding private user data](https://www.anthropic.com/engineering/managed-agents).
Keeping API keys outside required a separate gateway to proxy model requests.
We kept moving responsibilities out of the sandbox to make an agent inside it
workable.
Swipe or scroll horizontally to explore the full diagram →
The first architecture begins with an entire agent loop inside one E2B sandbox. A control plane then appears outside it to manage sandbox capacity and proxy model traffic. Finally a web app connects users to that control plane, which still scales complete agent-sandbox bundles.
**How the first app grew**01 · Agent in Sandbox02 · Control Plane03 · Product Surfaceproduct surface**Web app**users · tasks
streamed results**Control plane**control plane**Sandbox lifecycle**capacity · reuse
LRU eviction**Model Gateway**credentials
request · stream**Task state + events**session sync · files · product updates**E2B fleet**tasks A–C**E2B sandbox**task A**Agent loop**contextmodelresulttool call**Agent loop**contextmodelresulttool callfilesystem · shell · tools**E2B sandbox**task B**Agent loop**contextmodelresulttool call**E2B sandbox**task C**Agent loop**contextmodelresulttool callThe entire agent runs inside one E2B sandbox.The control plane manages sandbox capacity and model traffic, but every sandbox still carries a complete agent.The product talks through the control plane. Scaling the app still means scaling complete agent-sandbox bundles.Back01 / 03NextSandboxControl PlaneProductⅡ PauseThe first app grew in three layers: a complete agent inside E2B, a control plane for sandbox capacity and model traffic, and finally a product surface. The control plane scaled sandboxes, but every sandbox still carried an entire agent.
By February, those constraints had convinced me that the architecture needed to
change. For my second product, Tetral, I wanted a general-purpose agent package
rather than another application with a fixed UI. That meant an SDK developers
could use to bring cloud agents into their own products, without writing the
loop or operating the infrastructure behind it. Delivering that product
meant owning the hosting layer, but it still left the sandbox as the unit of
capacity. I considered two routes.
Kubernetes could operate the service, but its pods were a poor unit for
sandboxes created and destroyed at high frequency. Modal later [documented the
same mismatch at
scale](https://modal.com/blog/scaling-to-1-million-concurrent-sandboxes-in-seconds):
the serialized scheduler and coordinated pod lifecycle become bottlenecks under
extreme sandbox churn.
The other route was EC2, Firecracker, and a control plane for microVM creation,
cold starts, and reclamation. It was viable, but it led to building a sandbox
provider. Agent capacity would still follow the number of computers the fleet
could supply. Either route left sandbox provisioning as its own replaceable
infrastructure problem rather than part of the agent service.
The agent and the sandbox fleet followed different scaling curves. The agent
was a stable, shared service whose capacity could be reused across many pieces
of work. The sandbox fleet was isolated, bursty, and disposable. Keeping that
volatility independent required separating the two. The agent became a stable
service, while sandboxes remained disposable execution resources. This design
was intended to let Kubernetes run a pool of agent runtimes and distribute
concurrent sessions across replicas without also managing sandbox churn.
Separating them did not make sandbox scaling unnecessary; it made the sandbox
one resource among models, memory, files, credentials, and tools, each with its
own lifecycle. Linux, Windows, and macOS became different forms of the same
execution resource. **A computer should be something the agent calls, not
somewhere the agent lives.** The next question was where this agent ended and
the cloud system around it began.
## Building the system, finding the runtime
### The runtime boundary
Separating the agent from its sandbox left a more precise question: how could
the agent be abstracted into a service that scaled across concurrent sessions?
The technical bet was to treat the agent as a runtime: a continuing program
that interprets model output and gives the agent controlled access to models,
networks, files, tools, subagents, and the external world. Claude Code and Codex
already behaved as local runtimes. In the cloud, the same loop could become a
replaceable compute unit only if its identity, state, and resources lived
outside the process. That criterion defined the runtime boundary: every
responsibility with a different owner, lifecycle, or scaling pattern had to
move outside it.
Swipe or scroll horizontally to explore the full diagram →
1. One process owns every responsibility. Provider integration, state, delivery, computer lifecycle, and product surfaces all sit inside the agent process.
1. Provider integration becomes Gateway. Provider formats, credentials, connections, and streams move behind one normalized request boundary.
1. State moves behind Bridge. Bridge owns the PostgreSQL protocol, while the agent process keeps only replaceable working state.
1. Delivery becomes Queue. Accepted work is registered independently from the process that will eventually receive or perform it.
1. Computer lifecycle becomes Sandbox Service. The agent declares a computer operation. Sandbox Service owns activation, execution, and replacement.
1. The remaining compute is the Runtime. Public surfaces move outside as well. What remains loads a thread, applies the reducer, and declares the next action.
Agent Systemdeliverjobrequeststreamdeclareackresultinputeventsagent processruntimesessions**S1****S2***…*active threads**T1****T2***…*thread loop**state******reducer******action****provider integration****Gateway**formats · credentials
connections · streams**state + database protocol****Bridge + PostgreSQL**ownership · ordering
recovery · transactions**delivery****Queue**ordering · leases
retries · cancellation**computer lifecycle****Sandbox Service**activation · execution
replacement**product surfaces****Public API + Event Stream**accept work · expose recordsBack01 / 06 · BundledNextBundledGatewayStateQueueComputersRuntimeⅡ Pause**One process owns every responsibility**Provider integration, state, delivery, computer lifecycle, and product surfaces all sit inside the agent process.************************Finding the runtime by moving provider integration, state, delivery, computer lifecycle, and product surfaces outside the replaceable compute boundary.
Provider integration was the first responsibility to leave. Provider formats,
credentials, outbound connections, and streaming protocols did not determine
the agent’s next action. Gateway took ownership of them and exposed one
normalized request and stream contract to the runtime. Because Gateway retained
no session state between requests, provider traffic could scale independently.
Accepted inputs, execution progress, and results had to survive any Kubernetes
pod, so PostgreSQL became the source of truth. The runtime did not access it
directly: that would bind every runtime implementation to the schema,
transactions, ownership, ordering, and retry protocol. Bridge owned that
boundary, checking ownership and order before committing a transition and
returning its result.
State alone did not deliver work. A producer therefore committed each input,
agent message, or resource operation together with a Queue job. Delivery could
then outlive the producer and be attempted by any compatible consumer. Queue
owned ordering, leases, retries, cancellation, and dead-lettering.
Computer lifecycle was another responsibility to leave. Sandbox Service owned
provider-backed computers and executed the work scheduled for them. The runtime
only declared that a thread required a computer operation.
The Public API and Event Stream also remained outside the execution path: one
accepted SDK requests, and the other exposed PostgreSQL’s ordered records.
Neither executed an agent.
What remained was computation over sessions and threads.
A session is one continuing body of agent work, configured with an agent
version and a selected set of resources. A thread is an actor-like serialization
boundary: one independently ordered execution path inside that session. A
session begins with a root thread for the main agent and may create child
threads for subagents.
For each active thread, a reducer examines the state reconstructed from
committed inputs and results, then returns the next valid transition. It
performs no database or network I/O. Its answer may be to call a model, route a
tool call, wait for more input, or finish.
The runtime loaded a thread through Bridge, applied the reducer, and declared
the next action. A runtime pod was only a replaceable compute host. It could
keep multiple sessions and threads hot, but owned none of them and could not
dispatch an external operation until its declaration had been accepted.
One route considered from the beginning was to place the agent loop inside a
general-purpose durable execution engine. [Cursor takes this route with
Temporal](https://cursor.com/blog/cloud-agent-lessons): its workers run the
agent loop while Temporal replays workflow code against its Event History to
recover control flow. Cursor also maintains a separate append-only conversation
store for agent output and client streaming.
Tetral chose a different recovery boundary. PostgreSQL holds the agent
transitions, conversation history, and projections. A replacement runtime
reconstructs a thread checkpoint from those records and asks the pure reducer
for its current state and next transition. Queue carries work registered around
the same commits, so the alpha keeps durable agent control state under one
transactional database authority.
### Write ahead of execution
A replaceable runtime creates one hard problem. After a pod disappears, its
replacement must know whether an operation had never started, was still in
progress, or had already completed. Process memory cannot answer that question.
Guessing could either skip the work or perform the same external effect twice.
This protocol borrows [WAL’s ordering
rule](https://www.postgresql.org/docs/current/wal-intro.html): record a
transition before performing the operation it authorizes. Any transition that
can advance a thread or create an external obligation must therefore commit
before dispatch. After a failure, the runtime reconstructs the turn from those
committed facts instead of restoring the lost process.
Before dispatch, the runtime submits an immutable declaration with a stable
identity to Bridge. Bridge verifies ownership and order, then commits the
transition and its receipt in one transaction. Only after that acknowledgement
may the runtime dispatch the operation. The stable identity is an idempotency
key: retrying the same declaration returns its existing receipt instead of
creating a second transition.
Swipe or scroll horizontally to explore the full diagram →
**Runtime Pod**one session · three stages of its loop**Stage 01**model request✓ received**committed context***↓***reducer**derive next action*↓***request start**declare before call**Stage 02**tool calling✓ received**model output***↓***tool call**declare before dispatch*↓***raw tool result**not yet in context**Stage 03**next loop✓ received**result committed***↓***turn complete**request ended + tools settled*↓***next request**commit before callmodel requesttool callingnext loopnext iteration → Stage 01runtime boundary**Bridge**verify owner + order → commit → receipt**01**idle**02**idle**03**idle**PostgreSQL**same session · records committed at each stage**01****************02****************03**************01020301 · Restore01 · Request02 · Tool call02 · Raw result03 · Close turn03 · Next turn◀ BackⅡ PauseNext ▶**01 · Restore**The runtime reconstructs the turn from records already committed in PostgreSQL.One session is shown at three stages of its loop. At each stage, the runtime sends its declaration through Bridge and waits for the commit receipt before advancing.
One session, shown at three stages of its loop. Before it dispatches an action or continues from a result, Bridge records that transition in PostgreSQL.
Consider a model turn that produces a Bash call. The input is committed before
it enters context, and span.model_request_start records the exact context
boundary before Gateway receives the request. When the model returns the Bash
call, Bridge commits the runtime’s agent.tool_use declaration before the call
can be routed.
Bridge records the sandbox execution and its Queue job in one transaction. A
sandbox worker runs the command and stores the raw result as completed but not
yet consumed. Bridge returns that result to the waiting runtime, which declares
agent.tool_result for the original tool use.
In one transaction, Bridge appends agent.tool_result, updates the
corresponding entry in session_messages, marks the stored sandbox result as
consumed, and records an idempotent receipt. Only after the acknowledgement may
the reducer depend on that result and calculate the next step.
span.model_request_end closes the provider request. The reducer can prepare
another request only after it and every required tool result have been
committed.
The storage model behind this protocol began with two ideas from OpenCode v2:
an [event
table](https://github.com/anomalyco/opencode/blob/a3bc5d35b0f8f542d4531193b8816bc8b55363e3/packages/opencode/src/sync/event.sql.ts)
beside a [session-message
projection](https://github.com/anomalyco/opencode/blob/a3bc5d35b0f8f542d4531193b8816bc8b55363e3/packages/opencode/src/session/session.sql.ts).
The schema extends that split with the ordering and receipts required by
replaceable compute.
session_events is the event log. It keeps the ordered execution history, including accepted
inputs, request boundaries, tool calls, tool results, interrupts, and closeout.
session_messages is its model-context projection. It stores the context that
can be loaded for the model. User
messages are appended in order, while one assistant message accumulates text,
tool calls, and tool results during a model request. After a successful
compaction ([Tetral’s compaction mechanism was adapted from OpenCode’s
design](https://opencode.ai/v2/docs/compaction)), future loads begin from the
new summary checkpoint, while the earlier execution history remains unchanged.
Compaction determines what the next model request loads; it does not erase the
earlier session log. That preserved history can later become [searchable
context](https://openai.com/index/gpt-6-astra/), rather than asking one summary
to carry the entire past.
session_bridge_operations stores the receipt for each idempotent declaration.
Together, these records form the session log: a logical execution record, not
one physical table or merely a conversation transcript. Each thread maintains
its own order, while the event stream assigns positions across the session.
These records are also sufficient to recover a thread; the system does not
store a mutable snapshot of the running state machine. On a cold load, Bridge
returns the committed messages, request and tool boundaries, and unresolved
work. The runtime builds a checkpoint from them, and the reducer determines
whether the thread is waiting for a request, waiting for tools, or ready to
continue.
If a commit acknowledgement is lost, the runtime resubmits the same identity
and Bridge returns the stored receipt. Reusing that identity for different
content is rejected.
If a runtime pod disappears during an open model request, Bridge records the
request as failed. Durable pending work can still be recovered; otherwise,
the thread returns to idle. A replacement runtime can reconstruct the committed
checkpoint, but it does not resume the lost provider stream. Work already
committed remains with the service responsible for it.
The protocol cannot make an arbitrary external system transactional. It gives
each effect a committed identity and owner so retries converge on the same
operation: record what the thread may do before performing it, and record what
happened before the agent depends on it. An ambiguous outcome cannot advance
the thread silently.
### Durable delivery
The write-ahead execution protocol determined how a runtime could safely
advance a thread. It did not yet guarantee that an accepted input would reach
one.
Bridge commits let an active thread advance. Queue carried work that could wait
for a consumer and outlive its producer.
Consider a user message that arrives while no runtime pod is ready. In an
[outbox-style atomic
enqueue](https://learn.microsoft.com/en-us/azure/architecture/databases/guide/transactional-out-box-cosmos),
one PostgreSQL transaction appends the input event, creates an Inbox entry for
its target thread, and creates a Queue job that points to that entry.
The Queue job tells Bridge’s Job Runner that delivery still needs an attempt.
The Inbox is the receiving-side record: it names the target thread and records
whether the input is queued, being delivered, or accepted by a runtime.
Once that transaction commits, the Public API returns 200; delivery continues
asynchronously, and processed_at is set only when the runtime commits the input
into its target thread.
Swipe or scroll horizontally to explore the full diagram →
**Durable delivery**register together · deliver independently**Queue**available work**Queue Job 41**S1 · user inputACK ✓**Queue Job 18**S2 · agent mailACK ✓**Queue Job 07**S3 · user inputACK ✓**Job Runner**poll Queueleased Queue Job 41deliver input #41 to S1leased Queue Job 18deliver mail #18 to S2leased Queue Job 07deliver input #07 to S3**input #41****mail #18****input #07****Runtime Inbox**delivery state**S1 · input #41**queueddeliveringaccepted ✓**S2 · mail #18**queueddeliveringaccepted ✓**S3 · input #07**queueddeliveringaccepted ✓three registrations create three Queue Jobs and three Inbox recordsRunner takes Queue Job 41Runner takes Queue Job 18Runner takes Queue Job 07Queue empty · all three deliveries acceptedⅡ PauseEach registration transaction creates a Queue job and its Inbox record. The Job Runner takes the job, delivers the referenced input, advances the Inbox to accepted, and acknowledges the job.
After the transaction commits, PostgreSQL emits pg_notify to wake Bridge’s Job
Runner. The notification contains no message content and owns no delivery
state. If it is lost, the runner’s polling loop discovers the same Queue job
later; the message remains in PostgreSQL.
Before the Job Runner leases the message, Queue checks its target thread.
Inputs that advance one context remain ordered, so a later ordinary message
cannot pass one being delivered or retried. Other threads proceed concurrently.
Session-wide changes form a barrier across those lanes. An interrupt is handled
separately so it can reach its target without waiting behind ordinary pending
input.
After leasing the job, the runner sends the message, with a stable identity, to
the runtime pod responsible for the session. It waits in the target thread’s
input queue if another turn is already advancing.
Reaching the runtime closes the delivery obligation in two steps. Bridge first
records the Inbox entry as accepted, then the Job Runner acknowledges the Queue
job. At that point the Job Runner is finished. Whether and when the runtime
commits the accepted input into its thread belongs to the runtime’s own loop,
not to delivery.
The accepted Inbox record closes the remaining failure windows. A lost RPC
response causes a retry with the same input identity. A lost Queue
acknowledgement lets the next runner observe that acceptance and close the job
without delivering it again.
A timeout alone does not prove that the old runtime has stopped processing the
message. The binding generation and pod UID act as a fencing token: Bridge
returns an already-accepted delivery to the Queue only after Kubernetes
confirms that the bound pod identity has disappeared. A replacement runtime can
then load the thread’s last committed state and continue from the same Inbox
obligation.
### Calling the model
Once the runtime committed an accepted input, the reducer could declare a model
call. The runtime assembled a normalized request from the named provider and
model, thread context, system instructions, tools, and attachments. Bridge
recorded span.model_request_start with the exact message sequence before the
request left the runtime.
The request carried no API key or OAuth token. Gateway verified the pod’s
Kubernetes workload identity and a short-lived Bridge token proving that it
still owned the named session and thread. A replaced pod could no longer
refresh that token or call models for its former threads.
Gateway then loaded the credential selected for the session. A missing,
revoked, archived, or undecryptable selection caused rejection rather than a
silent fallback; only a session with no selection could use the platform key
pool.
OAuth refresh happened at the same boundary. Gateway locked the credential row,
refreshed the token, saved the replacement, and injected the new access token
only into the outbound provider request. The plaintext credential never entered
the runtime, Bridge, the session log, or a sandbox.
Gateway converted the request through the [Vercel AI
SDK](https://ai-sdk.dev/docs/introduction) and returned normalized
ProviderStreamEvent values over gRPC. It chose no model and retained no
session state, so any replica could serve the explicitly named provider and
model.
The runtime accumulated text and tool calls for the turn. Output crossed Bridge
before entering stored context; tool calls waited for agent.tool_use; and
span.model_request_end closed the provider stream.
If the runtime pod disappeared while the stream was open, another pod could
recover the recorded request boundary but not the network connection owned by
the lost process. Bridge closed that request as runtime_pod_lost, allowing the
reducer to reconstruct a consistent thread state instead of treating an unknown
partial response as complete.
MCP applied the same boundary to tools. Before a session first ran, Bridge asked
the MCP connector for the configured server’s tool list and stored the accepted
version. The runtime received names, descriptions, and input schemas, but no
server credential or connection details. Tool-list changes produced a new
stored version.
When the model selected an MCP tool, the runtime first committed
agent.mcp_tool_use. The connector verified its authority, injected the
session credential only into the remote request, and handled OAuth refresh.
The result crossed Bridge before entering the thread’s context.
In both paths, the runtime declared what capability it needed and which resource
should handle it. Gateway and the MCP connector owned the external connections,
provider formats, and credentials. The agent could use those capabilities
without any runtime pod or sandbox receiving the underlying secret.
### Computers as resources
Most capabilities did not require a computer. Model and web requests belonged
to Gateway, MCP calls belonged to the MCP connector, and memory operations went
through Bridge. Shell and filesystem tools were different because they required
an execution environment.
A computer is the resource exposed to the agent. A sandbox is the current
provider-backed isolation instance, and Sandbox Service owns its lifecycle and
execution.
That did not mean every session needed a sandbox from the moment it was created.
Computers were allocated lazily, only when one of those tools required them.
The earlier Bash declaration and Queue job could exist before any computer was
ready. When a Sandbox Service worker leased that job, it inspected the computer
assigned to the session.
If a compatible computer was already running and prepared for the current
session resources, the worker could execute the command. Otherwise, Sandbox
Service began an activation.
Activation meant making a computer available for execution. Depending on its
current state, Sandbox Service could reuse it, start it, create it, or replace
it. If the selected files, helper state, and session access were not ready on
that computer, a separate materialization job prepared them afterward.
Queue advanced both dependencies. The first execution job ended after attaching
the Bash execution to its activation, while the declaration remained
waiting_activation in PostgreSQL. Concurrent calls could share that
activation instead of starting competing computers. After activation and
materialization, each logical execution returned to Queue as a new job.
Swipe or scroll horizontally to explore the full diagram →
One Bash tool call, execution 42, is committed through Bridge before it is scheduled. Sandbox Service discovers that its computer is cold, records the execution as waiting, activates the computer, requeues the same logical execution, runs Bash, stores the raw result, and returns it through Bridge. Bridge commits the tool result before the runtime continues.
1. validate ownership
1. commit one transition
1. return its receipt
**One Bash call, one cold computer**execution #42**Runtime**compute**thread #42**reducer → Bash declarationtool result → reducer continuesowns no durable state**Bridge**state boundaryreceived**Sandbox Service**computer lifecycle**Execution worker**waiting for workleased #42 · generation 1leased #42 · generation 2**Lifecycle worker**waiting for workactivating A7**Computer**coldactivatingready**PostgreSQL**authority**session log**—agent.tool_useagent.tool_result**execution #42**—pending · generation 1waiting_activation · A7pending · generation 2raw result · unconsumedresult consumed**Queue**—execute #42 · g1activate A7execute #42 · g2**Bash #42****agent.tool_use****receipt****execute #42 · g1****execute #42 · g1****wait on A7****activate A7****A7 ready****execute #42 · g2****run Bash****stdout · exit 0****raw result****tool result****receipt****01 / 10** Runtime declares Bash #42.**02 / 10** Bridge commits the Tool Use and returns a receipt.**03 / 10** Bridge records execution #42 and its first Queue Job.**04 / 10** An execution worker leases #42 and finds a cold computer.**05 / 10** Sandbox Service parks #42 on activation A7.**06 / 10** A lifecycle worker activates the computer.**07 / 10** The same execution returns to Queue as generation 2.**08 / 10** The worker runs Bash and stores the raw result.**09 / 10** Runtime receives the stored result through Bridge.**10 / 10** Bridge commits the Tool Result; the reducer may continue.Back01 / 10Next********************Ⅱ PauseBash execution #42 reaches a cold computer. Sandbox Service parks the logical execution on activation A7, then returns it to Queue as a new generation after the computer is ready.
Before submitting the command, Sandbox Service bound that execution to the
exact current computer. If another worker replaced or released the computer in
the meantime, a stale worker could not send the accepted command to the new one.
Sandbox Service then stored the output for the waiting runtime to settle through
Bridge. Runtime failure did not cancel the computer operation or require the
Bash command to be issued again.
The current implementation lazily assigns one Daytona-backed computer to a
session, but that mapping is not the abstraction. A computer is one resource
whose implementation can vary with the operation. File access may eventually
use a virtual filesystem, a small isolated task may need only a lightweight
container, and other work may require Linux, macOS, Windows, or specialized
compute.
### Scaling in two dimensions
Making computers independently schedulable did not let one ordered context
advance in two directions. Concurrent model requests would read the same
boundary and produce competing next states, so parallel work required separate
execution paths.
A workspace held long-lived resources such as files and memory. A session was
one continuing task with its own configuration, history, lifecycle, and
selected resources. A thread was one ordered context and execution path inside
that session.
Threads shared a session without sharing context. Sessions shared a workspace
without sharing execution history.
Swipe or scroll horizontally to explore the full diagram →
One session first expands from a root thread into two independent child threads. The view then pulls back to show three independent sessions in the same workspace. Each session can expand its own threads while selecting resources from the shared workspace.
**One workspace, two dimensions**threads within a task · sessions across tasksworkspace**Session A**one continuing task**root thread**state → reducer
action ↩**child T1**state → reducer
action ↩**child T2**state → reducer
action ↩**Session B**independent task**root thread**state → reducer
action ↩**child T1**state → reducer
action ↩**child T2**state → reducer
action ↩**Session C**independent task**root thread**state → reducer
action ↩**child T1**state → reducer
action ↩**child T2**state → reducer
action ↩**workspace resources**files · memory · repositories · credentials
agent version → tools · skillsOne task begins on one ordered thread.Child threads create independent paths within the task.Independent tasks become separate sessions.Every session can scale its own execution paths.Agent work scales in two dimensions: threads create independent execution paths within one task, while sessions create independent tasks over resources selected from the same workspace.
Tetral’s subagent control model was adapted from [Codex’s multi-agent
design](https://github.com/openai/codex/blob/main/codex-rs/core/src/tools/handlers/multi_agents_spec.rs).
A parent can spawn a child from selected context, continue working
independently, send further messages, wait for completion, or interrupt it.
Tetral maps those operations onto child threads and the same ordered delivery
path used by other session inputs.
If the main agent wanted an implementation inspected while it continued the
design, it created a child thread running the same reducer and tool loop over a
separate context. An independent review might need no parent history, a
continuation might need all retained context, and a focused investigation only
the most recent turns.
fork_turns made that choice explicit: none for no parent history, all for
all retained parent context, or a positive number of recent turns. The runtime
resolved it into an exact, immutable starting context for the child.
An in-memory child could disappear before receiving its instruction, or be
created twice after a lost response. The runtime therefore committed the
spawn_agent tool call first. In one transaction, Bridge created the child and parent
relationship, saved its context and instruction, placed the instruction in its
Inbox, and created the delivery job.
Only after Bridge acknowledged that transaction did the tool call return the
child thread ID. Retrying the same committed call returned the same child
instead of creating another.
After the fork, parent and child still had separate contexts. New parent
messages did not automatically appear in the child, and neither thread could
directly write into the other’s context. Further communication had to be
delivered as another ordered input.
Messages and child completions returned as ordered inputs. Bridge recorded the
message, destination, Inbox entry, and Queue job in one transaction. If the
receiving thread was busy, the input waited behind its current turn.
send_message, child completion, and wait_agent used this path. A child’s
final answer was committed before reaching the parent’s Inbox. Waiting added no
second durable content channel and did not repeat the child’s work.
Child threads were appropriate when several execution paths still belonged to
one task. They were not the right boundary for every responsibility around a
workspace. Code implementation, documentation, auditing, and knowledge
maintenance could each require an independent root agent, context, agent
version, credential set, and lifecycle. Those belonged in separate sessions.
Separate sessions could still select files, memory stores, repositories,
credentials, and an agent version from the same workspace. Tools and skills
came from that resolved version. Execution and history stayed independent; a
product could later decide which reviewed results became shared resources.
### A separate decision
Scaling agent work also scales its external effects. Keeping credentials behind
Gateway prevents the runtime and its computers from possessing a provider key
or OAuth token, but it does not decide whether one proposed action should use
that credential.
Credential isolation controls access to a capability. Authorization decides
whether one proposed action may exercise it.
That decision belongs before execution and outside the agent proposing it. A
cloud boundary can apply the same deterministic policy, content inspection,
classifiers, and server-side enforcement across clients and execution
environments, as [Claude Code auto
mode](https://www.anthropic.com/engineering/claude-code-auto-mode) demonstrates.
OpenAI’s [Hugging Face
incident](https://openai.com/index/hugging-face-incident-and-the-road-ahead/)
shows why recognizing risk inside the acting agent is not the same as enforcing
a boundary around it. This does not imply that an LLM reviewer would have
prevented that incident. It means a tool call must cross an authorization
boundary before it can affect the outside world.
approve_for_me is the first mode implemented at this boundary. Its review
model was inspired by Codex’s [automatic approval
reviewer](https://developers.openai.com/codex/sandboxing/auto-review), then
adapted to the write-ahead execution protocol.
Consider a model that proposes a Bash command whose policy is always_ask. The
runtime first passes the proposal through a deterministic tool gate. The gate
combines the session approval mode, the tool catalog, and the policy attached to
that tool. Under approve_for_me, the first evaluation says that an independent
review is required.
Nothing has been accepted for execution yet. There is no public
agent.tool_use, no sandbox job, and no external effect. The Bash command is
still a proposal produced by the open model request.
Schematically, the proposal receives a stable review identity derived from its
workspace, session, thread, model request, model tool call, tool name, canonical
action, and policy:

```
review_id = H(workspace, session, thread, request, tool_call, tool, action, policy)
```
The hash binds the decision to one exact proposal. Retrying the review uses the
existing identity, while changing the command or its policy creates a different
review.
The reviewer runs as an internal thread using the same runtime machinery as
other agent work. It receives the proposed action, the relevant parent context,
the current assistant output, sibling tool calls from the same model turn, and
the effective policy. These inputs are evidence, not instructions. Files,
websites, tool results, and even the acting model may contain prompt injection,
so platform-owned reviewer policy remains separate from the material being
reviewed.
The reviewer returns only a risk level, the user authorization visible in
context, an allow or deny outcome, and a rationale. Malformed output is a
review failure, not permission.
Within one hot parent-runtime lifetime, later reviews can reuse one reviewer
thread, which processes one review at a time. Overlapping reviews use temporary
threads copied from its latest committed state, allowing parallel decisions
without interleaving context histories.
Swipe or scroll horizontally to explore the full diagram →
Three tool calls arrive on one main thread. Each completed call first enters the Tool Gate. One review runs on the persistent reviewer thread. If another tool call needs review before it finishes, a temporary reviewer thread is copied from the persistent thread's latest committed state so both reviews can proceed in parallel. Every decision is committed to PostgreSQL before it returns to the Tool Gate for re-evaluation. Temporary threads close after their decisions settle; the persistent thread remains for later reviews.
**A separate decision**one model stream · gate before review**main thread**streaming model outputassistant draft********Tool call A***model call · A*Bash  npm testapproval pendingTool Gate → allow**Tool call B***model call · B*Write  release.mdapproval pendingTool Gate → allow**Tool call C***model call · C*Bash  npm publishapproval pendingTool Gate → deny**Tool Gate**policy → review_requireddecision → allow / deny**reviewer workbench**platform-owned prompt**reviewer trunk***ready**reviewing A**A committed*last committed context**sidecar B***reviewing B***sidecar C***reviewing C***PostgreSQL**decision commit rail**A**allow**B**allow**C**denycommitted receipt returns to the same callABCallow Aallow Bdeny Creceipt Areceipt Breceipt CA complete tool call reaches the Tool Gate before review.Overlapping reviews fork from committed reviewer context.Each decision becomes authority only after its commit.Committed decisions return to the Tool Gate for one final evaluation.Each completed tool call first reaches the Tool Gate. One review continues on the main reviewer thread while overlapping reviews use temporary copies of its latest committed state. Every decision is committed before the Tool Gate evaluates the exact proposal again.
The reviewer’s output is not yet authorization. Bridge first records the
decision in PostgreSQL under the proposal’s stable identity. Only after that
commit may the result return to the parent thread.
The runtime then runs the tool gate a second time, now with the committed review
outcome. An allowed decision produces an executable tool use. A denial records a
rejected tool result without running the command. A reviewer failure falls back
to user approval only after Bridge acknowledges the failure record. If that
commit fails or the runtime loses authority, the tool call does not advance.
Only after this second evaluation does the runtime commit the public
agent.tool_use. That event is the acceptance boundary after which execution
may be placed on the Queue and routed to the service that owns the requested
capability.
Cancellation follows the same ordering. If the parent turn is cancelled before
the review decision is acknowledged, a late outcome may remain available for
audit but cannot advance the cancelled tool call.
Before the public tool use is committed, the alpha remains deliberately
conservative. If the runtime disappears after the proposal but before
authorization completes, the request closes with runtime_pod_lost; the
proposal is neither reconstructed nor executed later. Recovery is sacrificed
at this boundary so an orphaned decision cannot become permission.
The reviewer may use the same model as the acting agent, and its policy is still
early. The system guarantees something narrower: reviewed actions cannot become
schedulable before a recorded decision; platform instructions are kept separate
from review evidence; each decision belongs to one proposal; and uncertainty
never becomes permission. The reviewer can improve behind that boundary without changing the
runtime or execution services.
## The next scaling problem
Once agent work can outlive any one process or computer, scaling it no longer
means adding only runtime capacity. Its authority, identity, history, and
resource use all grow with it. Isolation therefore has to follow the product:
what an agent can reach, how long it can act, and [where policy can be
enforced](https://www.anthropic.com/engineering/how-we-contain-claude). Tetral
keeps the agent outside the sandbox, credentials outside both, and computers as
temporary resources so execution, identity, and history can [fail, change, and
scale independently](https://www.anthropic.com/engineering/managed-agents).
Making identity and resources independent requires a public contract that names
them. [The Managed Agents
API](https://platform.claude.com/docs/en/managed-agents/agent-setup) provided
versioned agents, sessions pinned to a resolved version, per-session overrides,
and first-class files, memory stores, vaults, skills, and environments. Tetral
forked that SDK and remains compatible with the Managed Agents surface it has
implemented, with [registered deviations](/docs/reference/compatibility/), while
building the runtime and cloud system beneath it. By naming the agent, its
version, sessions, and resources independently, that contract makes the agent
addressable beyond any one client.
### A durable participant
An addressable agent can continue across a terminal, browser, phone, GitHub, or
team product because those surfaces share one ordered session history. Closing
a client does not end the session or transfer the agent between computers.
Identity makes that continuity accountable. An external action can be traced
to an agent version, session, thread, policy, and review. Its deployer remains
responsible, but the agent becomes a distinct actor in that chain.
[RoboBun](https://github.com/robobun) makes work on GitHub attributable to a
public agent identity. [Raft](https://raft.build/resources/blog/introducing-raft-where-humans-and-agents-build-together/)
places named, stateful agents together in a multi-agent workspace. [Claude
Tag](https://www.anthropic.com/news/introducing-claude-tag) gives a Slack channel
an asynchronous Claude and lets a team delegate to several Claudes in parallel.
The interfaces differ, but each treats the agent as an addressable participant
rather than an invisible completion behind a user’s account.
Identity becomes operational when it carries delegated authority. An agent can
[provision an account, obtain an API token, purchase a domain, and
deploy](https://blog.cloudflare.com/agents-stripe-projects/), or request a
[merchant- and amount-bound payment credential without receiving card
details](https://stripe.com/blog/giving-agents-the-ability-to-pay). The user or
organization remains the principal; the identified agent receives limited,
traceable authority.
Tetral keeps identity with the agent while the system controls credentials,
policy, approval, and execution. A CLI fits work bound to an operating system,
repository, compiler, or debugger. Reading an issue or posting a message should
not require a computer: MCP exposes the capability, its connector supplies the
session credential, and the runtime’s Tool Gate applies policy and approval.
A planned Code Mode, inspired by
[OpenCode](https://github.com/anomalyco/opencode/blob/dev/packages/codemode/README.md),
would let a confined JavaScript program discover and compose permitted MCP
tools, transform their results, and run independent calls in parallel. CLI
remains the interface for computer-native work; MCP becomes the preferred
interface for capabilities native to the cloud agent.
### Work that compounds
Adding communication or participants does not automatically improve
collaboration; [coordinated swarms and independent parallel agents can spend
similar tokens per result, and larger shared coding swarms can merge a smaller
share of their
work](https://www.anthropic.com/research/multiagent-systems).
Tetral’s bet is adversarial review before synthesis. Before work enters the
shared workspace, other agents must actively challenge its conclusions and
evidence, not merely agree with them. A human then decides what is accepted.
This scrutiny matters because accepted work becomes the basis for subsequent
exploration: an unchecked mistake can propagate into everything built upon it.
The workspace holds the work itself, together with the reasoning and evidence
needed to review it. Agents explore many paths, but progress accumulates by
[building on validated
results](https://www.anthropic.com/research/formalizing-fermats-last-theorem),
not by inheriting one another’s unexamined conclusions.
Swipe or scroll horizontally to explore the full diagram →
Two collaboration structures are compared. In the conversation-centered structure, three agents exchange messages in a shared channel while each retains a different working memory. In the artifact-centered structure, sessions begin from an accepted workspace version, produce independent proposals, review one another's artifacts, pass a candidate through human review, and merge the accepted result into the next workspace version.
**What should become shared?**conversation coordinates · accepted artifacts compound**Conversation-centered**shared room**Agent A**A's memory**Agent B**B's memory**Agent C**C's memory**shared channel**A: try thisB: another ideaC: wait—why?Coordination spreads through messages.
Each working memory keeps diverging.
**Artifact-centered**review and admission**Workspace v12**accepted source of truth**Session A**independent path**Session B**independent path**Session C**independent path**proposal A**reviewed by B · C**proposal B**reviewed by A · C**proposal C**reviewed by A · B**human review**accept · reject · ask again**Workspace v13**one accepted result mergedChat can coordinate the work. Only admitted artifacts change what future agents trust.Two collaboration structures: shared conversation, and independent work admitted into a shared workspace.
The workspace would preserve what the team accepted; the session log already
preserves how each candidate was produced.
Running the same task with different agent versions turns their trajectories
into comparable evaluations. Rejected tool calls, overturned reviews, failed
verification, and human corrections identify concrete failures that can become
[evaluation and alignment
data](https://openai.com/index/safety-alignment-long-horizon-models/). The same
[deployment trajectories](https://openai.com/index/deployment-simulation/) can
be used to evaluate successor models under realistic tools and external state.
Long-horizon products can therefore supply evidence for future evaluation and
training, provided provenance survives, private data is removed, and human
judgment identifies success or failure. Training should reduce harmful
proposals, but external effects still need deterministic policy, validation,
content inspection, classifiers, independent review, organization rules, and
human escalation.
### Scaling the system around intelligence
More capable models create more work for every system around them. Longer
horizons and more parallel paths mean more runtime transitions, tests,
computers, files, network requests, stored trajectories, and external effects.
The shortest of those capacities becomes the next scaling problem.
Programming languages and toolchains are part of that surface. Runtime pods
have finite CPU and memory for active threads, while every generated change may
start another edit, build, and test cycle. [Bun’s move from Zig to
Rust](https://bun.com/blog/bun-in-rust) reduced memory use and improved
throughput while addressing stability and memory-safety failures.
[TypeScript’s native Go
port](https://devblogs.microsoft.com/typescript/typescript-native-port/) began
because the existing implementation could not scale to the largest codebases;
early builds ran roughly ten times faster with substantially less memory. On my
development server, one Tetral integration path can take seven or eight minutes
and a full validation pass roughly half an hour. Compilation and verification
can become the limit before inference does.
Execution environments have a different load from stable services. Short-lived
environments must be scheduled, created, supplied with resources, paused,
resumed, released, and reclaimed. Burst creation, attachment and resume latency,
and high-churn scheduling matter as much as boot time. At sufficient scale they
encounter
[coordination and control-plane limits that ordinary service orchestration was
not designed
around](https://modal.com/blog/scaling-to-1-million-concurrent-sandboxes-in-seconds).
A sandbox is too heavy for every operation. File access may require only a
virtual filesystem; untrusted code needs stronger isolation; platform-specific
work needs the corresponding machine. The question is not only how many
sandboxes can run, but how much work must pass through a full computer and how
quickly each required boundary can be supplied.
[Actor systems](https://rivet.dev/actors/) suggest another point in this design
space: lightweight, addressable compute that can sleep and wake without
provisioning a full computer. How such a primitive should map to Tetral’s
sessions, threads, or resource workers remains open. The immediate conclusion
is only that a full sandbox should not be the default boundary for every
operation.
A disposable execution environment is useful only if its output can outlive it.
This exposes another resource boundary: storage. Session events, tool results,
and logs must enter an ordered session history, while code, documents, and
build outputs must return to repositories, object stores, or workspace files
that another environment can load later.
More parallel agents produce more transitions, files, commits, pull requests,
and test runs, pushing the systems behind those interfaces toward new limits.
Session logs may scale through [PostgreSQL replicas, pooling, caching, workload
isolation, and separation of write-heavy
data](https://openai.com/index/scaling-postgresql/). Code storage may need a new
implementation when agent-generated Git operations outgrow a traditional host,
as shown by [a Git-compatible host rebuilt around an object-storage write-ahead
log and replaceable local
repositories](https://cursor.com/blog/git-at-any-scale).
The agent still asks for session history, files, or a repository. What changes
under growing demand is the infrastructure that implements those storage
interfaces.
The model itself is also moving into a larger delivery unit. temperature,
top_k, and top_p are [deprecated for models released after Claude Opus
4.6](https://platform.claude.com/docs/en/api/messages/create), while current
agent interfaces emphasize effort, tools, skills, MCP servers, context, policy,
and orchestration. [Current model
guidance](https://developers.openai.com/api/docs/guides/latest-model) makes the
same move toward reasoning controls, hosted tools, and multi-agent execution.
The product being configured may increasingly be an agent system that includes
the model, rather than a raw model endpoint surrounded by product-specific
infrastructure.
### From an alpha to an agent-native cloud
Tetral is an alpha running on a personal k3s cluster, not a production-proven
cloud. Its runtime placement is not capacity-aware, backpressure does not yet
connect admission, Queue pressure, and scaling, and sustained multi-node
recovery has not been demonstrated. Runtime rollouts also interrupt in-flight
turns because graceful draining across releases is not yet implemented. The
current service topology needs production evidence because this release
concentrated first on the runtime, declaration, and recovery boundaries.
Each limitation points to the next build. Sessions need placement by runtime
capacity and recovery across nodes. Queue pressure must control admission and
worker supply. Execution needs faster activation, mounting, resume, lighter
file access, self-hosted providers, and the ability for one agent to coordinate
several computers at once. Small installations should also be able to group
logical services into fewer processes while production deployments scale them
independently, a flexibility already demonstrated by [Temporal’s service
deployment model](https://github.com/temporalio/documentation/blob/main/docs/encyclopedia/temporal-service/temporal-server.mdx).
The product direction is a hosted agent system service. Product teams should be
able to define their tools, reviewers, thread policies, resources, models, and
interfaces without first rebuilding continuity, identity, authorization,
recovery, and resource scheduling. The same system should support safer
execution, new products that span several clients and computers, and the
session evidence required for retrospective, evaluation, and future training.
The implementation will diverge as those workloads become real. Services may
merge, the runtime may move beyond Bun, storage may split, and the queue,
Bridge, or Kubernetes topology may be replaced. Three bets remain: the agent is
cloud native; the agent system, not only the model, must scale; and the runtime
keeps the agent as the computational center while the system around it preserves
continuity and control.
Those bets are now concrete enough to test with other people. Tetral is open
under the MIT license so product builders, infrastructure engineers, security
researchers, and model providers can challenge its boundaries, implement new
runtimes, connect new resources, and build products the current system did not
anticipate. The thesis is now concrete enough to test in public. This alpha is
the starting point for exploring the much larger space of an agent-native cloud.
