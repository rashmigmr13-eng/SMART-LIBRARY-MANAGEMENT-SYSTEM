"""
app.py

Streamlit frontend for Smart Library Management System.

Backend logic is maintained separately in data.py.
"""

import streamlit as st

from data import (

    CATEGORIES,

    MEMBER_ROLES,

    initial_books,

    initial_members,

    initial_transactions,

    books_as_dict,

    members_as_dict,

    add_book,

    add_member,

    borrow_book,

    return_book,

    search_books,

    get_active_member_ids,

    get_unique_categories,

    get_overdue_transactions

)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(

    page_title="Smart Library",

    page_icon="📚",

    layout="wide"

)


# ============================================================
# SESSION STATE
# ============================================================

if "books" not in st.session_state:

    st.session_state.books = initial_books()


if "members" not in st.session_state:

    st.session_state.members = initial_members()


if "transactions" not in st.session_state:

    st.session_state.transactions = initial_transactions()


# Get current data

books = st.session_state.books

members = st.session_state.members

transactions = st.session_state.transactions


# ============================================================
# RESET DATA
# ============================================================

def reset_data():

    st.session_state.books = initial_books()

    st.session_state.members = initial_members()

    st.session_state.transactions = initial_transactions()


# ============================================================
# HEADER
# ============================================================

st.title(
    "📚 Smart Library Management System"
)

st.caption(
    "Python List + Tuple + Set + Dictionary "
    "with Streamlit"
)


# ============================================================
# DASHBOARD CALCULATIONS
# ============================================================

total_titles = len(books)

total_copies = 0

available_copies = 0


for book in books:

    total_copies += book["total_copies"]

    available_copies += book["available_copies"]


borrowed_copies = (
    total_copies - available_copies
)


overdue_count = len(
    get_overdue_transactions(
        transactions
    )
)


active_member_count = len(
    get_active_member_ids(
        transactions
    )
)


# ============================================================
# DASHBOARD METRICS
# ============================================================

col1, col2, col3, col4, col5 = st.columns(5)


col1.metric(
    "📚 Book Titles",
    total_titles
)


col2.metric(
    "📦 Total Copies",
    total_copies
)


col3.metric(
    "✅ Available",
    available_copies
)


col4.metric(
    "📕 Borrowed",
    borrowed_copies
)


col5.metric(
    "⏰ Overdue",
    overdue_count
)


st.divider()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title(
    "📚 Library Menu"
)


menu = st.sidebar.radio(

    "Choose Operation",

    [

        "Dashboard",

        "Books",

        "Members",

        "Borrow Book",

        "Return Book",

        "Transactions",

        "Backend Concepts"

    ]

)


if st.sidebar.button(
    "🔄 Reset Demo Data"
):

    reset_data()

    st.rerun()


# ============================================================
# DASHBOARD
# ============================================================

if menu == "Dashboard":

    st.subheader(
        "📊 Library Dashboard"
    )


    col1, col2 = st.columns(2)


    with col1:

        st.write(
            "### 📂 Available Categories"
        )

        categories = get_unique_categories(
            books
        )

        st.write(
            sorted(categories)
        )


        st.write(
            "### 👥 Active Members"
        )

        st.write(
            active_member_count
        )


    with col2:

        st.write(
            "### 📋 Library Status"
        )

        if overdue_count > 0:

            st.warning(
                f"{overdue_count} overdue book(s)"
            )

        else:

            st.success(
                "No overdue books"
            )


    st.write(
        "### 📚 Current Books"
    )

    st.dataframe(
        books,
        use_container_width=True
    )


# ============================================================
# BOOK MANAGEMENT
# ============================================================

