variable "vpc_id" {
  description = "VPC ID"
  type        = string
}

variable "internet_cidr_block" {
  description = "Internet routing IPv4 cidr block"
  type        = string
  default     = "0.0.0.0/0"
}

variable "igw_id" {
  description = "Internet Gateway ID"
  type        = string
}

variable "natgw_id" {
  description = "NAT Gateway ID"
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
