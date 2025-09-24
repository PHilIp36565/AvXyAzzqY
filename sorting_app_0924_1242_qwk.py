# 代码生成时间: 2025-09-24 12:42:37
import tornado.ioloop
import tornado.web
import tornado.options

# 定义全局变量存储排序算法名称
SORTING_ALGORITHMS = {
    "bubble_sort": self.bubble_sort,
    "insertion_sort": self.insertion_sort,
    "quick_sort": self.quick_sort
}

class SortingHandler(tornado.web.RequestHandler):
    """
    Handlers for sorting requests.
    It accepts GET requests with a list of numbers and a sorting algorithm.
    """
    def get(self):
        try:
            numbers_str = self.get_query_argument('numbers')
            algorithm = self.get_query_argument('algorithm')
            numbers = list(map(int, numbers_str.split(',')))
            if algorithm in SORTING_ALGORITHMS:
                sorted_numbers = SORTING_ALGORITHMS[algorithm](numbers)
                self.write({'sorted': sorted_numbers})
            else:
                self.set_status(400)
                self.write({'error': 'Invalid sorting algorithm specified'})
        except ValueError:
            self.set_status(400)
            self.write({'error': 'Invalid input provided'})

    def bubble_sort(self, arr):
        """
        Performs bubble sort on the given array.
        
        :param arr: List of numbers to sort.
        :return: Sorted list of numbers.
        """
        n = len(arr)
        for i in range(n):
            for j in range(0, n-i-1):
                if arr[j] > arr[j+1]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
        return arr

    def insertion_sort(self, arr):
        """
        Performs insertion sort on the given array.
        
        :param arr: List of numbers to sort.
        :return: Sorted list of numbers.
        """
        for i in range(1, len(arr)):
            key = arr[i]
            j = i-1
            while j >= 0 and key < arr[j]:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key
        return arr

    def quick_sort(self, arr):
        """
        Performs quick sort on the given array.
        
        :param arr: List of numbers to sort.
        :return: Sorted list of numbers.
        """
        if len(arr) <= 1:
            return arr
        else:
            pivot = arr[0]
            less = [x for x in arr[1:] if x <= pivot]
            greater = [x for x in arr[1:] if x > pivot]
            return self.quick_sort(less) + [pivot] + self.quick_sort(greater)

def main():
    parser = tornado.options.OptionParser()
    parser.add_option('-p', '--port', default=8888, type=int, help='run on the given port')
    options = parser.parse_command_line()
    app = tornado.web.Application(
        [(r'/sort', SortingHandler)],
        debug=True
    )
    app.listen(options.port)
    print('Sorting application is running on http://localhost:%d' % options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()