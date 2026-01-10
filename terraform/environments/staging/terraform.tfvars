# =============================================================================
# D'Agri Talk - Development Environment Values
# =============================================================================

project_name           = "dagri-talk"
region                 = "us-east-1"
vpc_cidr               = "10.0.0.0/16"
availability_zones     = ["us-east-1a", "us-east-1b"]
public_subnet_cidrs    = {
  "us-east-1a" = "10.0.1.0/24",
  "us-east-1b" = "10.0.2.0/24"
}
private_subnet_cidrs   = ["10.0.10.0/24", "10.0.20.0/24"]
db_instance_class      = "db.t3.micro"
db_allocated_storage   = 20
db_name                = "dagri_talk_dev"
db_username            = "dagri_admin"
app_port               = 5000
allowed_cidr_blocks    = ["0.0.0.0/0"]
enable_monitoring      = true
enable_nat_gateway     = false
common_tags = {
  ManagedBy   = "Terraform"
  Environment = "dev"
  Owner       = "Development Team"
  CostCenter  = "Engineering"
}