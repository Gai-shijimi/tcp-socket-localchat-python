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


try:

    while True:
        connection, _ = sock.accept()
        print('クライアントと接続しました。')
        try:
            file = connection.makefile('rwb', buffering=0)
            for line in file:
                msg = line.rstrip(b'\n').decode('utf-8')
                print('受信:', msg)
                response = ('サーバーからの応答:'+msg + '\n').encode('utf-8')
                file.write(response)

        finally:
            print("現在の接続を閉じます。")
            connection.close()

except KeyboardInterrupt:
    print("\nKeyboardInterruptを受け取りました。サーバーを終了します。")

finally:
    sock.close()
    print("ソケットを閉じました。終了します。")

