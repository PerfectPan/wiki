---
title: Shell
type: topic
category: systems
status: seed
created: 2026-04-12
updated: 2026-04-12
tags:
  - shell
source_refs:
  - raw/sources/Shell.md
---
# Shell

- Syntax Cheat Sheet:
	- \$@ - 所有参数的列表，如 "\$@" 用 " 括起来的情况，以 "\$1", "\$2", ... "\$n" 的形式输出所有参数
	- $0： name of the scirpt
	- \$\#：参数个数
	- $?：上一个命令的返回 code
	- $$：当前进程号
	- !!：上一条完整的命令
	- $_：Last argument from the last command.
	- cd - ：返回上一次调用的工作目录
	- ```
	  *# This creates files foo/a, foo/b, ... foo/h, bar/a, bar/b, ... bar/h*
	  touch {foo,bar}/{a..h}
	  ```
- 单引号是原样输出
- 双引号可以替换变量
- Useful Script:
	- 找脚本执行的绝对路径
		- ```sh
		  #!/bin/bash

		  # All these options work on bash 3.2 on macOS where 'readlink -f' is not available

		  # Ref http://stackoverflow.com/a/246128

		  # 1. Get script path, don't canonicalise symlinks used in script path

		  # ${BASH_SOURCE[0]} is set but includes './' prefix
		  DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" 2>/dev/null)" && pwd 2>/dev/null)"
		  SCRIPT_PATH=$DIR/$(basename $0)
		  echo $DIR
		  echo $SCRIPT_PATH
		  exit 0

		  # 2. Canonicalise symlinks - option 1
		  SCRIPT_PATH="${BASH_SOURCE[0]}";
		  if ([ -h "${SCRIPT_PATH}" ]) then
		    while([ -h "${SCRIPT_PATH}" ]) do SCRIPT_PATH=`readlink "${SCRIPT_PATH}"`; done
		  fi
		  pushd . > /dev/null
		  cd `dirname ${SCRIPT_PATH}` > /dev/null
		  SCRIPT_PATH=`pwd`;
		  echo $SCRIPT_PATH
		  popd  > /dev/null
		  exit 0

		  # 3. Canonicalise symlinks - option 2
		  SOURCE="${BASH_SOURCE[0]}"
		  # SOURCE="$0"
		  while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
		    TARGET="$(readlink "$SOURCE")"
		    if [[ $TARGET == /* ]]; then
		      echo "SOURCE '$SOURCE' is an absolute symlink to '$TARGET'"
		      SOURCE="$TARGET"
		    else
		      DIR="$( dirname "$SOURCE" )"
		      echo "SOURCE '$SOURCE' is a relative symlink to '$TARGET' (relative to '$DIR')"
		      SOURCE="$DIR/$TARGET" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
		    fi
		  done
		  echo $SOURCE
		  ```

## Source Pointers

- `raw/sources/Shell.md`

