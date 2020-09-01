package main

import "fmt"

type student struct {
	name string
	age  int
}

func main() {
	m := make(map[string]*student)
	stus := []student{
		{name: "小王子", age: 18},
		{name: "娜扎", age: 23},
		{name: "大王八", age: 9000},
	}

	fmt.Printf("%v %p\n",stus,stus)

	for _, stu := range stus {
		fmt.Printf("%p",stu)
		// m[stu.name] 存的都是指针，
		m[stu.name] = &stu
	}

	for k, v := range m {
		fmt.Println(k, "=>", v.name)
	}
}
