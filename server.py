import subprocess
import threading
import queue

class Server():
    def __init__(self):
        self.p = None
        self.running = False
        self.t = None
        self.outq = queue.Queue()

    def log_w(self, line):
        with open("log.txt", "a") as f:
            f.write(line)

    def log_r(self):
        try:
            line = self.outq.get(block=False)
            return line
        except queue.Empty:
            return None

    def logd(self):
        while self.running:
            for line in iter(self.p.stdout.readline, b""):
                line = line.decode()
                self.outq.put(line)
                self.log_w(line)
            if not self.running:
                break
            if self.p.poll() != None:
                self.p = subprocess.Popen("bds/bedrock_server.exe", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def start(self):
        if not self.running:
            self.p = subprocess.Popen("bds/bedrock_server.exe", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.running = True
            self.t = threading.Thread(target=self.logd)
            self.t.start()
            return "成功"
        else:
            return "服务器已开启"

    def stop(self):
        if self.running:
            self.running=False
            self.p.stdin.write(b"stop\n")
            self.p.stdin.flush()
            self.p.wait(timeout=3)
            self.t.join()
            return "成功"
        else:
            return "服务器未开启"
    
    def kill(self):
        if self.running:
            self.running=False
            self.p.kill()
            self.t.join()
            return "成功"
        else:
            return "服务器未开启"
    
    def command(self, cmd):
        if self.running:
            cmd = bytes(cmd+"\n", "utf-8")
            self.p.stdin.write(cmd)
            self.p.stdin.flush()
            return "成功"
        else:
            return "失败"