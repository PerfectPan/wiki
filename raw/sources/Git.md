- 存储的数据模型：
	- ```ts
	  type blob = Array<byte> // 最基础的文件
	  type tree = Map<string, tree | blob>
	  type commit = {
	    parent: Array<commit>; // 有向无环图
	    author: string;
	    message: string;
	    snapshot: tree;
	  }
	  
	  type object = blob | tree | commit;
	  type objects = Map<string, object>; // string 是一个 object 的哈希值
	  // 第二个 string 代表代表 objects 的 key，第一个就是
	  // 常说的 HEAD 或者是什么
	  type references = Map<string, string> 
	  ```
- git merge 的时候如果被 merge 的分支正好是基于当前分支往前开发的几个 commit 的话，就会直接 fast forward，不会创建新的 commit，而是直接移动 HEAD 指针
- 为什么要先 add？
	- 很多时候我们不希望把当前的所有改动都提交上去，因此先 add，可以做到当前改动和暂存区的分开，相当于有一个选择的机会
- git add -p <文件名> 可以交互式地把部分内容添加到暂存区（但是似乎仍然无法按行提交）
- `git log --all --graph --decorate`: visualizes history as a DAG
- `git fetch`: retrieve objects/references from a remote
- `git pull`: same as `git fetch; git merge`
- `git clone`: download repository from remote
- `git checkout -- <file>`: discard changes（不包含暂存区的改动）
- **GitHub**: Git is not GitHub. GitHub has a specific way of contributing code to other projects, called [pull requests](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/about-pull-requests).
- **Other Git providers**: GitHub is not special: there are many Git repository hosts, like [GitLab](https://about.gitlab.com/) and [BitBucket](https://bitbucket.org/).
- 可阅读的材料
	- [Oh Shit, Git!?!](https://ohshitgit.com/) is a short guide on how to recover from some common Git mistakes.
	- [Git for Computer Scientists](https://eagain.net/articles/git-for-computer-scientists/) is a short explanation of Git’s data model, with less pseudocode and more fancy diagrams than these lecture notes.
	- [Git from the Bottom Up](https://jwiegley.github.io/git-from-the-bottom-up/) is a detailed explanation of Git’s implementation details beyond just the data model, for the curious.
	- [How to explain git in simple words](https://smusamashah.github.io/blog/2017/10/14/explain-git-in-simple-words)
-