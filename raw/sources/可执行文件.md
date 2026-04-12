- https://refspecs.linuxbase.org/
- 描述了状态机的初始状态 + 转移的数据结构
- 常见的可执行文件：
	- Windows 95 / NT+, UEFI
		- PE(Portable Executable), since Windows 95 / NT+
	- UNIX / Linux
		- a.out
		- ELF(Executable Linkable Format)
		- She-bang
			- 偷换参数的 execve
- Binary Utilities：
	- 生成可执行文件：ld, as, ar, ranlib
	- 分析可执行文件：objcopy, objdump, readelf, addr2line, size, nm
- 运行时分析可执行文件的状态
	- gcc (-static -g)
	- 类似 [[SourceMap]] 将 assembly 状态映射到「C 世界」状态的函数
		- https://dwarfstd.org/
- ABI 是描述了应用程序和操作系统之间约定的接口 / 格式
- 汇编器生成二进制指令序列的过程中有些地址会不知道，先填一个 0，最终链接的时候要填上，满足一个等式：S + A - P（S 代表目标函数的地址，A 代表一个偏移量，P 代表 callq 的地址，其实就是 S - (P - A)）
- 重新理解编译、链接流程：
	- 编译器（gcc）：High-level semantics（C 状态机）-> Low-level semantics（汇编）
	- 汇编器（as）：Low-level semantics -> Binary semantics（状态机容器）
		- 一一对应翻译成二进制代码
		- 如果不能决定的要留下之后怎么办的信息 - relocations
	- 链接器（ld）：
		- 合并所有容器，得到一个完整的状态机，满足所有的 assertion
			- ldscript(-Wl, --verbose); 和 C Runtime Objects(CRT)链接
			- missing/duplicate symbol 会出错
- callq 的解释：
	- The callq instruction has only one operand, not two as implied in the question. The disassembler displays it in two forms, as an address and as a symbol + offset.
	- You are looking at disassembly of an **unlinked** object file. Since the file being disassembled isn't linked, the destination address shown isn't the address of `fun`. The assembler puts **0** in the operand field of the instruction and creates a relocation record for the linker to fill in the offset to the final address of the destination.
	- The operand of the call instruction is an **offset**, relative to the address of the next instruction after the call. So a value of 0 in the operand field causes the disassembler to display the address of the next instruction as the destination of the call. In the disassembly shown, that is address 23.
	- If you make `fun` a static function, the assembler may fill in the true offset of the function, since it won't require relocation, and you will see it in the disassembly. (This may depend on the exact tools and options you are using.)
	- If you disassemble a **linked** executable, the disassembler will show the true destination address of the call.
	- You can also use `objdump -drwC` (optionally with `-Mintel`) to show relocations as comments on instructions when disassembling a file like a `.o` that has some placeholders with relocations
