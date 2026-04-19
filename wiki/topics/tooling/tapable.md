---
title: tapable
type: topic
category: tooling
status: seed
created: 2026-04-12
updated: 2026-04-12
tags:
  - tapable
source_refs:
  - raw/sources/tapable.md
---
# tapable

- #frontend
- https://github.com/webpack/tapable/tree/master
- 动态生成函数的一些依据：https://mrale.ph/blog/2015/01/11/whats-up-with-monomorphism.html
- https://github.com/webpack/tapable/issues/62
- 本质就是个事件订阅器，具备异步同步，还有熔断，waterfall 等种类，
- https://juejin.cn/post/7097881373754687525
- https://juejin.cn/post/7040982789650382855#heading-25
- 实际到 .call | .callAsync 的时候才会根据注册的事件去动态 gen 一个函数，并且如果注册的事件没有变化不会重新 gen
- Async 类的都会补充一个 callback 函数，作为异步的桥接，类似于 [[Node]] 的 callback 机制
- 之所以要标明 name 还有参数列表，应该就是为了动态生成函数用的，不过 https://juejin.cn/post/7097881373754687525 这篇文章貌似已经证伪了，这样并没有多快，可能是因为 V8 性能优化的越来越好了 https://github.com/lizuncong/mini-tapable
- tapAsync 理论上需要自己处理好[[异步]]的捕获，不然会有 unHandledPromiseRejection 的问题
- ```js
  // Sync .call 生成
  function anonymous(name) {
    "use strict";
    var _context;
    var _x = this._x;
    var _fn0 = _x[0];
    _fn0(name);
    var _fn1 = _x[1];
    _fn1(name);
  }

  // Sync .callAsync 生成
  function anonymous(name, _callback
  ) {
    "use strict";
    var _context;
    var _x = this._x;
    var _fn0 = _x[0];
    var _hasError0 = false;
    try {
      _fn0(name);
    } catch(_err) {
      _hasError0 = true;
      _callback(_err);
    }
    if(!_hasError0) {
      var _fn1 = _x[1];
      var _hasError1 = false;
  	try {
  	  _fn1(name);
  	} catch(_err) {
  	  _hasError1 = true;
  	  _callback(_err);
  	}
  	if(!_hasError1) {
  		_callback();
  	}
    }
  }

  // Async .callAsync 生成
  function anonymous(zzm, zzm2, _callback) {
    "use strict";
    var _context;
    var _x = this._x;
    function _next0() {
      var _fn1 = _x[1];
  	_fn1(zzm, zzm2, (function(_err1) {
  	  if(_err1) {
  	    _callback(_err1);
  	  } else {
  		_callback();
  	  }
  	}));
    }
    var _fn0 = _x[0];
    _fn0(zzm, zzm2, (function(_err0) {
      if(_err0) {
  	  _callback(_err0);
  	} else {
  	  _next0();
  	}
    }));
  }

  ```

## Source Pointers

- `raw/sources/tapable.md`
