- 副作用在顶层定义，结束后交还控制权
- 可以跨调用栈获取当前 Continuation
- 可以替换当前 Continuation 内 Effect 的实现
- 实验性质的库：
	- https://github.com/koka-ts/koka?tab=readme-ov-file
- 之所以说 [[React]] 也是一种 Algebraic Effects 是因为 React 内置 hook 是对 React 组件里副作用的抽象, 注册的 callback 则是该组件副作用的实现.
-
- https://overreacted.io/algebraic-effects-for-the-rest-of-us/
	- 当我们抛出一个异常的时候，执行引擎会摧毁所有上层调用栈以及其中的局部变量（「回卷（unwind）」）；但是当我们执行一个效应时，虚构的引擎会创建一个回调函数，这个回调函数的函数体是正在执行的函数体的剩余部分，并且在我们执行`resume with`时执行这个回调函数。
	- 可以把「做什么」和「怎么做」完全分离。
		- 它可以让你写代码的时候先把注意力都放在「做什么」上：
			- ```js
			  function enumerateFiles(dir) {
			    const contents = perform OpenDirectory(dir);
			    perform Log('Enumerating files in ', dir);
			    for (let file of contents.files) {
			      perform HandleFile(file);
			    }
			    perform Log('Enumerating subdirectories in ', dir);
			    for (let directory of contents.dir) {
			      // 我们可以递归或者调用别的有效应的函数
			      enumerateFiles(directory);
			    }
			    perform Log('Done');
			  }
			  ```
		- 然后再把上面的代码用「怎么做」包裹起来：
			- ```js
			  let files = [];
			  try {
			    enumerateFiles('C:\\');
			  } handle (effect) {
			    if (effect instanceof Log) {
			      myLoggingLibrary.log(effect.message);
			      resume;
			    } else if (effect instanceof OpenDirectory) {
			      myFileSystemImpl.openDir(effect.dirName, (contents) => {
			        resume with contents;
			      });
			    } else if (effect instanceof HandleFile) {
			      files.push(effect.fileName);
			      resume;
			    }
			  }
			  // `files`数组里现在有所有的文件了
			  ```
	- 代数效应同样允许我们不用写太多脚手架代码就能把业务逻辑和实现它的效应的具体代码分离开。比如说，我们可以在测试中用一个伪造的文件系统和日志系统来代替上面的生产环境