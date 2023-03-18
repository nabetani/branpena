set GOARCH=amd64
go build -o win_amd64.exe .
set GOARCH=386
go build -o win_386.exe .
set GOARCH=
