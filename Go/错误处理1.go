package main

import (
	"errors"
)


func test(f float64) (int, error) {
	//return 0, fmt.Errorf("square root of negative number %g", f)
	return 0, errors.New ("math - square root of negative number")
}

func main() {
	code, msg := test(0)
	println(code,msg.Error())
}
