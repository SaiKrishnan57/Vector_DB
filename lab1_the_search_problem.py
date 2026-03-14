#!/usr/bin/env python3
"""
Lab 1: The Search Problem - Why Traditional Keyword Search Fails
A simple demonstration showing why SQL LIKE search doesn't understand meaning
"""

import sqlite3
import os

def create_database():
    """Create a SQLite database with our company handbook"""
    # Remove old database if it exists
    if os.path.exists('company_handbook.db'):
        os.remove('company_handbook.db')
    
    # Create new database
    conn = sqlite3.connect('company_handbook.db')
    cursor = conn.cursor()
    
    # Create table
    cursor.execute('''
        CREATE TABLE policies (
            id INTEGER PRIMARY KEY,
            title TEXT,
            content TEXT
        )
    ''')
    
    # Insert our dress code policy
    cursor.execute('''
        INSERT INTO policies (title, content) VALUES (?, ?)
    ''', (
        'Dress Code Policy',
        'Business casual attire required Monday through Thursday. Jeans permitted on Fridays. No shorts or flip-flops allowed in the office.'
    ))
    
    conn.commit()
    return conn

def sql_search(conn, query):
    """Search using SQL LIKE - the traditional way"""
    cursor = conn.cursor()
    
    # Extract meaningful words from query
    words = query.lower().split()
    search_words = []
    skip_words = ['what', 'is', 'the', 'are', 'can', 'i', 'tell', 'me', 'about', 'should', 'to']
    
    for word in words:
        clean_word = word.strip('?.,!')
        if clean_word not in skip_words:
            search_words.append(clean_word)
    
    # Build SQL query
    conditions = []
    for word in search_words:
        conditions.append(f"LOWER(content) LIKE '%{word}%'")
    
    if conditions:
        sql = f"SELECT title, content FROM policies WHERE {' OR '.join(conditions)}"
    else:
        sql = "SELECT title, content FROM policies WHERE 1=0"
    
    # Execute the actual query
    cursor.execute(sql)
    results = cursor.fetchall()
    
    return results, search_words, sql

