#=====importing libraries===========
from datetime import datetime


#=====Functions===========

def get_login_details():
# Read lines from user.txt and add to the logindetails dictionary
    with open("user.txt", "r") as userfile: 
        login = userfile.readlines()
        for line in login:
            line = line.strip().split(", ")
            logindetails[line[0]] = line[1]


def reg_user():
# Request new username
    new_user = input("\nPlease enter a new username: ")

# Check if username already exists
    while True:    
        if new_user in logindetails:
            new_user = input("User already exists. Please enter a new username: ")
        else:
            break

# Request new password
    new_password = input("Please enter a password: ")
    confirm_password = input("Please confirm your password: ")

# Check passwords match & add to user.txt if they do
    if confirm_password == new_password:
        with open("user.txt", "a") as f:
            f.write(new_user + ", " + new_password + "\n")
            return print(f"New user '{new_user}' added\n")
    else:
        return print("Passwords do not match\n")

def get_tasks():
# Read lines from tasks.txt as add to tasks dictionary
    with open("tasks.txt", "r") as f:
        task_id = 1
        temp = f.readlines()
        for task in temp:
            id = {}
            task = task.strip().split(", ")
            id["task_id"] = task_id
            id["assigned_to"] = task[0]
            id["task_title"] = task[1]
            id["task_description"] = task[2]
            id["date_assigned"] = task[3]
            id["due_date"] = task[4]
            id["task_status"] = task[5]
            tasks[task_id] = id
            task_id += 1
        return(tasks)

def update_taskfile():
# Update tasks.txt from the tasks dictionary
    with open("tasks.txt", "w") as taskfile:
        for task in tasks:
            taskfile.write(tasks[task]["assigned_to"] + ", " + tasks[task]["task_title"] + ", " + tasks[task]["task_description"] + ", " + tasks[task]["date_assigned"] + ", " + tasks[task]["due_date"] + ", " + tasks[task]["task_status"] + "\n")

def add_task():
    get_tasks()

# Ask which user to assign to
    assign_user = input("\nWhich user should the task be assigned to: ")
    while True:

# Check user exists, and if so, ask for task details and add to tasks dictionary
        if assign_user in logindetails:
            tasks["new_task"] = {"assigned_to" : assign_user, "task_title" : input("Task Title: "), "task_description" : input("Task Description: "), "due_date" : input("Task Due Date (e.g. '10 Oct 2019'): "), "date_assigned" : datetime.today().strftime("%d %b %Y"), "task_status" : "No"}
            update_taskfile()
            print("\nTask added successfully \n")
            break
        else:
            assign_user = input("User doesn't exist. Please enter another user: ")

def view_all():
    print("\nAll Tasks:")

# Retrive tasks from tasks.txt and print
    get_tasks()
    for task in tasks:
        print(f'''
Task ID:\t\t{tasks[task]["task_id"]}
Task:\t\t\t{tasks[task]["task_title"]}
Assigned to:\t\t{tasks[task]["assigned_to"]}
Date assigned:\t\t{tasks[task]["date_assigned"]}
Due date:\t\t{tasks[task]["due_date"]}
Task Complete?\t\t{tasks[task]["task_status"]}
Task description:\t{tasks[task]["task_description"]}

-----------------------------------------------------------------------------------------------------------------------------------------
''')

def view_mine():
    print("\nMy Tasks:")

# Retrive tasks from tasks.txt and print all tasks for the current user
    get_tasks()
    for task in tasks:
        if username == tasks[task]["assigned_to"]:
            print(f'''
Task ID:\t\t{tasks[task]["task_id"]}
Task:\t\t\t{tasks[task]["task_title"]}
Assigned to:\t\t{tasks[task]["assigned_to"]}
Date assigned:\t\t{tasks[task]["date_assigned"]}
Due date:\t\t{tasks[task]["due_date"]}
Task Complete?\t\t{tasks[task]["task_status"]}
Task description:\t{tasks[task]["task_description"]}

-----------------------------------------------------------------------------------------------------------------------------------------
''')

    edit_my_task()

def edit_my_task():

# Select which task to edit
    selection = int(input("To edit a task, enter the task number. Or enter '-1' to exit to menu: ")) # Select which task to edit
    while True:    

# '-1' exits to menu
        if selection == -1:
            break

# Ask if the user to like to mark as complete
        elif selection == tasks[selection]["task_id"] and tasks[selection]["task_status"] == "No":
            change_status = input("Would you like to mark the task as complete? Yes/No : ").lower()
            while True:
                if change_status == "yes":
                    tasks[selection]["task_status"] = "Yes"
                    break
                elif change_status == "no":
                    break
                else:
                    change_status = input("Invalid selection. Please try again: ").lower()

# Ask if the user wants to change who the task is assigned to
            change_user = input("Would you like to assign this task to another user? Yes/No : ").lower()
            while True:
                if change_user == "yes":
                    user_update = input("Which user would you like to assign this task to? ")
                    while True:    
                        if user_update in logindetails:
                            tasks[selection]["assigned_to"] = user_update
                            break
                        else:
                            user_update = input("This user doesn't exist. Please enter another user:  ")
                    break
                elif change_user == "no":
                    break
                else:
                    change_user = input("Invalid selection. Please try again: ").lower()

