variable "project_name" {
  description = "The name of the project."
  type        = string
}

variable "region" {
  description = "The AWS region to deploy resources in."
  type        = string
}

variable "vpc_cidr" {
  description = "The CIDR block for the VPC."
  type        = string
}

variable "availability_zones" {
  description = "A list of availability zones for the VPC."
  type        = list(string)
}

variable "public_subnet_cidrs" {
  description = "A map of public subnet CIDR blocks, keyed by availability zone."
  type        = map(string)
}

variable "private_subnet_cidrs" {
  description = "A list of private subnet CIDR blocks."
  type        = list(string)
}

variable "db_instance_class" {
  description = "The instance class for the RDS database."
  type        = string
}

variable "db_allocated_storage" {
  description = "The allocated storage for the RDS database in GB."
  type        = number
}

variable "db_name" {
  description = "The name of the database to create."
  type        = string
}

variable "db_username" {
  description = "The username for the database administrator."
  type        = string
}

variable "app_port" {
  description = "The port the application listens on."
  type        = number
}

variable "allowed_cidr_blocks" {
  description = "List of CIDR blocks allowed to access the ALB."
  type        = list(string)
}

variable "enable_monitoring" {
  description = "Enable enhanced monitoring for RDS."
  type        = bool
  default     = true
}

variable "enable_nat_gateway" {
  description = "Set to false to disable NAT Gateways for cost savings in development."
  type        = bool
  default     = true
}

variable "common_tags" {
  description = "A map of common tags to apply to all resources."
  type        = map(string)
  default     = {}
}