import json
import csv

from datetime import datetime

class Person:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class User(Person):
    def __init__(self, username, password):
        super().__init__(username, password)

class Admin(Person):
    def __init__(self, username, password):
        super().__init__(username, password)

class RentalItem:

    def __init__(self, item_type, name, price, details):
        self.item_type = item_type
        self.name = name
        self.price = price
        self.details = details
        self.availability = True
        self.return_date = None


    def to_dict(self):

        return {
            'item_type': self.item_type,
            'name': self.name,
            'price': self.price,
            'details': self.details,
            'availability': self.availability,
            'return_date': self.return_date.strftime('%Y-%m-%d') if self.return_date else None
        }



class RentalService:

    def __init__(self):
        self.goods = []
        self.users = []
        self.admins = []



    def add_rental(self, item):
        self.goods.append(item)


    def find_goods(self, item_type):

        found_items = [item for item in self.goods if item.item_type.lower() == item_type.lower()]
        return found_items


    def display_all_goods(self):

        print("All Goods:")

        for item in self.goods:

            print(

                f"Item: {item.name}, Type: {item.item_type}, Details: {item.details}, Price: {item.price}, Availability: {item.availability}")


    def save_to_json(self):

        with open("rent_service_data.json", "w") as json_file:

            json.dump([item.to_dict() for item in self.goods], json_file, indent=4)

        print("Data saved to rent_service_data.json")

    def save_to_csv(self):

        with open("rent_service_data.csv", "w", newline='') as csv_file:

            fieldnames = ['item_type', 'name', 'price', 'details', 'availability', 'return_date']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

            for item in self.goods:

                item_dict = item.to_dict()

                if item_dict['return_date'] is None:

                    del item_dict['return_date']  # Remove return_date field if it's None
                writer.writerow(item_dict)


    def load_from_json(self):

        with open("rent_service_data.json", "r") as json_file:

            data = json.load(json_file)
            self.goods = [RentalItem(item['item_type'], item['name'], item['price'], item['details']) for item in data]


    def load_from_csv(self):

        with open("rent_service_data.csv", "r") as csv_file:
            reader = csv.DictReader(csv_file)

            self.goods = [RentalItem(row['item_type'], row['name'], row['price'], row['details']) for row in reader]


    def modify_rental(self, item_name, new_price=None, new_details=None):

        found_item = None

        for item in self.goods:

            if item.name.lower() == item_name.lower():
                found_item = item

                break

        if found_item:

            if new_price is not None:
                found_item.price = new_price

            if new_details is not None:
                found_item.details = new_details

            print(f"Rental item '{item_name}' details modified successfully!")

        else:

            print(f"Rental item '{item_name}' not found.")


    def remove_rental(self, item_identifier):

        removed = False

        for item in self.goods:

            if item.name.lower() == item_identifier.lower():
                self.goods.remove(item)

                removed = True

                print(f"Rental item '{item_identifier}' removed successfully!")
                break

        if not removed:

            print(f"Rental item '{item_identifier}' not found.")


    def add_rental_condition(self, item_name, conditions):

        found_item = None

        for item in self.goods:

            if item.name.lower() == item_name.lower():
                found_item = item

                break

        if found_item:

            found_item.details += f", Conditions: {conditions}"
            print(f"Rental conditions added successfully for '{item_name}'!")
        else:
            print(f"Rental item '{item_name}' not found.")


    def add_review(self, item_name, review):

        found_item = None

        for item in self.goods:

            if item.name.lower() == item_name.lower():
                found_item = item

                break

        if found_item:
            found_item.details += f", Review: {review}"

            print(f"Review added successfully for '{item_name}'!")
        else:

            print(f"Rental item '{item_name}' not found.")


    def search_by_keyword(self, keyword):

        found_items = [item for item in self.goods if keyword.lower() in item.details.lower()]
        if found_items:

            print("Found rental items:")
            for item in found_items:

                print(f"Item: {item.name}, Details: {item.details}, Price: {item.price}")
        else:

            print("No rental items found matching the keyword.")

    def filter_items(self, criteria):
        try:
            price_criteria = float(criteria)
            filtered_items = []

            print("Filtered rental items:")
            for item in self.goods:
                if item.price <= price_criteria:
                    filtered_items.append(item)

            for item in filtered_items:
                print(f"Item: {item.name}, Details: {item.details}, Price: {item.price}")

        except ValueError:
            print("Invalid input for criteria. Please enter a valid price.")

    def rent_item(self, item_name, renter_info, rental_period):


        found_item = None
        for item in self.goods:

            if item.name.lower() == item_name.lower():
                found_item = item

                break

        if found_item:
            found_item.availability = False
            print(f"Item '{item_name}' rented successfully by {renter_info} for {rental_period}!")

        else:

            print(f"Rental item '{item_name}' not found.")


    def return_item(self, item_name):


        found_item = None
        for item in self.goods:

            if item.name.lower() == item_name.lower():
                found_item = item

                break

        if found_item:
            found_item.availability = True

            print(f"Item '{item_name}' returned successfully!")

        else:

            print(f"Rental item '{item_name}' not found.")


    def statistics(self):

        available_count = sum(1 for item in self.goods if item.availability)
        rented_count = len(self.goods) - available_count

        print(f"Total items: {len(self.goods)}")
        print(f"Available items: {available_count}")
        print(f"Rented items: {rented_count}")

    def set_return_date(self, item_name, return_date):
        found_item = None
        for item in self.goods:
            if item.name.lower() == item_name.lower():
                found_item = item
                break

        if found_item:
            found_item.return_date = return_date
            print(f"Return date set successfully for '{item_name}'!")
        else:
            print(f"Rental item '{item_name}' not found.")

    def notify_return_due(self, days_before):

        for item in self.goods:

            if item.return_date:

                days_until_return = (item.return_date - datetime.now()).days

                if 0 < days_until_return <= days_before:

                    print(f"Return due in {days_until_return} days for item '{item.name}'. Please return soon!")


    def register_user(self, username, password):

        self.users.append({'username': username, 'password': password})

        print(f"User '{username}' registered successfully!")


    def authenticate_user(self, username, password):

        for user in self.users:

            if user['username'] == username and user['password'] == password:

                return True

        return False


    def reserve_item(self, item_name, user, reservation_period):

        found_item = None

        for item in self.goods:

            if item.name.lower() == item_name.lower() and item.availability:

                found_item = item
                break

        if found_item:

            found_item.availability = False
            found_item.return_date = datetime.now() + timedelta(days=reservation_period)

            print(f"Item '{item_name}' reserved successfully by {user.username} for {reservation_period} days!")

        else:

            print(f"Rental item '{item_name}' not found or already rented.")


    def add_admin(self, username, password):

        self.admins.append(Admin(username, password))
        print(f"Admin '{username}' registered successfully!")

    def authenticate_admin(self, username, password):

        for admin in self.admins:

            if admin.username == username and admin.password == password:

                return True

        return False

