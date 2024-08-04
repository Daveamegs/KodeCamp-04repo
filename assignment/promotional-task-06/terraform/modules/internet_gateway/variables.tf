variable "vpc_id" {
  description = "VPC ID"
  type        = string
}

variable "igw_name" {
  description = "Name for the Internet Gateway"
  type = string
  default = "KC-IGW"
}