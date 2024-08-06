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

In the `varibles.tf` file, create the required variables.
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
**Public Subnet**

- Name: PublicSubnet
- IPv4 CIDR block: 10.0.1.0/24
- Availability Zone: Select any one from your region (eg. eu-west-1c)

**Private Subnet**

- Name: PrivateSubnet
- IPv4 CIDR block: 10.0.2.0/24
- Availability Zone: Same region as public subnet (eg. eu-west-1c)

In the modules directory, create a folder and name it `subnet`. Create the required files inside the `subnet` directory.
`main.tf`
`variables.tf`
`outputs.tf`
Inside our `main.tf` file, we write the code to create our `PublicSubnet` and `PrivateSubnet`.
`main.tf`

```bash
resource "aws_subnet" "public" {
  vpc_id            = var.vpc_id
  cidr_block        = var.public_cidr_block
  availability_zone = var.public_availability_zone

  tags = {
    Name = var.public_subnet_name
  }
}

resource "aws_subnet" "private" {
  vpc_id            = var.vpc_id
  cidr_block        = var.private_cidr_block
  availability_zone = var.private_availability_zone

  tags = {
    Name = var.private_subnet_name
  }
}

```

Then we create our variables as used in the `main.tf` file.
`variables.tf`

```bash
variable "vpc_id" {
  description = "VPC ID"
  type        = string
}

variable "public_subnet_name" {
  description = "Name of the public subnet"
  type        = string
  default     = "PublicSubnet"
}

variable "public_cidr_block" {
  description = "CIDR block for the public subnet"
  type        = string
  default     = "10.0.1.0/24"
}

variable "public_availability_zone" {
  description = "Availability zone for the public subnet"
  type        = string
  default = "eu-west-1c"
}

variable "private_subnet_name" {
  description = "Name of the private subnet"
  type        = string
  default     = "PrivateSubnet"
}

variable "private_cidr_block" {
  description = "CIDR block for the private subnet"
  type        = string
  default     = "10.0.2.0/24"
}

variable "private_availability_zone" {
  description = "Availability zone for the private subnet"
  type        = string
  default = "eu-west-1c"
}

```

Now we output values or variables we want to expose to other resources.
`outputs.tf`

```bash
output "public_subnet_id" {
  value = aws_subnet.public.id
}

output "private_subnet_id" {
  value = aws_subnet.private.id
}

```

The above code will create a public and a private subnet with the details specified and will expose the `public_subnet_id` and `private_subnet_id` values for other resources to access.

### STEP 3 - CONFIGURE AN INTERNET GATEWAY

Still in the modules directory, create `internet_gateway` folder and create the `main.tf`, `variables.tf`, and `outputs.tf` files inside it.
Write the code to create an Internet Gateway in the `main.tf` file.
`main.tf`

```bash
resource "aws_internet_gateway" "main" {
  vpc_id = var.vpc_id

  tags = {
    Name = var.igw_name
  }
}

```

Create the variables specified
`variables.tf`

```bash
variable "vpc_id" {
  description = "VPC ID"
  type        = string
}

variable "igw_name" {
  description = "Name for the Internet Gateway"
  type = string
  default = "KC-IGW"
}

```

Expose variables
`outputs.tf`

```bash
output "internet_gateway_id" {
  value = aws_internet_gateway.main.id
}

```

We created and attached the `internet_gateway` to our VPC.

### STEP 4 - CONFIGURE ROUTE TABLES

We will create Public and Private Route Tables with the following details
**Public Route Table**

- Name: PublicRouteTable
- Associate with `PublicSubnet`
- Add route to `internet_gateway` (0.0.0.0/0 -> IGW)

**Private Route Table**

- Name: PrivateRouteTable
- Associate with `PrivateSubnet`
- Ensure no direct route to the internet.

Just as we've been doing, create the necessary files inside `route_table` folder in the modules directory.

- Folder: `route_table`
  - Files: `main.tf`, `variables.tf`, `outputs.tf`
    We create our `route_table` resources in the `main.tf` file
    `main.tf`

