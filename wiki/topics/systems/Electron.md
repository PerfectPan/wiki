---
title: Electron
type: topic
category: systems
status: seed
created: 2026-04-12
updated: 2026-04-25
tags:
  - electron
source_refs:
  - raw/sources/Electron.md
---
# Electron

- [electron-log](https://github.com/megahertz/electron-log) 这个包可以挂在 electron-updater 上去打印日志
- electron-updater 就是自己在本地起了个 server，然后把远程的先 down 下来，再调用内置的 updater 模块从这个 server 上去下载，免去开发者自己去维护一个 release server 的心智负担，这样只要有一个静态的文件托管平台就好
- 自定义协议除了安装时注册，也可以在运行时检查当前协议头是否仍然指向自己；如果被别的应用覆盖，可以在应用启动后重新注册回来
- `open-url` 事件早于 `ready`，因此第一次通过自定义协议拉起时，需要先缓存 URL 参数，等应用初始化完成后再消费；Windows 首次通过协议打开时，也可以直接从 `process.argv` 读取 URL
- Electron 自动更新在“下载完成但重启后还是老版本”这类问题上，不要只盯下载链路；macOS 上还要检查 `~/Library/Caches/${your app id}.Shipit/stderr.log`，常见失败点是安装阶段因为只读文件或移除 quarantine 属性失败而回滚
- [https://juejin.cn/post/7035494774899474468](https://juejin.cn/post/6968254840275206174) [[快捷键]]相关实践
- [[Node]] Native 模块编译失败 issue：https://github.com/electron/electron/issues/35193
- NODE_MODULE_VERSION https://newsn.net/say/electron-node-module-version.html
- asar 文件在生成的时候会包含每个文件的信息，包括是否被 exclude 掉了，然后 Electron 实际在读取的时候会根据这个信息去决定要在哪里读，所以如果你这个文件一开始没有被放进去，在 asar 结束以后去拷贝或者生成啥的，在运行时的时候是会报错的，因为就没有这个文件信息
- TODO asar 和 ttpkg 博客
- ```js
  // Windows 上隐藏菜单栏
  this.browserWindow.setMenu(null);
  ```

## Source Pointers

- `raw/sources/Electron.md`
