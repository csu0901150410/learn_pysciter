import sciter

import os

class Frame(sciter.Window):

    def __init__(self):
        super().__init__(ismain=True, uni_theme=True)
        pass

    # 可以在tis脚本中通过view.call_python()调用此函数
    @sciter.script
    def call_python(self, arg):
        print('成功调用Python函数')
        pass

    
if __name__ == '__main__':
    sciter.runtime_features(allow_sysinfo=True, file_io=True)

    htm = os.path.join(os.path.dirname(__file__), 'pysciter.htm')

    frame = Frame()
    frame.set_dispatch_options(raw_handlers=False)
    frame.load_file(htm)
    frame.run_app()
