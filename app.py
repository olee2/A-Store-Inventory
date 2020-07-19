from collections import OrderedDict
import datetime
import csv
import os

from peewee import *

db = SqliteDatabase("inventory.db")


class Product(Model):
    
    product_id = AutoField()
    product_name = CharField(unique=True)
    product_quantity = IntegerField(default=0)
    product_price = IntegerField(default=0)
    date_updated = DateTimeField(default=datetime.datetime.now())

    class Meta:
        database = db


def initialize():
    """Connect to and create tables in the database"""
    
    db.connect()
    db.create_tables([Product], safe=True)


def import_and_clean():
    """Import and clean data from a csv-file"""
    
    with open("inventory.csv", newline="") as csvfile:
        inventory = csv.DictReader(csvfile)
        rows = list(inventory)

    for row in rows:
        row["product_price"] = row["product_price"].replace("$", "")
        row["product_price"] = row["product_price"].replace(".", "")
        row["product_price"] = int(float(row["product_price"]))
        row["date_updated"] = datetime.datetime.strptime(row["date_updated"], "%m/%d/%Y")
        row["product_quantity"]= int(row["product_quantity"])
            
    return rows


def add_product(name="", price=0, quantity=0, date=datetime.datetime.now()):
    """Add a product"""
    
    name = name
    price = price
    quantity = quantity
    date = date

    while True:
        if not name:
            name = input("\nProduct name: ").strip()
            quantity = input("Quantity(integers only): ")
            price = input("Price in cents(integers only): ")

        if len(name):
            try:
                quantity = int(quantity)
                price = int(price)

            except ValueError:
                print("\nOnly input integers for quantity and price!")
                name = ""
                continue
    
        else:
            print("Product name has to be one or more characters!")
            continue
        
        break

    try:
        Product.create(product_name=name, product_quantity=quantity, product_price=price, date_updated=date.date())

    except IntegrityError:
        product_info = Product.get(product_name=name)

        if (product_info.date_updated < date):
            product_info.product_quantity = quantity
            product_info.product_price = price
            product_info.date_updated = date.date()
            product_info.save()

            
def add_imported(products):
    """Add a list of products to the database"""
    
    for product in products:
        add_product(product["product_name"], product["product_quantity"], product["product_price"], product["date_updated"])

        
def clear():
    """Clear the terminal"""
    
    os.system("cls" if os.name == "nt" else "clear")


def view_product():
    """View a product"""
    
    while True:
        try:
            input_id = int(input("\nPlease enter the product ID: "))

        except ValueError:
            print("\nProduct ID must be an integer.")
            continue
        
        else:
            if input_id > 0:
                try:
                    clear()
                    product=Product.get_by_id(input_id)
                    print("\nProduct: {}".format(product.product_name))
                    print("Quantity: {}".format(product.product_quantity))
                    print("Price: ${}".format(product.product_price/100))
                    print("Date updated: {}\n".format(product.date_updated.date()))

                    break
                    
                except:
                    num_items = Product.select().order_by(Product.product_id.desc()).get()
                    print("\nOnly {} product(s) in the inventory. Try again.".format(num_items))
                    continue

            else:
                print("\nThe ID must be a positive integer.")
                continue


def backup():
    """Backup the database"""
    
    with open("backup.csv", "a") as csvfile:
        fieldnames = ["product_id", "product_name", "product_quantity", "product_price", "date_updated"]
        backup = csv.DictWriter(csvfile, fieldnames=fieldnames)

        backup.writeheader()
        
        for i in range(1, int(str(Product.select().order_by(Product.product_id.desc()).get()))+1):
            product=Product.get_by_id(i)
            backup.writerow({
                "product_id": product.product_id,
                "product_name": product.product_name,
                "product_quantity": product.product_quantity,
                "product_price": product.product_price,
                "date_updated": product.date_updated.date()})
            
            i += 1

        print("\nBackup created.")


def menu_loop():
    """Interact with the menu to chose action"""

    action = None
    
    while action != "q":
        print("\nEnter 'q' to quit.")
        for key, value in menu.items():
            print("{}) {}".format(key, value.__doc__))
        action = input("\nAction: ").lower()

        if action in menu:
            clear()
            menu[action]()
        elif action == "q":
            print("\nGoodbye!\n")
            break
        else:
            print("\nPlease choose a valid action!")
            

menu = OrderedDict([
    ("a", add_product),
    ("v", view_product),
    ("b", backup)])


if __name__=="__main__":           
    initialize()
    add_imported(import_and_clean())
    menu_loop()
        

                    



