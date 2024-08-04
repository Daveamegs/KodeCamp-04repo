output "vpc_id" {
  value = module.vpc.vpc_id
}

output "public_subnet_id" {
  value = module.subnet.public_subnet_id
}

output "private_subnet_id" {
  value = module.subnet.private_subnet_id
}

output "public_route_table_id" {
  value = module.route_tables.public_route_table_id
}

output "private_route_table_id" {
  value = module.route_tables.private_route_table_id
}

output "public_instance_id" {
  value = module.instances.public_instance_id
}

output "private_instance_id" {
  value = module.instances.private_instance_id
}

output "public_instance_public_ip" {
  value = module.instances.public_instance_public_ip
}

output "private_instance_private_ip" {
  value = module.instances.private_instance_private_ip
}
