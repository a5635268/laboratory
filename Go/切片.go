package main

import "fmt"

func main() {
	/* 创建切片 numbers1 是之前切片的两倍容量*/
	numbers1 := [] int {1,2,3}
	numbers1 = append(numbers1,1,3,4,5,6,8)
	fmt.Println(numbers1)
}
