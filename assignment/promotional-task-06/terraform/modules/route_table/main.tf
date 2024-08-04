resource "aws_route_table" "public" {
  vpc_id = var.vpc_id

  route {
    cidr_block = var.internet_cidr_block
    gateway_id = var.internet_gateway_id
  }

  tags = {
    Name = var.public_route_table_name
  }
}

resource "aws_route_table_association" "public" {
  subnet_id      = var.public_subnet_id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table" "private" {
  vpc_id = var.vpc_id

  route {
    cidr_block     = var.internet_cidr_block
    nat_gateway_id = var.nat_gateway_id
  }

  tags = {
    Name = var.private_route_table_name
  }
}

resource "aws_route_table_association" "private" {
  subnet_id      = var.private_subnet_id
  route_table_id = aws_route_table.private.id
}