```bash
resource "aws_route_table" "public" {
  vpc_id = var.vpc_id

  route {
    cidr_block = var.internet_cidr_block
    gateway_id = var.internet_gateway_id
  }

  tags = {
    Name = var.public_route_table_name
  }
}

resource "aws_route_table_association" "public" {
  subnet_id      = var.public_subnet_id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table" "private" {
  vpc_id = var.vpc_id

  tags = {
    Name = var.private_route_table_name
  }
}

resource "aws_route_table_association" "private" {
  subnet_id      = var.private_subnet_id
  route_table_id = aws_route_table.private.id
}

```

Create the specified variables
`variables.tf`

```bash
variable "vpc_id" {
  description = "VPC ID"
  type        = string
}

variable "internet_cidr_block" {
  description = "Internet routing IPv4 cidr block"
  type        = string
  default     = "0.0.0.0/0"
}

variable "internet_gateway_id" {
  description = "Internet Gateway ID"
  type        = string
}

variable "public_subnet_id" {
  description = "Public subnet ID"
  type        = string
}

variable "public_route_table_name" {
  description = "Name of public route table"
  type        = string
  default     = "PublicRouteTable"
}

variable "private_subnet_id" {
  description = "Private subnet ID"
  type        = string
}

variable "private_route_table_name" {
  description = "Name of private route table"
  type        = string
  default     = "PrivateRouteTable"
}

```

Expose needed variables
`output.tf`

```bash
output "public_route_table_id" {
  value = aws_route_table.public.id
}

output "private_route_table_id" {
  value = aws_route_table.private.id
}

output "internet_cidr_block" {
  value = var.internet_cidr_block
}
```

We have created public and private route tables and associated each to their respective subnets. Also we have added a route to the `internet_gateway` in the `PublicRouteTable` and have ensured that there is no direct route to the internet in the `PrivateRouteTable`.

### STEP 5 - CONFIGURE NAT GATEWAY

Now we're going to create a NAT Gateway in the `PublicSubnet`, allocate an Elastic IP for it and later update the `PrivateRouteTable` to route internet traffic to the NAT Gateway.
Create `nat_gateway` folder in the modules directory with the necessary files.

Write the code to create our `nat_gateway` resource.
`main.tf`

```bash
resource "aws_eip" "nat" {
  domain = "vpc"
}

resource "aws_nat_gateway" "main" {
  allocation_id = aws_eip.nat.id
  subnet_id     = var.public_subnet_id

  tags = {
    Name = var.nat_gateway_name
  }
}

```

Create the variables specified
`variables.tf`

```bash
variable "public_subnet_id" {
  description = "Public subnet ID"
  type        = string
}

variable "private_route_table_id" {
  description = "Private route table ID"
  type        = string
}

variable "nat_gateway_name" {
  description = "Name of NAT Gateway"
  type        = string
  default     = "KC-NAT-Gateway"
}

```

Output the needed values
`outputs.tf`

```bash
output "nat_gateway_id" {
  value = aws_nat_gateway.main.id
}

```

Now we will update `PrivateRouteTable` to route internet traffic to the `nat_gateway`.
Edit the `main.tf` file in the `route_table` with the following code.

`route_table/main.tf`

```bash
  route {
    cidr_block     = var.internet_cidr_block
    nat_gateway_id = var.nat_gateway_id
  }
```

Add the variablec `nat_gateway_id` to the `route_table`'s `variable.tf` file
`route_table/variables.tf`

```bash
variable "nat_gateway_id" {
  description = "NAT Gateway ID"
  type        = string
}

```

### STEP 6 - SET UP SECURITY GROUPS

We are going to create Security group for public and private instances(eg. web server and database server). We will specify inbound and outbound rules for both as follows
**Public Instance**
**Inbound Rules**

- HTTP(80) from anywhere(0.0.0.0/0)
- HTTPS(443) from anywhere(0.0.0.0/0)
- SSH(22) from local IP

**Outbound Rules**

