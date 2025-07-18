# =============================================================================
# D'Agri Talk - Database Module Variables
# =============================================================================

variable "project_name" {
  description = "Name of the project"
  type        = string
}

variable "environment" {
  description = "Environment name"
  type        = string
}

variable "db_instance_class" {
  description = "RDS instance class"
  type        = string
}

variable "db_allocated_storage" {
  description = "Allocated storage for RDS instance (GB)"
  type        = number
}

variable "db_name" {
  description = "Name of the database"
  type        = string
}

variable "db_username" {
  description = "Master username for the database"
  type        = string
  sensitive   = true
}

variable "private_subnet_ids" {
  description = "IDs of private subnets for database"
  type        = list(string)
}

variable "database_security_group_id" {
  description = "ID of the database security group"
  type        = string
}

variable "enable_monitoring" {
  description = "Enable enhanced monitoring"
  type        = bool
}

variable "common_tags" {
  description = "Common tags to apply to all resources"
  type        = map(string)
}