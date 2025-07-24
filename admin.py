from user import User
import os

ADMIN_EMAIL = "admin@gmail.com"
ADMIN_PASSWORD = "adminmain90@"

def is_admin(email, password):
    return email == ADMIN_EMAIL and password == ADMIN_PASSWORD

def admin_login():
    print("\n--- Admin Login ---")
    email = input("Email: ")
    password = input("Password: ")
    
    if is_admin(email, password):
        print("🔑 Admin login successful!")
        admin_menu()
    else:
        print("❌ Invalid admin credentials")

def admin_menu():
    while True:
        print("\n===== Admin Panel =====")
        print("1. View All Users")
        print("2. Delete User")
        print("3. View All Scores")
        print("4. Add New Game")
        print("5. Back to Main Menu")
        choice = input("Choose an option: ")
        
        if choice == "1":
            view_all_users()
        elif choice == "2":
            delete_user()
        elif choice == "3":
            view_all_scores()
        elif choice == "4":
            add_new_game()
        elif choice == "5":
            break
        else:
            print("❌ Invalid choice")

def view_all_users():
    users = User.load_users()
    print("\n👥 All Users:")
    for i, user in enumerate(users, 1):
        print(f"{i}. {user.name} ({user.email}) - {user.nick}")

def delete_user():
    email = input("\nEnter user email to delete: ")
    users = User.load_users()
    updated_users = [u for u in users if u.email != email]
    
    with open("data/users.txt", "w") as file:
        for user in updated_users:
            file.write(f"{user.name},{user.email},{user.password},{user.age},{user.gender},{user.nick}\n")
    print("✅ User deleted successfully" if len(updated_users) < len(users) else "❌ User not found")

def view_all_scores():
    if not os.path.exists("data/scores"):
        print("No scores recorded yet")
        return
        
    print("\n📊 All User Scores:")
    for filename in os.listdir("data/scores"):
        if filename.endswith(".txt"):
            with open(f"data/scores/{filename}") as f:
                print(f"\n📄 {filename.replace('.txt','')}:")
                print(f.read())

def add_new_game():
    print("\n🎮 Add New Game (Feature in development)")
    # Implementation would add new games to the menu