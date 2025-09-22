# 代码生成时间: 2025-09-23 01:22:08
import tornado.ioloop
import tornado.web
import json

# 库存管理系统数据库模型
class InventoryModel:
    def __init__(self):
        self.inventory = {}

    def add_product(self, product_id, quantity):
        if product_id in self.inventory:
            self.inventory[product_id] += quantity
        else:
            self.inventory[product_id] = quantity

    def remove_product(self, product_id, quantity):
        if product_id in self.inventory:
            if self.inventory[product_id] >= quantity:
                self.inventory[product_id] -= quantity
                if self.inventory[product_id] == 0:
                    del self.inventory[product_id]
            else:
                raise ValueError("Insufficient inventory for product ID: {}".format(product_id))
        else:
            raise ValueError("There is no such product in inventory with ID: {}".format(product_id))

    def get_inventory(self):
        return self.inventory

# 库存管理请求处理器
class InventoryHandler(tornado.web.RequestHandler):
    def initialize(self, inventory_model):
        self.inventory_model = inventory_model

    def post(self):
        try:
            product_data = json.loads(self.request.body)
            product_id = product_data["product_id"]
            quantity = product_data["quantity"]
            self.inventory_model.add_product(product_id, quantity)
            self.write({
                "status": "success",
                "message": "Product added to inventory."
            })
        except (ValueError, KeyError) as e:
            self.write({
                "status": "error",
                "message": str(e)
            })
            self.set_status(400)

    def delete(self):
        try:
            product_id = self.get_query_argument("product_id")
            quantity = self.get_query_argument("quantity\)
            self.inventory_model.remove_product(product_id, int(quantity))
            self.write({
                "status": "success",
                "message": "Product removed from inventory."
            })
        except (ValueError, KeyError) as e:
            self.write({
                "status": "error",
                "message": str(e)
            })
            self.set_status(400)

    def get(self):
        inventory = self.inventory_model.get_inventory()
        self.write({
            "status": "success",
            "inventory": inventory
        })

# 库存管理应用
class InventoryApplication(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/inventory", InventoryHandler, dict(inventory_model=InventoryModel())),
        ]
        tornado.web.Application.__init__(self, handlers)

# 主函数
def main():
    application = InventoryApplication()
    application.listen(8888)
    print("Inventory management system is running on http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()