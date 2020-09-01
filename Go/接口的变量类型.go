package main

import "fmt"

type Mover interface {
	move()
}

type dog struct {}

func (d *dog) move() {
	fmt.Println("狗会动")
}

func main() {
	var x Mover
	var wangcai = dog{} // 旺财是dog类型
	x = &wangcai        // x可以接收dog类型
	var fugui = &dog{}  // 富贵是*dog类型
	x = fugui           // x可以接收*dog类型
	x.move()
}

