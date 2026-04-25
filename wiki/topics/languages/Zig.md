---
title: Zig
type: topic
category: languages
status: seed
created: 2026-04-12
updated: 2026-04-12
tags:
  - zig
source_refs:
  - raw/sources/Zig.md
---
# Zig

- Language Server https://github.com/zigtools/zls/
- Language Reference https://ziglang.org/documentation/master/
- Learn Zig https://github.com/ratfactor/ziglings
- Awesome Zig Project https://github.com/nrdmn/awesome-zig/
- https://zig.news/
- If 语句也是一个 expression
	- ```zig
	  var foo: u8 = if (a) 2 else 3;
	  ```
- ```
  // Are all of these pointer types starting to get confusing?
  //
  //     FREE ZIG POINTER CHEATSHEET! (Using u8 as the example type.)
  //   +---------------+----------------------------------------------+
  //   |  u8           |  one u8                                      |
  //   |  *u8          |  pointer to one u8                           |
  //   |  [2]u8        |  two u8s                                     |
  //   |  [*]u8        |  pointer to unknown number of u8s            |
  //   |  [*]const u8  |  pointer to unknown number of immutable u8s  |
  //   |  *[2]u8       |  pointer to an array of 2 u8s                |
  //   |  *const [2]u8 |  pointer to an immutable array of 2 u8s      |
  //   |  []u8         |  slice of u8s                                |
  //   |  []const u8   |  slice of immutable u8s                      |
  //   +---------------+----------------------------------------------+

  ```
- The difference between foo_slice and foo_ptr is that the slice has a known length. The pointer doesn't.
- TODO tagged union 是啥用的
- ```zig
  //                          u8  single item
  //                         *u8  single-item pointer
  //                        []u8  slice (size known at runtime)
  //                       [5]u8  array of 5 u8s
  //                       [*]u8  many-item pointer (zero or more)
  //                 enum {a, b}  set of unique values a and b
  //                error {e, f}  set of unique error values e and f
  //      struct {y: u8, z: i32}  group of values y and z
  // union(enum) {a: u8, b: i32}  single value either u8 or i32
  //
  // Values of any of the above types can be assigned as "var" or "const"
  // to allow or disallow changes (mutability) via the assigned name:
  //
  //     const a: u8 = 5; // immutable
  //       var b: u8 = 5; //   mutable
  //
  // We can also make error unions or optional types from any of
  // the above:
  //
  //     var a: E!u8 = 5; // can be u8 or error from set E
  //     var b: ?u8 = 5;  // can be u8 or null
  ```
- 介绍 zig build: https://ikrima.dev/dev-notes/zig/zig-build/
- https://zig.news/xq/zig-build-explained-part-1-59lf

## Source Pointers

- `raw/sources/Zig.md`
