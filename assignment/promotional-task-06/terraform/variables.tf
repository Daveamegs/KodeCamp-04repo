variable "ami" {
  description = "AMI ID for the EC2 instances"
  type        = string
  default     = "ami-0c38b837cd80f13bb" # Ubuntu
}

variable "instance_type" {
  description = "Instance type for the EC2 instances"
  type        = string
  default     = "t2.micro"
}

variable "ssh_access_ip" {
  description = "IP address to allow SSH access from"
  type        = string
  default     = "154.160.0.0/24"
}

