package main

import (
	"fmt"
	"log"
	"math/rand"
	"os"
	"sort"
	"strconv"
	"time"
)

func measure(name string, data []uint, proc func(data []uint) int64) {
	sum := int64(0)
	t0 := time.Now()
	for i := 0; i < 1000; i++ {
		sum += proc(data)
	}
	duration := time.Since(t0)
	durSec := float64(duration.Nanoseconds()) * 1e-9
	fmt.Printf("  %10s: duration=%4.2fs  sum=%d\n", name, durSec, sum)
}

func hoge(data []uint) int64 {
	sum := int64(0)
	size := len(data)
	for c := 0; c < size; c++ {
		if 128 <= data[c] {
			sum += int64(data[c])
		}
	}
	return sum
}

func hogev(data []uint) int64 {
	sum := int64(0)
	size := len(data)
	for c := 0; c < size; c++ {
		v := data[c]
		if 128 <= v {
			sum += int64(v)
		}
	}
	return sum
}

func fuga(data []uint) int64 {
	sum := int64(0)
	for _, v := range data {
		if 128 <= v {
			sum += int64(v)
		}
	}
	return sum
}

func fugao(data []uint) int64 {
	sum := int64(0)
	for _, v := range data {
		sum += int64(v) & func() int64 {
			if 128 <= v {
				return 0xff
			}
			return 0
		}()
	}
	return sum
}
func hogeo(data []uint) int64 {
	sum := int64(0)
	size := len(data)
	for c := 0; c < size; c++ {
		sum += int64(data[c]) & func() int64 {
			if 128 <= data[c] {
				return 0xff
			}
			return 0
		}()
	}
	return sum
}

func makeData(size int) []uint {
	data := []uint{}
	for i := 0; i < size; i++ {
		data = append(data, uint(i&0xff))
	}
	return data
}

func getSize() int {
	if len(os.Args) < 2 {
		return 1000
	}
	n, err := strconv.Atoi(os.Args[1])
	if err != nil {
		log.Panicln(err)
	}
	return n
}

func main() {
	data := makeData(getSize())
	for i := 0; i < 2; i++ {
		rand.Shuffle(len(data), //
			func(i, j int) { data[i], data[j] = data[j], data[i] })
		fmt.Println("shuffled")
		measure("simple", data, hoge)
		measure("dry", data, hogev)
		measure("range", data, hogeo)
		measure("opt-range", data, fuga)
		measure("opt-simple", data, fugao)
		sort.Slice(data, //
			func(i, j int) bool { return data[i] < data[j] })
		fmt.Println("sorted")
		measure("simple", data, hoge)
		measure("dry", data, hogev)
		measure("range", data, hogeo)
		measure("opt-range", data, fuga)
		measure("opt-simple", data, fugao)
	}
}
