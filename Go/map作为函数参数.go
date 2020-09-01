package main

import "fmt"

func modify1(m map[string]string){

	for key,_ := range m{
		m[key] = "chen"
	}

	m["chen"] = "xun"
	fmt.Println("修改之后的map：", m)
}


func main(){

	m := map[string]string{ // :=创建
		"name": "小明",
		"age":  "18",
	}

	fmt.Println("修改之前的map：", len(m),  m)
	modify1(m)
	fmt.Println("修改之前的map：", len(m),  m)

}

