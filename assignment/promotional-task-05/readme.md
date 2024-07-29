# SETTING UP A VPC WITH PRIVATE AND PUBLIC SUBNETS, SECURITY GROUPS AND NETWORK ACCESS CONTROL LISTS(NACLs) ON AWS

## STEP 1 - CREATE VPC
To create a VPC, open the AWS console and select the region of choice(eg. eu-west-1) at the top right. Click on Services, and select Networking & Content Delivery. From the menu that appears, choose VPC, you can still search in the search bar for easy access. On the next page, click the Create VPC button and enter the following details:
Select VPC only instead of VPC and more
Name tag: KCVPC
IPv4 CIDR block: 10.0.0.0/16
After entering these details, click Create VPC. Your VPC named KCVPC will be created in the eu-west-1 region.
![aws-vpc-created](https://github.com/user-attachments/assets/fed53a6b-c0a3-4523-acb9-e5f536f04c35)

## STEP 2 - CREATE SUBNETS
Now to create a subnet, select Subnets from the menu on the left. By default AWS has already created subnets in your account, that is not a problem, just click on Create subnet at the top right and create a public and private subnets with these details
Public Subnet
Name: PublicSubnet
IPv4 subnet CIDR block: 10.0.1.0/24
Availability Zone: eu-west-1b (You can choose any)

Private Subnet
Name: PrivateSubnet
IPv4 subnet CIDR block: 10.0.2.0/24
Availability Zone: eu-west-1b (Choose any but same as PublicSubnet for simplicity)
![aws-create-subnets](https://github.com/user-attachments/assets/9b337e1d-6a92-4410-9a8d-c2558f0f8900)

## STEP 3 - CONFIGURE AN INTERNET GATEWAY (IGW)
To create and configure an internet gateway, click on Internet Gateways from the left menu and then click the Create Internet Gateway button at the top right. Name it (I named it kc-igw) and click Create Internet Gateway.
![aws-create-igw](https://github.com/user-attachments/assets/0436100e-f77c-4e04-8649-89cdba98c7c2)

To attach the internet gateway to a VPC, click on Actions and select Attach to VPC. AWS simplifies this by including the action button in the success message. Click on it, select KCVPC, and finally, click Attach Internet Gateway.
![aws-igw-attached](https://github.com/user-attachments/assets/56256626-4d25-495a-878f-db26cabfbd48)

## STEP 4 - CONFIGURING ROUTE TABLES
Click on Route Tables from the left menu. Click the Create Route Table button at the top right to create both public and private route tables with the following details:

Public Route Table

Name: PublicRouteTable
VPC: KCVPC
Click the Create Route Table button after providing the above details for the PublicRouteTable.
![aws-public-route-table-created](https://github.com/user-attachments/assets/6716d33c-ae54-4ac4-98e1-d96cdf41a6a7)

To associate PublicRouteTable with PublicSubnet, click on Actions under the route table's name and select Edit Subnet Associations, or select Subnet Associations below the details section and click Edit Subnet Associations. Choose either method, select PublicSubnet from the list of available subnets, and click the Save Associations button.
![aws-public-rt-associated](https://github.com/user-attachments/assets/c4f5d899-71d8-4df6-922c-ba19e8a5c370)

To add a public route (internet traffic) to the internet gateway (kc-igw), use the following details:

Destination: 0.0.0.0/0
Target: Internet Gateway (kc-igw)
Click on Actions and select Edit Routes, or click the Edit Routes button beneath the Details section, then click Add Route and use the above information to add routing to the internet gateway. Click the Save Changes button to save.
![aws-public-route-added](https://github.com/user-attachments/assets/680d318d-62a4-484b-af6c-e36c4bd0daa5)

Private Route Table

Name: PrivateRouteTable
VPC: KCVPC
Navigate to Route Tables and click the Create Route Table button, input the above details, and click Create Route Table. Then, click on Actions and select Edit Subnet Associations, select or tick PrivateSubnet from the list of available subnets, and click the Save Associations button to save.
![aws-private-rt-associated](https://github.com/user-attachments/assets/bd3f0300-07a8-40bd-85b7-5f85c064f54b)

## STEP 5 - CONFIGURE NAT GATEWAY
To configure a NAT Gateway, click on NAT Gateways from the left menu. Click the Create NAT Gateway button, name it (e.g., kc-nat-gateway), and select PublicSubnet for the Subnet field. Then, click Allocate Elastic IP and click the Create NAT Gateway button to save.
![aws-nat-gateway-created](https://github.com/user-attachments/assets/8ccc264c-b976-4e43-9052-9f0328aa29ff)

To configure the PrivateRouteTable to route internet traffic to the NAT Gateway, navigate to the Route Tables page and click on PrivateRouteTable. Click Edit Routes and then Add Route. Provide the following information:

Destination: 0.0.0.0/0
Target: NAT Gateway (kc-nat-gateway)
Click Save Changes to save.
![aws-internet-traf-add-nat-gateway-private-rtb](https://github.com/user-attachments/assets/89da706b-2bc6-4a15-acdf-696963fe24e3)

## STEP 6 - SETTING UP SECURITY GROUPS
In the left menu under Security, click on Security Groups, then click Create Security Group.

For public instances, use the following information:

Security group name: KcWebServer
VPC: KCVPC
Description: Allow all HTTP, HTTPS, and specific or local SSH traffic to the web server
In the Inbound rules section, click Add Rule and add the following rules:

HTTP (Port 80)

Type: HTTP
Source type: Anywhere-IPv4
HTTPS (Port 443)

Type: HTTPS
Source type: Anywhere-IPv4
SSH (Port 22)

Type: SSH
Source type: Local (My IP)
Leave the default for Outbound rules to allow all outbound traffic, then click Create Security Group to save.
![aws-webserver-sg-created](https://github.com/user-attachments/assets/35d50bf3-d66e-4256-b607-0d44f721abb4)

For private instances, create a security group like the public instances but with the following information:

Security group name: KcDBServer
Description: Allow inbound traffic from PublicSubnet
VPC: KCVPC
In the Inbound rules section, add the following rule:

MYSQL/Aurora
Source type: Custom
Source: 10.0.1.0/24 (PublicSubnet)
Leave the default for Outbound rules, then click Create Security Group to save.
![aws-kcdbserver-sg-created](https://github.com/user-attachments/assets/16a79c08-f2fc-4998-9720-2288c4896978)

## STEP 7 - CREATING NETWORK ACLs
In the left menu under security, click on Network ACLs and then Create network ACL button. Provide the following details.
Name: public-subnet-nacl
VPC: KCVPC
After it has been created successfully,
![aws-public-sub-nacl-created](https://github.com/user-attachments/assets/e1aff38b-1fed-4f0b-9dbe-7d3ee07e7c37)
Select it and click on Edit inbound rules to configure the inbound traffic with the below details

Inbound rules
Rule One(HTTP)
Rule number: 100(According to your preference)
Type: HTTP(80)
Source: 0.0.0.0/0
Allow/Deny: Allow

Rule Two(HTTPS)
Rule number: 70(According to your preference)
Type: HTTPS(443)
Source: 0.0.0.0/0
Allow/Deny: Allow

Rule Three(SSH)
Rule number: 40(According to your preference)
Type: SSH(22)
Source: Local IP(Your IP)/32
Allow/Deny: Allow

Click Save changes to save.
After that, just below the Details section select Outbound rules and click on Edit outbound rules, configure using these details

Outbound rules
Rule One(All Traffic)
Rule number: 100 (According to your preference)
Type: All traffic
Destination: 0.0.0.0/0
Allow/Deny: Allow

Click Save changes to save after editing.
![aws-public-sub-nacl-outbound-created](https://github.com/user-attachments/assets/a3ea38b2-712e-47e8-a6e8-4e5d17fdc3c6)

Next click on Subnet associations and then Edit subnet associations. Select PublicSubnet from the available subnets and click Save changes to associate the public subnet to the public network acls.
![aws-public-nacl-associated-pub-subnet](https://github.com/user-attachments/assets/87413d1c-77d8-4ca3-9e63-69ce068f0ade)

Navigate to Network ACLs page and click on Create network ACL. Input these details and click Create network ACL to create a private network acl.
Name: private-subnet-nacl
VPC: KCVPC

Now select the private subnet network acl and click on Edit inbound rules. Click on Add new rule and provide the following information and click Save changes to save.

Inbound rules
Rule number: 100(base on preference)
Type: MYSQL/Aurora(3306)
Source: 10.0.1.0/24
Allow/Deny: Allow
![aws-private-sub-nacl-created](https://github.com/user-attachments/assets/ff6667ef-bb84-4143-9235-f1e6f79b6f0a)

After that, select Outbound rules and then Edit outbound rules. Add two new rules with these details.

Outbound rules
Rule One
Rule number: 100(base on preference)
Type: All traffic
Destination: 10.0.1.0/24
Allow/Deny: Allow

Rule Two
Rule number: 80(base on preference)
Type: All traffic
Destination: 0.0.0.0/0
Allow/Deny: Allow

Click Save changes to save.
![aws-private-sub-outb-ru-created](https://github.com/user-attachments/assets/d3f000d0-87df-445e-a25c-5ac7c0320e26)

After that select Subnet associations and then click on Edit subnet associations. Choose PrivateSubnet from the list of subnets available and click Save changes to save.
![aws-private-nacl-subnet associated](https://github.com/user-attachments/assets/c27f7d38-1b93-4d08-b0ba-7448681a7e2e)

## STEP 8 - DEPLOYING INSTANCES
To deploy an instance, navigate to the EC2 dashboard and click on Launch instance. Fill in the fields with the following information.
Name: KC Web Server
Application and OS Images (AMI): Amazon Linux
Amazon Machine Image (AMI): Amazon Linux 2023 AMI
Instance type: t2.micro
Key pair: Select existing or create new one. click on Create new key pair and choose a name and the type you want.
VPC: KCVPC
Subnet: PublicSubnet 
Auto-assign public IP: Enable
Firewall(security groups): KcWebServer (Public SG)

Leave the default settings and click on Launch instance to launch the web server instance.
![aws-web-server-instance-created](https://github.com/user-attachments/assets/c5409d61-5e90-4c17-b92a-2c7ae57a0b21)

Now, to verify if the instance can be accessed via the internet, click on Instances and check if the Status check is 2/2 checks passed. If it is not wait for it and after that, connect to it by clicking on the Connect button at the top and selecting SSH. Follow the example given to connect.
Open terminal and navigate to the directory where your key pair can be located and first change permission on the file
`chmod 400 key-pair.pem`
And then
`ssh -i "key-pair.pem" ec2-user@web-server-instance-IPv4-public-address`
when prompted to add fingerprint type yes and that's it you're connected if everything was done correctly.
![aws-connect-public-instance](https://github.com/user-attachments/assets/1a98cc7f-0f4f-49a0-8d50-032f28de0c65)

Now ping any sever address
Example: Google
`ping www.google.com`
![aws-connect-ping-public](https://github.com/user-attachments/assets/541bb4fa-5846-4c05-889d-9ef58892f5a0)

To launch an EC2 instance in the private subnet, we navigate to the EC2 dashboard and launch an instance with the following information.
Name: KC DB Server
Application and OS Images (AMI): Amazon Linux
Amazon Machine Image (AMI): Amazon Linux 2023 AMI
Instance type: t2.micro
Key pair: Select existing or create new one. click on Create new key pair and choose a name and the type you want.
VPC: KCVPC
Subnet: PrivateSubnet
Auto-assign public IP: Disable
Firewall(security groups): KcDBServer (Private SG)

Now launch and verify that the instance can access the internet through the NAT Gateway and can communicate with the public instance
![aws-private-instance-created](https://github.com/user-attachments/assets/15c4542f-c74c-4d13-912c-5578eb8fbc35)

