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
