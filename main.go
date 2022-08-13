//package main
//
//import "fmt"
//
//type Node struct {
//	children             []*Node
//	Type string
//}
//
//func main() {
//	fmt.Println("a new file")
//}
//
//// 邻接表，广度遍历
//func findWhetherExistsPath(n int, graph [][]int, start int, target int) bool {
//	adjacentList := make([][]int, n)
//	for _, link := range graph {
//		src, dst := link[0], link[1]
//		adjacentList[src] = append(adjacentList[src], dst)
//	}
//	q := []int{start}
//	visited := make([]bool, n)
//	for len(q) > 0 {
//		node := q[0]
//		visited[node] = true
//		q = q[1:]
//		for _, adj := range adjacentList[node] {
//			if adj == target {
//				return true
//			}
//			if !visited[adj] {
//				q = append(q, adj)
//			}
//		}
//	}
//	return false
//}
//
//// 邻接表，深度遍历
//func findWhetherExistsPath2(n int, graph [][]int, start int, target int) bool {
//	adjacentList := make([][]int, n)
//	for _, link := range graph {
//		src, dst := link[0], link[1]
//		adjacentList[src] = append(adjacentList[src], dst)
//	}
//	visited := make([]bool, n)
//	var dfs func(src int) bool
//	dfs = func(src int) bool {
//		visited[src] = true
//		for _, adj := range adjacentList[src] {
//			if adj == target {
//				return true
//			}
//			if !visited[adj] && dfs(adj) {
//				return true
//			}
//		}
//		return false
//	}
//	return dfs(start)
//}

package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strings"
)

type Graph struct {
	Num          int
	AdjacencyMap map[int]map[int]struct{}
}

func NewGraph(num int) *Graph {
	graph := Graph{Num: num, AdjacencyMap: make(map[int]map[int]struct{})}
	for i := 1; i < num+1; i++ {
		if i == 1 {
			graph.AdjacencyMap[1] = map[int]struct{}{
				2: {},
				3: {},
			}
			continue
		} else if i == num-1 {
			//graph.AdjacencyMap[num - 1] = []int{num - 3, num}
			graph.AdjacencyMap[num-1] = map[int]struct{}{
				num - 3: {},
				num:     {},
			}
			continue
		}
		if i%2 == 1 {
			//graph.AdjacencyMap[i] = []int{i - 2, i + 1, i + 2}
			graph.AdjacencyMap[i] = map[int]struct{}{
				i - 2: {},
				i + 1: {},
				i + 2: {},
			}
		} else {
			//graph.AdjacencyMap[i] = []int{i - 1, num + 2 - i}
			graph.AdjacencyMap[i] = map[int]struct{}{
				i - 1:       {},
				num + 2 - i: {},
			}
		}
	}
	return &graph
}

// FindAllCycles find all cycles
func FindAllCycles(g *Graph, num int) {
	for i := 3; i < num+1; i++ {
		FindCirOfLength(g, num, i)
	}
	defer close(WriteChan)
}

func FindCirOfLength(g *Graph, num int, length int) {
	for i := 0; i < num-length+2; i++ {
		FindCirStartsWith(g, length, []int{i})
	}
}

func FindCirStartsWith(g *Graph, length int, path []int) {
	l := len(path)
	last := path[l-1]
	if l == length-1 {
		for num := range g.AdjacencyMap[last] {
			if _, ok := g.AdjacencyMap[num]; ok && num > path[1] && !IsInSlice(path, num) {
				WriteChan <- "[" + IntSliceToString(path, " ") + "]"
			}
		}
	} else {
		for num := range g.AdjacencyMap[last] {
			if num > path[0] && !IsInSlice(path, num) {
				path = append(path, num)
				FindCirStartsWith(g, length, path)
				path = path[:len(path)-1]
			}
		}
	}
}

func IntSliceToString(a []int, delim string) string {
	return strings.Trim(strings.Replace(fmt.Sprint(a), " ", delim, -1), "[]")
}

func IsInSlice(path []int, num int) bool {
	for _, item := range path {
		if num == item {
			return true
		}
	}
	return false
}

var FilePath = "data.txt"
var file *os.File
var WriteChan = make(chan string, 20)
var err error

func main() {
	file, err = os.OpenFile(FilePath, os.O_WRONLY|os.O_APPEND, 0666)
	if err != nil {
		fmt.Println("Fail to open the file", err)
	}
	// file must close
	defer func(file *os.File) {
		err := file.Close()
		if err != nil {

		}
	}(file)
	// use buffered *Writer
	writer := bufio.NewWriter(file)
	go func() {
		for {
			select {
			case writeString, ok := <-WriteChan:
				// channel close but there is still some string buffered in the channel
				if !ok && writeString != "" {
					break
				}
				_, err := writer.WriteString(writeString)
				if err != nil {
					log.Panicln("Fail to write string")
				}
			}
		}
	}()
	graph := NewGraph(1000)
	FindAllCycles(graph, graph.Num)
	fmt.Println(graph)
	//Flush将缓存的文件真正写入到文件中
	err = writer.Flush()
	if err != nil {
		log.Println("Flush fai")
	}
}

var cycleChan = make(chan map[int]struct{})

func unblock() {

}

func simpleCycles(g *Graph) {

}

func getStronglyConnectComponents(g *Graph) {
	preOrder := map[int]int{}
	lowLink := map[int]int{}
	sccFound := map[int]struct{}{}
	var sccQueue []int
	index := 0
	for source := range g.AdjacencyMap {
		if _, ok := sccFound[source]; !ok {
			queue := []int{source}
			for len(queue) != 0 {
				v := queue[len(queue)-1]
				if _, ok := preOrder[v]; !ok {
					index++
					preOrder[v] = index
				}
				done := true
				for w := range g.AdjacencyMap[v] {
					if _, ok := preOrder[v]; !ok {
						queue = append(queue, w)
						done = false
						break
					}
				}
				if done {
					lowLink[v] = preOrder[v]
					for w := range g.AdjacencyMap[v] {
						if _, ok := sccFound[w]; !ok {
							if preOrder[w] > preOrder[v] {
								lowLink[v] = min(lowLink[v], lowLink[w])
							} else {
								lowLink[v] = min(lowLink[v], preOrder[w])
							}
						}
					}
					queue = queue[:len(queue)-1]
					if lowLink[v] == preOrder[v] {
						scc := map[int]struct{}{v: {}}
						for len(sccQueue) != 0 && preOrder[sccQueue[len(sccQueue)-1]] > preOrder[v] {
							scc[sccQueue[len(sccQueue)-1]] = struct{}{}
							sccQueue = sccQueue[:len(sccQueue)-1]
						}
						update(sccFound, scc)
						cycleChan <- scc
					} else {
						sccQueue = append(sccQueue, v)
					}
				}
			}
		}
	}
}

func min(x, y int) int {
	if x > y {
		return y
	}
	return y
}

func update(pre, new map[int]struct{}) {
	for key := range new {
		pre[key] = struct{}{}
	}
}
