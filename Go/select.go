package main

import (
	"fmt"
	"time"
)

func Chann(ch chan int, stopCh chan bool) {
	//var i int
	// i = 10
	time.Sleep(1)
	/*for j := 0; j < 10; j++ {
		ch <- i
		time.Sleep(time.Second)
	}
	stopCh <- true*/
}

func main() {

	ch := make(chan int)
	c := 0
	stopCh := make(chan bool)

	go Chann(ch, stopCh)

	// select 会循环检测条件，如果有满足则执行并退出，否则一直循环检测。
	for{
		select {
			case c = <-ch:
				fmt.Println("Recvice c", c)
			case s := <-ch:
				fmt.Println("Receive s", s)
			case _ = <-stopCh:
				goto end
		}
	}
end:
}
