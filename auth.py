from user import User
from home import HomePage
from admin import is_admin

def sign_up():
    print("\n--- Sign Up ---")
    name = input("Name: ")
    email = input("Email: ")
    password = input("Password: ")
    age = input("Age: ")
    gender = input("Gender: ")
    nick = input("Nick Name: ")

    new_user = User(name, email, password, age, gender, nick)
    new_user.save_to_file()
    print("✅ Signed up successfully!")

def login():
    print("\n--- Login ---")
    email = input("Email: ")
    password = input("Password: ")

    # Check if admin first
    if is_admin(email, password):
        print("🔑 Admin login detected! Redirecting to admin panel...")
        from admin import admin_menu
        admin_menu()
        return

    # Regular user login
    users = User.load_users()
    for user in users:
        if user.email == email and user.password == password:
            print("✅ Login successful!")
            homepage = HomePage()
            homepage.set_current_user(user)
            homepage.show_home_menu()
            return

    print("❌ Invalid email or password")