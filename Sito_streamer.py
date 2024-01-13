import socket
from datetime import datetime
import os
import threading
from flask import Flask, jsonify

app = Flask(__name__)

def connect_to_twitch(channel):
    server = "irc.chat.twitch.tv"
    port = 6667
    token = "oauth:531khtxtr53s32dr3s93407nmwixig"

    irc = socket.socket()
    irc.connect((server, port))
    irc.send(f"PASS {token}\r\n".encode("utf-8"))
    irc.send(f"NICK metjum\r\n".encode("utf-8"))
    irc.send(f"JOIN #{channel}\r\n".encode("utf-8"))

    return irc

def get_twitch_messages(irc, channel):
    today = datetime.now().strftime("%Y-%m-%d")
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
    log_file_path = os.path.join(log_dir, f"{channel}_log_{today}.txt")
    html_file_path = "index.html" 

    try:
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        while True:
            data = irc.recv(1024).decode("utf-8")

            if data.startswith("PING"):
                irc.send("PONG\r\n".encode("utf-8"))
            elif "PRIVMSG" in data:
                username = data.split(":", 2)[1].split("!", 1)[0]
                message = data.split(":", 2)[2].strip()  
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_line = f"{timestamp} {username}: {message}\n"

                with open(log_file_path, "a", encoding="utf-8") as log_file:
                    log_file.write(log_line)

                print(log_line, end='')

    except FileNotFoundError:
        print(f"Error: The file '{log_file_path}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

@app.route('/messages/<channel>', methods=['GET'])
def get_messages(channel):
    today = datetime.now().strftime("%Y-%m-%d")
    log_file_path = f"logs/{channel}_log_{today}.txt"

    try:
        with open(log_file_path, "r", encoding="utf-8") as log_file:
            messages = log_file.readlines()
            return jsonify(messages)

    except FileNotFoundError:
        return jsonify({"error": f"File '{log_file_path}' not found"}), 404
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500

def start_twitch_monitoring(channels):
    irc_connections = {channel: connect_to_twitch(channel) for channel in channels}
    threads = []

    for channel, irc in irc_connections.items():
        thread = threading.Thread(target=get_twitch_messages, args=(irc, channel), daemon=True)
        threads.append(thread)
        thread.start()

if __name__ == "__main__":
    channels = ["haiset", "metjum", "xqc"] 
    threading.Thread(target=start_twitch_monitoring, args=(channels,), daemon=True).start()
    app.run(debug=True)
