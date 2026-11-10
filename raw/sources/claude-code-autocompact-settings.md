<!--
source: https://zenn.dev/zozotech/articles/1a26d1775c06f7
type: blog
fetched: 2026-11-10
-->

# [株式会社ZOZO](/p/zozotech)[株式会社ZOZO](/p/zozotech)[Publicationへの投稿](/faq/what-is-publication)🗜️Claude Codeの自動コンパクト、何で・どこで・いつ効かせるか（/autocompact・autoCompactWindow・idle
[さっと](/satto_sann)2026/10/15に公開[Claude Code](/topics/claudecode)[contextwindow](/topics/contextwindow)[compaction](/topics/compaction)[autocompact](/topics/autocompact)[tech](/tech-or-idea)
## 概要
Claude Codeは、会話がコンテキストウィンドウの上限に近づくと、古い履歴を要約して空きを作ります。この仕組みを自動コンパクト（auto-compaction）と呼びます。
これまでは、settings.jsonのenvにCLAUDE_AUTOCOMPACT_PCT_OVERRIDEを書いてパーセンテージを指定するだけで済ませていました。v2.1.288〜v2.1.300のリリースノートを読み返したところ、コンパクトまわりの設定がかなり増えていました。トークン数でしきい値を指定する/autocompactはモデルごとに値を保存するようになり、サブエージェント単位のautoCompactWindowと、放置中の会話を要約するアイドル時コンパクトも追加されています。
この記事では、これらの設定を「何で（単位）」「どこで（対象）」「いつ（タイミング）」の3つの観点で整理します。
## 前提
この記事はClaude Code v2.1.300時点の情報です。公式ドキュメントの[Model configuration](https://code.claude.com/docs/en/model-config)、[Settings reference](https://code.claude.com/docs/en/settings-reference)、[Environment variables](https://code.claude.com/docs/en/env-vars)と、公式CHANGELOGをもとに書いています。
説明では1Mコンテキストのモデルを使う前提とし、例としてOpus 5.5を使います。1Mのモデルとしてドキュメントに挙がっているのは、Opus 4.7以降、Sonnet 5以降、Haiku 5.5、Fableです。
## 先に結論
自動コンパクトのタイミングを早めたい場合は、まず/autocompactでトークン数を指定するのがおすすめです。

```
> /autocompact 500k

```
このコマンドを実行すると、今使っているモデルでは会話が500Kトークンに達した時点でコンパクトされます。値はユーザー設定に保存されるので、次のセッション以降にも引き継がれます。元に戻すときは/autocompact autoを実行してください。
設定方法の全体像は次の表の通りです。

| 設定方法 | 単位 | 対象 | 有効期間 | バージョン |
| --- | --- | --- | --- | --- |
| /autocompact 500k | トークン数 | 今のモデルのメイン会話 | 保存され、以降のセッションでも有効 | v2.1.288以降はモデルごとに保存 |
| settings.jsonの"autoCompactWindow": 500000 | トークン数 | 全モデルのメイン会話 | 設定ファイルに書いてある間 | - |
| claude --autocompact 500k | トークン数 | その起動のメイン会話 | その起動の間だけ | - |
| 環境変数CLAUDE_CODE_AUTO_COMPACT_WINDOW=500000 | トークン数 | メイン会話とサブエージェント | 環境変数が設定されている間 | - |
| サブエージェントのfrontmatterのautoCompactWindow: 200000 | トークン数 | そのサブエージェント | 定義ファイルに書いてある間 | v2.1.296以降 |
| 環境変数CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=70 | パーセンテージ | メイン会話とサブエージェント | 環境変数が設定されている間 | - |
| settings.jsonの"idleCompaction" | 放置時間 | ターミナルの対話セッション | デフォルトで有効 | v2.1.299で告知、キーはv2.1.290以降で認識 |

``

``

``

``

``

``

``

以降で、それぞれを順に解説します。
## 背景：デフォルトではいつコンパクトされるのか
何も設定しない場合、Claude Codeはモデルのコンテキスト上限に達した時点で会話をコンパクトします。ただし1Mのモデルは例外で、コンパクトが走るのは上限の少し手前の約967Kトークンです。
つまりOpus 5.5のような1Mのモデルでは、何も設定しなければ1M近くまで会話が溜まります。もっと早い段階で要約させたいときに、以降で紹介する設定を使います。
## 何で：トークン数かパーセンテージか
### トークン数で指定する（auto-compact window）
コンパクトが発動するしきい値の、ドキュメントでの呼び名はauto-compact windowです。指定できる範囲は100K〜1Mトークンです。モデルのコンテキストウィンドウより大きい値を指定した場合、Claude Codeはそのモデルの上限を使います。
受け付ける書式は設定場所ごとに違います。500Kを指定するつもりで書いた値が、どう解釈されるかをまとめました。

| 設定場所 | 500k | 500000 | 500 |
| --- | --- | --- | --- |
| /autocompact、--autocompact | 500K | 500K | 500K（千単位として解釈） |
| settings.jsonのautoCompactWindow | JSONの数値として書けない | 500K | 範囲外 |
| 環境変数CLAUDE_CODE_AUTO_COMPACT_WINDOW | 500と解釈され、最小値の100Kに丸められる | 500K | 100Kに丸められる |
| サブエージェントのfrontmatter | 500と解釈され、範囲外のため無視される | 500K | 範囲外のため無視される |

``
``
``

````

``

``

コマンドと同じ感覚で環境変数に500kと書くと、会話が100Kに達するたびにコンパクトされます。コマンドとフラグ以外では、500000のように整数で書いてください。
### パーセンテージで指定する（CLAUDE_AUTOCOMPACT_PCT_OVERRIDE）
CLAUDE_AUTOCOMPACT_PCT_OVERRIDEは以前からある環境変数で、settings.jsonのenvに"70"を設定して使っていました。ドキュメントを読み直すと、この変数には3つの制約がありました。
値はauto-compact windowに対する割合として扱われます。しきい値を下げることしかできず、デフォルトの割合より大きい値は無視されます。また、1Mのモデルのように上限より手前でコンパクトするセッションでしか効果がありません。
トークン数の指定と組み合わせることもできます。ただし組み合わせると、何トークンでコンパクトされるかは計算しないとわかりません。これから設定するなら、トークン数で直接指定するほうがわかりやすいと思います。
## どこで：メイン会話とサブエージェント
### メイン会話の優先順位
トークン数の指定が複数ある場合、最も優先されるのは環境変数CLAUDE_CODE_AUTO_COMPACT_WINDOWです。この変数が設定されている間は、/autocompactを実行しても値は変わらず、環境変数で上書きされていることが表示されます。次に起動時の--autocompactフラグが優先され、その次がsettings.jsonの値です。
settings.jsonの値の決まり方は2段階です。まず、managed、local、project、userといった設定スコープの優先順位で、どのファイルの値を使うかが決まります。同じファイルの中では、modelSettingsに保存されたモデルごとのautoCompactWindowが、トップレベルのautoCompactWindowより優先されます。/autocompactが書き込むのは、ユーザー設定のモデルごとの値です。
そのため、managed settingsで値が決められている環境では、/autocompactを実行しても値が保存されるだけで、セッションには反映されません。その場合はコマンドの実行結果にその旨が表示されます。--autocompactフラグはmanaged settingsより優先されるので、1回の起動だけ値を変えたいときはフラグを使えます。
v2.1.288より前の/autocompactは、モデルを区別せず、トップレベルのautoCompactWindowに値を1つだけ保存していました。古い記事を参考にするときは、この違いに注意してください。
### サブエージェント（v2.1.296以降）
長いログファイルを読むサブエージェントなど、特定のサブエージェントだけ早めにコンパクトさせたい場合は、frontmatterにautoCompactWindowを書きます。

```
---
name: log-reader
description: 長いログファイルを読んで要約する
autoCompactWindow: 200000
---

```
この値は、メイン会話から引き継ぐしきい値より小さくしないと効果がありません。コンパクトを遅らせる目的には使えません。環境変数CLAUDE_CODE_AUTO_COMPACT_WINDOWが設定されている場合、サブエージェントは環境変数の値を使い、frontmatterの値は無視されます。
frontmatterの値が無視されたかどうかを確認したい場合は、claude --debugで起動し、デバッグログでinvalid autoCompactWindowを検索してください。なお、CLAUDE_AUTOCOMPACT_PCT_OVERRIDEはサブエージェントにも適用されます。
## いつ：アイドル時コンパクト
アイドル時コンパクトは、v2.1.299のCHANGELOGで新機能として告知されました。
1時間のプロンプトキャッシュを使っている会話の場合、キャッシュの有効期限は最後のリクエストから1時間です。その後に次のメッセージを送ると、Claude Codeは会話全体をキャッシュなしで処理し直します。アイドル時コンパクトは、キャッシュが切れる直前に会話を要約しておき、戻ってきたときに処理し直す量を減らす機能です。
発動するには、次の条件をすべて満たす必要があります。
- 対話モードのターミナルセッションである
- 1時間のプロンプトキャッシュを使っている
- Claude CodeがAnthropicからfeature flagsを取得できる
- コンテキストが200Kトークン以上ある
- 最後のリクエストから約54分経っていて、その時点でPCがスリープしていない
発動した場合は、戻ってきたときにCompacted while idle, before the prompt cache expiredと表示されます。
アイドル時コンパクトはデフォルトで有効です。無効にする場合は、settings.jsonに次の設定を追加してください。

```
{
  "idleCompaction": false
}

```
発動するトークン数は、環境変数CLAUDE_CODE_IDLE_COMPACT_MIN_TOKENSで変更できます。デフォルトは200Kで、100Kより小さい値は100Kに引き上げられます。

```
{
  "env": {
    "CLAUDE_CODE_IDLE_COMPACT_MIN_TOKENS": "300000"
  }
}

```
idleCompactionキーとCLAUDE_CODE_IDLE_COMPACT_MIN_TOKENSを認識するのは、v2.1.290以降のバージョンです。それより前のバージョンはidleCompactionキーを無視するので、アイドル時コンパクトを止めるにはautoCompactEnabledをfalseにする必要があります。
また、"autoCompactEnabled": falseか環境変数DISABLE_AUTO_COMPACT=1で自動コンパクトを止めると、アイドル時コンパクトも止まります。
## 注意点：statusLineの使用率とコンパクトのタイミングはずれる
以前の記事「[Claude CodeのstatusLineのすゝめ](https://zenn.dev/satto_sann/articles/cb767af383bc78)」では、statusLineにコンテキスト使用率context_window.used_percentageを表示する方法を紹介しました。
ドキュメントによると、**used_percentageは常にモデルのコンテキストウィンドウ全体に対する割合**です。auto-compact windowを小さくしても、その値に対する割合には変わりません。
たとえばOpus 5.5でauto-compact windowを500Kにすると、statusLineの使用率が50%前後のときにコンパクトが走ります。表示がまだ半分でもコンパクトされるので、使用率だけを見てコンパクトのタイミングを判断しないようにしてください。
v2.1.300では、/autocompactで小さいウィンドウを選んだときに表示される、トークン使用量の警告に関する不具合が修正されています。
## 手元の設定
今のところ、settings.jsonのenvにあるCLAUDE_AUTOCOMPACT_PCT_OVERRIDEの"70"を残し、autoCompactWindowはデフォルトのままにしています。アイドル時コンパクトもデフォルトの有効のままです。
今回、試しにOpus 5.5で/autocompact 200kを実行しました。~/.claude/settings.jsonのmodelSettingsに、モデルIDごとの値が保存されます。

```
{
  "modelSettings": {
    "claude-opus-5-5": {
      "autoCompactWindow": 200000
    }
  }
}

```
引数なしで/autocompactを実行すると、現在の値とその出どころが表示されます。今どの設定が使われているかを確かめるときに便利です。

```
> /autocompact
Auto-compact window for Opus 5.5 unchanged: 1m tokens (default for this model)

> /autocompact
Auto-compact window for Opus 5.5 unchanged: 200k tokens (from settings)

```
/autocompact autoで元に戻すと、キーは削除されずに"autoCompactWindow": "auto"が書き込まれます。settings.jsonを手で管理している方は、この行が残ることを覚えておくとよいと思います。
## まとめ
Claude Codeの自動コンパクトは、ここ数バージョンで、トークン数、モデル、サブエージェント、放置時間の単位で設定できるようになりました。
タイミングを早めたい場合は、まず/autocompactでトークン数を指定するのが手軽です。環境変数とサブエージェントのfrontmatterには、500kではなく500000のように整数で書く必要があります。長い会話を放置した場合は、デフォルトで有効なアイドル時コンパクトが、キャッシュが切れる前に会話を要約します。statusLineに表示される使用率はコンテキスト全体に対する割合なので、コンパクトのしきい値とは一致しません。
コンテキストの溜めすぎもコンパクトのしすぎも避けたい方の参考になれば幸いです。
[さっと](/satto_sann)ECサイトの検索機能を開発するエンジニア
触っている技術：Dify、LangChain、Elasticsearch
[株式会社ZOZO](/p/zozotech)[Publication](/faq/what-is-publication)ファッションEC「ZOZOTOWN」、ファッションコーディネートアプリ「WEAR」などの各種サービスの企画・開発・運営や、「ZOZOSUIT」「ZOZOMAT」「ZOZOGLASS」などの計測テクノロジーの開発・活用をおこなっています。また、カスタマーサポート、物流拠点「ZOZOBASE」を運営しています。
バッジを贈って著者を応援しようバッジを受け取った著者にはZennから現金やAmazonギフトカードが還元されます。
### バッジを贈るDiscussion
[さっと](/satto_sann)ECサイトの検索機能を開発するエンジニア
触っている技術：Dify、LangChain、Elasticsearch
1. 概要
1. 前提
1. 先に結論
1. 背景：デフォルトではいつコンパクトされるのか
  1. トークン数で指定する（auto-compact window）
  1. パーセンテージで指定する（CLAUDE_AUTOCOMPACT_PCT_OVERRIDE）
  1. メイン会話の優先順位
  1. サブエージェント（v2.1.296以降）
1. いつ：アイドル時コンパクト
1. 注意点：statusLineの使用率とコンパクトのタイミングはずれる
1. 手元の設定
1. まとめ
