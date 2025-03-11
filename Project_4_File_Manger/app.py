import json

class LibraryManager:
    def __init__(self, filename="library.json"):
        self.filename = filename
        self.library = self.load_library()

    def load_library(self):
        """Load the library from a file."""
        try:
            with open(self.filename, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_library(self):
        """Save the library to a file."""
        with open(self.filename, "w") as file:
            json.dump(self.library, file, indent=4)

    def add_book(self):
        """Add a new book to the library."""
        title = input("Enter book title: ")
        author = input("Enter book author: ")
        year = input("Enter publication year: ")
        genre = input("Enter book genre: ")
        read_status = input("Have you read this book? (yes/no): ").strip().lower() == "yes"
        
        book = {
            "title": title,
            "author": author,
            "year": int(year),
            "genre": genre,
            "read": read_status
        }
        self.library.append(book)
        self.save_library()
        print("Book added successfully!\n")

    def remove_book(self):
        """Remove a book by title."""
        title = input("Enter the title of the book to remove: ")
        for book in self.library:
            if book["title"].lower() == title.lower():
                self.library.remove(book)
                self.save_library()
                print("Book removed successfully!\n")
                return
        print("Book not found!\n")

    def search_book(self):
        """Search for a book by title or author."""
        query = input("Enter book title or author to search: ").lower()
        results = [book for book in self.library if query in book["title"].lower() or query in book["author"].lower()]
        
        if results:
            print("\nSearch Results:")
            for book in results:
                self.display_book(book)
        else:
            print("No books found!\n")

    def display_all_books(self):
        """Display all books in the library."""
        if not self.library:
            print("No books in the library!\n")
            return
        print("\nLibrary Collection:")
        for book in self.library:
            self.display_book(book)

    def display_book(self, book):
        """Format and display a book's details."""
        status = "Read" if book["read"] else "Unread"
        print(f"Title: {book['title']}, Author: {book['author']}, Year: {book['year']}, Genre: {book['genre']}, Status: {status}")

    def display_statistics(self):
        """Show library statistics."""
        total_books = len(self.library)
        read_books = sum(1 for book in self.library if book["read"])
        percentage_read = (read_books / total_books * 100) if total_books > 0 else 0
        
        print("\nLibrary Statistics:")
        print(f"Total books: {total_books}")
        print(f"Books read: {read_books} ({percentage_read:.2f}%)\n")

    def menu(self):
        """Display the main menu."""
        while True:
            print("\nPersonal Library Manager")
            print("1. Add a book")
            print("2. Remove a book")
            print("3. Search for a book")
            print("4. Display all books")
            print("5. Display statistics")
            print("6. Exit")
            
            choice = input("Enter your choice (Number Of the list): ")
            if choice == "1":
                self.add_book()
            elif choice == "2":
                self.remove_book()
            elif choice == "3":
                self.search_book()
            elif choice == "4":
                self.display_all_books()
            elif choice == "5":
                self.display_statistics()
            elif choice == "6":
                print("Exiting the program. Goodbye!")
                break
            else:
                print("Invalid choice! Please try again.\n")

if __name__ == "__main__":
    library = LibraryManager()
    library.menu()
