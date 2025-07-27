import sciter

import os

from client import socket_client

class Frame(sciter.Window):

    def __init__(self):
        super().__init__(ismain=True, uni_theme=True, size=(800, 600))
        self.client = socket_client()
        pass

    # 可以在tis脚本中通过view.call_python()调用此函数
    @sciter.script
    def call_python(self, arg):
        print('成功调用Python函数')
        pass

    @sciter.script
    def get_jlccam_work_directory(self):
        ret = self.client.send_command('script_get_work_directory')
        dir = ret["result"]
        dir = os.path.normpath(dir) # 路径标准化，去除对父级目录的引用
        return dir
    
    @sciter.script
    def get_jlccam_job_list(self):
        workdir = self.get_jlccam_work_directory()
        job_list = []
        for root, dirs, files in os.walk(workdir):
            for file in files:
                if file.endswith(".ddw"):
                    job_list.append(file[:-4])
        return job_list

    
if __name__ == '__main__':
    sciter.runtime_features(allow_sysinfo=True, file_io=True)

    htm = os.path.join(os.path.dirname(__file__), 'pysciter.htm')

    frame = Frame()
    frame.set_dispatch_options(raw_handlers=False)
    frame.load_file(htm)
    frame.run_app()
