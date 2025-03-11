import json
import streamlit as st

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

    def add_book(self, title, author, year, genre, read_status):
        """Add a new book to the library."""
        book = {
            "title": title,
            "author": author,
            "year": int(year),
            "genre": genre,
            "read": read_status
        }
        self.library.append(book)
        self.save_library()

    def remove_book(self, title):
        """Remove a book by title."""
        self.library = [book for book in self.library if book["title"].lower() != title.lower()]
        self.save_library()

    def search_book(self, query):
        """Search for a book by title or author."""
        return [book for book in self.library if query.lower() in book["title"].lower() or query.lower() in book["author"].lower()]

    def display_statistics(self):
        """Show library statistics."""
        total_books = len(self.library)
        read_books = sum(1 for book in self.library if book["read"])
        percentage_read = (read_books / total_books * 100) if total_books > 0 else 0
        return total_books, read_books, percentage_read

library = LibraryManager()

st.title("📚 Personal Library Manager")

menu = st.sidebar.selectbox("Menu", ["Add Book", "Remove Book", "Search Book", "View All Books", "Statistics"])

if menu == "Add Book":
    with st.form("add_book_form"):
        title = st.text_input("Title")
        author = st.text_input("Author")
        year = st.number_input("Publication Year", min_value=1000, max_value=9999, step=1)
        genre = st.text_input("Genre")
        read_status = st.checkbox("Read")
        submitted = st.form_submit_button("Add Book")
        if submitted:
            library.add_book(title, author, year, genre, read_status)
            st.success("Book added successfully!")

elif menu == "Remove Book":
    title = st.text_input("Enter the title of the book to remove")
    if st.button("Remove Book"):
        library.remove_book(title)
        st.success("Book removed successfully!")

elif menu == "Search Book":
    query = st.text_input("Enter book title or author")
    if st.button("Search"):
        results = library.search_book(query)
        if results:
            for book in results:
                st.write(f"**Title:** {book['title']} | **Author:** {book['author']} | **Year:** {book['year']} | **Genre:** {book['genre']} | **Status:** {'Read' if book['read'] else 'Unread'}")
        else:
            st.warning("No books found!")

elif menu == "View All Books":
    st.subheader("Library Collection")
    for book in library.library:
        st.write(f"**Title:** {book['title']} | **Author:** {book['author']} | **Year:** {book['year']} | **Genre:** {book['genre']} | **Status:** {'Read' if book['read'] else 'Unread'}")

elif menu == "Statistics":
    total_books, read_books, percentage_read = library.display_statistics()
    st.subheader("Library Statistics")
    st.write(f"**Total books:** {total_books}")
    st.write(f"**Books read:** {read_books} ({percentage_read:.2f}%)")