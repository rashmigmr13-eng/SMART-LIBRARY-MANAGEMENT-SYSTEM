"""
data.py
Backend logic for Smart Library Management System.

LIST       -> books, members, transactions
TUPLE      -> fixed categories and member roles
SET        -> unique categories and active members
DICTIONARY -> fast lookup of books and members
"""

from datetime import date, timedelta


# ============================================================
# TUPLE
# Fixed values that should not normally change
# ============================================================

CATEGORIES = (
    "Programming",
    "Cloud",
    "Database",
    "DevOps",
    "AI"
)

MEMBER_ROLES = (
    "Student",
    "Faculty",
    "Guest"
)


# ============================================================
# LIST
# Books
# ============================================================

def initial_books():

    books = [

        {
            "id": "B001",
            "title": "Python Programming",
            "author": "Mark Lutz",
            "category": "Programming",
            "total_copies": 3,
            "available_copies": 3
        },

        {
            "id": "B002",
            "title": "Learning AWS",
            "author": "John Doe",
            "category": "Cloud",
            "total_copies": 2,
            "available_copies": 2
        },

        {
            "id": "B003",
            "title": "Mastering Docker",
            "author": "James Turnbull",
            "category": "DevOps",
            "total_copies": 2,
            "available_copies": 2
        },

        {
            "id": "B004",
            "title": "SQL Fundamentals",
            "author": "Alan Beaulieu",
            "category": "Database",
            "total_copies": 4,
            "available_copies": 4
        }

    ]

    return books


# ============================================================
# LIST
# Members
# ============================================================

def initial_members():

    members = [

        {
            "id": "M001",
            "name": "Rashmi",
            "role": "Student",
            "phone": "9999999999"
        },

        {
            "id": "M002",
            "name": "Anita",
            "role": "Faculty",
            "phone": "8888888888"
        }

    ]

    return members


# ============================================================
# LIST
# Transactions
# ============================================================

def initial_transactions():

    transactions = []

    return transactions


# ============================================================
# DICTIONARY
# Convert book LIST into DICTIONARY
#
# Example:
#
# [
#   {"id": "B001", ...},
#   {"id": "B002", ...}
# ]
#
# becomes
#
# {
#   "B001": {...},
#   "B002": {...}
# }
# ============================================================

def books_as_dict(books):

    book_dictionary = {}

    for book in books:

        book_dictionary[book["id"]] = book

    return book_dictionary


# ============================================================
# DICTIONARY
# Convert member LIST into DICTIONARY
# ============================================================

def members_as_dict(members):

    member_dictionary = {}

    for member in members:

        member_dictionary[member["id"]] = member

    return member_dictionary


# ============================================================
# ADD BOOK
# ============================================================

def add_book(
    books,
    book_id,
    title,
    author,
    category,
    copies
):

    book_id = book_id.strip().upper()

    if not book_id:

        return False, "Book ID is required."

    if not title.strip():

        return False, "Book title is required."

    if not author.strip():

        return False, "Author is required."

    # Dictionary lookup

    book_dictionary = books_as_dict(books)

    if book_id in book_dictionary:

        return False, "Book ID already exists."

    if category not in CATEGORIES:

        return False, "Invalid category."

    if copies <= 0:

        return False, "Copies must be greater than zero."

    # LIST append

    books.append({

        "id": book_id,

        "title": title.strip(),

        "author": author.strip(),

        "category": category,

        "total_copies": copies,

        "available_copies": copies

    })

    return True, f"Book {book_id} added successfully."


# ============================================================
# ADD MEMBER
# ============================================================

def add_member(
    members,
    member_id,
    name,
    role,
    phone
):

    member_id = member_id.strip().upper()

    if not member_id:

        return False, "Member ID is required."

    if not name.strip():

        return False, "Member name is required."

    member_dictionary = members_as_dict(members)

    if member_id in member_dictionary:

        return False, "Member ID already exists."

    if role not in MEMBER_ROLES:

        return False, "Invalid member role."

    members.append({

        "id": member_id,

        "name": name.strip(),

        "role": role,

        "phone": phone.strip()

    })

    return True, f"Member {member_id} added successfully."


# ============================================================
# BORROW BOOK
# ============================================================

def borrow_book(
    books,
    members,
    transactions,
    book_id,
    member_id
):

    book_id = book_id.strip().upper()

    member_id = member_id.strip().upper()

    # DICTIONARY lookup

    book_dictionary = books_as_dict(books)

    member_dictionary = members_as_dict(members)

    # Check book

    if book_id not in book_dictionary:

        return False, "Book not found."

    # Check member

    if member_id not in member_dictionary:

        return False, "Member not found."

    book = book_dictionary[book_id]

    # Check availability

    if book["available_copies"] <= 0:

        return False, "No copies available."

    # Check duplicate borrowing

    for transaction in transactions:

        if (
            transaction["book_id"] == book_id
            and
            transaction["member_id"] == member_id
            and
            transaction["status"] == "Borrowed"
        ):

            return False, "This member already has this book."

    # Reduce available copies

    book["available_copies"] -= 1

    # Add transaction to LIST

    transactions.append({

        "book_id": book_id,

        "member_id": member_id,

        "borrow_date": str(date.today()),

        "due_date": str(
            date.today() + timedelta(days=14)
        ),

        "return_date": None,

        "status": "Borrowed"

    })

    return True, f"{book['title']} borrowed successfully."


# ============================================================
# RETURN BOOK
# ============================================================

def return_book(
    books,
    transactions,
    book_id,
    member_id
):

    book_id = book_id.strip().upper()

    member_id = member_id.strip().upper()

    book_dictionary = books_as_dict(books)

    if book_id not in book_dictionary:

        return False, "Book not found."

    for transaction in transactions:

        if (
            transaction["book_id"] == book_id
            and
            transaction["member_id"] == member_id
            and
            transaction["status"] == "Borrowed"
        ):

            transaction["status"] = "Returned"

            transaction["return_date"] = str(
                date.today()
            )

            book_dictionary[book_id][
                "available_copies"
            ] += 1

            return True, "Book returned successfully."

    return False, "Active borrowing record not found."


# ============================================================
# SEARCH BOOKS
# ============================================================

def search_books(
    books,
    keyword="",
    category="All"
):

    keyword = keyword.lower().strip()

    results = []

    for book in books:

        searchable_text = (

            book["id"]
            + " "
            + book["title"]
            + " "
            + book["author"]

        ).lower()

        if keyword:

            keyword_match = (
                keyword in searchable_text
            )

        else:

            keyword_match = True

        if category == "All":

            category_match = True

        else:

            category_match = (
                book["category"] == category
            )

        if keyword_match and category_match:

            results.append(book)

    return results


# ============================================================
# SET
# Get unique active members
# ============================================================

def get_active_member_ids(transactions):

    active_members = set()

    for transaction in transactions:

        if transaction["status"] == "Borrowed":

            active_members.add(
                transaction["member_id"]
            )

    return active_members


# ============================================================
# SET
# Get unique categories
# ============================================================

def get_unique_categories(books):

    categories = set()

    for book in books:

        categories.add(
            book["category"]
        )

    return categories


# ============================================================
# OVERDUE BOOKS
# ============================================================

def get_overdue_transactions(transactions):

    today = date.today()

    overdue = []

    for transaction in transactions:

        if transaction["status"] == "Borrowed":

            due_date = date.fromisoformat(
                transaction["due_date"]
            )

            if due_date < today:

                overdue.append(transaction)

    return overdue