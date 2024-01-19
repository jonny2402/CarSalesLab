import csv

class CarManufacturer:
    """Represents a car manufacturer."""
    def __init__(self, name, monthly_sales):
        """Initializes the manufacturer with name and sales data."""
        self.name = name
        self.monthly_sales = monthly_sales

    def total_yearly_sales(self):
        """Returns total yearly sales."""
        return sum(self.monthly_sales)
    
    def get_monthly_sales(self, month):
        """Returns sales for a specific month."""
        if month < len(self.monthly_sales):
            return self.monthly_sales[month]
        else:
            return 0

class FileReader:
    """Handles reading of CSV files."""
    def __init__(self, filename):
        """Initializes the reader with a filename."""
        self.filename = filename

    def read(self):
        """Returns data from the file as a list of rows."""
        data = []
        try:
            with open(self.filename, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    data.append(row)
        except IOError as e:
            print(f"Error reading file: {e}")
        return data


class CarManufacturersManager:
    """Manages a collection of CarManufacturer instances."""
    def __init__(self):
        """Initializes the manager."""
        self.manufacturers = []

    def parse_and_add_manufacturer(self, row, line_is_header=False):
        """Parses a row and adds a new CarManufacturer instance."""
        if line_is_header:
            return
        name = row[0]
        if len(row) < 9:  # Assuming 8 months of sales data plus the name
            raise IndexError(f"Missing data in row: {row}")
        try:
            monthly_sales = [int(sale.replace(',', '')) for sale in row[1:]]
        except ValueError:
            raise ValueError(f"Invalid data format in row: {row}")
        self.manufacturers.append(CarManufacturer(name, monthly_sales))

    def get_total_sales_by_manufacturer(self):
        """Returns total sales for all manufacturers for a specific month."""
        return {m.name: m.total_yearly_sales() for m in self.manufacturers}
    
    def get_total_sales_by_month(self, month):
        """Returns grand total sales for all manufacturers."""
        return sum(manufacturer.get_monthly_sales(month) for manufacturer in self.manufacturers)
    
    def get_grand_total_sales(self):
        return sum(manufacturer.total_yearly_sales() for manufacturer in self.manufacturers)



def main():
    """Main function. Reads data from a CSV file and prints total sales information."""
    filename = "car_sales.csv"
    file_reader = FileReader(filename)
    lines = file_reader.read()

    manager = CarManufacturersManager()

    line_is_header = True
    for line in lines:
        manager.parse_and_add_manufacturer(line, line_is_header)
        line_is_header = False

    months = ["January", "February", "March", "April", "May", "June", "July", "August"]

    for i, month in enumerate(months):
        total_sales = manager.get_total_sales_by_month(i)
        print(f"Total sales in {month}: {total_sales}")

    grand_total_sales = manager.get_grand_total_sales()
    print(f"Grand total sales: {grand_total_sales}")


if __name__ == "__main__":
    main()
