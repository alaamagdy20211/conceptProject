inventory = {}
total_sales = 0.0



def add_product(product_id, name, price, quantity):
    if product_id in inventory:
        print(f"Error: Product with ID {product_id} already exists.")
        return
    inventory[product_id] = {"name": name, "price": price, "quantity": quantity}


def update_product(product_id, name=None, price=None, quantity=None):
    if product_id not in inventory:
        print(f"Error: Product with ID {product_id} does not exist.")
        return
    if name:
        inventory[product_id]["name"] = name
    if price is not None:
        inventory[product_id]["price"] = price
    if quantity is not None:
        inventory[product_id]["quantity"] = quantity


def remove_product(product_id):
    if product_id not in inventory:
        print(f"Error: Product with ID {product_id} does not exist.")
        return
    del inventory[product_id]



def update_stock(product_id, quantity_change):
    if product_id not in inventory:
        print(f"Error: Product with ID {product_id} does not exist.")
        return
    inventory[product_id]["quantity"] += quantity_change
    if inventory[product_id]["quantity"] < 0:
        print(f"Error: Stock for {product_id} cannot go below zero.")
        inventory[product_id]["quantity"] -= quantity_change 



def notify_low_stock(threshold):
    low_stock_items = [product_id for product_id, details in inventory.items() if details["quantity"] < threshold]
    if low_stock_items:
        print(f"Low stock items: {', '.join(low_stock_items)}")
    else:
        print("No low-stock items.")



def process_order(orders):
    global total_sales
    total_cost = 0.0
    for product_id, quantity in orders.items():
        if product_id not in inventory:
            print(f"Error: Product {product_id} is not available.")
            return
        if inventory[product_id]["quantity"] < quantity:
            print(f"Error: Not enough stock for {product_id}.")
            return
        inventory[product_id]["quantity"] -= quantity
        total_cost += inventory[product_id]["price"] * quantity
    total_sales += total_cost
    print(f"Order processed. Total cost: ${total_cost:.2f}")



def generate_reports():
    print("\nReports:")
    print("-" * 20)
    print("Low Stock Items:")
    notify_low_stock(10)
    print(f"Total Sales: ${total_sales:.2f}")
    inventory_value = sum(details["price"] * details["quantity"] for details in inventory.values())
    print(f"Total Inventory Value: ${inventory_value:.2f}")


 
add_product("001", "Laptop", 1500.0, 10)
add_product("002", "Mouse", 25.0, 10)
add_product("003", "alaa", 25.0, 10)
 
update_product("001", quantity=15)
# remove_product("003")
print (inventory)
   
process_order({"001": 2, "002": 5})
process_order({"003": 2, "002": 5})
notify_low_stock(10)

generate_reports()