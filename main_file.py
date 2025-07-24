# from auth import login, sign_up
# from admin import admin_login
# import os

# def main():
#     # Create data directories if they don't exist
#     os.makedirs("data/scores", exist_ok=True)
    
#     while True:
#         print("\n===== 🎮 Game Management System =====")
#         print("1. Sign Up")
#         print("2. Login")
#         print("3. Admin Login")
#         print("4. Exit")
#         choice = input("Choose an option: ")

#         if choice == "1":
#             sign_up()
#         elif choice == "2":
#             login()
#         elif choice == "3":
#             admin_login()
#         elif choice == "4":
#             print("👋 Exiting...")
#             break
#         else:
#             print("❌ Invalid choice. Please try again.")

# if __name__ == "__main__":
#     main()