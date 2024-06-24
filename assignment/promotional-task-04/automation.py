import os
import subprocess

# Company's Base Directory
base_directory = "/vagrant"

# Company's Directory
company_directory = "Kodecamp-Stores"

# Name of Company CEO
ceo_name = "Bach"

# Employees
employees = {
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
company_directories = {
    "Finance-Budgets": "Finance-Manager",
    "Contract-Documents": "Legal",
    "Business-Projections": "Business-Strategist",
    "Business-Models": "Sales-Manager",
    "Employee-Data": "HR",
    "Company-Vision-and-Mission-Statement": "CEO",
    "Server-Configuration-Script": "System-Administrator"
}

# create_user_and_group_command = ["sudo", "useradd", "-m", "-G", "group", "employee_name"]  # legal Julius


# Create Users and assign them to a group
def create_employee(employee_name, group):
    try:
        subprocess.run(["sudo", "useradd", "-m", "-G", group, employee_name], )
        print(
            f"Created employee {employee_name} successfully and added to group {group}")

    except subprocess.CalledProcessError as e:
        print(f"Could not create employee {employee_name}: {e}")


# Create groups
def create_group(group_name):
    try:
        subprocess.run(['sudo', 'groupadd', group_name], check=True)
        print(f"Group '{group_name}' created successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to create group '{group_name}'. Error: {e.stderr}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")


# Check if directory exist
def check_dir():
    dirs = os.listdir("./")

    if company_directory in dirs:
        exist = "Directory exists"
    else:
        exist = "Directory does not exist"
    return exist


# Get current working directory
cwd = os.getcwd()


# Create directory
def create_directory(directory_name):
    if cwd == base_directory:
        directory_exist = check_dir()
        if directory_exist == "Directory does not exist":
            try:
                os.mkdir(f"{company_directory}/")
                create_directories(directory_name)
                print(
                    f"Directory /{company_directory}/{directory_name} created")

            except OSError as e:
                print(f"Error creating directory: {e}")
        else:
            create_directories(directory_name)
    else:
        os.chdir(base_directory)
        os.mkdir(f"{company_directory}/")
        create_directories(directory_name)
        print(f"Directory /{company_directory}/{directory_name} created")

# Create Directories


def create_directories(directory_name):
    try:
        os.makedirs(f"/{company_directory}/{directory_name}", exist_ok=True)
        print(f"Directory /{company_directory}/{directory_name} created")
    except OSError as e:
        print(
            f"Error creating directory /{company_directory}/{directory_name}: {e}")

# Set Permissions Functions


def set_permissions(directory_name, employee_name, group):
    try:
        subprocess.run(["sudo", "chown", f"{employee_name}:{group}",
                       f"/{company_directory}/{directory_name}"], check=True)
        if group == "CEO" and employee_name == ceo_name:
            set_ceo_permission(directory_name)
        else:
            subprocess.run(
                ["sudo", "chmod", "770", f"/{company_directory}/{directory_name}"], check=True)
        print(f"Permissions set for /{company_directory}/{directory_name}")
    except subprocess.CalledProcessError as e:
        print(
            f"Error setting permissions for /{company_directory}/{directory_name}: {e}")

# Set specific permissions for CEO


def set_ceo_permission(directory_name):
    try:
        subprocess.run(
            ["sudo", "chmod", "774", f"/{company_directory}/{directory_name}"], check=True)
        print(f"Permissions set for /{company_directory}/{directory_name}")
    except subprocess.CalledProcessError as e:
        print(
            f"Error setting permissions for /{company_directory}/{directory_name}: {e}")

# Add CEO to other groups


def other_groups_add_ceo():
    for group in company_directories.values():
        if group != "System-Administrator":
            try:
                subprocess.run(["sudo", "usermod", "-aG", group, ceo_name])
                print(f"Added CEO {ceo_name} to group {group}")
            except subprocess.CalledProcessError as e:
                print(f"Error adding CEO {ceo_name} to group {group}")


# Create Files in a specified directory
def create_file():
    filename = input("Enter the name of the file: ")
    directory_name = input("Enter the directory to create the file in: ")

    if directory_name in company_directories.keys():
        file_path = f"/{company_directory}/{directory_name}/{filename}"
        try:
            with open(file_path, "w") as file:
                file.write("This is a new file.\n")
            print(
                f"File {filename} created in /{company_directory}/{directory_name}")
        except IOError as e:
            print(f"Error creating file {filename}: {e}")
    else:
        print(
            f"Directory /{company_directory}/{directory_name} does not exist. File not created.")

# Main Function


def main():
    # Create users/Employees and directories
    for employee_name, group in employees.items():
        create_group(group)
        create_employee(employee_name, group)

    # Create directories
    for directory_name, group in company_directories.items():
        create_directory(directory_name)

        # Get employee
        employee = [employee_name for employee_name,
                    emp_group in employees.items() if emp_group == group]
        # Set Permissions
        if employee:
            set_permissions(directory_name, employee[0], group)

    # Call to add ceo to other groups
    other_groups_add_ceo()

    # Call to create file
    create_file()


# Call to main function
main()
