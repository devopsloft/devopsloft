#!/usr/bin/env bash

set -exuo pipefail

# Make sure AWS CLI is installed
if ! hash aws 2>/dev/null; then
    virtualenv .venv && source .venv/bin/activate
    pip install awscli
fi

# Create a keypair. It is required for creating a new instance.
# It can fail since keypair might exist already.
aws ec2 create-key-pair --key-name my_keypair || true

# Create a new instance using Ubuntu image
EC2_RUN_RESULT=$(aws ec2 run-instances --instance-type t2.nano --count 1 --key my_keypair --image-id ami-79873901)
