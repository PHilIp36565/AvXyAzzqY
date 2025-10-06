# 代码生成时间: 2025-10-06 23:51:48
import tornado.ioloop
import tornado.web

# 数据库模型（这里用字典代替实际数据库）
inventory = {
    "products": []
}

# 产品类
class Product:
    def __init__(self, id, name, quantity):
        self.id = id
        self.name = name
        self.quantity = quantity

    def __str__(self):
        return f"Product(id={self.id}, name={self.name}, quantity={self.quantity})"

# 库存管理类
class InventoryManager:
    def add_product(self, product):
        inventory['products'].append(product)

    def get_product(self, product_id):
        for product in inventory['products']:
            if product.id == product_id:
                return product
        return None

    def update_product_quantity(self, product_id, new_quantity):
        product = self.get_product(product_id)
        if product:
            product.quantity = new_quantity
            return True
        return False

    def remove_product(self, product_id):
        global inventory
        inventory['products'] = [product for product in inventory['products'] if product.id != product_id]

# Tornado HTTP 路由
class ProductHandler(tornado.web.RequestHandler):
    def post(self):
        # 从请求体中获取产品信息
        data = tornado.escape.json_decode(self.request.body)
        product_id = data.get('id')
        name = data.get('name')
        quantity = data.get('quantity')

        try:
            product = Product(product_id, name, quantity)
            manager.add_product(product)
            self.write({'status': 'success', 'message': 'Product added successfully'})
        except Exception as e:
            self.write({'status': 'error', 'message': str(e)})

    def get(self, product_id=None):
        if product_id:
            product = manager.get_product(product_id)
            if product:
                self.write({'status': 'success', 'data': str(product)})
            else:
                self.write({'status': 'error', 'message': 'Product not found'})
        else:
            products = inventory['products']
            self.write({'status': 'success', 'data': [str(product) for product in products]})

    def put(self, product_id):
        # 更新产品库存数量
        new_quantity = tornado.escape.json_decode(self.request.body)
        success = manager.update_product_quantity(product_id, new_quantity)
        if success:
            self.write({'status': 'success', 'message': 'Product quantity updated successfully'})
        else:
            self.write({'status': 'error', 'message': 'Product not found'})

    def delete(self, product_id):
        # 从库存中移除产品
        manager.remove_product(product_id)
        self.write({'status': 'success', 'message': 'Product removed successfully'})

# 创建库存管理实例
manager = InventoryManager()

# 设置路由
def make_app():
    return tornado.web.Application([
        (r"/", ProductHandler),
        (r"/product/([0-9]+)", ProductHandler)
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("Supply Chain Management System is running on http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()