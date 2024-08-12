use std::{io::{stdout, Write}, process::exit};

use crossterm::{cursor, execute, terminal::{self, ClearType}};
use reqwest;
use tokio_tungstenite::{connect_async, tungstenite::Message};
use futures_util::{SinkExt, StreamExt};

#[tokio::main]
async fn main() -> Result<(),Box<dyn std::error::Error>>{
    println!("enter your name");
    print!(">");
    let _ = stdout().flush();
    let mut username = String::new();
    std::io::stdin().read_line(&mut username).unwrap();

    match username.trim()
    {
        "SERVER" =>
        {
            println!("User cannot be named server");
            exit(0);
        }
        _=>{}
    }


    let client = reqwest::Client::builder().user_agent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3").build()?;
    let res = client.get("https://utilsy.glitch.me/rat.txt").send().await?;
    let internet_protocol = res.text().await?;
    
    let addr = format!("ws://{}:2208",internet_protocol.trim());
    let url = url::Url::parse(&addr)?;

    let (mut socket,_response) = connect_async(url.to_string()).await.expect("Failed to connect");

    socket.send(Message::text(format!("[SERVER] User '{}' joined the chat",username.trim()).to_string())).await?;

    let socket_clone = socket;
    let t1 = tokio::spawn(async move
        {
            let mut socket = socket_clone;
            while let Some(message) = socket.next().await
            {
                match message
                {
                    Ok(Message::Text(text)) => 
                    {
                        execute!(
                            stdout(),
                            cursor::MoveDown(1),
                            cursor::SavePosition,
                            cursor::MoveToColumn(0),
                            cursor::MoveUp(1),
                            terminal::Clear(ClearType::CurrentLine),
                        ).unwrap();
                        println!("{}",text);
                        execute!(
                            stdout(),
                            cursor::RestorePosition,
                        ).unwrap();
                    },
                    Err(e) => println!("{e}"),
                    _ =>{}
                }
            }
        });  

    let (mut socket,_response) = connect_async(url.to_string()).await.expect("Failed to connect");
    loop
    {
        print!(">");
        let _ = stdout().flush();

        let mut msg = String::new();
        std::io::stdin().read_line(&mut msg).unwrap();

        if msg.trim() == "exit"
        {
            t1.abort();
            break;
        }

        socket.send(Message::text(format!("[{}] {}",username.trim(),msg.trim()).to_string())).await?;
    }
    Ok(())
}
