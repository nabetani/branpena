set -eu
GOARCH=amd64 go run . 3000000 > mac_amd64.txt
go run . 3000000 > mac_m1.txt
