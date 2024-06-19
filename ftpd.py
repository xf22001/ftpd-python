from pyftpdlib.handlers import FTPHandler
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.servers import FTPServer
import asyncio


class ThrottledFTPHandler(FTPHandler):
    def __init__(self, conn, server, ioloop=asyncio.get_event_loop()):
        super().__init__(conn, server, ioloop=ioloop)
        # 设置下载速度限制：比如每秒限制 100 KB
        self.read_limit = 100 * 1024


def main():
    # 实例化虚拟用户授权器
    authorizer = DummyAuthorizer()

    # 添加用户权限和路径，这里密码设置为 "12345"
    authorizer.add_user("user", "12345", ".", perm="elradfmw")

    # 匿名用户只读权限
    authorizer.add_anonymous(".", perm="elr")

    # 初始化 FTP 服务器处理器并设置用户授权器
    handler = ThrottledFTPHandler
    handler.authorizer = authorizer

    # 创建 FTP 服务器实例并运行
    server = FTPServer(("0.0.0.0", 2121), handler)
    server.serve_forever()


if __name__ == "__main__":
    main()
