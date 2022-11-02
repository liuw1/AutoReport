import os
import subprocess
from sendmail import SendEmail

cwd = os.getcwd()

def clean():
    file_list = ["log.html", "output.xml", "report.html"]
    for file in file_list:
        file_path = os.path.join(cwd, file)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                print(e)

if __name__ == "__main__":
    clean()
    
    robot_cmd = ["robot", "robot/tdshim.robot"]
    
    test = subprocess.Popen(" ".join(robot_cmd), shell=True)
    test.wait()
    
    email = SendEmail()
    email.send_mail()
