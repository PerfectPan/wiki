- https://cheats.rs/
- 变量（let）只能在函数里定义，常量（const）可以在文件，模块里定义
- String 和 &str
	- String 可以理解为是变长的 Vec<u8>（是放在标准库里的），底下封装了很多方法，存储在堆上
	- String 是 utf8 存储的，因此一些超过 BMP 的字符，你直接用 index 去取会有问题，Rust 提供了 to_bytes 和 to_char 的方法让你用两种视角去看这个 Vec<u8>
	- &str 存储在栈上
- if let 语法让我们以一种不那么冗长的方式结合 if 和 let，来处理只匹配一个模式的值而忽略其他模式的情况
	- ```rust
	  let mut count = 0;
	  if let Coin::Quarter(state) = coin {
	    println!("State quarter from {:?}!", state);
	  } else {
	    count += 1;
	  }
	  ```
- `mut self` 在需要所有权转移并且需要修改对象的场景下特别有用，尤其是在实现构建器模式或链式调用时。这种模式既保证了内存安全，又提供了良好的 API 设计
-