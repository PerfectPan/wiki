- set 存在 swap 和 merge 两个 API，可以在启发式合并中用到
	- ```cpp
	  if (geneSet[node].size() < geneSet[child].size()) {
	    geneSet[node].swap(geneSet[child]);
	  }
	  geneSet[node].merge(geneSet[child]); // 一定是从小的并到大的
	  ```
-