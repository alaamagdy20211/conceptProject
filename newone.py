from typing import List, Dict, Tuple, Optional


# Define a type alias for Product
Product = Dict[str, Tuple[str, float, int]] 

# Initialize an empty inventory
def initialize_inventory() -> Product:
    return {}

# Check if the product exists in the inventory (no in operator)
def product_exists(inventory: Product, product_id: str) -> bool:
    return product_id in inventory  

# Add a product to the inventory (without using built-in methods or loops)
def add_product(inventory: Product, product_id: str, name: str, price: float, quantity: int) -> Product:
    if product_exists(inventory, product_id): 
        return inventory  
    return {product_id: (name, price, quantity)} | inventory  

# Update a product in the inventory
def update_product(inventory: dict, product_id: str, name: Optional[str] = None, 
                   price: Optional[float] = None, quantity: Optional[int] = None) -> dict:
    if product_id not in inventory: 
        return inventory  
    
    # Retrieve current product details
    current_name, current_price, current_quantity = inventory[product_id]
    
    # Update only the specified fields
    updated_name = name if name is not None else current_name
    updated_price = price if price is not None else current_price
    updated_quantity = quantity if quantity is not None else current_quantity
    
    # Create a new inventory with the updated product details
    updated_inventory = inventory.copy()
    updated_inventory[product_id] = (updated_name, updated_price, updated_quantity)
    
    return updated_inventory

# Remove a product from the inventory
def remove_product(inventory: dict, product_id: str) -> dict:
   
    if not inventory:
        return {}

    # Extract the first key-value pair
    key, value = next(iter(inventory.items()))

    # Remove the current key-value pair from the rest of the inventory
    rest_inventory = inventory.copy()
    rest_inventory.pop(key)

    # Recursively process the rest of the inventory
    updated_inventory = remove_product(rest_inventory, product_id)

    # Include the current key-value pair only if the key is not the product_id
    if key == product_id:
        return updated_inventory
    return {key: value, **updated_inventory}


# Notify if stock is below threshold (without loops)
def notify_low_stock(inventory: Product, threshold: int) -> List[str]:
    def filter_low_stock(products: List[Tuple[str, Tuple[str, float, int]]]) -> List[str]:
        if len(products) == 0:
            return []
        product_id, (_, _, quantity) = products[0]
        rest = filter_low_stock(products[1:])
        if quantity < threshold:
            return [product_id] + rest
        return rest
    
    return filter_low_stock(list(inventory.items()))  # Convert dictionary to list and filter manually

def process_order_and_check_low_stock_recursive(inventory: dict, orders: list, threshold: int) -> tuple:
    # Base case: no more orders to process
    if not orders:
        low_stock = notify_low_stock_recursive(inventory, threshold)  # Use a recursive implementation of notify_low_stock
        return inventory, 0.0, low_stock

    # Process the first order
    product_id, quantity = orders[0]
    if product_id not in inventory:
        raise ValueError(f"Product {product_id} does not exist.")
    name, price, stock = inventory[product_id]
    if stock < quantity:
        raise ValueError(f"Not enough stock for product {product_id}.")

    # Recursively update stock for the current product
    def update_stock_recursively(inv: dict, pid: str, qty_change: int) -> dict:
        if not inv:  # Base case: empty inventory
            return {}
        key, value = next(iter(inv.items()))
        rest_inv = inv.copy()
        rest_inv.pop(key)
        updated_rest = update_stock_recursively(rest_inv, pid, qty_change)
        if key == pid:
            name, price, stock = value
            return {key: (name, price, stock + qty_change), **updated_rest}
        return {key: value, **updated_rest}

    updated_inventory = update_stock_recursively(inventory, product_id, -quantity)

    # Recursively process the rest of the orders
    remaining_inventory, total_cost, low_stock = process_order_and_check_low_stock_recursive(
        updated_inventory,
        orders[1:], 
        threshold
    )

    # Add the cost of the current product
    total_cost += price * quantity

    return remaining_inventory, total_cost, low_stock

# Recursive implementation of notify_low_stock
def notify_low_stock_recursive(inventory: dict, threshold: int) -> list:
    if not inventory:  
        return []

    # Extract the first key-value pair
    key, value = next(iter(inventory.items()))
    name, price, quantity = value
    remaining_inventory = inventory.copy()
    remaining_inventory.pop(key)

    # If the quantity is below the threshold, add the product_id to the result
    if quantity < threshold:
        return [key] + notify_low_stock_recursive(remaining_inventory, threshold)

    # Otherwise, skip the current product and recurse on the rest
    return notify_low_stock_recursive(remaining_inventory, threshold)

# Generate low stock report (without using built-in functions or loops)
def generate_low_stock_report(inventory: Product, threshold: int) -> List[Tuple[str, int]]:
    def filter_low_stock(products: List[Tuple[str, Tuple[str, float, int]]], threshold: int) -> List[Tuple[str, int]]:
        if len(products) == 0:
            return []
        product_id, (_, _, quantity) = products[0]
        rest = filter_low_stock(products[1:], threshold)
        if quantity < threshold:
            return [(product_id, quantity)] + rest
        return rest
    
    return filter_low_stock(list(inventory.items()), threshold) 

# Generate sales report
def generate_sales_report(total_sales: float) -> str:
    return f"Total Sales: ${total_sales:.2f}"

# Generate inventory value report
def generate_inventory_value_report(inventory: Product) -> float:
    def calculate_inventory_value(products: List[Tuple[str, Tuple[str, float, int]]]) -> float:
        if len(products) == 0:
            return 0.0
        _, (_, price, quantity) = products[0]
        rest = calculate_inventory_value(products[1:])
        return price * quantity + rest
    
    return calculate_inventory_value(list(inventory.items()))  # Recursively calculate inventory value


# Example Usage


inventory = initialize_inventory()

   # Adding products using add_product
inventory = add_product(inventory, "001", "Laptop", 1500.0, 10)
inventory = add_product(inventory, "002", "Mouse", 25.0, 50)
inventory = add_product(inventory, "003", "Keyboard", 100.0, 5)
inventory = add_product(inventory, "004", "alaa", 100.0, 5)
    # Now we will update the stock using update_product
inventory = update_product(inventory, "001", quantity=8)  # Update stock for Laptop
inventory = update_product(inventory, "002", quantity=45)  # Update stock for Mouse

    # Order details as a list of tuples
orders = [("001", 2), ("003", 4)]  # Order for 2 Laptops and 4 Keyboards
print("Initial Inventory:", inventory)

    # Removing a product (e.g., Monitor)
inventory = remove_product(inventory, "004")
print("Inventory after removing 'Monitor':", inventory)
    # Placing the order
try:
        inventory, total_cost, low_stock = process_order_and_check_low_stock_recursive(
            inventory,
            orders,     
            threshold=10 
        )
        print(generate_sales_report(total_cost))
        print("Low Stock:", low_stock)
        print(f"Inventory Value: ${generate_inventory_value_report(inventory):.2f}")
except ValueError as e:
 print(e)