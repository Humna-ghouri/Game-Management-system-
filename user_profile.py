# from user import User

# def view_profile(current_user):
#     if current_user:
#         print(f"\n👤 Profile of {current_user.nick}:")
#         print(f"Name: {current_user.name}")
#         print(f"Email: {current_user.email}")
#         print(f"Age: {current_user.age}")
#         print(f"Gender: {current_user.gender}")
#         print(f"Nickname: {current_user.nick}")

# def edit_profile(current_user):
#     if current_user:
#         print("\n✏️ Edit Profile")
#         name = input(f"Name [{current_user.name}]: ") or current_user.name
#         email = input(f"Email [{current_user.email}]: ") or current_user.email
#         password = input(f"Password [{current_user.password}]: ") or current_user.password
#         age = input(f"Age [{current_user.age}]: ") or current_user.age
#         gender = input(f"Gender [{current_user.gender}]: ") or current_user.gender
#         nick = current_user.nick

#         updated_user = User(name, email, password, age, gender, nick)
#         User.update_user(nick, updated_user)
#         current_user = updated_user
#         print("✅ Profile updated successfully!")