- All traffic

**Private Instances**
**Inbound Rules**

- PostgreSQL(5432) from `PublicSubnet`(10.0.1.0/24)

**Outbound Rules**

- All traffic

Create `security_groups` folder under the `modules` directory with the required Terraform files (`main.tf`, `variables.tf`, `outputs.tf`).
In the `main.tf` file write the below code

```bash
resource "aws_security_group" "public" {
  name        = var.public_sg_name
  description = "Security group for public instances"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = [var.internet_cidr_block]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = [var.internet_cidr_block]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.local_ip]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = [var.internet_cidr_block]
  }

  tags = {
    Name = "PublicSecurityGroup"
  }
}

resource "aws_security_group" "private" {
  name        = var.private_sg_name
  description = "Security group for private instances"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    security_groups = [aws_security_group.public.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = [var.internet_cidr_block]
  }

  tags = {
    Name = "PrivateSecurityGroup"
  }
}

```

Now create the variables used above.
`variables.tf`

```bash
variable "vpc_id" {
  description = "VPC ID"
  type        = string
}

variable "internet_cidr_block" {
  description = "public internet routing IPv4 cidr block"
  type        = string
}

variable "local_ip" {
  description = "IP address to allow SSH access from"
  type        = string
}

variable "public_sg_name" {
  description = "Name of public security group"
  type = string
  default = "PublicSG"
}

variable "private_sg_name" {
  description = "Name of private security group"
  type = string
  default = "PrivateSG"
}

```

Expose the needed values
`outputs.tf`

```bash
output "public_sg_id" {
  value = aws_security_group.public.id
}

output "private_sg_id" {
  value = aws_security_group.private.id
}

```

### STEP 7 - CONFIGURE NETWORK ACLS (NACLs)

We will create a public and private NACLs to add additional security layer to both subnets with the below details.
**Public Subnet NACL**
**Inbound Rules**

- HTTP(80) from anywhere(0.0.0.0/0)
- HTTPS(443) from anywhere(0.0.0.0/0)
- SSH(22) from local IP

**Outbound Rules**

- All traffic

**Private Subnet NACL**
**Inbound Rules**

- PostgreSQL(5432) from `PublicSubnet`(10.0.1.0/24)

**Outbound Rules**

- All traffic

Create `nacls` folder inside the `modules` directory with the required files.
In the `main.tf` file write

```bash
resource "aws_network_acl" "public" {
  vpc_id     = var.vpc_id
  subnet_ids = [var.public_subnet_id]

  egress {
    from_port  = 0
    to_port    = 0
    protocol   = "-1"
    rule_no    = 100
    action     = "allow"
    cidr_block = "0.0.0.0/0"
  }

  ingress {
    from_port  = 80
    to_port    = 80
    protocol   = "tcp"
    rule_no    = 100
    action     = "allow"
    cidr_block = "0.0.0.0/0"
  }

  ingress {
    from_port  = 443
    to_port    = 443
    protocol   = "tcp"
    rule_no    = 110
    action     = "allow"
    cidr_block = "0.0.0.0/0"
  }

  ingress {
    from_port  = 22
    to_port    = 22
    protocol   = "tcp"
    rule_no    = 120
    action     = "allow"
    cidr_block = var.local_ip
  }

  tags = {
    Name = var.public_nacl_name
  }
}

resource "aws_network_acl" "private" {
  vpc_id     = var.vpc_id
  subnet_ids = [var.private_subnet_id]

  egress {
    from_port  = 80
    to_port    = 80
    protocol   = "tcp"
    rule_no    = 100
    action     = "allow"
    cidr_block = "0.0.0.0/0"
  }

  egress {
    from_port  = 0
    to_port    = 0
    protocol   = "-1"
    rule_no    = 110
    action     = "allow"
    cidr_block = "10.0.1.0/24"
  }

  ingress {
    from_port  = 0
    to_port    = 0
    protocol   = "tcp"
    rule_no    = 100
    action     = "allow"
    cidr_block = "10.0.1.0/24"
  }

  tags = {
    Name = var.private_nacl_name
  }
}

```

