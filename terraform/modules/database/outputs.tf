# =============================================================================
# D'Agri Talk - Database Module Outputs
# =============================================================================

output "database_credentials_secret_arn" {
  description = "The ARN of the Secrets Manager secret for DB credentials."
  value       = aws_secretsmanager_secret.db_credentials.arn
}