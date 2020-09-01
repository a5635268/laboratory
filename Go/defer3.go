package main

import "fmt"


func fun1() (i int) {
	defer func() {
		i++
		fmt.Println("defer2:", i)
	}()



	defer func() {
		i++
		fmt.Println("defer1:", i)
	}()



	return 0
}

func fun2() int {
	var i int
	defer func() {
		i++
		fmt.Println("defer2:", i)
	}()

	defer func() {
		i++
		fmt.Println("defer1:", i)
	}()
	return i
}

func fun3() (r int) {
	t := 5
	defer func() {
		t = t + 5
		fmt.Println(t)
	}()
	return t
}

func fun4() int {
	i := 8

	defer func(i int) {
		i = 99
		fmt.Println(i)
	}(i)
	i = 19
	return i
}


func main() {
	fmt.Println("=========================")
	fmt.Println("return:", fun1())

	fmt.Println("=========================")
	fmt.Println("return:", fun2())
	fmt.Println("=========================")

	fmt.Println("return:", fun3())
	fmt.Println("=========================")

	fmt.Println("return:", fun4())
}

/**
=========================
defer1:1
defer2:2
return:2
=========================
defer1:1
defer2:2
return:0
=========================
10
return:5
=========================
99
return:19
=========================

 */
