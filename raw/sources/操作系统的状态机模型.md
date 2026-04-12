- 经典研究论文 (OSDI, SOSP, ATC, EuroSys, ...)
- 久经考验的经典教学材料 (xv6, OSTEP, CSAPP, ...)
- 海量的开源工具 (GNU 系列, qemu, gdb, ...)
- 第三方资料，慎用 (tutorials, osdev wiki, ...)
- https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html
- 为了让计算机能够运行任何我们的程序，一定存在软件/硬件的约定
	- CPU Reset 以后，处理器处于某个确定的状态
		- PC 指针一般指向一段 memory-mapped ROM
		- ROM 存储了厂商提供的 firmware（固件）
		- 处理器的大部分特性处于关闭的状态
			- 缓存、虚拟存储、...
	- Firmware(固件，厂商提供的代码)
		- 主板/主板上外插设备的软件抽象
		- 将用户数据加载到内存
			- 直接加载操作系统（嵌入式系统）
			- 存储介质上的第二级 loader（加载器）
		- 可以放置一些「绝对安全的代码」，比如 BIOS 终端，ARM Trusted Firmware
- Reset 以后从 PC 指针处取指令、译码、执行...
- Firmware: BIOS，UEFI（联合制定了标准，易于扩展）
- Legacy BIOS 把第一个可引导设备（Boot Loader）的第一个扇区加载到物理内存的 7c00 位置
	- 此时处理器仍处于 16-bit 的模式
- 代码直接存在于硬件，CPU Reset 后 Firmware 执行，加载 512 字节到内存（Legacy Boot），然后功成身退，Boot Loader 再继续执行把操作系统加载到内存中
- [[Linux]]
- https://consen.github.io/2018/01/17/debug-linux-kernel-with-qemu-and-gdb/
- https://mgalgs.io/2015/05/16/how-to-build-a-custom-linux-kernel-for-qemu-2015-edition.html
- https://wiki.gentoo.org/wiki/Custom_Initramfs
- https://www.kernel.org/doc/html/latest/dev-tools/gdb-kernel-debugging.html
- ```sh
  qemu-system-x86_64 -S -s -drive format=raw,file=amgame-x86_64-qemu
  
  # 再起一个 shell
  gdb amgame-x86_64-qemu
  target remote localhost:1234 # 远程连接到 qemu
  
  ```
- ![CleanShot 2023-01-22 at 22.16.09@2x.png](../assets/CleanShot_2023-01-22_at_22.16.09@2x_1674396977371_0.png)
-