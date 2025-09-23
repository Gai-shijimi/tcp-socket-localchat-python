import socket
import sys
import signal

def handler(signum, _):
    print(f"{signum}を受け取りました。終了します。")
    sys.exit(0)


sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
server_address = '/tmp/socket_file'
print('{}に接続します'.format(server_address))


try:
    sock.connect(server_address)
except socket.error as err:
    print(err)
    sys.exit(1)

file = sock.makefile('rwb', buffering=0)

signal.signal(signal.SIGINT, handler)

try:
    while True:
        message = input("message >>> ")
        file.write((message + '\n').encode('utf-8'))

        data = file.readline()
        print('サーバーからの応答: ', data.decode('utf-8').rstrip('\n'))
        

        if not data:
            print('サーバーが切断しました')
            break

finally:
    print('ソケットを閉じます')
    sock.close()