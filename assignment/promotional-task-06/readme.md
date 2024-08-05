# SETTING UP a VPC WITH PUBLIC AND PRIVATE SUBNETS, INTERNET AND NAT GATEWAYS, ROUTE TABLES, SECURITY GROUPS AND NETWORK ACCESS CONTROL LISTS (NACLs) USING TERRAFORM

## INTRODUCTION
In today's cloud-driven world, efficient and secure network infrastructure is paramount for the success of any application deployment. Amazon Web Services (AWS) provides robust tools to create and manage such infrastructures, and Terraform, an infrastructure as code (IaC) tool, simplifies this process by allowing you to define and provision your AWS resources using code.

Leveraging Terraform to manage your AWS infrastructure not only enhances efficiency and scalability but also ensures that your environment is consistently configured and easily reproducible, paving the way for a streamlined and secure cloud deployment process.

In the next few minutes we're going to set up a Virtual Private Cloud (VPC) on AWS, complete with both public and private subnets, Internet Gateway (IGW) and NAT Gateway for internet connectivity, route tables for traffic management, security groups for instance-level security, and Network Access Control Lists (NACLs) for subnet-level security, all using Terraform.

## PREREQUISITES
Before we get started, ensure you have an AWS account and have already installed the Terraform CLI and AWS CLI. If you haven't installed them yet, you can follow the links below for the installation instructions:
- Terraform CLI (https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli)
- AWS CLI (https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
Having these tools installed and configured is essential for the setup process.

## CONFIGURE AWS PROFILE
After acquiring and installing the necessary tools, you need to configure your AWS profile locally. This configuration will allow Terraform to create all the resources in that profile. To configure your AWS profile, it's recommended to create an IAM user.

**Create an IAM User**
   - Log in to your AWS account.
   - Create an IAM user and generate a secret access key.
   - Attach the required policies (examples include VPC Full Access and EC2 Full Access).

   **Note:** Download your secret key and keep it safe, as this is the only time you can view or access it.

**Configure Your AWS Profile**
   - Open your terminal and enter the following command:
     ```bash
     aws configure --profile <aws-profile-name>
     ```
   - Replace `<aws-profile-name>` with your AWS username, e.g., `kc-dave`.
   - At the prompts, copy and paste your keys. Set your region to `eu-west-1` and output format to `json`.

<!-- By following these steps, you'll have your AWS profile configured and ready for Terraform to use in creating and managing your resources. -->

## WRITE TERRAFORM CODE
Now that our setup is complete, we will write the Terraform code to create the resources in our AWS account. Terraform recommends using modules so we're going to create modules for each resource. The structure of our directory will look like this
```bash
├── .gitignore
├── readme.md
├── terraform
│   ├── main.tf
│   ├── modules
│   │   ├── instances
│   │   │   ├── main.tf
│   │   │   ├── outputs.tf
│   │   │   ├── scripts
│   │   │   │   ├── install_nginx.sh
│   │   │   │   └── install_postgresql.sh
│   │   │   └── variables.tf
│   │   ├── internet_gateway
│   │   │   ├── main.tf
│   │   │   ├── outputs.tf
│   │   │   └── variables.tf
│   │   ├── nacls
│   │   │   ├── main.tf
│   │   │   ├── outputs.tf
│   │   │   └── variables.tf
│   │   ├── nat_gateway
│   │   │   ├── main.tf
│   │   │   ├── outputs.tf
│   │   │   └── variables.tf
│   │   ├── route_table
│   │   │   ├── main.tf
│   │   │   ├── outputs.tf
│   │   │   └── variables.tf
│   │   ├── security_groups
│   │   │   ├── main.tf
│   │   │   ├── outputs.tf
│   │   │   └── variables.tf
│   │   ├── subnets
│   │   │   ├── main.tf
│   │   │   ├── outputs.tf
│   │   │   └── variables.tf
│   │   └── vpc
│   │       ├── main.tf
│   │       ├── outputs.tf
│   │       └── variables.tf
│   ├── output.tf
│   ├── tfplan.json
│   └── variables.tf

```
You can create all the files and folders at once or one at a time.
We start by creating the VPC.

### STEP 1 - CREATE VPC
We create the VPC with the following details
- Name: KCVPC
- IPv4 CIDR block: 10.0.0.0/16

Create the vpc directory and create `main.tf`, `variables.tf` and `outputs.tf`
In the `main.tf` files, create your vpc resource
`main.tf`
```bash
resource "aws_vpc" "vpc" {
  cidr_block = var.vpc_cidr_block

  tags = {
    Name = var.vpc_name
   }
}
```

In the `varibles.tf` file, create the required variables
`variables.tf`
```bash
variable "vpc_name" {
  description = "Name of the VPC"
  type        = string
  default     = "KCVPC"
}

variable "vpc_cidr_block" {
  description = "CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"
}
```

In the `outputs.tf` file, output any variable or value that you may need. Outputting a value or variable will make it available for use by other resources.
`outputs.tf`
```bash
output "vpc_id" {
  value = aws_vpc.vpc.id
}

output "vpc_cidr_block" {
  value = var.vpc_cidr_block
}
```
The above code blocks will create a VPC in the eu-west-1 region with the name `KCVPC` and a CIDR block `10.0.0.0/16`

### STEP 2 - CREATE SUBNETS
Now we create a public and private subnets with following information


## EXECUTE TERRAFORM COMMANDS

## ARCHITECTURAL DIAGRAM

## TFPLAN OUTPLAN