variable "vpc_id" {
  description = "VPC ID"
  type        = string
}

variable "internet_cidr_block" {
  description = "public internet routing IPv4 cidr block"
  type        = string
}

variable "ssh_access_ip" {
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