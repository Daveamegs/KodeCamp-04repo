variable "public_subnet_id" {
  description = "Public subnet ID"
  type        = string
}

variable "vpc_id" {
  description = "VPC ID"
  type        = string
}

variable "nat_gateway_name" {
  description = "Name of NAT Gateway"
  type = string
  default = "KC-NAT-Gateway"
}
