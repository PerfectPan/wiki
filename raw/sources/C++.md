- [[STL]]
- 常用库函数
	- 字符串转数字 std::stoi https://en.cppreference.com/w/cpp/string/basic_string/stol
	- 生成 id 数组：iota(id.begin(), id.end(), init_value); https://en.cppreference.com/w/cpp/algorithm/iota
		- #include <numeric>
	- 数字转字符串 std::to_string
		- #include <string>
- g++ -DMY_MACRO 编译带上 MY_MACRO 的宏
- cin.tie(nullptr)->sync_with_stdio(false); 关闭同步，可以加快 cin 的速度，但是 cin 和 scanf 就不能混用了，包括 cout 和 printf，本质上是为了解决混用带来的顺序混乱的问题（可以再查查资料）
- ```C++
  ios::sync_with_stdio(false);
  cin.tie(0); cout.tie(0);
  ```
-