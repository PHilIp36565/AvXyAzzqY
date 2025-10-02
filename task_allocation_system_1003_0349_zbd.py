# 代码生成时间: 2025-10-03 03:49:24
import tornado.ioloop
import tornado.web
import json

# 定义一个全局的任务存储
tasks = []

class TaskHandler(tornado.web.RequestHandler):
    """
    用于处理任务分配的请求。
    """
    def post(self):
        """
        接收新任务并将其添加到任务列表中。
        """
        try:
            # 解析请求体中的JSON数据
            task_data = json.loads(self.request.body)
            # 检查必要的字段
            if 'task_id' not in task_data or 'description' not in task_data:
                self.set_status(400)  # 400 Bad Request
                self.write({'error': 'Missing task_id or description'})
                return
            # 将任务添加到全局任务列表中
            task = {'task_id': task_data['task_id'], 'description': task_data['description']}
            tasks.append(task)
            self.write({'message': 'Task added successfully', 'task': task})
        except json.JSONDecodeError:
            self.set_status(400)  # 400 Bad Request
            self.write({'error': 'Invalid JSON format'})
        except Exception as e:
            self.set_status(500)  # 500 Internal Server Error
            self.write({'error': str(e)})

    def get(self):
        """
        获取当前所有任务的列表。
        """
        try:
            self.write({'tasks': tasks})
        except Exception as e:
            self.set_status(500)  # 500 Internal Server Error
            self.write({'error': str(e)})

def make_app():
    """
    创建并返回Tornado应用程序。
    """
    return tornado.web.Application(
        handlers=[
            (r"/", TaskHandler),
        ],
        debug=True,  # 开启调试模式
    )

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)  # 监听端口
    print("Task Allocation System server started on http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()