-- Table: customers 
CREATE TABLE customers ( 
customer_id INT PRIMARY KEY, 
name VARCHAR(100) NOT NULL, 
email VARCHAR(100) UNIQUE NOT NULL, 
country VARCHAR(50) NOT NULL 
);

 -- Table: orders 
CREATE TABLE orders ( 
order_id INT PRIMARY KEY, 
customer_id INT NOT NULL, 
order_date DATE NOT NULL, 
total_amount DECIMAL(10, 2) NOT NULL, 
status VARCHAR(20) NOT NULL, 
FOREIGN KEY (customer_id) REFERENCES customers(customer_id) 
); 

-- Table: products 
CREATE TABLE products ( 
product_id INT PRIMARY KEY, 
product_name VARCHAR(100) NOT NULL, 
category_id INT NOT NULL, 
FOREIGN KEY (category_id) REFERENCES categories(category_id) 
); 

-- Table: order_items 
CREATE TABLE order_items ( 
item_id INT PRIMARY KEY, 
order_id INT NOT NULL, 
product_id INT NOT NULL, 
quantity INT NOT NULL, 
price DECIMAL(10, 2) NOT NULL, 
FOREIGN KEY (order_id) REFERENCES orders(order_id), 
FOREIGN KEY (product_id) REFERENCES products(product_id) 
); 



-- Table: categories 
CREATE TABLE categories ( 
category_id INT PRIMARY KEY, 
category_name VARCHAR(100) NOT NULL 
); -- Table: reviews 
CREATE TABLE reviews ( 
review_id INT PRIMARY KEY, 
product_id INT NOT NULL, 
customer_id INT NOT NULL, 
rating INT CHECK (rating BETWEEN 1 AND 5), 
review_date DATE NOT NULL, 
FOREIGN KEY (product_id) REFERENCES products(product_id), 
FOREIGN KEY (customer_id) REFERENCES customers(customer_id) 
); 


-- Table: reviews 
CREATE TABLE reviews ( 
review_id INT PRIMARY KEY, 
product_id INT NOT NULL, 
customer_id INT NOT NULL, 
rating INT CHECK (rating BETWEEN 1 AND 5), 
review_date DATE NOT NULL, 
FOREIGN KEY (product_id) REFERENCES products(product_id), 
FOREIGN KEY (customer_id) REFERENCES customers(customer_id) 
); 