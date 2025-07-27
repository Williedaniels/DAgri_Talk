# =============================================================================
# D'Agri Talk - Development Environment Outputs
# =============================================================================

# -----------------------------------------------------------------------------
# Networking Outputs
# -----------------------------------------------------------------------------
output "vpc_id" {
  description = "The ID of the VPC."
  value       = module.networking.vpc_id
}

output "public_subnet_ids" {
  description = "List of IDs of public subnets."
  value       = module.networking.public_subnet_ids
}

output "private_subnet_ids" {
  description = "List of IDs of private subnets."
  value       = module.networking.private_subnet_ids
}

output "ecs_security_group_id" {
  description = "The ID of the ECS service's security group."
  value       = module.networking.ecs_security_group_id
}

output "alb_security_group_id" {
  description = "The ID of the ALB's security group."
  value       = module.networking.alb_security_group_id
}

# -----------------------------------------------------------------------------
# Other Application Outputs
# -----------------------------------------------------------------------------
output "database_credentials_secret_arn" {
  description = "The ARN of the Secrets Manager secret for DB credentials."
  value       = module.database.database_credentials_secret_arn
}

output "backend_ecr_repository_url" {
  description = "The URL of the backend ECR container registry."
  value       = module.container_registry.backend_repository_url
}

output "frontend_ecr_repository_url" {
  description = "The URL of the frontend ECR container registry."
  value       = module.container_registry.frontend_repository_url
}