-- SQL script creates a trigger named 'reduce_quantity' that runs after an insert on the 'orders' table.
-- The trigger reduces the quantity of an item in the 'items' table by the number of items ordered in the new 'orders' row.

CREATE TRIGGER decrease_items_quantity AFTER INSERT ON orders FOR EACH ROW
UPDATE items SET quantity = quantity - NEW.number WHERE name=NEW.item_name;
