# set up virtual environment
python -m venv venv
venv\Scripts\activate

#install dependencies
pip install -r requirements.txt

#set up mysql dependencies
mysql -u root -p

#create database in terminal
CREATE DATABASE sandwich_maker_api;
USE sandwich_maker_api;
SHOW DATABASES;

# run app
uvicorn api.main:app --reload


## INPUT DATA INTO MYSQL or in terminal
USE sandwich_maker_api;

-- Insert test users
INSERT INTO customers (name, email, phone_number, address, password, saved_payment, created_at, updated_at)
VALUES
('Audy Vee', 'veeaudy@example.com', '1234567890', '123 Elm Street, Springfield', 'audy1234', NULL, NOW(), NOW()),
('John Doe', 'john.doe@example.com', '9876543210', '456 Oak Street, Springfield', 'john1234', NULL, NOW(), NOW());

-- Insert menu items
INSERT INTO menu_items (name, description, ingredients, price, calories, menu_category, dietary_category, available)
VALUES
('Classic Burger', 'A juicy grilled beef burger with lettuce, tomato, and cheese.', 'Beef Patty, Lettuce, Tomato, Cheese, Bun', 9.99, 700, 'Main Course', 'Non-Vegetarian', TRUE),
('Grilled Chicken Sandwich', 'Grilled chicken breast sandwich with lettuce and mayo.', 'Chicken Breast, Lettuce, Mayo, Bun', 12.99, 500, 'Main Course', 'Non-Vegetarian', TRUE),
('Veggie Wrap', 'A healthy wrap filled with fresh vegetables and hummus.', 'Lettuce, Tomato, Cucumber, Hummus, Tortilla', 8.49, 350, 'Main Course', 'Vegetarian', TRUE),
('Chocolate Shake', 'Rich and creamy chocolate milkshake.', 'Milk, Chocolate Syrup, Ice Cream', 5.99, 450, 'Beverage', 'Vegetarian', TRUE);

-- place order

{
  "customer_name": "Audy Vee",
  "email": "veeaudy@example.com",
  "phone_number": "1234567890",
  "address": "123 Elm Street, Springfield",
  "menu_items": [
    {
      "menu_item_id": 1,
      "quantity": 2
    },
    {
      "menu_item_id": 2,
      "quantity": 1
    },
    {
      "menu_item_id": 3,
      "quantity": 1
    },
    {
      "menu_item_id": 4,
      "quantity": 1
    }
  ]
}