def main():

    rent_service = RentalService()

    while True:
        print("\n     ===== Rental Service Menu =====       ")
        print("1. Add Electronic Goods for Rent")
        print("2. Add Book for Rent")
        print("3. Find Goods for Rent")
        print("4. Display All Goods")
        print("5. Save to JSON")
        print("6. Save to CSV")
        print("7. Load from JSON")
        print("8. Load from CSV")
        print("9. Modify Rental Item")
        print("10. Remove Rental Item")
        print("11. Add Rental Condition")
        print("12. Add Review")
        print("13. Search by Keyword")
        print("14. Filter Items")
        print("15. Rent Item")
        print("16. Return Item")
        print("17. Set Return Date")
        print("18. Show Return Notifications")
        print("19. Register User")
        print("20. Login")
        print("21. Reserve Item")
        print("22. Register Admin")
        print("23. Admin Login")
        print("24. Exit")

        choice = input("Enter your choice (1-24): ")

        if choice == '1':

            print("\n=== Adding Electronic Goods for Rent ===")

            name = input("Enter electronic item name: ")
            price = float(input("Enter rent price: "))
            brand = input("Enter brand: ")
            rent_service.add_rental(RentalItem("Electronic", name, price, f"Brand: {brand}"))

            print("Goods added successfully!")

        elif choice == '2':

            print("\n=== Adding Book for Rent ===")

            name = input("Enter book name: ")
            price = float(input("Enter rent price: "))
            author = input("Enter author: ")
            rent_service.add_rental(RentalItem("Book", name, price, f"Author: {author}"))
            print("Goods added successfully!")

        elif choice == '3':

            print("\n=== Finding Goods for Rent ===")

            item_type = input("Enter item type to find: ")
            found_items = rent_service.find_goods(item_type)
            print("\nAvailable Goods:")

            for item in found_items:
                print(f"Item: {item.name}, Type: {item.item_type}, Details: {item.details}, Price: {item.price}, Availability: {item.availability}")

        elif choice == '4':

            print("\n=== Displaying All Goods ===")
            rent_service.display_all_goods()

        elif choice == '5':

            print("\n=== Saving to JSON ===")
            rent_service.save_to_json()

        elif choice == '6':

            print("\n=== Saving to CSV ===")
            rent_service.save_to_csv()

        elif choice == '7':

            print("\n=== Loading from JSON ===")
            rent_service.load_from_json()
            print("Data loaded from rent_service_data.json")

        elif choice == '8':

            print("\n=== Loading from CSV ===")
            rent_service.load_from_csv()
            print("Data loaded from rent_service_data.csv")

        elif choice == '9':

            print("\n=== Modifying Rental Item ===")
            item_name = input("Enter item name to modify: ")
            new_price = float(input("Enter new rent price (leave blank to keep the same): ") or "-1")
            new_details = input("Enter new item details (leave blank to keep the same): ")
            rent_service.modify_rental(item_name, new_price=new_price if new_price != -1 else None, new_details=new_details or None)

        elif choice == '10':

            print("\n=== Removing Rental Item ===")
            item_name = input("Enter item name to remove: ")
            rent_service.remove_rental(item_name)

        elif choice == '11':

            print("\n=== Adding Rental Condition ===")
            item_name = input("Enter item name to add rental condition: ")
            conditions = input("Enter rental conditions: ")
            rent_service.add_rental_condition(item_name, conditions)

        elif choice == '12':

            print("\n=== Adding Review ===")

            item_name = input("Enter item name to add review: ")
            review = input("Enter review: ")
            rent_service.add_review(item_name, review)

        elif choice == '13':

            print("\n=== Searching by Keyword ===")

            keyword = input("Enter keyword to search: ")
            rent_service.search_by_keyword(keyword)

        elif choice == '14':

            print("\n=== Filtering Items ===")
            criteria = input("Enter criteria to filter items: ")
            rent_service.filter_items(criteria)

        elif choice == '15':

            print("\n=== Renting Item ===")

            item_name = input("Enter item name to rent: ")
            renter_info = input("Enter renter information: ")
            rental_period = input("Enter rental period: ")
            rent_service.rent_item(item_name, renter_info, rental_period)

        elif choice == '16':

            print("\n=== Returning Item ===")

            item_name = input("Enter item name to return: ")

            rent_service.return_item(item_name)

        if choice == '17':

            print("\n=== Set Return Date ===")

            item_name = input("Enter item name: ")

            return_date_str = input("Enter return date (YYYY-MM-DD): ")

            try:

                return_date = datetime.strptime(return_date_str, '%Y-%m-%d')

                rent_service.set_return_date(item_name, return_date)

            except ValueError:

                print("Invalid date format. Please use YYYY-MM-DD.")


        elif choice == '18':

            print("\n=== Show Return Notifications ===")

            days_before = int(input("Enter number of days before return for notification: "))

            rent_service.notify_return_due(days_before)


        elif choice == '19':

            print("\n=== Register User ===")

            username = input("Enter username: ")

            password = input("Enter password: ")

            rent_service.register_user(username, password)


        elif choice == '20':

            print("\n=== Login ===")

            username = input("Enter username: ")

            password = input("Enter password: ")

            user = rent_service.authenticate_user(username, password)

            if user:

                print("Login successful!")

            else:

                print("Invalid username or password.")

        elif choice == '21':

            if is_admin:
                print("\n=== Reserve Item ===")
                item_name = input("Enter item name to reserve: ")
                user = input("Enter user name: ")
                reservation_period = int(input("Enter reservation period (in days): "))
                rent_service.reserve_item(item_name, user, reservation_period)

            else:
                print("Only admins can access this feature. Please login as admin.")

        elif choice == '22':

            if is_admin:
                print("\n=== Register Admin ===")
                username = input("Enter admin username: ")
                password = input("Enter admin password: ")
                rent_service.add_admin(username, password)

            else:
                print("Only admins can access this feature. Please login as admin.")

        elif choice == '23':
            print("\n=== Admin Login ===")
            username = input("Enter admin username: ")
            password = input("Enter admin password: ")
            is_admin = rent_service.authenticate_admin(username, password)
            if is_admin:
                print("Admin login successful!")
            else:
                print("Invalid admin username or password.")

        elif choice == '24':
                print("\nExiting program. Goodbye!")
                break
        else:
                print("\nInvalid choice. Please enter a number from 1 to 24.")

if __name__ == "__main__":
    main()