- ELF Loader 本质上就是对着手册解析数据结构，然后把相关的部分搬到内存，最后跳转即可
- 静态链接库加载器的实现：
	- ```c
	  #include <stdint.h>
	  #include <stdio.h>
	  #include <string.h>
	  #include <stdlib.h>
	  #include <unistd.h>
	  #include <assert.h>
	  #include <elf.h>
	  #include <fcntl.h>
	  #include <sys/mman.h>
	  
	  #define STK_SZ           (1 << 20)
	  #define ROUND(x, align)  (void *)(((uintptr_t)x) & ~(align - 1))
	  #define MOD(x, align)    (((uintptr_t)x) & (align - 1))
	  #define push(sp, T, ...) ({ *((T*)sp) = (T)__VA_ARGS__; sp = (void *)((uintptr_t)(sp) + sizeof(T)); })
	  
	  void execve_(const char *file, char *argv[], char *envp[]) {
	    // WARNING: This execve_ does not free process resources.
	    int fd = open(file, O_RDONLY);
	    assert(fd > 0);
	    Elf64_Ehdr *h = mmap(NULL, 4096, PROT_READ, MAP_PRIVATE, fd, 0);
	    assert(h != (void *)-1);
	    assert(h->e_type == ET_EXEC && h->e_machine == EM_X86_64);
	  
	    Elf64_Phdr *pht = (Elf64_Phdr *)((char *)h + h->e_phoff);
	    for (int i = 0; i < h->e_phnum; i++) {
	      Elf64_Phdr *p = &pht[i];
	      if (p->p_type == PT_LOAD) {
	        int prot = 0;
	        if (p->p_flags & PF_R) prot |= PROT_READ;
	        if (p->p_flags & PF_W) prot |= PROT_WRITE;
	        if (p->p_flags & PF_X) prot |= PROT_EXEC;
	        void *ret = mmap(
	          ROUND(p->p_vaddr, p->p_align),              // addr, rounded to ALIGN
	          p->p_memsz + MOD(p->p_vaddr, p->p_align),   // length
	          prot,                                       // protection
	          MAP_PRIVATE | MAP_FIXED,                    // flags, private & strict
	          fd,                                         // file descriptor
	          (uintptr_t)ROUND(p->p_offset, p->p_align)); // offset
	        assert(ret != (void *)-1);
	        memset((void *)(p->p_vaddr + p->p_filesz), 0, p->p_memsz - p->p_filesz);
	      }
	    }
	    close(fd);
	  
	    static char stack[STK_SZ], rnd[16];
	    void *sp = ROUND(stack + sizeof(stack) - 4096, 16);
	    void *sp_exec = sp;
	    int argc = 0;
	  
	    // argc
	    while (argv[argc]) argc++;
	    push(sp, intptr_t, argc);
	    // argv[], NULL-terminate
	    for (int i = 0; i <= argc; i++)
	      push(sp, intptr_t, argv[i]);
	    // envp[], NULL-terminate
	    for (; *envp; envp++) {
	      if (!strchr(*envp, '_')) // remove some verbose ones
	        push(sp, intptr_t, *envp);
	    }
	    // auxv[], AT_NULL-terminate
	    push(sp, intptr_t, 0);
	    push(sp, Elf64_auxv_t, { .a_type = AT_RANDOM, .a_un.a_val = (uintptr_t)rnd } );
	    push(sp, Elf64_auxv_t, { .a_type = AT_NULL } );
	  
	    asm volatile(
	      "mov $0, %%rdx;" // required by ABI
	      "mov %0, %%rsp;"
	      "jmp *%1" : : "a"(sp_exec), "b"(h->e_entry));
	  }
	  
	  int main(int argc, char *argv[], char *envp[]) {
	    if (argc < 2) {
	      fprintf(stderr, "Usage: %s file [args...]\n", argv[0]);
	      exit(1);
	    }
	    execve_(argv[1], argv + 1, envp);
	  }
	  
	  ```
