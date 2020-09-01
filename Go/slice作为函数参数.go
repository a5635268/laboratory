package main


import (
	"fmt"
	"reflect"
)

func modify1(slice []int)  {
	for i:=0;i<len(slice);i++{
		slice[i] = 0
	}

	fmt.Println("Inside  modify1 after append: ", len(slice))
	fmt.Println("Inside  modify1 after append: ", cap(slice))
	fmt.Println("Inside  modify1 after append: ", slice)
}

func modify2(slice []int)  {
	length := len(slice)
	for i:=0;i<length;i++{
		slice = append(slice, 1)
	}

	fmt.Println("Inside  modify2 after append: ", len(slice))
	fmt.Println("Inside  modify2 after append: ", cap(slice))
	fmt.Println("Inside  modify2 after append: ", slice)
}

func main(){

	s1 := make([]int,10,10)
	for i:=0;i<10;i++{
		s1[i] = i
	}
	fmt.Println("makeslcie return type: ", reflect.TypeOf(s1))

	fmt.Println("before modify slice: ", s1)

	modify1(s1)
	fmt.Println("after modify1 slice: ", s1)

	for i:=0;i<10;i++{
		s1[i] = i
	}
	modify2(s1)
	fmt.Println("after modify2 slice: ", len(s1))
	fmt.Println("after modify2 slice: ", cap(s1))
	fmt.Println("after modify2 slice: ", s1)

}
