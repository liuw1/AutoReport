import subprocess
from sendmail import SendEmail

if __name__ == "__main__":
    robot_cmd = ["robot", "tdshim.robot"]
    
    test = subprocess.Popen(" ".join(robot_cmd), shell=True)
    test.wait()
    
    email = SendEmail()
    email.send_mail()
