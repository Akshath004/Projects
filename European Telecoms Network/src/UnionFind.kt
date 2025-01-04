class UnionFind(size: Int) {
    private val parent = IntArray(size) { it }
    private val rank = IntArray(size) { 0 }

    private fun find(node: Int): Int {
        if (parent[node] != node) {
            parent[node] = find(parent[node])
        }
        return parent[node]
    }

    fun union(node1: Int, node2: Int): Boolean {
        val root1 = find(node1)
        val root2 = find(node2)

        if (root1 == root2) return false

        if (rank[root1] > rank[root2]) {
            parent[root2] = root1
        } else if (rank[root1] < rank[root2]) {
            parent[root1] = root2
        } else {
            parent[root2] = root1
            rank[root1]++
        }
        return true
    }
}