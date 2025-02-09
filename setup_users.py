from AttendanceProject import initialize_users_file, add_user

# Initialize Users.csv
initialize_users_file('Users.csv')

# Add users (update names and IDs as needed)
add_user('Users.csv', 'Mummy', '001')
add_user('Users.csv', 'NARENDRA-MODI', '002')
add_user('Users.csv', 'RAHUL GANDHI', '003')
add_user('Users.csv', 'SWAYAM(ME)', '004')

print("Users setup completed successfully!")
