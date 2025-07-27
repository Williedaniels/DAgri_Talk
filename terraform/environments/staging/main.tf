# =============================================================================
# D'Agri Talk - Development Environment
# =============================================================================

terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.1"
    }
  }

  # Backend configuration for state management
  # Uncomment and configure for production use
  # backend "s3" {
  #   bucket = "dagri-talk-terraform-state"
  #   key    = "dev/terraform.tfstate"
  #   region = "us-east-1"
  #   encrypt = true
  #   dynamodb_table = "dagri-talk-terraform-locks"
  # }
}

# -----------------------------------------------------------------------------
# Provider Configuration
# -----------------------------------------------------------------------------
provider "aws" {
  region = var.region

  default_tags {
    tags = var.common_tags
  }
}

# -----------------------------------------------------------------------------
# Local Values
# -----------------------------------------------------------------------------
locals {
  environment = "dev"
  
  # Override common tags for this environment
  common_tags = merge(var.common_tags, {
    Environment = local.environment
  })
}

# -----------------------------------------------------------------------------
# Networking Module
# -----------------------------------------------------------------------------
module "networking" {
  source = "../../modules/networking"

  project_name           = var.project_name
  environment           = local.environment
  vpc_cidr              = var.vpc_cidr
  availability_zones    = var.availability_zones
  public_subnet_cidrs   = var.public_subnet_cidrs
  private_subnet_cidrs  = var.private_subnet_cidrs
  allowed_cidr_blocks   = var.allowed_cidr_blocks
  app_port              = var.app_port
  enable_nat_gateway    = var.enable_nat_gateway
  common_tags           = local.common_tags
}

# -----------------------------------------------------------------------------
# Database Module
# -----------------------------------------------------------------------------
module "database" {
  source = "../../modules/database"

  project_name               = var.project_name
  environment               = local.environment
  db_instance_class         = var.db_instance_class
  db_allocated_storage      = var.db_allocated_storage
  db_name                   = var.db_name
  db_username               = var.db_username
  private_subnet_ids        = module.networking.private_subnet_ids
  database_security_group_id = module.networking.database_security_group_id
  enable_monitoring         = var.enable_monitoring
  common_tags               = local.common_tags

  depends_on = [module.networking]
}

# -----------------------------------------------------------------------------
# Container Registry Module
# -----------------------------------------------------------------------------
module "container_registry" {
  source = "../../modules/container-registry"

  project_name = var.project_name
  environment  = local.environment
  common_tags  = local.common_tags
}