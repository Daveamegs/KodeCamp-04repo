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
