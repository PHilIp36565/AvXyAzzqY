# 代码生成时间: 2025-09-15 20:48:42
import tornado.ioloop
import tornado.web

# 排序算法实现
class SortingAlgorithm:
    def __init__(self):
        pass

    # 冒泡排序
    def bubble_sort(self, arr):
        """
        冒泡排序算法实现
        
        参数:
            arr (list): 待排序的列表
        
        返回:
            list: 排序后的列表
        """
        n = len(arr)
        for i in range(n):
            for j in range(0, n-i-1):
                if arr[j] > arr[j+1]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
        return arr

    # 快速排序
    def quick_sort(self, arr):
        """
        快速排序算法实现
        
        参数:
            arr (list): 待排序的列表
        
        返回:
            list: 排序后的列表
        """
        if len(arr) <= 1:
            return arr
        else:
            pivot = arr[0]
            less_than_pivot = [x for x in arr[1:] if x <= pivot]
            greater_than_pivot = [x for x in arr[1:] if x > pivot]
            return self.quick_sort(less_than_pivot) + [pivot] + self.quick_sort(greater_than_pivot)

class SortingHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            sorting_algorithm = SortingAlgorithm()
            # 测试冒泡排序
            test_list = [64, 34, 25, 12, 22, 11, 90]
            sorted_list = sorting_algorithm.bubble_sort(test_list)
            self.write(f"Bubble Sort Result: {sorted_list}")

            # 测试快速排序
            sorted_list = sorting_algorithm.quick_sort(test_list)
            self.write(f"Quick Sort Result: {sorted_list}")
        except Exception as e:
            self.write(f"Error: {e}")

def make_app():
    return tornado.web.Application([
        (r"/", SortingHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("Server is running on http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()