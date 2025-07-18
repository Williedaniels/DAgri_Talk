#!/bin/bash

# A robust script to delete an AWS VPC and its core dependencies.
# It is designed to be safer and more reliable than a simple sequence of delete commands.
#
# Usage:
# ./cleanup-vpc.sh <vpc-id>
#
# Example:
# ./cleanup-vpc.sh vpc-00c7c47549cd82ae1

set -e # Exit immediately if a command exits with a non-zero status.

# --- 1. Input Validation ---
if [ -z "$1" ]; then
    echo "❌ Error: No VPC ID provided."
    echo "Usage: $0 <vpc-id>"
    exit 1
fi

VPC_ID=$1
AWS_REGION=$(aws configure get region)

echo "=== Starting Cleanup for VPC: $VPC_ID in region: $AWS_REGION ==="
echo "⚠️ WARNING: This script will delete network resources associated with the specified VPC."
echo "It will NOT delete EC2 instances, RDS databases, or Load Balancers."
echo "Please ensure those have been terminated manually before running this script."
echo
read -p "Press Enter to continue or Ctrl+C to abort..."

# --- 2. Check for Major Resources ---
# It's too risky to auto-delete these, so we just check and warn the user.
echo
echo "--- Checking for major resources (Manual cleanup required) ---"

INSTANCES=$(aws ec2 describe-instances --filters "Name=vpc-id,Values=$VPC_ID" "Name=instance-state-name,Values=pending,running,stopping,stopped" --query "Reservations[*].Instances[*].InstanceId" --output text)
if [ -n "$INSTANCES" ]; then
    echo "❌ Found active EC2 instances: $INSTANCES. Please terminate them first."
    exit 1
fi

LOAD_BALANCERS=$(aws elbv2 describe-load-balancers --query "LoadBalancers[?VpcId=='$VPC_ID'].LoadBalancerArn" --output text)
if [ -n "$LOAD_BALANCERS" ]; then
    echo "❌ Found active Load Balancers: $LOAD_BALANCERS. Please delete them first."
    exit 1
fi

echo "✅ No running instances or load balancers found in the VPC."

# --- 3. Delete NAT Gateways & Identify Their EIPs ---
# Start deleting NAT gateways first as they take time.
# Crucially, we identify their associated EIPs *before* deletion for safe cleanup later.
echo
echo "--- Deleting NAT Gateways and identifying associated Elastic IPs ---"
NAT_GATEWAYS=$(aws ec2 describe-nat-gateways --filter "Name=vpc-id,Values=$VPC_ID" --query 'NatGateways[?State!=`deleted`].{ID: NatGatewayId, EIP: NatGatewayAddresses[0].AllocationId}' --output json)
EIP_ALLOC_IDS=$(echo "$NAT_GATEWAYS" | jq -r '.[].EIP | select(.!=null)')
NAT_GW_IDS=$(echo "$NAT_GATEWAYS" | jq -r '.[].ID | select(.!=null)')

if [ -n "$NAT_GW_IDS" ]; then
    for nat_gw in $NAT_GW_IDS; do
        echo "Deleting NAT Gateway: $nat_gw"
        aws ec2 delete-nat-gateway --nat-gateway-id "$nat_gw"
    done
else
    echo "No NAT Gateways found."
fi

# --- 4. Delete VPC Endpoints ---
echo
echo "--- Deleting VPC Endpoints ---"
VPC_ENDPOINTS=$(aws ec2 describe-vpc-endpoints --filters "Name=vpc-id,Values=$VPC_ID" --query 'VpcEndpoints[].VpcEndpointId' --output text)
if [ -n "$VPC_ENDPOINTS" ]; then
    for endpoint in $VPC_ENDPOINTS; do
        echo "Deleting VPC Endpoint: $endpoint"
        aws ec2 delete-vpc-endpoint --vpc-endpoint-id "$endpoint"
    done
else
    echo "No VPC Endpoints found."
fi

# --- 5. Detach and Delete Internet Gateways ---
echo
echo "--- Detaching and Deleting Internet Gateways ---"
IGW_IDS=$(aws ec2 describe-internet-gateways --filters "Name=attachment.vpc-id,Values=$VPC_ID" --query 'InternetGateways[].InternetGatewayId' --output text)
if [ -n "$IGW_IDS" ]; then
    for igw in $IGW_IDS; do
        echo "Detaching IGW: $igw from VPC: $VPC_ID"
        aws ec2 detach-internet-gateway --internet-gateway-id "$igw" --vpc-id "$VPC_ID"
        echo "Deleting IGW: $igw"
        aws ec2 delete-internet-gateway --internet-gateway-id "$igw"
    done
