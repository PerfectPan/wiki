- [[fork]] 状态机复制包括持有的所有操作系统对象
- [[execve]] 重制状态机，但继承持有的所有操作系统对象
- 文件描述符指一个指向操作系统内对象的指针
	- 0，1，2 分别是 stdin，stdout，stderr
	- 通过 open 取得，close 释放，dup 复制
	- 对于数据文件，文件描述符会记住上次访问文件的地址
	- dup 的两个文件描述符是共享 offset
- 概念上状态机被复制了，但是实际上复制后的内存都是共享的，开始写入的时候才会复制，进程不持有页面，页面是由操作系统所持有的，提升 fork-execve 的效率，因此实际上统计进程占用的内存是一个伪命题
- 创造平行宇宙：
	- 搜索并行化，不用回溯，我们每次执行的方向都是唯一的，可以很快的探索完路径，不用等这条分支探索完了再接着探索。 按课上的说法，如果不断 fork 的话，可以在进行探索失败的时候，一步跳回原来 fork 的地方，会很快，不用像回溯那样一层一层的撤销状态，但是不断 fork 的话进程的销毁难道不是一个个销毁么？
		- ```c
		  void dfs(int x, int y) {
		    if (map[x][y] == DEST) {
		      display();
		    } else {
		      int nfork = 0;
		  
		      for (struct move *m = moves; m < moves + 4; m++) {
		        int x1 = x + m->x, y1 = y + m->y;
		        if (map[x1][y1] == DEST || map[x1][y1] == EMPTY) {
		          int pid = fork(); assert(pid >= 0);
		          if (pid == 0) { // map[][] copied
		            map[x][y] = m->ch;
		            dfs(x1, y1);
		            exit(0); // clobbered map[][] discarded
		          } else {
		            nfork++;
		            // 不等了
		            // waitpid(pid, NULL, 0); // wait here to serialize the search
		          }
		        }
		      }
		  
		      while (nfork--) wait(NULL);
		    }
		  }
		  
		  ```
	- 跳过初始化，如果初始化很长的话，可以再初始化结束后进行 fork，初始化的状态保留了，可以节省很多时间
		- Zygote Process(Android)
			- Java Virtual Machine 初始化涉及大量的类加载
			- 一次加载，全员使用
				- App 使用的系统资源
				- 基础类库
				- libc
				- ...
		- Chrome site isolation
		- Fork Server(AFL)
	- 备份和容错，有些 bug 可能调整一下环境就消失了
- 从操作系统的角度，fork 可能不是 API 的最佳选择，因为后来的操作系统增加了很多新的东西：信号，进程组，线程，进程间通信的对象等
- https://www.microsoft.com/en-us/research/uploads/prod/2019/04/fork-hotos19.pdf
-