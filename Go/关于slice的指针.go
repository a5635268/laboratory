package main

import "fmt"

func main() {

	sl := []string{
		"a",
		"b",
		"c",
	}

	fmt.Printf("%v, %p\n",sl, sl)
	test_slice(sl)
	fmt.Printf("%v, %p\n",sl, sl)
}

func test_slice(sl []string){
	fmt.Printf("%v, %p\n",sl, sl)
	sl[0] = "aa"
	//sl = append(sl, "d")
	fmt.Printf("%v, %p\n",sl, sl)
}