# Ask the user if they want to amend the due date
            change_due_date = input("Would you like to change the due date? Yes/No : ").lower()
            while True:
                if change_due_date == "yes":
                    tasks[selection]["due_date"] = input("New task due date (e.g. '10 Oct 2019'): ")
                    break
                elif change_due_date == "no":
                    break
                else:
                    change_due_date = input("Invalid selection. Please try again: ").lower()
            break
        elif selection == tasks[selection]["task_id"] and tasks[selection]["task_status"] == "Yes":
            selection = int(input("You can't edit a task that is complete. Please enter another task id or '-1' to go back to menu: "))
        else:
            selection = int(input("Invalid input. Please try again: "))

# Update tasks.txt
    update_taskfile()
    print("\n")

def task_overview():
    with open("task_overview.txt", "w") as file:
        get_tasks()

# Create starting values
        total_tasks = len(tasks)
        completed_tasks = 0
        uncompleted_tasks = 0
        overdue_tasks = 0
        today = datetime.today()

# Check whether tasks are complete or not, and whether it's overdue
        for task in tasks:
            if tasks[task]["task_status"] == "Yes":
                completed_tasks += 1
            elif tasks[task]["task_status"] == "No":
                uncompleted_tasks += 1
        for task in tasks:
            if tasks[task]["task_status"] == "No" and datetime.strptime(tasks[task]["due_date"], '%d %b %Y') < today:
                overdue_tasks += 1

# Write to task_overview.txt
        file.write(f'''Task Overview:

Total number of tasks : {total_tasks}
Total number of completed tasks : {completed_tasks}
Total number of uncompleted tasks : {uncompleted_tasks}
Total number of overdue tasks : {overdue_tasks}
Percentage of tasks that are incomplete : {(uncompleted_tasks / total_tasks) * 100}%
Percentage of tasks that are overdue : {(overdue_tasks / uncompleted_tasks) * 100}%
''')
    print("\nTask overview report created.\nUser overview created\n")

def user_overview():
    with open("user_overview.txt", "w") as file:
        get_login_details()
        get_tasks()
        file.write(f'''User Overview:

Total number of users : {len(logindetails)}
Total number of tasks : {len(tasks)}
''')

        with open("user.txt", "r") as userfile: 

# Add usernames from users.txt to a list
            userlist = []
            login = userfile.readlines()
            for line in login:
                line = line.strip().split(", ")
                userlist.append(line[0])

# For each user in list, count the number of tasks that are complete, incomplete or overdue
            for user in userlist:
                user_total_tasks = 0
                completed_tasks = 0
                uncompleted_tasks = 0
                overdue_tasks = 0
                today = datetime.today()
                for task in tasks:
                    if tasks[task]["assigned_to"] == user:
                        if tasks[task]["task_status"] == "Yes":
                            user_total_tasks += 1
                            completed_tasks += 1
                        elif tasks[task]["task_status"] == "No":
                            user_total_tasks += 1                    
                            uncompleted_tasks += 1
                for task in tasks:
                    if tasks[task]["assigned_to"] == user:
                        if tasks[task]["task_status"] == "No" and datetime.strptime(tasks[task]["due_date"], '%d %b %Y') < today:
                            overdue_tasks += 1

# If total tasks for user is not 0, write details to user_overview.txt
                if user_total_tasks != 0:
                    file.write(f'''
User : {user}
Total tasks for user : {user_total_tasks}
Completed tasks for user : {completed_tasks}
Uncompleted tasks for user : {uncompleted_tasks}
Percentage of tasks that are incomplete : {(uncompleted_tasks / user_total_tasks) * 100}%
Percentage of tasks that are overdue : {(overdue_tasks / uncompleted_tasks) * 100}%       
''')

# If user tasks == 0 then just print that
                else:
                    file.write(f'''
User : {user}
Total tasks for user : {user_total_tasks}
''')

def generate_reports():
    task_overview()
    user_overview()

def view_stats():

# Generate reports and print from txt files to console
    generate_reports()
    with open("task_overview.txt", "r") as taskoverview_file:
        temp = taskoverview_file.read()
        print(temp)
    with open("user_overview.txt", "r") as useroverview_file:
        temp = useroverview_file.read()
        print(temp)


#====Login Section====

# Create dictionary for login details and tasks
logindetails = {}
tasks = {}

# Retrieve login details
get_login_details()

# Request username from user
username = input("Please enter your username: ")

# Check if username is in list
while True:
    if username in logindetails:

# Request password from user, check matches. If not ask again
        password = input("Please enter your password: ")
        while True:
            if password == logindetails[username]:
                print("\nLogin successful\n")
                break
            else:
                password = input("Incorrect password. Please enter your password again: ")
        break
    else:
        username = input("Incorrect username. Please enter your username again: ")

#====Program Section====
while True:

# Menu if admin
    if username == "admin":
        menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - Generate reports
ds - Display statistics
e - Exit
: ''').lower()

# Menu if not admin
    else:
        menu = input('''Select one of the following Options below:
a - Adding a task
va - View all tasks
vm - view my task
e - Exit
: ''').lower()

# If admin, allow user to register new users
    if menu == 'r' and username == "admin":
        reg_user()
        get_login_details() # Retrieve login details again to include new user into memory

# Add new tasks
    elif menu == 'a':
        add_task()

# View all tasks
    elif menu == 'va':
        view_all()

# View all tasks that are assigned to the current user
    elif menu == 'vm':
        view_mine()      

# If admin, allow use to view statistics
    elif menu == 'gr' and username == "admin":
        generate_reports()

# If admin, allow use to view statistics
    elif menu == 'ds' and username == "admin":
        view_stats()

# Exit
    elif menu == 'e':
        print('\nGoodbye!!!')
        exit()

# Incorrect entry
    else:
        print("\nYou have made a wrong choice, Please Try again\n")