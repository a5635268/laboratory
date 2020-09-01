package main

import (
	"fmt"
	"sync"
	"time"
)

var wg sync.WaitGroup

func hello(i int) {
	defer wg.Done() // goroutine结束就登记-1
	fmt.Println("Hello Goroutine!", i)
	time.Sleep(time.Second)
}
func main() {
	for i := 0; i < 10; i++ {
		wg.Add(2) // 启动一个goroutine就登记+1
		go hello(i)
		go hello(i * 2)
	}
	wg.Wait() // 等待所有登记的goroutine都结束
}

