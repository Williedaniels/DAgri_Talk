# ==============================================================================
# D'Agri Talk - Project Makefile
#
# Provides a simple command interface for common project operations.
# ==============================================================================

# --- Configuration ---
SHELL := /bin/bash
TERRAFORM_DIR := terraform/environments/dev
PROJECT_PREFIX := dagri-talk-dev

# Use .PHONY to ensure these targets run even if files with the same name exist.
.PHONY: help deploy destroy destroy-infra full-teardown check-vpc cleanup-vpc cleanup-ecr cleanup-tfstate

# --- Main Targets ---

help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  deploy          : Deploys the application layer (ECS, ALB) using the deploy.sh script."
	@echo "  destroy         : Destroys the application layer using the destroy.sh script."
	@echo "  destroy-infra   : Runs 'terraform destroy' on the underlying infrastructure."
	@echo "  full-teardown   : Runs 'make destroy' and then 'make destroy-infra'."
	@echo ""
	@echo "Recovery & Cleanup Targets (use if 'destroy-infra' fails):"
	@echo "  check-vpc       : Checks for lingering dependencies in a VPC. Usage: make check-vpc VPC_ID=vpc-xxxxxxxx"
	@echo "  cleanup-vpc     : Force-cleans a VPC's networking components. Usage: make cleanup-vpc VPC_ID=vpc-xxxxxxxx"
	@echo "  cleanup-ecr     : Force-deletes ECR repositories for the project."
	@echo "  cleanup-tfstate : Removes stuck resources from the Terraform state after manual cleanup."

deploy:
	@echo "🚀 Deploying application..."
	@./deployment/deploy.sh

destroy:
	@echo "🔥 Destroying application layer..."
	@./deployment/destroy.sh

destroy-infra:
	@echo "🔥 Destroying Terraform-managed infrastructure..."
	@cd $(TERRAFORM_DIR) && terraform destroy

full-teardown: destroy destroy-infra
	@echo "✅ Full teardown complete."

# --- Recovery & Cleanup Targets ---

check-vpc:
ifndef VPC_ID
	$(error VPC_ID is not set. Usage: make check-vpc VPC_ID=vpc-xxxxxxxx)
endif
	@echo "🔍 Checking dependencies for VPC: $(VPC_ID)..."
	@./deployment/check-vpc-dependencies.sh $(VPC_ID)

cleanup-vpc:
ifndef VPC_ID
	$(error VPC_ID is not set. Usage: make cleanup-vpc VPC_ID=vpc-xxxxxxxx)
endif
	@echo "🧹 Cleaning up VPC: $(VPC_ID)..."
	@./deployment/cleanup-vpc.sh $(VPC_ID)

cleanup-ecr:
	@echo "🧹 Cleaning up ECR repositories for prefix: $(PROJECT_PREFIX)..."
	@./deployment/cleanup-ecr.sh $(PROJECT_PREFIX)

cleanup-tfstate:
	@echo "🧹 Cleaning up Terraform state..."
	@./deployment/cleanup-tfstate.sh