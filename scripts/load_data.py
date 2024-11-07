import requests
import json
import psycopg2
import openai
import os
from time import sleep
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_embedding(text: str):
    """Generate embedding using OpenAI API"""
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

def fetch_books():
    """Fetch 100 books from Open Library"""

    categories = [
        'programming',
        'web_development',
        'artificial_intelligence',
        'computer_science',
        'software_engineering'
    ]

    all_books = []

    for category in categories:
        # Request API
        url = f"https://openlibrary.org/subjects/{category}.json?limit=20"
        response = requests.get(url)
        response.raise_for_status()  # Raises an error for a bad response

        data = response.json()
        books = data.get("works", [])

        # Check if books were fetched
        if not books:
            print(f"No books found for category '{category}'")
            continue

        # Format each book
        for book in books:
            book_data = {
                "title": book.get("title", "Untitled"),
                "authors": [
                    author.get("name", "Unknown Author")
                    for author in book.get("authors", [])
                ],
                "first_publish_year": book.get("first_publish_year", "Unknown"),
                "subject": category,
            }

            all_books.append(book_data)

        print(f"Successfully processed {len(books)} books for {category}")

    if not all_books:
        print("No books were fetched from any category.")

    return all_books

def load_books_to_db():
    """Load books with embeddings into PostgreSQL"""
    # Wait for database to be ready
    sleep(5)

    # Database connection
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    cur = conn.cursor()

    # Fetch books
    books = fetch_books()

    # Insert each book
    for book in books:
        # Create description for embedding
        description = f"Book titled '{book['title']}' by {', '.join(book['authors'])}. "
        description += f"Published in {book['first_publish_year']}. "
        description += f"This is a book about {book['subject']}."

        # Generate embedding
        embedding = get_embedding(description)

        # Insert into database
        cur.execute(
            """
            INSERT INTO items (name, metadata, embedding)
            VALUES (%s, %s, %s)
            """,
            (
                book["title"],
                json.dumps(book),
                embedding
            )
        )

    # Commit and close
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    try:
        load_books_to_db()
        print("Successfully loaded sample books!")
    except Exception as e:
        print(f"Error loading books: {e}")