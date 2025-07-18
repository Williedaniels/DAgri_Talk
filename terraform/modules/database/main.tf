# =============================================================================
# D'Agri Talk - Database Module (RDS PostgreSQL)
# =============================================================================

# -----------------------------------------------------------------------------
# Random Password Generation for Database
# -----------------------------------------------------------------------------
resource "random_password" "db_password" {
  length  = 16
  special = true
  
  # Ensure password meets RDS requirements
  min_lower   = 1
  min_upper   = 1
  min_numeric = 1
  min_special = 1
}

# -----------------------------------------------------------------------------
# Database Subnet Group
# -----------------------------------------------------------------------------
resource "aws_db_subnet_group" "main" {
  name       = "${var.project_name}-${var.environment}-db-subnet-group"
  subnet_ids = var.private_subnet_ids
  description = "Database subnet group for ${var.project_name} ${var.environment}"

  tags = merge(var.common_tags, {
    Name = "${var.project_name}-${var.environment}-db-subnet-group"
    Type = "database"
  })
}

# -----------------------------------------------------------------------------
# Database Parameter Group
# -----------------------------------------------------------------------------
resource "aws_db_parameter_group" "main" {
  family = "postgres15"
  name   = "${var.project_name}-${var.environment}-db-params"
  description = "Database parameter group for ${var.project_name} ${var.environment}"

  # Optimize for small workloads
  parameter {
    name  = "shared_preload_libraries"
    value = "pg_stat_statements"
  }

  parameter {
    name  = "log_statement"
    value = "all"
  }

  parameter {
    name  = "log_min_duration_statement"
    value = "1000"  # Log queries taking longer than 1 second
  }

  tags = merge(var.common_tags, {
    Name = "${var.project_name}-${var.environment}-db-params"
    Type = "database"
  })

  lifecycle {
    create_before_destroy = true
  }
}

# -----------------------------------------------------------------------------
# RDS PostgreSQL Instance
# -----------------------------------------------------------------------------
resource "aws_db_instance" "main" {
  # Basic Configuration
  identifier = "${var.project_name}-${var.environment}-db"
  engine     = "postgres"
  engine_version = "15.8"
  
  # Instance Configuration
  instance_class    = var.db_instance_class
  allocated_storage = var.db_allocated_storage
  storage_type      = "gp2"
  storage_encrypted = true
  
  # Database Configuration
  db_name  = var.db_name
  username = var.db_username
  password = random_password.db_password.result
  port     = 5432
  
  # Network Configuration
  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [var.database_security_group_id]
  publicly_accessible    = false
  
  # Parameter and Option Groups
  parameter_group_name = aws_db_parameter_group.main.name
  
  # Backup Configuration
  backup_retention_period = var.environment == "prod" ? 7 : 1
  backup_window          = "03:00-04:00"  # UTC
  maintenance_window     = "sun:04:00-sun:05:00"  # UTC
  
  # Monitoring and Logging
  monitoring_interval = var.enable_monitoring ? 60 : 0
  monitoring_role_arn = var.enable_monitoring ? aws_iam_role.rds_monitoring[0].arn : null
  
  enabled_cloudwatch_logs_exports = [
    "postgresql"
  ]
  
  # Performance Insights (for production)
  performance_insights_enabled = var.environment == "prod"
  performance_insights_retention_period = var.environment == "prod" ? 7 : null
  
  # Deletion Protection
  deletion_protection = var.environment == "prod"
  skip_final_snapshot = var.environment != "prod"
  final_snapshot_identifier = var.environment == "prod" ? "${var.project_name}-${var.environment}-final-snapshot-${formatdate("YYYY-MM-DD-hhmm", timestamp())}" : null
  
  # Auto Minor Version Upgrade
  auto_minor_version_upgrade = true
  
  tags = merge(var.common_tags, {
    Name = "${var.project_name}-${var.environment}-database"
    Type = "database"
  })

  depends_on = [
    aws_db_subnet_group.main,
    aws_db_parameter_group.main
  ]
}

# -----------------------------------------------------------------------------
# IAM Role for RDS Enhanced Monitoring
# -----------------------------------------------------------------------------
resource "aws_iam_role" "rds_monitoring" {
  count = var.enable_monitoring ? 1 : 0
  
  name = "${var.project_name}-${var.environment}-rds-monitoring-role"
  description = "IAM role for RDS Enhanced Monitoring"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "monitoring.rds.amazonaws.com"
        }
      }
    ]
  })

  tags = merge(var.common_tags, {
    Name = "${var.project_name}-${var.environment}-rds-monitoring-role"
    Type = "iam"
  })
}

resource "aws_iam_role_policy_attachment" "rds_monitoring" {
  count = var.enable_monitoring ? 1 : 0
  
  role       = aws_iam_role.rds_monitoring[0].name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonRDSEnhancedMonitoringRole"
}

# -----------------------------------------------------------------------------
# Secrets Manager for Database Credentials
# -----------------------------------------------------------------------------
resource "aws_secretsmanager_secret" "db_credentials" {
  name = "${var.project_name}-${var.environment}-db-credentials"
  description = "Database credentials for ${var.project_name} ${var.environment}"
  
  # Automatic rotation configuration (optional)
  # rotation_lambda_arn = aws_lambda_function.rotation.arn
  # rotation_rules {
  #   automatically_after_days = 30
  # }

  tags = merge(var.common_tags, {
    Name = "${var.project_name}-${var.environment}-db-credentials"
    Type = "secrets"
  })
}

resource "aws_secretsmanager_secret_version" "db_credentials" {
  secret_id = aws_secretsmanager_secret.db_credentials.id
  
  secret_string = jsonencode({
    username = var.db_username
    password = random_password.db_password.result
    engine   = "postgres"
    host     = aws_db_instance.main.endpoint
    port     = aws_db_instance.main.port
    dbname   = var.db_name
    # Full connection string for convenience
    database_url = "postgresql://${var.db_username}:${random_password.db_password.result}@${aws_db_instance.main.endpoint}:${aws_db_instance.main.port}/${var.db_name}"
  })

  depends_on = [aws_db_instance.main]
}