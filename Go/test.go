package main

import (
	"fmt"
	"os"
)

func main() {
	type a struct {
		val int
		next *a
	}
	//os.Args是一个[]string
	if len(os.Args) > 0 {
		for index, arg := range os.Args {
			fmt.Printf("args[%d]=%v\n", index, arg)
		}
	}
}