Create variables used
`variables.tf`

```bash
variable "vpc_id" {
  description = "VPC ID"
  type        = string
}

variable "local_ip" {
  description = "IP address to allow SSH access from"
  type        = string
}

variable "public_subnet_id" {
  description = "Public subnet ID"
  type        = string
}

variable "public_nacl_name" {
  description = "Name of the public NACL"
  type        = string
  default     = "KCPublicNACL"

}

variable "private_subnet_id" {
  description = "Private subnet ID"
  type        = string
}

variable "private_nacl_name" {
  description = "Name of the private NACL"
  type        = string
  default     = "KCPrivateNACL"
}

```

Output needed values
`outputs.tf`

```bash
output "public_nacl_id" {
  value = aws_network_acl.public.id
}

output "private_nacl_id" {
  value = aws_network_acl.private.id
}

```

### STEP 8 - DEPLOY INSTANCES

We will now launch two instances, one in the `PublicSubnet` and the other in the `PrivateSubnet`.
Create `instances` folder with the required files in the `modules` directory. Since we're going to write scripts to install a web server and a database, create another folder called `scripts` inside the `instances` directory with `install_nginx.sh` and `install_postgresql.sh` files created in it.

In the `main.tf` file, write

```bash
resource "aws_instance" "public_instance" {
  ami                         = var.ami
  instance_type               = var.instance_type
  subnet_id                   = var.public_subnet_id
  vpc_security_group_ids      = [var.public_sg_id]
  associate_public_ip_address = true
  key_name                    = var.key_name

  user_data = file("${path.module}/scripts/install_nginx.sh")

  tags = {
    Name = var.public_instance_name
  }
}

resource "aws_instance" "private_instance" {
  ami                    = var.ami
  instance_type          = var.instance_type
  subnet_id              = var.private_subnet_id
  vpc_security_group_ids = [var.private_sg_id]

  user_data = file("${path.module}/scripts/install_postgresql.sh")

  tags = {
    Name = var.private_instance_name
  }
}

```
Create the variables

`variables.tf`
```bash
variable "ami" {
  description = "AMI ID for the EC2 instances"
  type        = string
}

variable "instance_type" {
  description = "Instance type for the EC2 instances"
  type        = string
}

variable "public_subnet_id" {
  description = "Public subnet ID"
  type        = string
}

variable "private_subnet_id" {
  description = "Private subnet ID"
  type        = string
}

variable "public_sg_id" {
  description = "Public security group ID"
  type        = string
}

variable "private_sg_id" {
  description = "Private security group ID"
  type        = string
}

variable "public_instance_name" {
  description = "Public instance name"
  type = string
  default = "KCWebServer"
}

variable "private_instance_name" {
  description = "Private instance name"
  type = string
  default = "KCDBServer"
}

variable "key_name" {
  description = "Key pair name"
  type = string
}

```

Output the needed values

`outputs.tf`
```bash
output "public_instance_id" {
  value = aws_instance.public_instance.id
}

output "private_instance_id" {
  value = aws_instance.private_instance.id
}

output "public_instance_public_ip" {
  value = aws_instance.public_instance.public_ip
}

output "private_instance_private_ip" {
  value = aws_instance.private_instance.private_ip
}

```

We will now write scripts to install nginx and postgresql
Navigate to the `install_nginx.sh` file and write

`install_nginx.sh`
```bash
#!/bin/bash
sudo apt-get update
sudo apt-get install -y nginx
sudo systemctl start nginx
sudo systemctl enable nginx

```

Now install postgresql

`install_postgresql.sh`
```bash
#!/bin/bash
sudo apt-get update
sudo apt-get install -y postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql

```
That's it, we have created all the modules needed for our infrastructure. So now we have to reference or use them in our root `main.tf` file.

