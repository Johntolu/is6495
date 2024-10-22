from collections import namedtuple
from tokenize import PlainToken

import DBbase as db

class Parts(db.DBbase):

    def __init__(self):
        super().__init__("inventoryDB.sqlite")

    def update(self, part_id, name):
        try:
            super().get_cursor.execute("update Parts set name = ? where id = ?;", (name, part_id))
            super().get_connection.commit()
            print(f"Updated record to {name} Successfully")
        except Exception as e:
            print("An error updating occured.", e)

    def add(self, name):
        try:
            super().get_cursor.execute("insert or ignore into Parts (name) values(?);", (name,))
            super().get_connection.commit()
            print(f"Add {name} successfully.")

        except Exception as e:
            print("An error adding occured.", e)

    def delete(self,  part_id):
        try:
            super().get_cursor.execute("DELETE FROM Parts where id = ?;", (part_id,))
            super().get_connection.commit()
            print(f"deleted {part_id} successfully.")
            return True
        except Exception as e:
            print("An error deleting occured.", e)
            return False

    def fetch(self, id=None, part_name=None):
        try:
            if id is not None:
                return super().get_cursor.execute("SELECT * FROM Parts WHERE id = ?", (id,)).fetchone()
            elif part_name is not None:
                return super().get_cursor.execute("SELECT * FROM Parts WHERE name = ?", (part_name,)).fetchone()
            else:
                return super().get_cursor.execute("SELECT * FROM Parts").fetchall()
        except Exception as e:
            print("An error fetching occured.", e)

    def reset_database(self):
        try:
            sql = """
                DROP TABLE IF EXISTS Parts;
                
                CREATE TABLE Parts (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                    name TEXT UNIQUE );
            """
            super().execute_script(sql)
        except Exception as e:
            print("An error resetting occured.", e)
        finally:
            super().close_db()

class Inventory(Parts):

    def add_inv(self, name, qty, price):
        try:
            super().add(name)
        except Exception as e:
            print("An error adding inventory occured.", e)
        else:
            try:
                part_id = super().fetch(part_name=name)[0]
                if part_id is not None:
                    super().get_cursor.execute("""INSERT INTO Inventory (part_id, quantity, price)  
                     VALUES (?,?,?);""", (part_id, qty, price))
                    super().get_connection.commit()
                    print(f"Inventory  {name} added successfully")
                else:
                    raise Exception("The id of the part name was not found")
            except Exception as ex:
                print("An error occured in the inventory class:", ex)

    def update_inv(self, id, qty, price):
        try:
            super().get_cursor.execute(""" UPDATE Inventory SET quantity = ?, price = ? WHERE id = ?;""",
                                       (qty, price, id))
            super().get_connection.commit()
            print("updated inventory ID record successfully")
            return True
            pass
        except Exception as e:
            print("An error updating inventory occured.", e)
            return False

    def delete_inv(self, inventory_id):
        try:
            part_id = self.fetch_inv(inventory_id)[1]
            if part_id is not None:
                rsts = super().delete(part_id)
                super().get_connection.commit()
                if rsts is False:
                    raise Exception("delete method in Parts failed. Delete aborted.")
        except Exception as e:
            print("An error deleting inventory occured.", e)
        else:
            try:
                super().get_cursor.execute("DELETE FROM Inventory WHERE id = ?; """, (inventory_id))
                super().get_connection.commit()
            except Exception as e:
                print("an error occurred in inventory delete", e)


    def fetch_inv(self, id=None):
        try:
            if id is not None:
                retval = super().get_cursor.execute("""SELECT Inventory.id, part_id, p.name, quantity, price 
                FROM Inventory JOIN Parts p on Inventory.part_id = p.id
                WHERE Inventory.id = ?;""", (id,)).fetchone()
                return retval
            else:
                return super().get_cursor.execute("""SELECT Inventory.id, part_id, p.name, quantity, price 
                FROM Inventory JOIN Parts p on Inventory.part_id = p.id
                WHERE Inventory.id;""").fetchall()

        except Exception as e:
            print("An error fetching inventory occured.", e)

    def reset_database(self):
        try:
            sql = """
                DROP TABLE IF EXISTS Inventory;
                
                CREATE TABLE Inventory (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                part_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                price varchar(20)
                );
            
            """
            super().execute_script(sql)
            print("Inventory table successfully created")
        except Exception as e:
            print("An error resetting inventory occured.", e)
        finally:
            super().close_db()
class Project:

    def run(self):

        inv_options = { "get":  "Get all inventory",
                        "getby": "Get inventory by Id",
                        "update": "Update inventory",
                        "add": "Add inventory",
                        "delete": "Delete inventory",
                        "reset": "Reset database",
                        "exit": "Exit program"
                        }
        print("Welcome to my inventory program, please choose a selection")

        user_selection = ""
        while user_selection != "exit":
            print("*** Option list ***")
            for option in inv_options.items():
                print(option)

            user_selection = input("Select an option ").lower()
            inventory = Inventory()

            if user_selection == "get":
                results = inventory.fetch_inv()
                for item in results:
                    print(item)

            elif user_selection == "getby":
                inv_id = input("Enter inventory ID: ")
                results = inventory.fetch_inv(inv_id)
                print(results)
                input("Press return to continue ")

            elif user_selection == "update":
                inv_id = input("Enter inventory ID: ")
                qty = input("Enter quantity amount: ")
                price = input("Enter unit price: ")
                inventory.update_inv(inv_id, qty, price)
                print(inventory.fetch_inv(inv_id))
                input("Press return to continue ")

            elif user_selection == "add":
                name = input("Enter part name: ")
                qty = input("Enter quantity amount: ")
                price = input("Enter unit price: ")
                inventory.add_inv(name, qty, price)
                print("Done\n")
                input("Press return to continue ")

            elif user_selection == "delete":
                inv_id = input("Enter inventory ID: ")
                inventory.delete_inv(inv_id)
                print("Done\n")
                input("Press return to continue ")

            elif user_selection == "reset":
                confirm = input("This will delete all records in parts and inventory, continue? (y/n) ").lower()
                if (confirm == "y"):
                     inventory.reset_database()
                     parts = Parts()
                     parts.reset_database()
                     print("reset complete")
                     input("Press return to continue ")
                else:
                    print("Reset aborted")

            else:
                if user_selection != "exit":
                    print("Invalid selection, please try again\n")
project = Project()
project.run()