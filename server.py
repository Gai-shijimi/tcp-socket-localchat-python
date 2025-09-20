import socket
import os


server_address = '/tmp/socket_file'

try:
    os.unlink(server_address)
except FileNotFoundError:
    pass

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
print('サーバーを起動しています....{}'.format(server_address))
sock.bind(server_address)
sock.listen(1)

while True:
    connection, client_address = sock.accept()
    print('クライアントと接続しました。')
    try :
        print('接続先', client_address)

        file = connection.makefile('rwb', buffering=0)
        for line in file:
            msg = line.rstrip(b'\n').decode('utf-8')
            print('受信:', msg)
            response = ('サーバーからの応答:'+msg + '\n').encode('utf-8')
            file.write(response)
        print('クライアント切断')

    finally:
        print("現在の接続を閉じます。")
        connection.close()

