- 共享内存的互斥
	- 理解并发的工具：
		- 线程 = 人
		- 共享内存 = 物理世界
		- 一切都是状态机
		- 互斥：
		  
		  实现 lock_t 数据结构和 lock/unlock API
		  
		  ```c
		  typedef struct {
		  ...
		  } lock_t;
		  
		  void lock(lock_t = lk);
		  void unlock(lock_t = lk);
		  ```
		  
		  一把排他性的锁，对于 lk，如果某个线程持有锁，则其他线程的 lock 不能返回
		  
		  **实现互斥的根本困难：不能同时读 / 写共享内存**
		  
		  load 看到的东西马上就过时了
		  
		  store 只能闭着眼睛动手，也不知道把什么改成了什么
- 自旋锁（线程直接共享 locked）
	- 改变假设 - 假设硬件能为我们提供一条瞬间读写的指令
	- 用 xchg 指令实现互斥（原子的交换变量）
	- 先交换钥匙，得到钥匙的人才能进营业区
	- ```c
	  int table = YES;
	  
	  void lock() {
	  retry:
	    int got = xchg(&table, NOPE);
	    if (got == NOPE) {
	      goto retry;
	  }
	  assert(got == YES);
	  }
	  
	  void unlock() {
	  xchg(table, YES);
	  }
	  ```
	- 自旋会触发处理器间的缓存同步，延迟增加
	- 除了进入临界区的线程，其他处理器上的线程都在空转
	- ```c
	  int table = YES;
	  
	  void lock() {
	  retry:
	    int got = xchg(&table, NOPE);
	    if (got == NOPE) {
	      goto retry;
	    }
	    assert(got == YES);
	  }
	  
	  void unlock() {
	    xchg(table, YES);
	  }
	  ```
- 操作系统不感知线程在做什么
- 单进程多线程会实现 100% 的资源浪费（？一个线程被切到后台了永远不执行释放锁的操作）
- 临界区几乎不拥堵（抢锁的人很少）2. 持有自旋锁时禁止执行流切换（就是上面说的线程被切换到后台）
  
  使用场景：操作系统内核的并发数据结构（短临界区）
  
  操作系统可以关闭中断和抢占 - 保证锁的持有者在很短的时间内可以释放锁
  
  虚拟机？ - PAUSE 指令会触发 VM exit
  
  但依然会有很多问题
  
  <aside> 💡 更快的 fast path: xchg 成功 → 立刻进入临界区，开销很小 更慢的 slow path: xchg 失败 → 浪费 CPU 自旋等待
  
  </aside>
- 互斥锁（通过系统调用访问 locked）
	- Scalability: 同一份计算任务，时间（CPU Cycle）和空间（mapped memory）会随处理器数量的增长而变化
	- Benchmarking crimes 做对比的时候需要考虑这个 CPU 的动态功耗
	- **线程 + 长临界区的互斥：**
		- 把自己的 CPU 让给其他线程执行不是 C 语言可以做到的，C 代码只能进行计算
		- 把锁的实现放在操作系统 → 一个 syscall 如果获取锁失败就会切换到其他线程
		- 释放锁 → 如果有等待锁的线程就唤醒
		-
		- 操作系统 = 更衣管理员
	- 先到的人（线程下）
		- 成功获得手环，进入游泳馆
		- *lk = 🔒，系统调用直接返回
	- 后到的人（线程）
		- 不能进入，排队等待
		- 线程放入等待队列，执行线程切换 yield
	- 洗完澡出来的人（线程）
		- 交还手环给管理员，管理员把手环交给排队的人
		- 等待队列不空，就取出一个线程允许执行
		- 等待队列为空就不管
		- 管理员使用自旋锁确保自己处理手环的过程是原子的
		  
		  <aside> 💡 更快的 slow path：上锁失败线程不再占用 CPU 更慢的 fast path：即使上锁成功也需要进出内核（syscall）
		  
		  </aside>
# Futex: Fast User muTexes

Futex = spin + mutex
- Fast Path: 一条原子指令，上锁成功立即返回
- Slow Path: 上锁失败，执行系统调用睡眠
- 性能优化常见技巧（跟算法求解考虑最差情况不同，也是工程考虑的，让大部分情况 work 就行）
- 看 avg case 而不是 worst case
  
  找到你依赖的假设并打破它
- 软件不够，硬件来凑（自旋锁）
- 用户不够，内核来凑（互斥锁）
- Fast path / Slow path 是性能优化的重要途径