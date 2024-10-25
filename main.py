import mysql.connector
from mysql.connector import Error

class InventoryManagement:
    def __init__(self):
        self.connection = self.create_connection()

    def create_connection(self):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='your_username',
                password='your_password',
                database='local_store_inventory'
            )
            if connection.is_connected():
                print("Connected to MySQL database")
                return connection
        except Error as e:
            print(f"Error: {e}")
            return None

    def add_product(self, name, category, stock_quantity, price):
        cursor = self.connection.cursor()
        query = "INSERT INTO products (name, category, stock_quantity, price) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (name, category, stock_quantity, price))
        self.connection.commit()
        print("Product added successfully")

    def view_products(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
        for product in products:
            print(product)

    def update_product(self, product_id, name=None, category=None, price=None, stock_quantity=None):
        cursor = self.connection.cursor()
        fields = []
        values = []
        
        if name:
            fields.append("name = %s")
            values.append(name)
        if category:
            fields.append("category = %s")
            values.append(category)
        if price:
            fields.append("price = %s")
            values.append(price)
        if stock_quantity is not None:
            fields.append("stock_quantity = %s")
            values.append(stock_quantity)
        
        values.append(product_id)
        query = f"UPDATE products SET {', '.join(fields)} WHERE id = %s"
        cursor.execute(query, values)
        self.connection.commit()
        print("Product updated successfully")

    def delete_product(self, product_id):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
        self.connection.commit()
        print("Product deleted successfully")

    def low_stock_alert(self, threshold=5):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM products WHERE stock_quantity < %s", (threshold,))
        low_stock_products = cursor.fetchall()
        for product in low_stock_products:
            print(product)

    def search_products(self, name=None, category=None):
        cursor = self.connection.cursor()
        query = "SELECT * FROM products WHERE"
        conditions = []
        values = []

        if name:
            conditions.append(" name LIKE %s")
            values.append(f"%{name}%")
        if category:
            conditions.append(" category LIKE %s")
            values.append(f"%{category}%")
        
        query += " AND".join(conditions)
        cursor.execute(query, values)
        results = cursor.fetchall()
        for product in results:
            print(product)

    def sort_products(self, by='price'):
        cursor = self.connection.cursor()
        query = f"SELECT * FROM products ORDER BY {by}"
        cursor.execute(query)
        sorted_products = cursor.fetchall()
        for product in sorted_products:
            print(product)

    def close_connection(self):
        if self.connection.is_connected():
            self.connection.close()
            print("MySQL connection closed")

if __name__ == "__main__":
    inventory = InventoryManagement()
    # Example usage:
    inventory.add_product('Apple', 'Groceries', 50, 0.5)
    inventory.view_products()
    inventory.update_product(1, stock_quantity=45)
    inventory.low_stock_alert()
    inventory.search_products(name='Apple')
    inventory.sort_products(by='stock_quantity')
    inventory.delete_product(1)
    inventory.close_connection()
