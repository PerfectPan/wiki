<!--
source: https://gist.github.com/aleclarson/0f4266d63fd83c7a5ea5512441bbea0c
type: repo
fetched: 2026-09-23
-->

**NOTICE:** I've summarized the perspectives of Octane's and Solid's creators here, for anyone short on time: [https://gist.github.com/aleclarson/829c10aa7d287944ef75e1c2a90bef06](https://gist.github.com/aleclarson/829c10aa7d287944ef75e1c2a90bef06)
I'm a React/Preact/Astro developer with an interest in other renderers. The two that have most caught my eye recently are [Octane](https://octanejs.dev/) (from Dominic Gannaway of React Hooks / Svelte / Inferno fame) and [Solid 2](https://www.solidjs.com/blog/solid-2-0-rc-the-big-reveal).
I asked ChatGPT to compare them with its own ["Renderer DX Pillars"](https://gist.github.com/aleclarson/64308585a36fe65692149b9cd2f59475), which I've shared below. This is its gut instinct, with very little hedging:

| Pillar | Winner | Why |
| --- | --- | --- |
| State architecture freedom | Solid 2 | Reactivity is independent of components. Much less component gravity. |
| Reactive reasoning | Solid 2 | The dependency graph is explicit and causal. Easier to answer “why did this update?” |
| Derived state & synchronization | Solid 2 | Fine-grained derivation is the native model; less need to coordinate state manually. |
| Async/data flow | Solid 2 | This is basically Solid 2's flagship idea. Async being part of reactivity feels deeper than improving Suspense/hooks ergonomics. |
| Component authoring | Octane | Normal values, normal functions, familiar TSX, fewer Solid-specific semantic gotchas. |
| Escape hatches | Solid 2, narrowly | Solid's primitives compose very directly with imperative JS without pretending everything is a component concern. |
| Ecosystem interoperability | Octane | If its React-ecosystem compatibility ambitions work, this could be a huge advantage. |
| Tooling & debuggability | Solid 2 today | More mature and battle-tested. Octane's compiler creates more invisible machinery that tooling has to explain well. |
| Architectural scaling | Solid 2 | Its reactive model naturally lets domain/application architecture exist independently of rendering. |

****
****

****
****

****
****

****
****

****
****

****
****

****
****

****
****

****
****

So my gut scoreboard is:
**Solid 2: 7**
**Octane: 2**
But the two Octane wins are meaningful ones.
### Where Octane feels strongest
Its pitch seems particularly strong around:
**“I want React's authoring experience without React's runtime/design baggage.”**
You get something like:

```
function Counter() {
  const [count, setCount] = useState(0);
  const doubled = count * 2;

  return <button onClick={() => setCount(count + 1)}>
    {doubled}
  </button>;
}
```
That's extremely approachable.
Solid asks you to internalize:

```
const [count, setCount] = createSignal(0);
const doubled = () => count() * 2;
```
which isn't hard, but it is a different programming model.
So for **day-one DX**, I wouldn't be surprised if Octane feels better.
### Where Solid feels fundamentally stronger
Solid's advantages seem to accumulate as the application becomes less like:
some components with state
and more like:
a complex reactive application that happens to have a UI.
That's where signals outside components, ownership, fine-grained derivation, async graph semantics, stores, and independent domain state all start reinforcing each other.
My gut says the trajectory looks something like:

```
small app

Octane  ██████████
Solid   █████████

         ↓ complexity

large/stateful app

Octane  ████████
Solid   ████████████

```
Not because Octane necessarily scales poorly, but because **Solid's abstraction seems closer to the actual problem being modeled** once state relationships get complicated.
### The pillar I'd be least confident about
**Escape hatches.**
Octane could easily end up winning there if its compiler makes effects, refs, subscriptions and integration code extraordinarily pleasant.
And **ecosystem interoperability could become an overwhelming Octane win** if their compatibility layer is genuinely broad and reliable rather than “we have adapters for the popular demos.”
### My strongest instincts
If I had to assign confidence rather than points:
- Solid strongly wins: state architecture, derived state, async, architectural scaling.
- Solid probably wins: reactive reasoning, escape hatches.
- Octane strongly wins: initial component authoring.
- Octane probably wins: ecosystem interoperability.
- Solid wins for now: tooling/maturity.
****
****
****
****
****

The biggest question I'd personally want answered before choosing between them is therefore not performance.
It's:
**Does Octane's compiler actually eliminate the architectural drawbacks of component-centric reactivity, or does it mostly make that model much nicer to write?**
If it's the latter, I'd expect Solid 2 to remain the stronger foundation for complex applications.

---

## 评论区（2026-08-14 ~ 2026-08-18，8 条，trueadm 与 ryansolid 的正面交锋）

> 以下为 gist 评论原文，按时间顺序。trueadm = Dominic Gannaway（Octane 作者，React 核心团队），ryansolid = Ryan Carniato（Solid 作者），aleclarson = 原帖作者。

### trueadm · 2026-08-14

Thanks for taking the time to write this up. I think it identifies the philosophical difference well, but I disagree with the 7–2 score and especially the small-app/large-app chart.

The main issue is that several pillars double-count the same preference: state architecture, reactive reasoning, derived state, and architectural scaling are largely different views of Solid's native reactive graph. Solid clearly wins if the criterion is “does the framework make a fine-grained graph the application's fundamental architecture?” It also has a real conceptual advantage in allowing async to compose through that graph.

But that does not establish an architectural-scaling win. React's component/hook model has already been proven at enormous scale. Octane deliberately preserves that programming model while removing dependency-array bookkeeping, call-order restrictions, virtual-DOM overhead, common stale-closure workarounds, and React-style async waterfalls. A large Octane application is also not required to put its domain state in components: `useSyncExternalStore` is a first-class, tearing-tested boundary, and there are Octane bindings for Zustand, Jotai, Redux, MobX, Valtio, TanStack Store, Alien Signals, and others. Domain state can live in an independent store or signal graph, with components acting as selected subscription/render boundaries.

So the answer to the final question is: the compiler mostly makes the component model substantially nicer and cheaper; it does not secretly turn hooks into a global Solid-style graph. But that is not a concession on scaling, because the underlying model already scales, and external stores remove “component gravity” where an application actually needs to.

A few other qualifications:

- Solid's graph is causal, but I would not call it unambiguously more explicit. Dependencies are dynamically captured through reads, and Solid 2 adds ownership, pending-state, transition, and flush semantics that also have to be understood. Octane is coarser, but “this hook/context/prop/selected snapshot caused this component to render” is often a very simple causal model.
- Solid deserves the native derived-state win for shared multi-stage graphs. Component-local derivation is a different comparison: ordinary values such as `const doubled = count * 2` are often simpler, and Octane automatically caches eligible derived declarations and render regions.
- The async section undersells Octane. Promise creations feeding `use()` are compiler-memoized; independent reads are stratified and batched into one suspension; and descendant fetch trees are warmed while an ancestor is suspended. Solid's async graph is deeper, but Octane is not merely React Suspense with nicer hook ergonomics: https://github.com/octanejs/octane/blob/main/docs/suspense-parallel-use-plan.md
- “React ecosystem compatibility” needs a precise caveat. Arbitrary already-compiled React components cannot simply rename imports and run on Octane. Octane reuses framework-neutral cores and ports thin React binding/component layers; `octane/react` hosts compiled Octane islands inside React. The growing binding catalog is here: https://github.com/octanejs/octane/blob/main/docs/bindings-status.md
- Solid wins tooling and maturity today. Octane is alpha. Solid 2 itself is an RC with a rewritten reactive core/compiler, though, so “battle-tested” applies more strongly to Solid's lineage and ecosystem than to every new 2.0 semantic.

My rough assessment would therefore be:

- **Solid:** native state architecture, complex shared derivation, first-class async.
- **Octane:** component authoring, React-ecosystem portability, architectural scaling.
- **Workload-dependent:** reactive reasoning and escape hatches.
- **Solid today:** tooling/maturity.

The central comparison is valuable; I just don't think “signals are closer to the problem” is evidence that component-oriented applications become architecturally weaker as they grow. React's history points strongly in the opposite direction.

### aleclarson · 2026-08-14

Hey @trueadm, I appreciate the response!

ChatGPT took your critique in stride and here's its response:

---

Thanks — this changes my view in a few important ways.

The double-counting criticism is fair. I was treating state architecture, reactive reasoning, derived state, and architectural scaling as independent evidence for Solid when several of them were really consequences of the same preference: making a fine-grained reactive graph fundamental to the programming model.

I also agree that I overreached on architectural scaling. A component-oriented renderer does not imply a component-oriented application architecture. If domain state can live cleanly in Valtio, MobX, Zustand, TanStack Store, signals, etc., with Octane components acting as subscription/render boundaries, then “component gravity” is much less of an architectural constraint than I implied. React proves that this general model can scale; that doesn't prove Octane wins scaling, but it removes my basis for giving Solid the win.

Your async explanation also substantially changes my impression. I had mentally categorized Octane as roughly “React Suspense semantics with much better ergonomics.” The compiler work around memoizing promise creation, stratifying independent reads, batching suspension, and warming descendant fetches is a much deeper attack on waterfalls than that characterization gives it credit for.

I think the comparison I’m left with is more interesting:

**Solid 2:** make dependencies—including async dependencies—part of an explicit reactive model, so coordination falls out of the semantics.

**Octane:** let developers write comparatively ordinary function/value/component code, then have the compiler recover enough dependency, caching, granularity, and concurrency information to produce similarly desirable behavior.

That also changes what I think the central DX question is. It’s less “which architecture scales?” and more:

**Which complexity do you want exposed to the programmer, and which complexity do you want inferred by the compiler?**

I’d now roughly score the original pillars as:

* Solid: native state architecture, complex shared derivation, async model, tooling/maturity today
* Octane: component authoring, ecosystem portability
* Workload-dependent: reactive reasoning, escape hatches
* Architectural scaling: I’d probably remove this as an independent pillar rather than award it to either

I still lean Solid for large shared reactive graphs because I like having those relationships represented directly in the programming model. But Octane makes the counterargument much stronger than “React, but faster”: perhaps an explicitly reactive application model is less necessary if a compiler can reliably recover most of its practical benefits from ordinary code.

That feels like the genuinely interesting Solid 2 vs Octane question to me now.

### ryansolid · 2026-08-17

Not going to lie. I had Fable write most of this response. This has been a genuinely good read though, and I think it is narrowing down on the critical distinctions.

------

The framing the thread ends on — "which complexity do you want exposed to the programmer, and which inferred by the compiler?" — treats the two as equivalent, just relocated. I'd argue they aren't. Exposed complexity is inspectable complexity. Inferred complexity doesn't disappear; it becomes invisible until it misbehaves, and then the answer to "why did this update?" lives somewhere you didn't write.

This is why I'd push back on filing observability under "tooling/maturity, Solid for now," as if it's a lead that erodes. In Solid the dependency graph isn't a mental model or a build-time artifact, it exists at runtime as a data structure. In dev you can walk any node's sources and observers, walk the ownership tree, and subscribe to a diagnostics stream where the system names problems precisely (a pending async value read outside a tracking scope, a reactive write in an owned scope, work scheduled on a disposed owner) because it knows exactly where every node sits. It can do that because dependencies are captured by actual reads as they happen — a conditional read produces exactly the edges that exist right now. Deriving dependencies from what a closure lexically captures, however good the inference, is a build-time answer to a runtime question. That's not a maturity gap; it's a difference in what the system knows while your app is running. And I'd argue runtime knowledge is getting more valuable, not less — it's the substrate devtools, tracing, and increasingly AI-assisted debugging stand on.

On async I'll actually cite Dominic's own planning doc. Octane inherits React's `use()` contract — a pending read throws and the body replays — and the compiler recovers parallelism by *proving* independence between fetches. The doc's own prior-art survey describes Solid as "parallel by model," and its benchmark target was reaching the parallel floor that Solid sits at by construction. Where the proof succeeds, great. But the doc is equally clear about where it can't: loops are excluded, dependent creations don't hoist, warm plans cut at any edge the compiler can't verify, and compiler-invisible promise shapes fall back to sequential behavior at runtime. "Warm less = slower but never wrong" is the right engineering call — but it means parallelism is an optimization whose applicability depends on whether your code's shape was provable, rather than a semantic you can rely on.

And the state itself stays opaque either way. When suspension is a thrown exception, "pending" isn't a value anyone can ask about — it's observable only as "this subtree stopped." In Solid 2, async status is data in the graph: `isPending` and `latest` are reads with real guarantees (`[isPending(x), x()]` observed together is atomic; a resolved value can never be observed as not-pending-yet-undefined), and pending-ness propagates through ordinary sync derivations of held values. That's what stale-while-refetch UIs, transitions, and optimistic updates are built out of — plain reactive primitives — and it's what lets tooling show *which* value is pending and what caused the refetch. Better-scheduled suspension is still suspension.

On the architectural-scaling concession: I think the external-store argument gives the point away rather than winning it. "Domain state lives in Zustand/MobX/Valtio with components as subscription boundaries" — sure, React proved that works. But look at what that boundary is: a knowledge boundary. Causality can't be traced through the external store, and the framework's async/pending/transition semantics stop at the snapshot edge — `useSyncExternalStore` prevents tearing precisely by coarsening to snapshots. The scaling story becomes two reactive systems stitched at a seam, and the hard coordination problems live exactly at the stitch. In Solid the store *is* the graph: a fetch flows through a store through a derivation into the specific binding it updates, and you can follow it — and query its pending state — the entire way. To me, "the fix for component gravity is a second reactive system" is evidence that fine-grained reactive state is what actually scales. The question is just whether it's native or bolted on.

Where I'll concede without a fight: day-one authoring. `const doubled = count * 2` reads better than `const doubled = () => count() * 2`, and Solid people shouldn't pretend otherwise. I'd only note what the trade buys: reads-as-function-calls is the entire interop protocol. Reactivity crosses any function boundary, any file, any third-party library, with no compiler cooperation and no provability requirements — and the value in your hand is never secretly stale.

So my version of the closing question: not "which complexity do you want inferred?" but "does the system's knowledge of your application survive to runtime — where you debug, where tools operate, and where behavior actually happens?" A compiler can approximate a lot from ordinary code, and Octane is the most serious attempt at that I've seen. But an approximation made at build time can't be interrogated at runtime, and I think that property — more than authoring ergonomics in either direction — is the one that compounds as applications get complex.

### trueadm · 2026-08-17

It's a good thread. Let me respond to that feedback though:

Octane is alpha, and this is exactly the kind of criticism that should help shape it.

Solid has a real advantage in making reactive relationships and async state part of one runtime model. I don’t think Octane should pretend that inferred dependency arrays or better-scheduled Suspense are the same thing.

My longterm bet, and this one I've had for a while from Ripple, is that a compiler-owned language can take substantially more responsibility for correctness, caching, scheduling, and state coordination than today’s React-shaped APIs suggest. We already use that approach for hook identity, dependency inference, derived-value caching, and independent async work. There is considerably more room to explore. However it's not always easy to convey this to the general audience too. There's been a lot of push back over compiler driven logic because it's still very new.

That does not mean the compiler gets to guess silently. Explicit dependency arrays remain authoritative today (you can opt into them when you think you need, them or LLM does) but generally they aren't needed for most cases. When the compiler analysis cannot establish something safely inferred, we need a clear contract, a conservative result, or an actionable error. We also need to explain what the compiler decided and connect that explanation to what happened at runtime (more work to do here though).

Increasingly agent-authored software changes which constraints are practical. An agent can handle a substantial refactor in response to a precise compiler diagnostic. That makes it more practical to reject patterns that are convenient locally but difficult to reason about globally. Humans still decide what the application should do; the compiler should make more of that intent enforceable.

`"use strong"` is an early step – it's a compiler feature for Octane that literally blocks things at compile time with no override (so not a linter where you can just ignore it). I wanted to explore a stronger world where manual `useMemo` and `useCallback`, etc are unnecessary, and `useEffect` is no longer the general-purpose mechanism for co-ordinating application state. Eventually, I would like strong application code to be able to prohibit all three. But that only works if we provide better primitives for derivation, actions, resources, subscriptions, and genuine external synchronisation. That's why we brought `useLinkedState`, added a third param to `useState` and have plans on `useAsyncExternalStore` to fix a whole category of issues there. Not only that, but we're deep in the cross-module compilation where we use TS native to determine props and types between components and modules, many levels deep, to avoid needing a dependency because we know it doesn't change. Literally, the work we're doing in compilation is beyond anything else that has happened since Prepack (I miss Prepack a lot).

Every restriction needs to buy a useful guarantee. Every removed API needs a better way to express its legitimate uses. And the resulting system needs to be understandable by people and agents when something goes wrong.

That experience is part of why I find this comparison interesting. Solid’s runtime graph offers real benefits, particularly around causality, shared derivation, and async state. I’ve worked on those ideas myself. Octane is a deliberate exploration of another part of the design space: how much responsibility can a compiler take while preserving ordinary values, familiar component authoring, and understandable runtime behaviour? I mean, I was the person that first invented the async idea for Svelte 5, and I'm glad it's made its way into Rich Harris's hands to implement and further improvised on and tuned by Ryan – that's why we do OSS.

I just find it kind of a weak one. It kind of feels like who can make a better garbage collector problem. I've had the experience of building a garbage collector in my engineering history and it's fascinating as, still today, no one has built the perfect one. That's because there isn't a perfect one. There also doesn't need to be a perfect one. There doesn't need to be a perfect async model either, the architecture and design of one doesn't mean we need one, having one is exciting, but then you'll also likely miss something later down the line and have even more frustration. I still have this with both Solid and Svelte 5's async design – you have a colouring problem when you don't know what signal is sync and what is async. The type-system doesn't tell you. The naming of the variable, property or method doesn't tell you – do you invent a $ suffix? Do you craft some internal logic that says "this might be an async signal", you just don't know. No one really knows – but a compiler, well that crafty thing is deterministic and it can know.

Anyway, like I said, Octane is still alpha. It's current React-shaped API is a useful starting point, but I don’t see it as the ceiling. As more software is written with agents, stronger language constraints become practical: the compiler can reject ambiguous patterns, explain what guarantee was violated, and give an agent a clear path to repair the code.

My experience gives me reasons to pursue this direction. It doesn’t exempt Octane from proving that it works.

I’m not claiming Octane has already solved all of that. I am saying its current React-shaped surface should not be mistaken for the limit of its ambition.

### ryansolid · 2026-08-17

We agree about a lot of things. And the cross-pollination is real — but I'd correct the lineage on the specific design you're critiquing. The purely colorless model — pending reads throw, value types stay clean, no marker anywhere — landed in our signals repo in August 2023, before runes were announced (we folded that repo into the monorepo, but the commits are all still there). Resources in Solid 1 pointed the direction but were nullable, so I won't claim more than we shipped — the fully colorless contract is the 2.0 work. What the Svelte conversations actually convinced me of was removing transitions, not the coloring approach. And notably, Svelte still doesn't have the colorless model today: `await` in a `$derived` or a template is the color, written right there in the source. This design is ours and very deliberate — which is exactly why I want to defend it properly.

Coloring is painful when color is static and viral — `async`/`await` recolors every caller in the chain. We erased the color at the read site instead. Every reactive read has one contract: it may not be ready, pending-ness propagates through derivation, and boundaries or `isPending`/`latest` absorb it wherever you actually care. The payoff is that asyncness isn't load-bearing in your code's structure — swap a sync signal for an async one and zero downstream code changes. Put it in the type system and that refactor goes viral again. Readiness as a dynamic, queryable property *is* our answer to coloring. And I'd gently note the compiler only "knows" inside its horizon — your own doc ships a runtime guard for promise shapes that escape the analysis through props and foreign modules. Deterministic where it can see; runtime fallback where it can't. Same boundary we're both living with, we just put the contract on different sides of it.

I'll also take the garbage collector analogy, because I think it points the other way. GCs won general-purpose memory management because the runtime owns the live object graph — reachability is a runtime property that static analysis provably can't recover. Every attempt to replace that with inference under familiar syntax (escape analysis, region inference) ended up as an optimization layered on a runtime system, never a substitute for it. The one static approach that genuinely worked, Rust, required a new, stricter language — and even Rust concedes the unprovable shapes back to the runtime: Rc, RefCell, Arc are all runtime mechanisms for exactly the cases the borrow checker can't see through. Static analysis where it can prove, runtime knowledge for the general case — that's the stable equilibrium in memory management, and I'd bet it's the stable equilibrium here. Which is, as far as I can tell, exactly what "use strong" is walking toward: a genuinely stricter language. I think that's a coherent, even exciting bet — but notice what it spends: the moment the compiler hard-rejects React habits with no override, "your React knowledge transfers" stops being the pitch. At that point we're both asking people to learn a new model, and the comparison becomes: where do the semantics live — in a specified runtime graph you can interrogate while the app runs, or in a compiler's analysis you trust and read diagnostics from? Your own list of remaining work ("explain what the compiler decided and connect that explanation to what happened at runtime") is that exact gap, described from the other side.

On agents we mostly agree, but the argument cuts both ways. Yes, agents make stricter compile-time contracts practical — they'll happily refactor against a precise diagnostic. They also make day-one authoring familiarity matter much less, and when they're debugging a *running* application they ask runtime questions: why is this pending, what is this transition waiting on, why did this update twice. A diagnostic explains what the compiler couldn't prove; it doesn't explain what the app just did. I don't think compile-time and runtime knowledge are rivals — we compile too, obviously. The difference is only what gets discarded before the app runs.

No perfect async model, agreed — that's not the claim. The claim is narrower: when the model inevitably misses something, I want the miss to be inspectable in a specified, running graph rather than reconstructed from generated output. That's the property I think compounds.

Genuinely looking forward to watching "use strong" evolve. If the endgame is that both of us abandon "familiar" as a value and compete on which new model earns its constraints — that's a much better framing than the one this thread started with.

### trueadm · 2026-08-17

Yeah, fair correction on the timeline. I was referring to the async work and discussions around Svelte, not claiming Solid’s colourless design came from me. I worded that badly, but I think you know what I meant anyway – actually you definitely do, we spoke about this on our podcast or Discord etc.

I also understand what you mean about every reactive read having the same contract. Being able to replace a synchronous source with an async one without rewriting everything downstream is valuable. I’m not suggesting you should put `Promise<T>` everywhere and bring that problem back. TBH my design for Svelte _was not this_, Rich changed it around originally, I literally pitched the same idea you had with `$derived` or I think at the time when I was on Svelte team it was `$async`. It was like a year ago now, who knows.

The distinction I was trying to get at is slightly different though. In ordinary JS, `const value = readValue()` gives me a value from that execution. A getter or a tracked derivation preserves a different relationship. Moving a read, passing its result instead of the getter, or calling it outside the right tracking scope can change the behaviour. The runtime might know exactly what happened, but that doesn't mean the distinction is obvious from the code or its value types. Async adds another question about where a read can prevent execution from continuing. I still think theres a real trade-off there, even when the reactive graph handles it correctly.

In the React "shaped" component model, the default is that calculations inside render run again. `const total = price * quantity` stays ordinary code. You then remove unnecessary work through memoisation, whether written manually or performed by the compiler. That doesn't make React free of snapshots or stale closures, obviously. But it is a different starting contract, and one I think is worth keeping.

You're right that I was too loose with the point about the compiler knowing. I don't mean it can see through arbitrary JS or predict every runtime branch. I mean we can define a language with stronger rules, establish more from those rules, and keep runtime behaviour or reject a pattern where the analysis ends. I want those semantics to be specified, rather than depending on whatever an optimisation happened to manage.

The Rust comparison is actually quite close to what I meant with `"use strong"`. Yes, it asks people to learn some new rules. I don't think that makes their React knowledge stop transferring, though. Components, props, state, composition, and a lot of existing application structure still make sense. Strong mode is opt-in today, and ordinary code and dependencies can keep their existing behaviour. Familiarity can be useful without being a promise to preserve every habit forever. TBH it doesn't really matter at all to agents, as asking them to adhere to new rules is hardly going to cause anyone to complain, and that goes back to my point in the prior comment.

You’re right about debugging, to some extent (unless I have got you wrong). If an agent is looking at a broken app, it needs evidence from what actually ran, a compiler error only gets you so far. Octane already exposes source-linked render causes, hook state, and transition/Suspense state, but it doesn’t yet give you the same view of causality as your graph. The missing part is connecting the compiler’s choices to what you can inspect at runtime. I think we can do that without making a fine-grained graph the model for everything. Plus we already have `octane-doctor`, devtools support is on the way. However, in real world practice, I think this area is going to be completely changed as agents become even more capable. I've already had a big issue debugged in realtime, in the compiled output of Octane debugged by an agent inserting `console.log` and it working, it fixed it. It didn't care for the compiled output being completely different from the user-code, it just worked great – thank you Codex and ChatGPT 5.6 Sol, which gets Octane so well in a very large codebase.

I suspect we agree on more than the earlier comments suggested. Agents make a new model easier to pick up, but they also make vague semantics easier to paper over, which isn’t good. Octane still has to prove that its extra constraints are worth it – which it will, I'm confident of that. The only useful answer to that is going to be in the implementation, not another round of analogies. Using `tsrx` has yielded so many benefits you wouldn't believe too, I can't really get into those details just yet, but believe me it's been transformative.

My push back is mostly – Solid 2.0 has been an exceptional launch, but don't use that as a reason to denounce Octane. I've got a strong hunch, a spider-sense almost that that I'm onto something equally as special Solid 2.0, except Octane might actually be the next big-thing (fucking finally). So that's why I never rained down on your celebration, because Solid is epic – you know me personally and I love your work Ryan. I never went on any of your threads on X, Reddit or whatever telling people to use Octane over Solid. So don't take what I say personally, we're just learning from one another, and that's healthy.

### ryansolid · 2026-08-18

This time no AI.

If I came off dismissive of Octane that isn't my intention. Especially not from a technology standpoint. The current push of AI forks I find distasteful given the effort it takes to create those libraries in the first place, but I wasn't grouping Octane in with them.

It is more that Ive been pushing back against React for over a decade now. Not React the implementation, but React the model. React the implementation has been poked at for years. But the model has had people feel secure despite what empirically was in front of them. It has taken a long time to gain any ground against its inertia.

So to me this is like OOP vs FP, or maybe closer to home immediate mode vs retained mode. I didn't enter the ring because of adoption, developer experience, or even performance, but a belief in a fundamentally better model. Obviously I acknowledge it isn't something so cut and dry. But it is why I focus on education and trends that span more than a single framework.

I don't doubt Octane is capable of everything you are setting out to accomplish. I think language/compiler is an important part of the authoring story even more so with AI. Solid just approaches the problem the way I always have with the view a compiler is a last stage optimization. We need to know what we are building first. It can be argued that maybe Svelte switched gears too quickly, but it is a textbook example of what Im talking about. They had the compiler but then they realized they had an incomplete model.

Solids track record of not changing is very much grounded in our approach. We didn't chase DX. And in that I think we have a lot in common with React. The prevalence of agents doesn't change those foundations of truth to me. Which is to say if you ask me what we should be building it isn't Reacts model. That foundation has had its chance and for the betterment of the ecosystem we need to explore different paths.

The compiler can come later. We're still catching up to the deficit of not having nearly as many people building on this model the past decade. The fact that we are still discovering concrete wins at runtime without a compiler I view as evidence this has more legs.  Far from solved. 

So if you hear me being critical here it is just rebelling against the calcification of Reacts core model. It has enough legacy as it is. I refuse to accept it and I will undermine it at every junction. Not out of malice or disrespect of the engineering that goes into solutions built on top of it, but because that is the foundation on which my work stands.

### trueadm · 2026-08-18

Thanks for clarifying Ryan. Like I said, it's all good.

I know you only have good intentions with your thinking and comments. I'm not trying to rain on your endeavours or your critical thinking into why React's model isn't the right one. We all know it's not right, I already tried and largely failed with trying to change that with Ripple. The community just have no appetite to adopt new frameworks anymore. I was having a chat with a very well known software engineer that used to work at Google the other month and he said that he was excited by Ripple but has no reason to move from React, because the migration path simply isn't worth it anymore. He can get an agent to fix the performance issue in React and it largely just works eventually.

I'm just a builder and tinkerer. Octane is an attempt for me to delve further down the path I first started on with Inferno all those years back. I feel like I left unfinished business on the table when I was working on the OG React Compiler – Prepack whilst at Facebook and this has been a nice change of scenery for me. If the migration story from moving from React to something a lot better is watertight, then just maybe it will move the needle, or at least their agent will tell them they should.

It's also crucial to point out here that signals play a major role in Octane too – just not as a first-class citizen just yet – they might though, but we first wanted to let people decide what to use and our recommendation has been to use Alien Signals or Jotai/Zustland if people are already using that in their React apps. `useState` is a good local state mechanic, but again, with "use strong" we can detect people using it in problematic ways and push people to use better state mechanics, such as signals, state machines or context.
