variable "project_name" {
  description = "The name of the project."
  type        = string
}

variable "environment" {
  description = "The environment name (e.g., dev, prod)."
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

variable "allowed_cidr_blocks" {
  description = "List of CIDR blocks allowed to access the ALB."
  type        = list(string)
}

variable "app_port" {
  description = "The port the application listens on."
  type        = number
}

variable "enable_nat_gateway" {
  description = "Enable NAT Gateway for private subnets"
  type        = bool
  default     = true
}

variable "common_tags" {
  description = "A map of common tags to apply to all resources."
  type        = map(string)
  default     = {}
}