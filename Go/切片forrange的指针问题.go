package main

import "fmt"

func main() {
	/*s :=[] int {1,2,3,4,5}
	for i,v := range s {
		fmt.Printf("%p, %v,%v\n",s,&i,&v)
	}*/


	/*m := map[string]string{
		"name" : "zhouzhou",
		"age" : "18",
	}
	for i,v := range m {
		fmt.Printf("%p, %v,%v\n",m,&i,&v)
	}*/

	str := "zhouzhou"
	for i,v := range str{
		fmt.Printf("%p, %v,%v\n",&str,&i,&v)
	}
}