def main():
    """Run the interactive demonstration"""
    
    # Header
    print("=" * 70)
    print("🗄️  LAB 1: THE SEARCH PROBLEM")
    print("=" * 70)
    print("\nWelcome! I'm going to show you why traditional search frustrates users.")
    print("We'll use a real SQLite database with a company dress code policy.\n")
    
    # Setup database
    print("📚 STEP 1: Setting up the database...")
    print("-" * 50)
    conn = create_database()
    print("✅ Created SQLite database: company_handbook.db")
    print("✅ Added dress code policy to the database\n")
    
    # Show what's in the database
    cursor = conn.cursor()
    cursor.execute("SELECT title, content FROM policies")
    policy = cursor.fetchone()
    
    print("📄 What's in our database:")
    print("-" * 50)
    print(f"Title: {policy[0]}")
    print(f"Content: {policy[1]}\n")
    
    # Pause before starting
    input("➡️  Press Enter to see how employees search for this policy...")
    
    # Query 1: Using exact words that exist
    print("\n" + "=" * 70)
    print("🔍 QUERY 1: Employee uses words that EXIST in the policy")
    print("=" * 70)
    
    query1 = "Tell me about jeans and business casual"
    print(f'\nEmployee asks: "{query1}"')
    
    results, words, sql = sql_search(conn, query1)
    print(f"\n📝 SQL Query executed:")
    print(f"   {sql[:100]}...")
    print(f"\n🔎 Searched for words: {words}")
    
    if results:
        print(f"\n✅ SUCCESS! Found {len(results)} result(s)")
        print(f"   → {results[0][0]}: {results[0][1][:60]}...")
    else:
        print("\n❌ FAILED! No results found")
    
    print("\n💡 This worked because 'jeans' and 'business' and 'casual' are in the policy!")
    
    # Pause before next query
    input("\n➡️  Press Enter to see what happens with different words...")
    
    # Query 2: Using different words with same meaning
    print("\n" + "=" * 70)
    print("🔍 QUERY 2: Employee uses DIFFERENT words (same meaning)")
    print("=" * 70)
    
    query2 = "What are the clothing rules?"
    print(f'\nEmployee asks: "{query2}"')
    
    results, words, sql = sql_search(conn, query2)
    print(f"\n📝 SQL Query executed:")
    print(f"   {sql[:100]}...")
    print(f"\n🔎 Searched for words: {words}")
    
    if results:
        print(f"\n✅ SUCCESS! Found {len(results)} result(s)")
    else:
        print("\n❌ FAILED! No results found")
        print(f"   The database HAS the dress code policy...")
        print(f"   But SQL can't find it because these words aren't in it: {words}")
    
    print("\n💡 'clothing' means the same as 'attire', but SQL doesn't know that!")
    print("   'rules' means the same as 'policy', but SQL doesn't know that!")
    
    # Pause before next query
    input("\n➡️  Press Enter to try one more query...")
    
    # Query 3: Another example with different words
    print("\n" + "=" * 70)
    print("🔍 QUERY 3: Another employee query with different words")
    print("=" * 70)
    
    query3 = "What should I wear to work?"
    print(f'\nEmployee asks: "{query3}"')
    
    results, words, sql = sql_search(conn, query3)
    print(f"\n📝 SQL Query executed:")
    print(f"   {sql[:100]}...")
    print(f"\n🔎 Searched for words: {words}")
    
    if results:
        print(f"\n✅ SUCCESS! Found {len(results)} result(s)")
    else:
        print("\n❌ FAILED! No results found")
        print(f"   Again, the policy exists but SQL can't find it!")
        print(f"   None of these words are in the policy: {words}")
    
    print("\n💡 'wear' is related to 'dress code' but SQL only matches exact words!")
    
    # Pause before analysis
    input("\n➡️  Press Enter to see the analysis...")
    
    # Analysis
    print("\n" + "=" * 70)
    print("📊 THE PROBLEM WITH KEYWORD SEARCH")
    print("=" * 70)
    
    print("""
Our dress code policy contains:
   • "Business casual attire"
   • "Jeans permitted"
   • "No shorts or flip-flops"

But employees search using:
   • "clothing rules" (not "attire" or "policy")
   • "what to wear" (not "dress code")
   • "office fashion" (not "business casual")

SQL LIKE only matches EXACT words:
   ❌ "clothing" ≠ "attire" (even though they mean the same!)
   ❌ "rules" ≠ "policy" (even though they mean the same!)
   ❌ "wear" ≠ "dress" (even though they're related!)

Result: 67% of queries FAIL even though the answer EXISTS!

📈 Success Rate: Only 33% (1 out of 3 queries worked)
   • Query 1 ✅: Used exact words from the policy
   • Query 2 ❌: Used synonyms (clothing/attire)
   • Query 3 ❌: Used related words (wear/dress)
""")
    
    # What's next
    print("=" * 70)
    print("🎯 WHAT'S COMING NEXT")
    print("=" * 70)
    
    print("""
In the next labs, you'll learn how vector databases solve this:

Lab 2: Words → Numbers (Embeddings)
   • Convert "clothing" → [0.2, 0.8, 0.1, ...]
   • Convert "attire" → [0.2, 0.9, 0.1, ...]
   • Similar meanings = Similar numbers!

Ready to solve this problem?
Run: python lab2_embeddings_demo.py
""")
    
    # Save completion marker
    with open('lab1_the_search_problem.txt', 'w') as f:
        f.write("Lab 1 completed: SQL Search Problem Demonstrated\n")
        f.write("Database: company_handbook.db created\n")
        f.write("Success Rate: 33% (1/3 queries)\n")
        f.write("Failure Rate: 67% (2/3 queries)\n")
        f.write("Key Learning: SQL LIKE only matches exact words, not meaning\n")
    
    # Cleanup
    conn.close()
    
    print("\n✅ Lab 1 Complete!")
    print("   Completion file created: lab1_the_search_problem.txt")
    print("   Database saved: company_handbook.db")

if __name__ == "__main__":
    main()