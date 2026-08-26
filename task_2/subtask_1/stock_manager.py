STOCK_FILE = "stock.txt"  #zay define


def read_stock():
    """Read stock.txt and return its contents as a dictionary."""
    stock = {}

    try:
        with open(STOCK_FILE, "r") as file:
            for line_number, line in enumerate(file, start=1):  #bt number
                line = line.strip()
                if not line:
                    continue
                parts = line.split(",")
                if len(parts) != 2:
                    raise ValueError(
                        f"Invalid format on line {line_number}."
                    )
                name = parts[0].strip().lower()
                if not name:
                    raise ValueError(
                        f"Empty stock name on line {line_number}."
                    )

                try:
                    quantity = int(parts[1].strip())
                except ValueError:
                    raise ValueError(
                        f"Invalid quantity on line {line_number}."
                    )

                if quantity < 0:
                    raise ValueError(
                        f"Negative quantity on line {line_number}."
                    )

                stock[name] = quantity

    except FileNotFoundError: #handles missing file
        print("Error: stock.txt was not found.")
        return None

    except (OSError, ValueError) as error:
        print(f"Error reading stock.txt: {error}")
        return None

    return stock


def show_stock(stock):
    """Display all stock items with their IDs."""
    if not stock:
        print("\nThe stock is empty.")
        return

    print("\nCurrent stock:")

    for item_id, (name, quantity) in enumerate(stock.items(), start=1):
        print(f"{item_id}. {name}: {quantity}")


def get_existing_stock_name(stock):
    """Ask for a stock name or ID and return the selected name."""
    while True:
        user_input = input(
            '\nEnter the stock name or ID '
            '(e.g. "banana" or "1"): '
        ).strip()

        if not user_input:
            print("Invalid input. Please enter a stock name or ID.")
            continue

        # User entered an ID
        if user_input.isdigit():
            item_id = int(user_input)

            stock_names = list(stock.keys())

            if 1 <= item_id <= len(stock_names):
                return stock_names[item_id - 1]

            print("Invalid ID. Please choose an existing stock ID.")

        # User entered a stock name
        else:
            name = user_input.lower()

            if name in stock:
                return name

            print("Stock does not exist. Please choose an existing stock.")


def add_stock(stock):
    """Add stock to an existing item or create a new item."""
    show_stock(stock)

    while True:
        user_input = input(
            '\nEnter the stock name or ID to change, '
            'or enter a new stock name: '
        ).strip()

        if not user_input:
            print("Invalid input. Please enter a stock name or ID.")
            continue

        # Existing item selected by ID
        if user_input.isdigit():
            item_id = int(user_input)
            stock_names = list(stock.keys())

            if 1 <= item_id <= len(stock_names):
                name = stock_names[item_id - 1]
                break

            print("Invalid ID.")
            continue

        # Stock name
        name = user_input.lower()
        break

    while True:
        amount_input = input("Enter how much stock to add: ").strip()

        try:
            amount = int(amount_input)

            if amount <= 0:
                print("Invalid amount. Enter a positive integer.")
                continue

            break

        except ValueError:
            print("Invalid amount. Enter a whole number.")

    if name in stock:
        stock[name] += amount
        print(f"{amount} added to {name}.")
    else:
        stock[name] = amount
        print(f"New stock '{name}' added with quantity {amount}.")


def remove_stock(stock):
    """Remove stock from an existing item."""
    show_stock(stock)

    if not stock:
        return

    name = get_existing_stock_name(stock)

    while True:
        amount_input = input(
            f"Enter how much {name} stock to remove: "
        ).strip()

        try:
            amount = int(amount_input)

            if amount <= 0:
                print("Invalid amount. Enter a positive integer.")
                continue

            if amount > stock[name]:
                print(
                    f"Invalid amount. {name} only has "
                    f"{stock[name]} in stock."
                )
                continue

            break

        except ValueError:
            print("Invalid amount. Enter a whole number.")

    stock[name] -= amount

    print(f"{amount} removed from {name}.")


def save_stock(stock):
    """Save the current stock dictionary to stock.txt."""
    try:
        with open(STOCK_FILE, "w") as file:
            for name, quantity in stock.items():
                file.write(f"{name},{quantity}\n")

    except OSError as error:
        print(f"Error saving stock.txt: {error}")


def main():
    """Run the stock management program."""
    stock = read_stock()

    if stock is None:
        return

    while True:
        print("\n========== STOCK MANAGER ==========")
        print("1. Add stock")
        print("2. Remove stock")
        print("3. Show stock's contents")
        print("4. Exit")

        choice = input("Enter your choice (1/2/3/4): ").strip()

        if choice == "1":
            add_stock(stock)

        elif choice == "2":
            remove_stock(stock)

        elif choice == "3":
            show_stock(stock)

        elif choice == "4":
            save_stock(stock)
            print("Stock saved. Exiting program.")
            break

        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()