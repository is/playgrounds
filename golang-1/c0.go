package main

import (
	"fmt"
	"math"
)

func main() {
	fmt.Println("hello world")
	var a uint8 = 15
	fmt.Println((a / 8) + 1)
	a = 31
	fmt.Println((a / 8) + 1)
	a = a + 5
	fmt.Println((a / 8) + 1)

	var c = int(math.Pow(2, float64(3)))
	fmt.Println(c)
}
