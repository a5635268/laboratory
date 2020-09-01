package main

import "fmt"

func main() {
	a := 10
	b := &a
	fmt.Printf("变量a的内存地址： %v\n", &a) // 0xc0000180a0
	fmt.Printf("变量b本身的内存地址：%v\n", &b) // 0xc000006028
	fmt.Printf("变量b存储的内存地址：%v\n", b) // 0xc0000180a0
	fmt.Printf("变量b存储的内存地址的值：%v\n", *b) //10

	c := b
	d := *c // 从b的内存地址取出10给d
	*b += 1
	fmt.Printf("%v,%v,%v,%v\n",c,d,a,b) // 0xc0000180a0,10
}
