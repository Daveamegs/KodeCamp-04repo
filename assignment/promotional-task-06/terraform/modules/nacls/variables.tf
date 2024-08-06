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
