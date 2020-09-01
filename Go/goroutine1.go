package main

import (
	"fmt"
	"time"
)

func hello() {
	fmt.Println("Hello Goroutine!")
}
func main() {
	go hello()
	fmt.Println("main goroutine done!")
	time.Sleep(time.Millisecond)
}