- 动态链接库：大型项目的分解，编译一部分，不用重新链接，减少库函数的磁盘和内存拷贝
- 允许将可执行文件中的一部分以某个指定的权限映射到内存的某个位置
- 自己设计一个二进制格式
	- ```asm
	  DL_HEAD
	  
	  LOAD("libc.dl") # 加载动态库
	  IMPORT(putchar) # 加载外部符号
	  EXPORT(hello)   # 为动态库导出符号
	  
	  DL_CODE
	  
	  hello:
	    ...
	    call DSYM(putchar) # 动态链接符号
	    ...
	  
	  DL_END
	  ```
	- ```c
	  // dl.h
	  #define REC_SZ 32
	  #define DL_MAGIC "\x01\x14\x05\x14"
	  
	  #ifdef __ASSEMBLER__
	    #define DL_HEAD     __hdr: \
	                        /* magic */    .ascii DL_MAGIC; \
	                        /* file_sz */  .4byte (__end - __hdr); \
	                        /* code_off */ .4byte (__code - __hdr)
	    #define DL_CODE     .fill REC_SZ - 1, 1, 0; \
	                        .align REC_SZ, 0; \
	                        __code:
	    #define DL_END      __end:
	  
	    #define RECORD(sym, off, name) \
	      .align REC_SZ, 0; \
	      sym .8byte (off); .ascii name
	  
	    #define IMPORT(sym) RECORD(sym:,           0, "?" #sym "\0")
	    #define EXPORT(sym) RECORD(    , sym - __hdr, "#" #sym "\0")
	    #define LOAD(lib)   RECORD(    ,           0, "+" lib  "\0")
	    #define DSYM(sym)   *sym(%rip)
	  #else
	    #include <stdint.h>
	  
	    struct dl_hdr {
	      char magic[4];
	      uint32_t file_sz, code_off;
	    };
	  
	    struct symbol {
	      int64_t offset;
	      char type, name[REC_SZ - sizeof(int64_t) - 1];
	    };
	  #endif
	  
	  ```
	- ```c
	  // dlbox.c
	  #include <stdio.h>
	  #include <string.h>
	  #include <assert.h>
	  #include <stdint.h>
	  #include <stdlib.h>
	  #include <stdbool.h>
	  #include <unistd.h>
	  #include <sys/mman.h>
	  #include <fcntl.h>
	  #include "dl.h"
	  
	  #define SIZE 4096
	  #define LENGTH(arr) (sizeof(arr) / sizeof(arr[0]))
	  
	  struct dlib {
	    struct dl_hdr hdr;
	    struct symbol *symtab; // borrowed spaces from header
	    const char *path;
	  };
	  
	  static struct dlib *dlopen(const char *path);
	  
	  struct dlib *dlopen_chk(const char *path) {
	    struct dlib *lib = dlopen(path);
	    if (!lib) {
	      fprintf(stderr, "Not a valid dlib file: %s.\n", path);
	      exit(1);
	    }
	    return lib;
	  }
	  
	  // Implementation of binutils
	  
	  void dl_gcc(const char *path) {
	    char buf[256], *dot = strrchr(path, '.');
	    if (dot) {
	      *dot = '\0';
	      sprintf(buf, "gcc -m64 -fPIC -c %s.S && "
	        "objcopy -S -j .text -O binary %s.o %s.dl", path, path, path);
	      system(buf);
	    }
	  }
	  
	  
	  void dl_readdl(const char *path) {
	    struct dlib *h = dlopen_chk(path);
	    printf("DLIB file %s:\n\n", h->path);
	    for (struct symbol *sym = h->symtab; sym->type; sym++) {
	      switch (sym->type) {
	        case '+': printf("    LOAD  %s\n", sym->name); break;
	        case '?': printf("  EXTERN  %s\n", sym->name); break;
	        case '#': printf(   "%08lx  %s\n", sym->offset, sym->name); break;
	      }
	    }
	  }
	  
	  void dl_objdump(const char *path) {
	    struct dlib *h = dlopen_chk(path);
	    char *hc = (char *)h, cmd[64];
	    FILE *fp = NULL;
	  
	    printf("Disassembly of binary %s:\n", h->path);
	  
	    for (char *code = hc + h->hdr.code_off; code < hc + h->hdr.file_sz; code++) {
	      for (struct symbol *sym = h->symtab; sym->type; sym++) {
	        if (hc + sym->offset == code) {
	          int off = code - hc - h->hdr.code_off;
	          if (fp) pclose(fp);
	          sprintf(cmd, "ndisasm - -b 64 -o 0x%08x\n", off);
	          fp = popen(cmd, "w");
	          printf("\n%016x <%s>:\n", off, sym->name);
	          fflush(stdout);
	        }
	      }
	      if (fp) fputc(*code, fp);
	    }
	    if (fp) pclose(fp);
	  }
	  
	  // binutils: interpreter
	  void dl_interp(const char *path) {
	    struct dlib *h = dlopen_chk(path);
	    int (*entry)() = NULL;
	    for (struct symbol *sym = h->symtab; sym->type; sym++)
	      if (strcmp(sym->name, "main") == 0)
	        entry = (void *)((char *)h + sym->offset);
	    if (entry) {
	      exit(entry());
	    }
	  }
	  
	  struct cmd {
	    const char *cmd;
	    void (*handler)(const char *path);
	  } commands[] = {
	    { "gcc",     dl_gcc },
	    { "readdl",  dl_readdl },
	    { "objdump", dl_objdump },
	    { "interp",  dl_interp },
	    { "",        NULL },
	  };
	  
	  int main(int argc, char *argv[]) {
	    if (argc < 3) {
	      fprintf(stderr, "Usage: %s {gcc|readdl|objdump|interp} FILE...\n", argv[0]);
	      return 1;
	    }
	  
	    for (struct cmd *cmd = &commands[0]; cmd->handler; cmd++) {
	      for (char **path = &argv[2]; *path && strcmp(argv[1], cmd->cmd) == 0; path++) {
	        if (path != argv + 2) printf("\n");
	        cmd->handler(*path);
	      }
	    }
	  }
	  
	  // Implementation of dlopen()
	  
	  static struct symbol *libs[16], syms[128];
	  
	  static void *dlsym(const char *name);
	  static void dlexport(const char *name, void *addr);
	  static void dlload(struct symbol *sym);
	  
	  static struct dlib *dlopen(const char *path) {
	    struct dl_hdr hdr;
	    struct dlib *h;
	  
	    int fd = open(path, O_RDONLY);
	    if (fd < 0) goto bad;
	    if (read(fd, &hdr, sizeof(hdr)) < sizeof(hdr)) goto bad;
	    if (strncmp(hdr.magic, DL_MAGIC, strlen(DL_MAGIC)) != 0) goto bad;
	  
	    h = mmap(NULL, hdr.file_sz, PROT_READ | PROT_WRITE | PROT_EXEC, MAP_PRIVATE, fd, 0);
	    if (h == (void *)-1) goto bad;
	  
	    h->symtab = (struct symbol *)((char *)h + REC_SZ);
	    h->path = path;
	  
	    for (struct symbol *sym = h->symtab; sym->type; sym++) {
	      switch (sym->type) {
	        case '+': dlload(sym); break; // (recursively) load
	        case '?': sym->offset = (uintptr_t)dlsym(sym->name); break; // resolve
	        case '#': dlexport(sym->name, (char *)h + sym->offset); break; // export
	      }
	    }
	  
	    return h;
	  
	  bad:
	    if (fd > 0) close(fd);
	    return NULL;
	  }
	  
	  static void *dlsym(const char *name) {
	    for (int i = 0; i < LENGTH(syms); i++)
	      if (strcmp(syms[i].name, name) == 0)
	        return (void *)syms[i].offset;
	    assert(0);
	  }
	  
	  static void dlexport(const char *name, void *addr) {
	    for (int i = 0; i < LENGTH(syms); i++)
	      if (!syms[i].name[0]) {
	        syms[i].offset = (uintptr_t)addr; // load-time offset
	        strcpy(syms[i].name, name);
	        return;
	      }
	    assert(0);
	  }
	  
	  static void dlload(struct symbol *sym) {
	    for (int i = 0; i < LENGTH(libs); i++) {
	      if (libs[i] && strcmp(libs[i]->name, sym->name) == 0) return; // already loaded
	      if (!libs[i]) {
	        libs[i] = sym;
	        dlopen(sym->name); // load recursively
	        return;
	      }
	    }
	    assert(0);
	  }
	  
	  ```
	- ```asm
	  // libc.S
	  #include "dl.h"
	  #include <sys/syscall.h>
	  
	  DL_HEAD
	  
	  EXPORT(putchar)
	  EXPORT(exit)
	  
	  DL_CODE
	  
	  putchar:
	    mov %dil, buf(%rip)
	    mov $SYS_write, %rax
	    mov $1, %rdi
	    lea buf(%rip), %rsi
	    mov $1, %rdx
	    syscall
	    ret
	  buf:
	    .byte 0
	  
	  exit:
	    movq $SYS_exit, %rax
	    syscall
	  
	  DL_END
	  
	  ```
	- ```asm
	  // libhello.S
	  #include "dl.h"
	  
	  DL_HEAD
	  
	  LOAD("libc.dl")
	  IMPORT(putchar)
	  EXPORT(hello)
	  
	  DL_CODE
	  
	  hello:
	    lea str(%rip), %rdi
	    mov count(%rip), %eax
	    push %rbx
	    mov %rdi, %rbx
	    inc %eax
	    mov %eax, count(%rip)
	    add $0x30, %eax
	    movb %al, 0x6(%rdi)
	  loop:
	    movsbl (%rbx),%edi
	    test %dil,%dil
	    je out
	    call DSYM(putchar)
	    inc  %rbx
	    jmp loop
	  out:
	    pop %rbx
	    ret
	  
	  str:
	    .asciz "Hello X\n"
	  
	  count:
	    .int 0
	  
	  DL_END
	  
	  ```
	- ```asm
	  #include "dl.h"
	  
	  DL_HEAD
	  
	  LOAD("libc.dl")
	  LOAD("libhello.dl")
	  IMPORT(hello)
	  EXPORT(main)
	  
	  DL_CODE
	  
	  main:
	    call DSYM(hello)
	    call DSYM(hello)
	    call DSYM(hello)
	    call DSYM(hello)
	    movq $0, %rax
	    ret
	  
	  DL_END
	  
	  ```
-