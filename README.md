Treehouse Techdegree project #4 - A Store Inventory

This is an exercise in the use of CSV-files and databases in Python. Peewee is used to creating and interacting with the database. 

A Product model is made to create new instances of a product to add to the store inventory.  

Initialize() connects to the database and creates the tables according to the product model. 

Import_and_clean() imports product information from a CSV-file and clean it according to the instructions given, making a list with dictionaries of products. 

Add_product() adds a new product to the database or, if there is an older entry with the same product, replaces the existing one with new information. If no data is passed to the function, it prompts the user for information about the product. 

Add_imported() runs add_product() for every product in a list, ment for the result of the import_and_clean function. 

View_imported() lets the user see the information for a specific product in the database, based on the ID of the product. The ID is made unique for every product that is added to the database by the Product model. 

Backup() makes a CSV-file of the database. 

Menu_loop() lets the user maneuver the program by choosing the desired action. 