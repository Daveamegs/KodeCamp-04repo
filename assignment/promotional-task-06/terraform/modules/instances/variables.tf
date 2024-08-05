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
