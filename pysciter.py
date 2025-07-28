import sciter

import os
import json

import tkinter as tk

from client import socket_client

main_client = None

def get_main_client():
    global main_client
    if main_client is None:
        main_client = socket_client()
    return main_client

COMMANDS = {}

def register_command(name):
    def decorator(func):
        COMMANDS[name] = func
        return func
    return decorator

def execute_command(name, json_params = None):
    if name not in COMMANDS:
        return {"error": f"Command '{name}' not registered"}
    
    try:
        if isinstance(json_params, str):
            params = json.loads(json_params) if json_params else {}
        elif isinstance(json_params, dict):
            params = json_params
        else:
            params = {}
        return COMMANDS[name](params)
    except json.JSONDecodeError as e:
        return {"error": f"Invalid JSON parameters: {str(e)}"}
    except Exception as e:
        return {"error": str(e)}
    
# 注册命令
@register_command("hello_world")
def hello_world(params):
    print("命令 hello_world 被调用")
    print(f"参数: {str(params)}")
    pass

@register_command("open_job")
def open_job(params):
    jobname = params.get("jobname")
    show = params.get("show", True)
    js = {}
    js["job"] = jobname
    js["show"] = show
    return get_main_client().send_command("script_open_job", js)


class Frame(sciter.Window):

    def __init__(self):
        root = tk.Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.destroy()
        
        x = (screen_width - 800) / 2
        y = (screen_height - 600) / 2

        super().__init__(ismain=True, uni_theme=True, size=(800, 600), pos=(int(x), int(y)))
        self.client = get_main_client()
        pass

    # 调用jlccam接口
    def send_command(self, commandname, paramdict={}):
        return self.client.send_command(commandname, paramdict)

    # tis脚本通过view.call_command(xxx, params);调用名字为xxx的命令
    @sciter.script
    def call_command(self, command_name, json_params = None):
        return execute_command(command_name, json_params)

    @sciter.script
    def get_jlccam_work_directory(self):
        ret = self.send_command('script_get_work_directory')
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