`main.tf`
```bash
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region  = "eu-west-1"
  profile = "dave"

}

module "vpc" {
  source   = "./modules/vpc"
  vpc_name = "KCVPC"
}

module "subnet" {
  source = "./modules/subnets"
  vpc_id = module.vpc.vpc_id
}

module "internet_gateway" {
  source = "./modules/internet_gateway"
  vpc_id = module.vpc.vpc_id
}

module "nat_gateway" {
  source                 = "./modules/nat_gateway"
  public_subnet_id       = module.subnet.public_subnet_id
  private_route_table_id = module.route_table.private_route_table_id
}

module "route_table" {
  source              = "./modules/route_table"
  vpc_id              = module.vpc.vpc_id
  public_subnet_id    = module.subnet.public_subnet_id
  private_subnet_id   = module.subnet.private_subnet_id
  internet_gateway_id = module.internet_gateway.internet_gateway_id
  nat_gateway_id      = module.nat_gateway.nat_gateway_id
}

module "security_groups" {
  source              = "./modules/security_groups"
  internet_cidr_block = module.route_table.internet_cidr_block
  vpc_id              = module.vpc.vpc_id
  local_ip            = var.local_ip
}

module "nacls" {
  source            = "./modules/nacls"
  vpc_id            = module.vpc.vpc_id
  public_subnet_id  = module.subnet.public_subnet_id
  private_subnet_id = module.subnet.private_subnet_id
  local_ip          = var.local_ip
}

module "instances" {
  source            = "./modules/instances"
  ami               = var.ami
  instance_type     = var.instance_type
  public_subnet_id  = module.subnet.public_subnet_id
  private_subnet_id = module.subnet.private_subnet_id
  public_sg_id      = module.security_groups.public_sg_id
  private_sg_id     = module.security_groups.private_sg_id
  key_name          = var.key_name
}

```
Like we did previously, add the specified variables

`variables.tf`
```bash
variable "ami" {
  description = "AMI ID for the EC2 instances"
  type        = string
  default     = "ami-0c38b837cd80f13bb" # Ubuntu AMI ID
}

variable "instance_type" {
  description = "Instance type for the EC2 instances"
  type        = string
  default     = "t2.micro"
}

variable "local_ip" {
  description = "IP address to allow SSH access from"
  type        = string
  default     = "local_ip/32" # Change local_ip to your ip
}

variable "key_name" {
  description = "Key pair name"
  type        = string
  default     = "webserver-pem-key-pair"
}

```
Output the needed values

`outputs.tf`
```bash
output "vpc_id" {
  value = module.vpc.vpc_id
}

output "public_subnet_id" {
  value = module.subnet.public_subnet_id
}

output "private_subnet_id" {
  value = module.subnet.private_subnet_id
}

output "public_route_table_id" {
  value = module.route_table.public_route_table_id
}

output "private_route_table_id" {
  value = module.route_table.private_route_table_id
}

output "public_instance_id" {
  value = module.instances.public_instance_id
}

output "private_instance_id" {
  value = module.instances.private_instance_id
}

output "public_instance_public_ip" {
  value = module.instances.public_instance_public_ip
}

output "private_instance_private_ip" {
  value = module.instances.private_instance_private_ip
}

```

## EXECUTE TERRAFORM COMMANDS
Now that we have finished writing codes, we are going to execute commands to tell Terraform to create our resources in our AWS account.

Firstly, we will initialize Terraform. In your `terraform` directory, from the terminal, run
```bash
terraform init
```
Then run
```bash
terraform plan -out tfplan.json
```
The above command will create a new file called `tfplan.json` and will output all the information about the resources to be created.

After that, run
```bash
terraform apply
```
This will create all the resources you stated with code.

## VERIFY RESOURCES
Now that we have created our resources, it is time to verify if we truly created them just by running `terraform apply`
login to your AWS account to check your resources.

### VPC

### SUBNETS

### INTERNET GATEWAYS

### ROUTE TABLES

### NAT GATEWAY

### SECURITY GROUPS

### NETWORK ACCESS CONTROL LISTS (NACLs)

### INSTANCES

## TFPLAN OUTPLAN
```bash

```