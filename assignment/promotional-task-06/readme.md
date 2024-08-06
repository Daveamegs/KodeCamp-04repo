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
This will create all the resources you stated with code. See the output below.
```bash
david@ommema:~/Documents/DevOps/kodecamp/kodecamp4/github-clone/KodeCamp-04repo/assignment/promotional-task-06/terraform$ terraform apply "tfplan.json"
module.nat_gateway.aws_eip.nat: Creating...
module.vpc.aws_vpc.vpc: Creating...
module.nat_gateway.aws_eip.nat: Creation complete after 2s [id=eipalloc-08655cdc24deb6db3]
module.vpc.aws_vpc.vpc: Creation complete after 3s [id=vpc-0f7a67bf89ac8e585]
module.internet_gateway.aws_internet_gateway.main: Creating...
module.subnet.aws_subnet.public: Creating...
module.subnet.aws_subnet.private: Creating...
module.security_groups.aws_security_group.public: Creating...
module.subnet.aws_subnet.public: Creation complete after 1s [id=subnet-0c967b1478c8df800]
module.nat_gateway.aws_nat_gateway.main: Creating...
module.nacls.aws_network_acl.public: Creating...
module.subnet.aws_subnet.private: Creation complete after 1s [id=subnet-04a19fea1bea0ad03]
module.internet_gateway.aws_internet_gateway.main: Creation complete after 1s [id=igw-0f3bc332f1fbf4d0a]
module.route_table.aws_route_table.public: Creating...
module.nacls.aws_network_acl.private: Creating...
module.nacls.aws_network_acl.private: Creation complete after 2s [id=acl-09402e01f1f17c5f6]
module.route_table.aws_route_table.public: Creation complete after 2s [id=rtb-09430c59706d2b38e]
module.route_table.aws_route_table_association.public: Creating...
module.nacls.aws_network_acl.public: Creation complete after 2s [id=acl-0154faca27bcf4bb9]
module.route_table.aws_route_table_association.public: Creation complete after 1s [id=rtbassoc-0db080fe74d3af6f0]
module.security_groups.aws_security_group.public: Creation complete after 4s [id=sg-09d69fbc2e92dffda]
module.security_groups.aws_security_group.private: Creating...
module.instances.aws_instance.public_instance: Creating...
module.security_groups.aws_security_group.private: Creation complete after 4s [id=sg-02bcdb45367b3d171]
module.instances.aws_instance.private_instance: Creating...
module.nat_gateway.aws_nat_gateway.main: Still creating... [10s elapsed]
module.instances.aws_instance.public_instance: Still creating... [10s elapsed]
module.instances.aws_instance.private_instance: Still creating... [10s elapsed]
module.nat_gateway.aws_nat_gateway.main: Still creating... [20s elapsed]
module.instances.aws_instance.public_instance: Still creating... [20s elapsed]
module.instances.aws_instance.public_instance: Creation complete after 24s [id=i-0b76496c749e86e35]
module.instances.aws_instance.private_instance: Still creating... [20s elapsed]
module.nat_gateway.aws_nat_gateway.main: Still creating... [30s elapsed]
module.instances.aws_instance.private_instance: Still creating... [30s elapsed]
module.nat_gateway.aws_nat_gateway.main: Still creating... [40s elapsed]
module.instances.aws_instance.private_instance: Creation complete after 34s [id=i-026e35d4de804ecae]
module.nat_gateway.aws_nat_gateway.main: Still creating... [50s elapsed]
module.nat_gateway.aws_nat_gateway.main: Still creating... [1m0s elapsed]
module.nat_gateway.aws_nat_gateway.main: Still creating... [1m10s elapsed]
module.nat_gateway.aws_nat_gateway.main: Still creating... [1m20s elapsed]
module.nat_gateway.aws_nat_gateway.main: Still creating... [1m30s elapsed]
module.nat_gateway.aws_nat_gateway.main: Creation complete after 1m36s [id=nat-0d279a6643a6dab62]
module.route_table.aws_route_table.private: Creating...
module.route_table.aws_route_table.private: Creation complete after 1s [id=rtb-0c3d3b88e993f8243]
module.route_table.aws_route_table_association.private: Creating...
module.route_table.aws_route_table_association.private: Creation complete after 0s [id=rtbassoc-0575de4c8b3622299]

Apply complete! Resources: 16 added, 0 changed, 0 destroyed.

Outputs:

private_instance_id = "i-026e35d4de804ecae"
private_instance_private_ip = "10.0.2.31"
private_route_table_id = "rtb-0c3d3b88e993f8243"
private_subnet_id = "subnet-04a19fea1bea0ad03"
public_instance_id = "i-0b76496c749e86e35"
public_instance_public_ip = "3.253.38.15"
public_route_table_id = "rtb-09430c59706d2b38e"
public_subnet_id = "subnet-0c967b1478c8df800"
vpc_id = "vpc-0f7a67bf89ac8e585"
```