elif menu == "Books":

    st.subheader(
        "📖 Book Management"
    )


    # --------------------------------------------------------
    # ADD BOOK
    # --------------------------------------------------------

    with st.expander(
        "➕ Add New Book"
    ):

        with st.form(
            "add_book_form"
        ):

            col1, col2 = st.columns(2)


            with col1:

                book_id = st.text_input(
                    "Book ID",
                    placeholder="B005"
                )


                title = st.text_input(
                    "Book Title"
                )


                author = st.text_input(
                    "Author"
                )


            with col2:

                category = st.selectbox(

                    "Category",

                    CATEGORIES

                )


                copies = st.number_input(

                    "Number of Copies",

                    min_value=1,

                    value=1,

                    step=1

                )


            submitted = st.form_submit_button(
                "Add Book"
            )


            if submitted:

                success, message = add_book(

                    books,

                    book_id,

                    title,

                    author,

                    category,

                    copies

                )


                if success:

                    st.success(
                        message
                    )

                    st.rerun()

                else:

                    st.error(
                        message
                    )


    # --------------------------------------------------------
    # SEARCH
    # --------------------------------------------------------

    st.write(
        "### 🔎 Search Books"
    )


    col1, col2 = st.columns(2)


    with col1:

        keyword = st.text_input(

            "Search",

            placeholder="Python"

        )


    with col2:

        category_filter = st.selectbox(

            "Category",

            ["All"] + list(
                CATEGORIES
            )

        )


    results = search_books(

        books,

        keyword,

        category_filter

    )


    st.write(
        f"Found {len(results)} book(s)"
    )


    st.dataframe(

        results,

        use_container_width=True

    )


# ============================================================
# MEMBER MANAGEMENT
# ============================================================

elif menu == "Members":

    st.subheader(
        "👥 Member Management"
    )


    with st.expander(
        "➕ Add New Member"
    ):

        with st.form(
            "member_form"
        ):

            col1, col2 = st.columns(2)


            with col1:

                member_id = st.text_input(
                    "Member ID",
                    placeholder="M003"
                )


                name = st.text_input(
                    "Member Name"
                )


            with col2:

                role = st.selectbox(

                    "Role",

                    MEMBER_ROLES

                )


                phone = st.text_input(
                    "Phone"
                )


            submitted = st.form_submit_button(
                "Add Member"
            )


            if submitted:

                success, message = add_member(

                    members,

                    member_id,

                    name,

                    role,

                    phone

                )


                if success:

                    st.success(
                        message
                    )

                    st.rerun()

                else:

                    st.error(
                        message
                    )


    st.write(
        "### 👥 Registered Members"
    )


    st.dataframe(

        members,

        use_container_width=True

    )


# ============================================================
# BORROW BOOK
# ============================================================

elif menu == "Borrow Book":

    st.subheader(
        "📕 Borrow Book"
    )


    book_dictionary = books_as_dict(
        books
    )


    member_dictionary = members_as_dict(
        members
    )


    if not books:

        st.warning(
            "No books available."
        )


    elif not members:

        st.warning(
            "No members available."
        )


    else:

        with st.form(
            "borrow_form"
        ):


            book_id = st.selectbox(

                "Select Book",

                list(
                    book_dictionary.keys()
                ),

                format_func=lambda book_id:

                    f"{book_id} - "
                    f"{book_dictionary[book_id]['title']} "
                    f"("
                    f"{book_dictionary[book_id]['available_copies']}"
                    f" available)"

            )


            member_id = st.selectbox(

                "Select Member",

                list(
                    member_dictionary.keys()
                ),

                format_func=lambda member_id:

                    f"{member_id} - "
                    f"{member_dictionary[member_id]['name']}"

            )


            submitted = st.form_submit_button(

                "📕 Borrow Book"

            )


            if submitted:

                success, message = borrow_book(

                    books,

                    members,

                    transactions,

                    book_id,

                    member_id

                )


                if success:

                    st.success(
                        message
                    )

                    st.rerun()

                else:

                    st.error(
                        message
                    )


# ============================================================
# RETURN BOOK
# ============================================================

