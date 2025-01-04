import org.graphstream.graph.Graph
import org.graphstream.graph.implementations.SingleGraph
import java.io.File

class GraphProcessor {
    fun processFile(file: File): Pair<Graph, Int> {
        val edges = mutableListOf<Edge>()
        val cityToIndex = mutableMapOf<String, Int>()
        var cityCount = 0

        file.forEachLine { line ->
            val parts = line.split(", ").map { it.trim() }
            if (parts.size == 3) {
                val city1 = parts[0]
                val city2 = parts[1]
                val distance = parts[2].toInt()

                if (city1 !in cityToIndex) {
                    cityToIndex[city1] = cityCount++
                }
                if (city2 !in cityToIndex) {
                    cityToIndex[city2] = cityCount++
                }

                val node1 = cityToIndex[city1]!!
                val node2 = cityToIndex[city2]!!
                edges.add(Edge(node1, node2, distance))
            }
        }
        val (mst, totalSum) = kruskalMST(cityCount, edges)
        val graph = createGraph(mst, cityToIndex)
        return Pair(graph, totalSum)
    }

    private fun createGraph(mst: List<Edge>, cityToIndex: Map<String, Int>): Graph {
        val indexToCity = cityToIndex.entries.associate { (k, v) -> v to k }
        val graph = SingleGraph("MST")

        for ((index, city) in indexToCity) {
            graph.addNode(city).apply {
                setAttribute("ui.label", city)
            }
        }

        for (edge in mst) {
            val city1 = indexToCity[edge.node1]!!
            val city2 = indexToCity[edge.node2]!!
            graph.addEdge("${city1}-${city2}", city1, city2).apply {
                setAttribute("ui.label", edge.weight)
            }
        }

        graph.setAttribute("ui.stylesheet", "node { text-size: 20px; } edge { text-size: 15px; }")
        return graph
    }

    private fun kruskalMST(numVertices: Int, edges: List<Edge>): Pair<List<Edge>, Int> {
        val sortedEdges = edges.sortedBy { it.weight }
        val unionFind = UnionFind(numVertices)
        val mst = mutableListOf<Edge>()
        var totalSum = 0

        for (edge in sortedEdges) {
            if (unionFind.union(edge.node1, edge.node2)) {
                mst.add(edge)
            }
            if (mst.size == numVertices - 1) break
        }
        for (edge in mst) {
            totalSum += edge.weight
        }

        return Pair(mst, totalSum)
    }
}
