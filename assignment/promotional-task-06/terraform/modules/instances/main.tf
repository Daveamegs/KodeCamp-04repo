resource "aws_instance" "public_instance" {
  ami                    = var.ami
  instance_type          = var.instance_type
  subnet_id              = var.public_subnet_id
  vpc_security_group_ids = [var.public_sg_id]

  user_data = file("${path.module}/scripts/install_nginx.sh")

  tags = {
    Name = var.public_instance_name
  }
}

resource "aws_instance" "private_instance" {
  ami                    = var.ami
  instance_type          = var.instance_type
  subnet_id              = var.private_subnet_id
  vpc_security_group_ids = [var.private_sg_id]

  user_data = file("${path.module}/scripts/install_postgresql.sh")

  tags = {
    Name = var.private_instance_name
  }
}
