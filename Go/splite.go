package main

import (
	"fmt"
	"strings"
)

func Split(str string, sep string) []string {
	ret := []string{}
	index := strings.Index(str,sep)
	for index >= 0 {
		ret = append(ret,str[:index])
		str = str[index+1:]
		index = strings.Index(str,sep)
	}
	ret = append(ret,str)
	return ret
}

func main() {
	ret := Split("a,b,c",",")
	fmt.Println(ret)
}