elif menu == "Return Book":

    st.subheader(
        "📗 Return Book"
    )


    active_transactions = []


    for transaction in transactions:

        if transaction["status"] == "Borrowed":

            active_transactions.append(
                transaction
            )


    if not active_transactions:

        st.info(
            "No books are currently borrowed."
        )


    else:

        with st.form(
            "return_form"
        ):


            selected_index = st.selectbox(

                "Select Borrowing Record",

                range(
                    len(active_transactions)
                ),

                format_func=lambda i:

                    f"{active_transactions[i]['book_id']} → "
                    f"{active_transactions[i]['member_id']} "
                    f"| Due: "
                    f"{active_transactions[i]['due_date']}"

            )


            submitted = st.form_submit_button(

                "📗 Return Book"

            )


            if submitted:

                selected = (
                    active_transactions[
                        selected_index
                    ]
                )


                success, message = return_book(

                    books,

                    transactions,

                    selected["book_id"],

                    selected["member_id"]

                )


                if success:

                    st.success(
                        message
                    )

                    st.rerun()

                else:

                    st.error(
                        message
                    )


# ============================================================
# TRANSACTIONS
# ============================================================

elif menu == "Transactions":

    st.subheader(
        "📋 Library Transactions"
    )


    if transactions:

        st.dataframe(

            transactions,

            use_container_width=True

        )

    else:

        st.info(
            "No transactions yet."
        )


    st.write(
        "### ⏰ Overdue Books"
    )


    overdue = get_overdue_transactions(
        transactions
    )


    if overdue:

        st.dataframe(

            overdue,

            use_container_width=True

        )

    else:

        st.success(
            "No overdue books."
        )


# ============================================================
# BACKEND CONCEPTS
# ============================================================

elif menu == "Backend Concepts":

    st.subheader(
        "🧠 Python Data Structures Used"
    )


    # ========================================================
    # LIST
    # ========================================================

    st.markdown(
        """
        ## 1️⃣ LIST

        A List stores multiple values and is mutable.

        **Library example:**

        ```python
        books = [
            {"id": "B001", "title": "Python"},
            {"id": "B002", "title": "AWS"}
        ]
        ```

        We use List for:

        - Books
        - Members
        - Transactions
        """
    )


    # ========================================================
    # TUPLE
    # ========================================================

    st.markdown(
        """
        ## 2️⃣ TUPLE

        A Tuple is immutable.

        **Library example:**

        ```python
        CATEGORIES = (
            "Programming",
            "Cloud",
            "Database",
            "DevOps",
            "AI"
        )
        ```

        We use Tuple for fixed configuration.
        """
    )


    # ========================================================
    # SET
    # ========================================================

    st.markdown(
        """
        ## 3️⃣ SET

        A Set stores unique values.

        **Library example:**

        ```python
        active_members = {
            "M001",
            "M002"
        }
        ```

        We use Set for:

        - Unique categories
        - Active members
        """
    )


    # ========================================================
    # DICTIONARY
    # ========================================================

    st.markdown(
        """
        ## 4️⃣ DICTIONARY

        A Dictionary stores key-value pairs.

        **Library example:**

        ```python
        books = {
            "B001": {
                "title": "Python Programming"
            }
        }
        ```

        We use Dictionary for fast lookup
        using Book ID or Member ID.
        """
    )


    st.divider()


    st.subheader(
        "🔍 Live Backend Data"
    )


    col1, col2 = st.columns(2)


    with col1:

        st.write(
            "### Books Dictionary"
        )

        st.json(
            books_as_dict(books)
        )


    with col2:

        st.write(
            "### Members Dictionary"
        )

        st.json(
            members_as_dict(members)
        )


    st.write(
        "### Unique Categories — SET"
    )

    st.write(
        get_unique_categories(
            books
        )
    )


    st.write(
        "### Active Members — SET"
    )

    st.write(
        get_active_member_ids(
            transactions
        )
    )