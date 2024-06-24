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


def run_command(command):
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")


def create_employee(employee_name, group):
    run_command(["sudo", "useradd", "-m", "-G", group, employee_name])
    print(f"Created employee {employee_name} and added to group {group}")


def create_group(group_name):
    run_command(['sudo', 'groupadd', group_name])
    print(f"Group '{group_name}' created successfully.")


def directory_exists(directory):
    return os.path.exists(directory)


def create_directory(directory_path):
    if not directory_exists(directory_path):
        os.makedirs(directory_path, exist_ok=True)
        print(f"Directory '{directory_path}' created")
    else:
        print(f"Directory '{directory_path}' already exists")


def set_permissions(directory_path, employee_name, group):
    run_command(["sudo", "chown", f"{employee_name}:{group}", directory_path])
    permissions = "774" if group == "CEO" and employee_name == CEO_NAME else "770"
    run_command(["sudo", "chmod", permissions, directory_path])
    print(f"Permissions set for '{directory_path}'")


def add_ceo_to_groups():
    for group in COMPANY_DIRECTORIES.values():
        if group != "System-Administrator":
            run_command(["sudo", "usermod", "-aG", group, CEO_NAME])
            print(f"Added CEO {CEO_NAME} to group {group}")


def create_file():
    filename = input("Enter the name of the file: ")
    directory_name = input("Enter the directory to create the file in: ")

    if directory_name in COMPANY_DIRECTORIES:
        file_path = f"/{COMPANY_DIRECTORY}/{directory_name}/{filename}"
        try:
            with open(file_path, "w") as file:
                file.write("This is a new file.\n")
            print(f"File '{filename}' created in '{file_path}'")
        except IOError as e:
            print(f"Error creating file '{filename}': {e}")
    else:
        print(
            f"Directory '{directory_name}' does not exist. File not created.")


def main():
    for employee_name, group in EMPLOYEES.items():
        create_group(group)
        create_employee(employee_name, group)

    for directory_name, group in COMPANY_DIRECTORIES.items():
        directory_path = f"/{COMPANY_DIRECTORY}/{directory_name}"
        create_directory(directory_path)

        employee = next(
            (name for name, role in EMPLOYEES.items() if role == group), None)
        if employee:
            set_permissions(directory_path, employee, group)

    add_ceo_to_groups()
    create_file()


if __name__ == "__main__":
    main()
