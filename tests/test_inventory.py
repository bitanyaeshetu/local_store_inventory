import unittest
from main import InventoryManagement  # Adjust the import based on your structure

class TestInventoryManagement(unittest.TestCase):
    def setUp(self):
        self.inventory = InventoryManagement()

    def test_add_product(self):
        self.inventory.add_product('Test Product', 'Category', 10, 5.99)
        # Here you could add assertions to check if the product was added correctly

    # Add more tests as needed

if __name__ == '__main__':
    unittest.main()
