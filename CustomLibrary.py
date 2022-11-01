#from TestObject import TestObject
from robot.api.logger import info, debug, trace, console
import os
import shutil
import subprocess

class CustomLibrary:
    ROBOT_LIBRARY_SCOPE = 'SUITE'
    
    def __init__(self) -> None:
        self.folder = ""
    
    def clone(self, url, folder):
        if os.path.exists(folder):
            shutil.rmtree(folder)
        
        self.folder = folder
        
        # Clone source code from github
        clone_cmd = ["git", "clone", url, "-b script", folder]
        sub = subprocess.Popen(" ".join(clone_cmd), shell=True)
        return sub.wait()

    def get_git_hash(self):
        return os.popen("git log -1 | grep 'commit' | awk -F ' ' '{print$2}'").read()
    
    def submodule_init(self):
        # Init submodule
        os.chdir(self.folder)
        init_cmd = ["git", "submodule", "update", "--init"]
        sub = subprocess.Popen(" ".join(init_cmd), shell=True)
        return sub.wait()

    def apply_patch(self):
        apply_patch_cmd = ["bash", "sh_script/preparation.sh"]
        sub = subprocess.Popen(" ".join(apply_patch_cmd), shell=True)
        return sub.wait()
            
    def build(self, item):
        build_cmd = ["bash", "sh_script/build_final.sh", item]
        sub = subprocess.Popen(" ".join(build_cmd), shell=True)
        return sub.wait()
    
    def afl_test(self, time):
        afl_cmd = ["bash", "sh_script/fuzzing.sh", "-n", "afl_all", "-t", time]
        sub = subprocess.Popen(" ".join(afl_cmd), shell=True)
        return sub.wait()

    def libfuzzer_test(self, time):
        libfuzzer_cmd = ["bash", "sh_script/fuzzing.sh", "-n", "libfuzzer_all", "-t", time]
        sub = subprocess.Popen(" ".join(libfuzzer_cmd), shell=True)
        return sub.wait()
    
    def integration_test(self, cpus, memory, firmware):
        cmd = ["bash", "sh_script/integration_tdx_15.sh", "-c", cpus, "-m", memory, "-f", firmware]
        sub = subprocess.Popen(" ".join(cmd), shell=True)
        return sub.wait()
    
    
    
    