else
    echo "No Internet Gateways found."
fi

# --- 6. Delete non-default Network ACLs ---
echo
echo "--- Deleting non-default Network ACLs ---"
NACL_IDS=$(aws ec2 describe-network-acls --filters "Name=vpc-id,Values=$VPC_ID" --query 'NetworkAcls[?IsDefault==`false`].NetworkAclId' --output text)
if [ -n "$NACL_IDS" ]; then
    for nacl in $NACL_IDS; do
        echo "Deleting Network ACL: $nacl"
        aws ec2 delete-network-acl --network-acl-id "$nacl"
    done
else
    echo "No non-default Network ACLs found."
fi

# --- 7. Disassociate and Delete non-main Route Tables ---
echo
echo "--- Disassociating and Deleting non-main Route Tables ---"
ROUTE_TABLES=$(aws ec2 describe-route-tables --filters "Name=vpc-id,Values=$VPC_ID" --query 'RouteTables[?Associations[?Main!=`true`]]' --output json)
ASSOC_IDS=$(echo "$ROUTE_TABLES" | jq -r '.[].Associations[?Main!=`true`].RouteTableAssociationId')
RT_IDS=$(echo "$ROUTE_TABLES" | jq -r '.[].RouteTableId')

if [ -n "$ASSOC_IDS" ]; then
    for assoc_id in $ASSOC_IDS; do
        echo "Disassociating Route Table Association: $assoc_id"
        aws ec2 disassociate-route-table --association-id "$assoc_id"
    done
fi

if [ -n "$RT_IDS" ]; then
    for rt_id in $RT_IDS; do
        echo "Deleting Route Table: $rt_id"
        aws ec2 delete-route-table --route-table-id "$rt_id"
    done
fi

# --- 8. Delete non-default Security Groups (with retry logic) ---
echo
echo "--- Deleting non-default Security Groups ---"
while true; do
    SGS=$(aws ec2 describe-security-groups --filters "Name=vpc-id,Values=$VPC_ID" --query 'SecurityGroups[?GroupName!=`default`].GroupId' --output text)
    if [ -z "$SGS" ]; then
        echo "No non-default security groups to delete."
        break
    fi
    
    DELETED_IN_PASS=false
    for sg in $SGS; do
        if aws ec2 delete-security-group --group-id "$sg" 2>/dev/null; then
            echo "Successfully deleted Security Group: $sg"
            DELETED_IN_PASS=true
        else
            echo "Could not delete Security Group: $sg (likely has dependencies, will retry)."
        fi
    done

    if [ "$DELETED_IN_PASS" = false ]; then
        echo "❌ ERROR: Could not delete any remaining security groups. There might be a dependency cycle or a resource (like a Network Interface) still using one."
        echo "Remaining SGs: $SGS"
        echo "Run 'deployment/check-vpc-dependencies.sh $VPC_ID' to investigate."
        exit 1
    fi
done

# --- 9. Delete Subnets ---
echo
echo "--- Deleting Subnets ---"
SUBNETS=$(aws ec2 describe-subnets --filters "Name=vpc-id,Values=$VPC_ID" --query 'Subnets[].SubnetId' --output text)
if [ -n "$SUBNETS" ]; then
    for subnet in $SUBNETS; do
        echo "Deleting Subnet: $subnet"
        aws ec2 delete-subnet --subnet-id "$subnet"
    done
else
    echo "No Subnets found."
fi

# --- 10. Wait for NAT Gateways and Release EIPs ---
echo
echo "--- Waiting for NAT Gateways to be fully deleted ---"
if [ -n "$NAT_GW_IDS" ]; then
    echo "Waiting for NAT GW(s): $NAT_GW_IDS"
    aws ec2 wait nat-gateway-deleted --nat-gateway-ids $NAT_GW_IDS
    echo "NAT Gateway(s) deleted."
fi

echo "--- Releasing associated Elastic IPs ---"
if [ -n "$EIP_ALLOC_IDS" ]; then
    for eip in $EIP_ALLOC_IDS; do
        echo "Releasing EIP with Allocation ID: $eip"
        aws ec2 release-address --allocation-id "$eip"
    done
else
    echo "No Elastic IPs associated with NAT Gateways to release."
fi

# --- 11. Final Instructions ---
echo
echo "--- Final Step: Delete the VPC ---"
echo "✅ Pre-cleanup complete."
echo "The script has removed dependencies. Please verify in the AWS console that all resources are gone."
echo "Then, run the following command to delete the VPC:"
echo
echo "aws ec2 delete-vpc --vpc-id $VPC_ID"