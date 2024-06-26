import os
import subprocess

# Company's Base Directory
BASE_DIRECTORY = "/vagrant"

# Company's Directory
COMPANY_DIRECTORY = "Kodecamp-Stores"

# Name of Company CEO
CEO_NAME = "Bach"

# Employees
EMPLOYEES = {
    "Andrew": "System-Administrator",
    "Julius": "Legal",
    "Chizi": "HR",
    "Jeniffer": "Sales-Manager",
    "Adeola": "Business-Strategist",
    "Bach": "CEO",
    "Gozie": "IT-Intern",
    "Ogochukwu": "Finance-Manager"
}

# Company directories
COMPANY_DIRECTORIES = {
    "Finance-Budgets": "Finance-Manager",
    "Contract-Documents": "Legal",
    "Business-Projections": "Business-Strategist",
    "Business-Models": "Sales-Manager",
    "Employee-Data": "HR",
    "Company-Vision-and-Mission-Statement": "CEO",
    "Server-Configuration-Script": "System-Administrator"
}

# Function to Run Subprocess Command
def run_command(command):
    # Use try/except to run subprocess command. catch any error thrown
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        # Print message when error occurs
        print(f"Command failed: {e}")

# Create Employees Function
def create_employee(employee_name, group):
    # Run command to create user/employee
    run_command(["sudo", "useradd", "-m", "-G", group, employee_name])
    # Print success message
    print(f"Created employee {employee_name} and added to group {group}")

# Create Group Function
def create_group(group_name):
    # Run command to create group
    run_command(['sudo', 'groupadd', group_name])
    # Print success messsage
    print(f"Group '{group_name}' created successfully.")

# Function to check if directory exists
def directory_exists(directory):
    # Return True if path exist and False if otherwise
    return os.path.exists(directory)

# Create directory function
def create_directory(directory_path):
    # Check if directory exists
    # If directory does not exist
    if not directory_exists(directory_path):
        # Create the directories
        os.makedirs(directory_path, exist_ok=True)
        # Print success message
        print(f"Directory '{directory_path}' created")
    else:
        # if directory exists, print directory exists message
        print(f"Directory '{directory_path}' already exists")

# Set permissions functions
def set_permissions(directory_path, employee_name, group):
    # Run command to change directory ownership
    run_command(["sudo", "chown", f"{employee_name}:{group}", directory_path])
    # set permission 774 for CEO and 770 for others
    permissions = "774" if group == "CEO" and employee_name == CEO_NAME else "770"
    # Run the command
    run_command(["sudo", "chmod", permissions, directory_path])
    # Print success message
    print(f"Permissions set for '{directory_path}'")

# function to add CEO to other groups except the system admin's group
def add_ceo_to_groups():
    # Loop through roles/groups
    for group in COMPANY_DIRECTORIES.values():
        # If role is not system admin
        if group != "System-Administrator":
            # Run command to add CEO
            run_command(["sudo", "usermod", "-aG", group, CEO_NAME])
            # Print Success message
            print(f"Added CEO {CEO_NAME} to group {group}")

# create file function
def create_file():
    # Get filename from user input
    filename = input("Enter the name of the file: ")
    # Get directory name from user input
    directory_name = input("Enter the directory to create the file in: ")

    # Check if directory name is in the company's directories
    if directory_name in COMPANY_DIRECTORIES:
        # Set file path to the specified directory
        file_path = f"/{COMPANY_DIRECTORY}/{directory_name}/{filename}"
        # Use try/except to create file and catch errors/exceptions
        try:
            # Create file
            with open(file_path, "w") as file:
                # Create file with dummy text
                file.write("This is a new file.\n")
            # print success message
            print(f"File '{filename}' created in '{file_path}'")
        # Catch errors/exceptions
        except IOError as e:
            # Print error message
            print(f"Error creating file '{filename}': {e}")
    else:
        # Print directory does not exist message
        print(
            f"Directory '{directory_name}' does not exist. File not created.")

# Main function
def main():
    for employee_name, group in EMPLOYEES.items():
        # call to create group function
        create_group(group)
        # call to create employee function
        create_employee(employee_name, group)

    for directory_name, group in COMPANY_DIRECTORIES.items():
        directory_path = f"/{COMPANY_DIRECTORY}/{directory_name}"
        # call to create directory function
        create_directory(directory_path)

        employee = next(
            (name for name, role in EMPLOYEES.items() if role == group), None)
        if employee:
            # call to set permissions function
            set_permissions(directory_path, employee, group)

    # call to add ceo to other group function
    add_ceo_to_groups()

    # call to create file function
    create_file()


# Run Script
if __name__ == "__main__":
    main()
