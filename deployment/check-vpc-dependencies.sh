#!/bin/bash

# A script to check for all dependencies of a given VPC.
# This is useful before attempting to delete a VPC.

if [ -z "$1" ]; then
    echo "Usage: $0 <vpc-id>"
    echo "Example: $0 vpc-12345678"
    exit 1
fi

VPC_ID=$1

echo "=== Checking VPC Dependencies for $VPC_ID ==="
echo

# Helper function to run a check and report errors without exiting
run_check() {
    local title="$1"
    shift
    echo "$title"
    # Execute the command. If it fails, print a generic error message.
    # The specific AWS CLI error will still be printed to stderr.
    if ! "$@"; then
        echo "--> Error running check. Please verify permissions and parameters."
    fi
    echo
}

# This comment is now correctly formatted.
run_check "1. Checking Subnets:" \
    aws ec2 describe-subnets --filters "Name=vpc-id,Values=$VPC_ID" --query 'Subnets[*].[SubnetId,CidrBlock,State]' --output table

run_check "2. Checking Internet Gateways:" \
    aws ec2 describe-internet-gateways --filters "Name=attachment.vpc-id,Values=$VPC_ID" --query 'InternetGateways[*].[InternetGatewayId,Attachments[0].State]' --output table

run_check "3. Checking NAT Gateways:" \
    aws ec2 describe-nat-gateways --filter "Name=vpc-id,Values=$VPC_ID" --query 'NatGateways[*].[NatGatewayId,State]' --output table

run_check "4. Checking Route Tables (non-main):" \
    aws ec2 describe-route-tables --filters "Name=vpc-id,Values=$VPC_ID" --query 'RouteTables[?!(Associations[?Main==`true`])].[RouteTableId]' --output table

run_check "5. Checking Security Groups (non-default):" \
    aws ec2 describe-security-groups --filters "Name=vpc-id,Values=$VPC_ID" --query "SecurityGroups[?GroupName!='default'].[GroupId,GroupName]" --output table

run_check "6. Checking Network ACLs (non-default):" \
    aws ec2 describe-network-acls --filters "Name=vpc-id,Values=$VPC_ID" --query 'NetworkAcls[?IsDefault==`false`].[NetworkAclId]' --output table

run_check "7. Checking VPC Endpoints:" \
    aws ec2 describe-vpc-endpoints --filters "Name=vpc-id,Values=$VPC_ID" --query 'VpcEndpoints[*].[VpcEndpointId,State]' --output table

run_check "8. Checking for general Network Interfaces (e.g., from EC2, Lambda):" \
    aws ec2 describe-network-interfaces --filters "Name=vpc-id,Values=$VPC_ID" --query 'NetworkInterfaces[*].[NetworkInterfaceId,Status,Description]' --output table

run_check "9. Checking for RDS DB Instances:" \
    aws rds describe-db-instances --query "DBInstances[?DBSubnetGroup.VpcId=='$VPC_ID'].[DBInstanceIdentifier,DBInstanceStatus,Engine]" --output table

run_check "10. Checking for ElastiCache Clusters (via ENIs):" \
    aws ec2 describe-network-interfaces --filters "Name=vpc-id,Values=$VPC_ID" "Name=description,Values=*ElastiCache*" --query 'NetworkInterfaces[*].[NetworkInterfaceId,Status,Description]' --output table

echo "=== Check Complete ==="
echo "Note: Default Security Groups, the main Route Table, and default Network ACLs cannot be deleted manually."
echo "All other resources listed above (including RDS, ElastiCache, EC2, LBs, etc.) must be deleted or detached before the VPC can be deleted."