## VERIFY RESOURCES
Now that we have created our resources, it is time to verify if we truly created them just by running `terraform apply`
login to your AWS account to check your resources.

### VPC


### SUBNETS

### INTERNET GATEWAY

### ROUTE TABLES

### NAT GATEWAY

### SECURITY GROUPS

### NETWORK ACCESS CONTROL LISTS (NACLs)

### INSTANCES

## TFPLAN OUTPLAN
```bash
Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # module.instances.aws_instance.private_instance will be created
  + resource "aws_instance" "private_instance" {
      + ami                                  = "ami-0c38b837cd80f13bb"
      + arn                                  = (known after apply)
      + associate_public_ip_address          = (known after apply)
      + availability_zone                    = (known after apply)
      + cpu_core_count                       = (known after apply)
      + cpu_threads_per_core                 = (known after apply)
      + disable_api_stop                     = (known after apply)
      + disable_api_termination              = (known after apply)
      + ebs_optimized                        = (known after apply)
      + get_password_data                    = false
      + host_id                              = (known after apply)
      + host_resource_group_arn              = (known after apply)
      + iam_instance_profile                 = (known after apply)
      + id                                   = (known after apply)
      + instance_initiated_shutdown_behavior = (known after apply)
      + instance_lifecycle                   = (known after apply)
      + instance_state                       = (known after apply)
      + instance_type                        = "t2.micro"
      + ipv6_address_count                   = (known after apply)
      + ipv6_addresses                       = (known after apply)
      + key_name                             = (known after apply)
      + monitoring                           = (known after apply)
      + outpost_arn                          = (known after apply)
      + password_data                        = (known after apply)
      + placement_group                      = (known after apply)
      + placement_partition_number           = (known after apply)
      + primary_network_interface_id         = (known after apply)
      + private_dns                          = (known after apply)
      + private_ip                           = (known after apply)
      + public_dns                           = (known after apply)
      + public_ip                            = (known after apply)
      + secondary_private_ips                = (known after apply)
      + security_groups                      = (known after apply)
      + source_dest_check                    = true
      + spot_instance_request_id             = (known after apply)
      + subnet_id                            = (known after apply)
      + tags                                 = {
          + "Name" = "KCDBServer"
        }
      + tags_all                             = {
          + "Name" = "KCDBServer"
        }
      + tenancy                              = (known after apply)
      + user_data                            = "ae035e4c870b77a834e3cb717f7813851df0ff50"
      + user_data_base64                     = (known after apply)
      + user_data_replace_on_change          = false
      + vpc_security_group_ids               = (known after apply)
    }

  # module.instances.aws_instance.public_instance will be created
  + resource "aws_instance" "public_instance" {
      + ami                                  = "ami-0c38b837cd80f13bb"
      + arn                                  = (known after apply)
      + associate_public_ip_address          = true
      + availability_zone                    = (known after apply)
      + cpu_core_count                       = (known after apply)
      + cpu_threads_per_core                 = (known after apply)
      + disable_api_stop                     = (known after apply)
      + disable_api_termination              = (known after apply)
      + ebs_optimized                        = (known after apply)
      + get_password_data                    = false
      + host_id                              = (known after apply)
      + host_resource_group_arn              = (known after apply)
      + iam_instance_profile                 = (known after apply)
      + id                                   = (known after apply)
      + instance_initiated_shutdown_behavior = (known after apply)
      + instance_lifecycle                   = (known after apply)
      + instance_state                       = (known after apply)
      + instance_type                        = "t2.micro"
      + ipv6_address_count                   = (known after apply)
      + ipv6_addresses                       = (known after apply)
      + key_name                             = "webserver-pem-key-pair"
      + monitoring                           = (known after apply)
      + outpost_arn                          = (known after apply)
      + password_data                        = (known after apply)
      + placement_group                      = (known after apply)
      + placement_partition_number           = (known after apply)
      + primary_network_interface_id         = (known after apply)
      + private_dns                          = (known after apply)
      + private_ip                           = (known after apply)
      + public_dns                           = (known after apply)
      + public_ip                            = (known after apply)
      + secondary_private_ips                = (known after apply)
      + security_groups                      = (known after apply)
      + source_dest_check                    = true
      + spot_instance_request_id             = (known after apply)
      + subnet_id                            = (known after apply)
      + tags                                 = {
          + "Name" = "KCWebServer"
        }
      + tags_all                             = {
          + "Name" = "KCWebServer"
        }
      + tenancy                              = (known after apply)
      + user_data                            = "661568f30463228651734a7acf6e051a7ce056d7"
      + user_data_base64                     = (known after apply)
      + user_data_replace_on_change          = false
      + vpc_security_group_ids               = (known after apply)
    }

  # module.internet_gateway.aws_internet_gateway.main will be created
  + resource "aws_internet_gateway" "main" {
      + arn      = (known after apply)
      + id       = (known after apply)
      + owner_id = (known after apply)
      + tags     = {
          + "Name" = "KC-IGW"
        }
      + tags_all = {
          + "Name" = "KC-IGW"
        }
      + vpc_id   = (known after apply)
    }

  # module.nacls.aws_network_acl.private will be created
  + resource "aws_network_acl" "private" {
      + arn        = (known after apply)
      + egress     = [
          + {
              + action          = "allow"
              + cidr_block      = "0.0.0.0/0"
              + from_port       = 80
              + protocol        = "tcp"
              + rule_no         = 100
              + to_port         = 80
                # (1 unchanged attribute hidden)
            },
          + {
              + action          = "allow"
              + cidr_block      = "10.0.1.0/24"
              + from_port       = 0
              + protocol        = "-1"
              + rule_no         = 110
              + to_port         = 0
                # (1 unchanged attribute hidden)
            },
        ]
      + id         = (known after apply)
      + ingress    = [
          + {
              + action          = "allow"
              + cidr_block      = "10.0.1.0/24"
              + from_port       = 0
              + protocol        = "tcp"
              + rule_no         = 100
              + to_port         = 0
                # (1 unchanged attribute hidden)
            },
        ]
      + owner_id   = (known after apply)
      + subnet_ids = (known after apply)
      + tags       = {
          + "Name" = "KCPrivateNACL"
        }
      + tags_all   = {
          + "Name" = "KCPrivateNACL"
        }
      + vpc_id     = (known after apply)
    }

  # module.nacls.aws_network_acl.public will be created
  + resource "aws_network_acl" "public" {
      + arn        = (known after apply)
      + egress     = [
          + {
              + action          = "allow"
              + cidr_block      = "0.0.0.0/0"
              + from_port       = 0
              + protocol        = "-1"
              + rule_no         = 100
              + to_port         = 0
                # (1 unchanged attribute hidden)
            },
        ]
      + id         = (known after apply)
      + ingress    = [
          + {
              + action          = "allow"
              + cidr_block      = "0.0.0.0/0"
              + from_port       = 443
              + protocol        = "tcp"
              + rule_no         = 110
              + to_port         = 443
                # (1 unchanged attribute hidden)
            },
          + {
              + action          = "allow"
              + cidr_block      = "0.0.0.0/0"
              + from_port       = 80
              + protocol        = "tcp"
              + rule_no         = 100
              + to_port         = 80
                # (1 unchanged attribute hidden)
            },
          + {
              + action          = "allow"
              + cidr_block      = "154.161.131.148/32"
              + from_port       = 22
              + protocol        = "tcp"
              + rule_no         = 120
              + to_port         = 22
                # (1 unchanged attribute hidden)
            },
        ]
      + owner_id   = (known after apply)
      + subnet_ids = (known after apply)
      + tags       = {
          + "Name" = "KCPublicNACL"
        }
      + tags_all   = {
          + "Name" = "KCPublicNACL"
        }
      + vpc_id     = (known after apply)
    }

  # module.nat_gateway.aws_eip.nat will be created
  + resource "aws_eip" "nat" {
      + allocation_id        = (known after apply)
      + arn                  = (known after apply)
      + association_id       = (known after apply)
      + carrier_ip           = (known after apply)
      + customer_owned_ip    = (known after apply)
      + domain               = "vpc"
      + id                   = (known after apply)
      + instance             = (known after apply)
      + network_border_group = (known after apply)
      + network_interface    = (known after apply)
      + private_dns          = (known after apply)
      + private_ip           = (known after apply)
      + ptr_record           = (known after apply)
      + public_dns           = (known after apply)
      + public_ip            = (known after apply)
      + public_ipv4_pool     = (known after apply)
      + tags_all             = (known after apply)
      + vpc                  = (known after apply)
    }

  # module.nat_gateway.aws_nat_gateway.main will be created
  + resource "aws_nat_gateway" "main" {
      + allocation_id                      = (known after apply)
      + association_id                     = (known after apply)
      + connectivity_type                  = "public"
      + id                                 = (known after apply)
      + network_interface_id               = (known after apply)
      + private_ip                         = (known after apply)
      + public_ip                          = (known after apply)
      + secondary_private_ip_address_count = (known after apply)
      + secondary_private_ip_addresses     = (known after apply)
      + subnet_id                          = (known after apply)
      + tags                               = {
          + "Name" = "KC-NAT-Gateway"
        }
      + tags_all                           = {
          + "Name" = "KC-NAT-Gateway"
        }
    }

  # module.route_table.aws_route_table.private will be created
  + resource "aws_route_table" "private" {
      + arn              = (known after apply)
      + id               = (known after apply)
      + owner_id         = (known after apply)
      + propagating_vgws = (known after apply)
      + route            = [
          + {
              + cidr_block                 = "0.0.0.0/0"
              + nat_gateway_id             = (known after apply)
                # (11 unchanged attributes hidden)
            },
        ]
      + tags             = {
          + "Name" = "PrivateRouteTable"
        }
      + tags_all         = {
          + "Name" = "PrivateRouteTable"
        }
      + vpc_id           = (known after apply)
    }

  # module.route_table.aws_route_table.public will be created
  + resource "aws_route_table" "public" {
      + arn              = (known after apply)
      + id               = (known after apply)
      + owner_id         = (known after apply)
      + propagating_vgws = (known after apply)
      + route            = [
          + {
              + cidr_block                 = "0.0.0.0/0"
              + gateway_id                 = (known after apply)
                # (11 unchanged attributes hidden)
            },
        ]
      + tags             = {
          + "Name" = "PublicRouteTable"
        }
      + tags_all         = {
          + "Name" = "PublicRouteTable"
        }
      + vpc_id           = (known after apply)
    }

  # module.route_table.aws_route_table_association.private will be created
  + resource "aws_route_table_association" "private" {
      + id             = (known after apply)
      + route_table_id = (known after apply)
      + subnet_id      = (known after apply)
    }

  # module.route_table.aws_route_table_association.public will be created
  + resource "aws_route_table_association" "public" {
      + id             = (known after apply)
      + route_table_id = (known after apply)
      + subnet_id      = (known after apply)
    }

  # module.security_groups.aws_security_group.private will be created
  + resource "aws_security_group" "private" {
      + arn                    = (known after apply)
      + description            = "Security group for private instances"
      + egress                 = [
          + {
              + cidr_blocks      = [
                  + "0.0.0.0/0",
                ]
              + from_port        = 0
              + ipv6_cidr_blocks = []
              + prefix_list_ids  = []
              + protocol         = "-1"
              + security_groups  = []
              + self             = false
              + to_port          = 0
                # (1 unchanged attribute hidden)
            },
        ]
      + id                     = (known after apply)
      + ingress                = [
          + {
              + cidr_blocks      = []
              + from_port        = 5432
              + ipv6_cidr_blocks = []
              + prefix_list_ids  = []
              + protocol         = "tcp"
              + security_groups  = (known after apply)
              + self             = false
              + to_port          = 5432
                # (1 unchanged attribute hidden)
            },
        ]
      + name                   = "PrivateSG"
      + name_prefix            = (known after apply)
      + owner_id               = (known after apply)
      + revoke_rules_on_delete = false
      + tags                   = {
          + "Name" = "PrivateSecurityGroup"
        }
      + tags_all               = {
          + "Name" = "PrivateSecurityGroup"
        }
      + vpc_id                 = (known after apply)
    }

  # module.security_groups.aws_security_group.public will be created
  + resource "aws_security_group" "public" {
      + arn                    = (known after apply)
      + description            = "Security group for public instances"
      + egress                 = [
          + {
              + cidr_blocks      = [
                  + "0.0.0.0/0",
                ]
              + from_port        = 0
              + ipv6_cidr_blocks = []
              + prefix_list_ids  = []
              + protocol         = "-1"
              + security_groups  = []
              + self             = false
              + to_port          = 0
                # (1 unchanged attribute hidden)
            },
        ]
      + id                     = (known after apply)
      + ingress                = [
          + {
              + cidr_blocks      = [
                  + "0.0.0.0/0",
                ]
              + from_port        = 443
              + ipv6_cidr_blocks = []
              + prefix_list_ids  = []
              + protocol         = "tcp"
              + security_groups  = []
              + self             = false
              + to_port          = 443
                # (1 unchanged attribute hidden)
            },
          + {
              + cidr_blocks      = [
                  + "0.0.0.0/0",
                ]
              + from_port        = 80
              + ipv6_cidr_blocks = []
              + prefix_list_ids  = []
              + protocol         = "tcp"
              + security_groups  = []
              + self             = false
              + to_port          = 80
                # (1 unchanged attribute hidden)
            },
          + {
              + cidr_blocks      = [
                  + "154.161.131.148/32",
                ]
              + from_port        = 22
              + ipv6_cidr_blocks = []
              + prefix_list_ids  = []
              + protocol         = "tcp"
              + security_groups  = []
              + self             = false
              + to_port          = 22
                # (1 unchanged attribute hidden)
            },
        ]
      + name                   = "PublicSG"
      + name_prefix            = (known after apply)
      + owner_id               = (known after apply)
      + revoke_rules_on_delete = false
      + tags                   = {
          + "Name" = "PublicSecurityGroup"
        }
      + tags_all               = {
          + "Name" = "PublicSecurityGroup"
        }
      + vpc_id                 = (known after apply)
    }

  # module.subnet.aws_subnet.private will be created
  + resource "aws_subnet" "private" {
      + arn                                            = (known after apply)
      + assign_ipv6_address_on_creation                = false
      + availability_zone                              = "eu-west-1c"
      + availability_zone_id                           = (known after apply)
      + cidr_block                                     = "10.0.2.0/24"
      + enable_dns64                                   = false
      + enable_resource_name_dns_a_record_on_launch    = false
      + enable_resource_name_dns_aaaa_record_on_launch = false
      + id                                             = (known after apply)
      + ipv6_cidr_block_association_id                 = (known after apply)
      + ipv6_native                                    = false
      + map_public_ip_on_launch                        = false
      + owner_id                                       = (known after apply)
      + private_dns_hostname_type_on_launch            = (known after apply)
      + tags                                           = {
          + "Name" = "PrivateSubnet"
        }
      + tags_all                                       = {
          + "Name" = "PrivateSubnet"
        }
      + vpc_id                                         = (known after apply)
    }

  # module.subnet.aws_subnet.public will be created
  + resource "aws_subnet" "public" {
      + arn                                            = (known after apply)
      + assign_ipv6_address_on_creation                = false
      + availability_zone                              = "eu-west-1c"
      + availability_zone_id                           = (known after apply)
      + cidr_block                                     = "10.0.1.0/24"
      + enable_dns64                                   = false
      + enable_resource_name_dns_a_record_on_launch    = false
      + enable_resource_name_dns_aaaa_record_on_launch = false
      + id                                             = (known after apply)
      + ipv6_cidr_block_association_id                 = (known after apply)
      + ipv6_native                                    = false
      + map_public_ip_on_launch                        = false
      + owner_id                                       = (known after apply)
      + private_dns_hostname_type_on_launch            = (known after apply)
      + tags                                           = {
          + "Name" = "PublicSubnet"
        }
      + tags_all                                       = {
          + "Name" = "PublicSubnet"
        }
      + vpc_id                                         = (known after apply)
    }

  # module.vpc.aws_vpc.vpc will be created
  + resource "aws_vpc" "vpc" {
      + arn                                  = (known after apply)
      + cidr_block                           = "10.0.0.0/16"
      + default_network_acl_id               = (known after apply)
      + default_route_table_id               = (known after apply)
      + default_security_group_id            = (known after apply)
      + dhcp_options_id                      = (known after apply)
      + enable_dns_hostnames                 = (known after apply)
      + enable_dns_support                   = true
      + enable_network_address_usage_metrics = (known after apply)
      + id                                   = (known after apply)
      + instance_tenancy                     = "default"
      + ipv6_association_id                  = (known after apply)
      + ipv6_cidr_block                      = (known after apply)
      + ipv6_cidr_block_network_border_group = (known after apply)
      + main_route_table_id                  = (known after apply)
      + owner_id                             = (known after apply)
      + tags                                 = {
          + "Name" = "KCVPC"
        }
      + tags_all                             = {
          + "Name" = "KCVPC"
        }
    }

Plan: 16 to add, 0 to change, 0 to destroy.

Changes to Outputs:
  + private_instance_id         = (known after apply)
  + private_instance_private_ip = (known after apply)
  + private_route_table_id      = (known after apply)
  + private_subnet_id           = (known after apply)
  + public_instance_id          = (known after apply)
  + public_instance_public_ip   = (known after apply)
  + public_route_table_id       = (known after apply)
  + public_subnet_id            = (known after apply)
  + vpc_id                      = (known after apply)
```