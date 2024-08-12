package main

import (
	"fmt"
	"io"
	"net/http"
	"github.com/gorilla/websocket"
)

func getMsgs(c *websocket.Conn){
	for{
		_,res,err := c.ReadMessage()
		if err != nil{
			fmt.Println(err)
		}
		fmt.Print("\033[1B")
		fmt.Print("\033[s")
		fmt.Print("\033[0G")
		fmt.Print("\033[1A")
		fmt.Print("\033[K")
		fmt.Println(string(res))
		fmt.Print(">")
		fmt.Print("\033[u")  
		fmt.Print("\033[2G")
	}
}

func sendMsgs(usrName string,c *websocket.Conn){
	for{
		var msg string
		fmt.Print(">")
		fmt.Scan(&msg)
		msg = "["+usrName+"] "+msg
		err := c.WriteMessage(websocket.TextMessage,[]byte(msg))
		if err != nil{
			fmt.Println(err)
		}
	}
}

func main(){
	res,err := http.Get("https://utilsy.glitch.me/rat.txt")
	if err != nil{
		fmt.Println(err)
	}
	body,err := io.ReadAll(res.Body)
	if err != nil{
		fmt.Println(err)
	}
	IP := string(body)
	url := "ws://" + IP + ":2208"

	var usrName string
	fmt.Print("enter your username\n>")
	fmt.Scan(&usrName)

	c,_,err := websocket.DefaultDialer.Dial(url,nil)
	if err != nil{
		fmt.Println(err)
	}
	defer c.Close()

	wMsg := "[SERVER] User '" + usrName + "' joined the chat"

	err = c.WriteMessage(websocket.TextMessage,[]byte(wMsg))
	if err != nil{
		fmt.Println(err)
	}

	go sendMsgs(usrName,c)
	go getMsgs(c)

	select {}
}