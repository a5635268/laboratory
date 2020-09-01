package main

import "fmt"

func test_chan2(ch chan string){
	fmt.Printf("inner: %v, %v\n",ch, len(ch))
	ch<-"b"
	fmt.Printf("inner: %v, %v\n",ch, len(ch))
}

func main() {
	ch := make(chan string, 10)
	ch<- "a"

	fmt.Printf("outer: %v, %v\n",ch, len(ch))
	test_chan2(ch)
	fmt.Printf("outer: %v, %v\n",ch, len(ch))
}
