<!--
source: https://www.framer.com/blog/harness-2/
type: blog
author: Adam Seckel
published: 2026-11-02
fetched: 2026-11-12
note: body pre-fetched; direct fetch skipped
-->

# Harness 2: executing agent code as it streams

[Adam Seckel](https://twitter.com/hemlok_)

Published Nov 2, 2026

We rebuilt the Framer Agent’s harness to let it take on whole workflows in a single program. Making it up to 33% cheaper, and 20% faster.

A request like “find every use of our old brand color and replace it” can involve inspecting thousands of nodes and changing hundreds of properties. The agent can now express that work in JavaScript, inspect the document, decide which nodes to change, and apply the updates without returning to the model for each decision.

To support that much work in one program, we built an execution system that runs JavaScript while the model is still writing it. We compile incoming code into executable cells and run them as they become available. You can see the first changes on the canvas before the model finishes generating the rest. We preserve the live feedback of our original harness while giving the agent loops, conditionals, and access to the document.

We can also catch failed assumptions before generation finishes, stop the remaining stream, avoid further output-token charges, and return the information the agent needs to try again.

The new architecture uses 2x fewer tool steps and 39% fewer cached input tokens per message, on average. This represents a meaningful increase in task efficiency with no measured reduction in quality.

## Background

Framer uses a tree structure to represent your design documents. This tree acts as an AST from which code and CMS content are deterministically generated.

The first version of our harness used a DSL (domain-specific language) for the model to describe its writes to this tree. The model emitted commands to create nodes and set properties. We could apply those commands as they arrived, so you could watch a page take shape.

The limitations showed up in repetitive edits and dependent operations:

- **Repeated edits:** changing a property across 100 frames could require 100 editing commands.
- **Dependent edits:** reading a value and using it in a write required separate model calls, replaying context between them.
- **Multi-step workflows:** inspecting changes, publishing to staging, and promoting to production required returning to the model between steps.

Even when the model knew the whole workflow in advance, the harness made it work one step at a time.

## Harness 2

### Part 1. Eager code execution

Completing a task in one program avoids the repeated model calls and input tokens required by many smaller programs. But longer programs introduce two problems:

1. **Delayed feedback:** the whole program must be generated before execution can begin, so users wait longer to see any progress.
2. **Wasted generation:** an early return or terminal error can stop execution after just a few lines, but the model has already spent time and tokens writing the rest.

Both problems grow as programs get longer: users wait longer for progress, and an early stop wastes more generation time and billed output tokens on code that never runs.

*配图：时间线对比——左为「先缓冲整个程序再执行」，右为「流式执行」，3 个 cell 在同一程序中随 token 到达依次执行，画布提前出现首次更新。*

### Eager execution with AST parsing

To make longer programs practical, we needed to start executing them before generation finished. We overlap generation and execution, so document edits—or longer-running operations such as publishing to staging—can begin while the model writes the code that follows.

As code streams in, we parse it to identify complete JavaScript statements, group them into executable “cells,” and send them to a dedicated Web Worker. Cells execute in order as classic scripts, with bindings preserved between them. We also transpile top-level await into syntax supported by classic scripts.

The same parsing step turns comments like // @step Building buttons into emit("Building buttons"), giving users progress updates throughout longer programs.

*配图：流式执行时间线——Cell 2 已执行完成时 Cell 3 仍在接收，完整 cell 在后续程序到达时即开始执行。*

### Cancellation

In a larger program, the model may base many later operations on an early assumption. A missing node or an unexpected property can invalidate much of what follows, wasting time and output tokens.

We prompt the agent to check required conditions before the work that depends on them. If those checks pass, execution continues without another model round trip. A terminal error or an early return—including when no changes are needed—cancels the remaining generation. Cancellation preserves edits already applied to the document.

Eager execution makes these savings possible: we discover that execution has stopped while the model is still generating code, so we can cancel the remaining stream. If we buffered the whole program before running it, that discovery would come too late—the generation time and billed output tokens would already have been spent. The exact savings depend on how far generation has progressed when cancellation takes effect.

Early cancellation also changes how we design errors. A terminal error can explain what went wrong and how to recover, allowing the next attempt to correct the failed assumption.

*配图：流式执行 + 取消场景——目标 button 缺失时 Cell 2 提前 return，后续生成被取消，在途 token 丢弃，return 之前没有任何文档写入。*

The ability to start work early, stop failed attempts, and guide recovery makes longer programs practical. Together, eager execution, early cancellation, and actionable errors form a novel and cutting-edge approach to real-time feedback harness design. Agents can take on larger workflows in a single program while users see progress as the model writes it. Fewer model round trips reduce repeated input tokens, overlapping generation and execution gets work started sooner, and early cancellation saves time and billed output tokens on code that would never run. This lets us pursue more ambitious programs while keeping execution responsive and failed attempts inexpensive.

1. Related work includes *Executing as You Generate*, which applies AST-based eager execution to Python.

## Part 2: Redesigned document Access

### Replacing DSL streaming with method calling

Since streaming code execution preserves real-time visual updates, we rewrote our tree modification API as individual method calls. DSL commands INSERT and PATCH became tree.insert() and tree.patch(), and could use references to other nodes for values.

```javascript
// "Clamp all opacity less than 50% to the opacity of this ("xxx") button"
const button = tree.get("xxx")
for (const node of tree.walk()) {
	if (node.opacity < 0.5) node.patch({ opacity: button.opacity })
}
```

Compared to our DSL-based writes, this program collapses a read–write cycle into a single request and ensures that the desired value comes straight from the live document instead of requiring the value to first be read into context and then echoed into the subsequent write.

### Efficient document writes

Although eager execution lets us cancel failed programs quickly, recoverable write errors shouldn’t stop the whole program.

The harness applies valid properties, clamps values to supported ranges, and skips unsupported properties. It reports warnings and errors when the program finishes, so the agent can address them without repeating successful writes.

Take the following program snippet as an example:

```javascript
tree.patch(node, {
  fill: "#09f",
  opacity: -0.1,
  unsupportedProperty: "hello!"
})
```

The harness applies the fill, clamps opacity to 0, and skips the unsupported property. The program continues, with warnings and errors attached to its final result so the agent can address them without repeating successful writes.

Further, we allow the model to author efficient patches of deeply nested arrays and objects by supporting dot notation and sparse arrays as a first-class patch format. This avoids forcing the model to use spreads to ensure that partial patches apply safely, reducing output tokens and improving accuracy.

```javascript
tree.patch(node, { "appearEffect.enter.x": "100px" })
tree.patch(node, { "boxShadow": [,, "0px 0px 10px #000",, "0px 0px 20px #000"] })
```

### Execution speed & efficient queries

Early cancellation only helps if execution returns before generation finishes. That made fast document access essential: round trips between the worker and the document could leave reads—and the writes behind them—lagging behind generation.

We keep an in-memory copy of the document in the Web Worker, allowing the agent’s programs to read and modify it synchronously. This has three benefits:

1. **Fewer output tokens:** reads and writes don’t need repeated await prefixes.
2. **Fast traversal:** programs can navigate and modify documents with millions of nodes using standard JavaScript.
3. **Simpler instructions:** the model doesn’t need guidance on writing performant queries.

### Unified agent harness

Our first release of Framer for Agents in June shipped with differences between how the in-app agent and external agents like ChatGPT Desktop, Claude Code, or Cursor interacted with Framer. External agents used their own execution systems to make repeated requests through Framer’s servers.

The new harness gives external agents the same tools as the in-app agent. They can submit a single program through MCP that runs directly in Framer, with synchronous access to the local document. Execution is faster because individual reads and writes no longer require round trips through the MCP server. A unified platform also lets us bring new features and improvements to whichever agent you use.

### Wrapping up

Together, these changes let us ask the agent to take on whole workflows in a single program: read the document, make decisions, apply changes, and publish. Work starts while the model is still writing, and failed assumptions stop generation early. The result is 43% fewer tool steps and 39% fewer cached input tokens per message, while preserving the live feedback of watching your site take shape.

The harness shapes how much work we can ask a model to take on at once. By making longer programs practical, we give the agent room to carry a task through—from inspecting the first node to publishing the finished site—with fewer interruptions along the way.

> When we were preparing this post, we believed we were the first to develop this concept. However, while researching this post we found [Executing as You Generate](https://arxiv.org/abs/2604.00491), first published on April 1, 2026, by Zhensu Sun and colleagues at Singapore Management University and Beihang University. Their Eager system applies the same core approach in Python: AST-based chunking, persistent execution state, and early interruption of generation on runtime errors. It also includes one efficiency improvement we did not think of: removing completed statements from the parse buffer before processing subsequent tokens. We plan to adopt this optimisation. Their paper examines the benefits of this approach in Python; our production harness demonstrates them in practice.
>
