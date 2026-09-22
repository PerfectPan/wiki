# 2026-09-22 Thrift Binary 线格式与 RPC 框架分层动手实验

## 实验对象

- Apache Thrift Binary protocol（线格式规范）：<https://github.com/apache/thrift/blob/master/doc/specs/thrift-binary-protocol.md>
- 开源 RPC 框架 CloudWeGo Kitex：<https://github.com/cloudwego/kitex>
- 其配套生成器 thriftgo：<https://github.com/cloudwego/thriftgo>

## IDL

```thrift
struct PingRequest {
    1: required string Msg
}
struct PingResponse {
    1: required string Msg
}
service PingPongService {
    PingResponse Ping(1: PingRequest req)
}
```

thriftgo 为每个方法额外生成两个包装结构（方法调用被建模成 struct）：

```
PingPongServicePingArgs   { 1: PingRequest req }
PingPongServicePingResult { 0: PingResponse success }
```

## 实测一：线上字节（framed transport + strict binary message）

对 `Ping(PingRequest{Msg:"hi"})`，实际在 TCP 上抓到 34 字节：

```
00 00 00 1e
80 01 00 01  00 00 00 04  50 69 6e 67  00 00 00 01
0c 00 01  0b 00 01  00 00 00 02  68 69  00  00
```

分段：

- `00 00 00 1e`：framed transport 的 4 字节大端 payload 长度，0x1e = 30。
- `80 01 00 01`：strict message 头，高 16 位 `0x8001` 是 version 1 标记，低 8 位 `01` 是消息类型 CALL（REPLY=2，EXCEPTION=3）。
- `00 00 00 04 50 69 6e 67`：方法名长度 4 + "Ping"。
- `00 00 00 01`：seqid = 1。
- body：
  - `0c 00 01`：type=12(STRUCT)，field id=1（args.req）。
  - `0b 00 01`：type=11(STRING)，field id=1（PingRequest.Msg）。
  - `00 00 00 02 68 69`：字符串长度 2 + "hi"。
  - 两个 `00`：内层 struct 与 args struct 各自的 STOP。

## 实测二：零依赖复现

不依赖任何 RPC 库，仅按 Thrift Binary 规范手写编码（大端 + type/id/value 规则），输出与抓包逐字节一致：

```
body  (14 bytes): 0c 00 01 0b 00 01 00 00 00 02 68 69 00 00
msg   (30 bytes): 80 01 00 01 00 00 00 04 50 69 6e 67 00 00 00 01 0c 00 01 0b 00 01 00 00 00 02 68 69 00 00
frame (34 bytes): 00 00 00 1e 80 01 00 01 00 00 00 04 50 69 6e 67 00 00 00 01 0c 00 01 0b 00 01 00 00 00 02 68 69 00 00
```

结论：线格式只由 Apache Thrift 规范决定，与具体框架运行时无关；任何兼容实现必须产出相同字节。

## 实测三：信封由运行时库函数写，body 由生成代码写

开源 Kitex v0.16.3 的 fast codec 路径 `pkg/remote/codec/thrift/codec_fast.go`：

```go
func fastMarshal(out bufiox.Writer, methodName string, msgType remote.MessageType, seqID int32, msg thrift.FastCodec) error {
    msgBeginLen := thrift.Binary.MessageBeginLength(methodName)
    buf, _ := out.Malloc(msgBeginLen + msg.BLength())
    offset := thrift.Binary.WriteMessageBegin(buf, methodName, thrift.TMessageType(msgType), seqID) // 信封：运行时通用库
    _ = msg.FastWriteNocopy(buf[offset:], nw)                                                        // body：生成代码
}
```

同目录并列三种 body 编码实现，信封写法在三者中相同：

- `codec_fast.go`：调生成的 `FastWrite/FastRead`；
- `codec_frugal.go`：frugal JIT 编码，不需要生成代码；
- `codec_apache.go`：经典 apache `TProtocol` 慢路径，用于兼容。

生成的每方法 client 代码只剩一行统一入口（概念形态）：

```go
func (p *kClient) Ping(ctx, req) (resp, err) {
    var _args = &PingArgs{Req: req}
    var _result = &PingResult{}
    err = p.c.Call(ctx, "Ping", _args, _result)
    return _result.GetSuccess(), nil
}
```

## 备注

- 实验中框架在缺少服务发现后端的本地环境运行，治理类组件（配置中心、metrics agent）连接失败只产生告警，RPC 主链路靠静态地址直连照常完成。
- 本记录只包含开源组件与公开协议事实。
