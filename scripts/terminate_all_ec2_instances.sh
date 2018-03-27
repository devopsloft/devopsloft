#!/usr/bin/env bash

set -exuo pipefail

# Make sure AWS CLI is installed
if ! hash aws 2>/dev/null; then
    virtualenv .venv && source .venv/bin/activate
    pip install awscli
fi

aws ec2 terminate-instances --instance-ids $(aws ec2 describe-instances --query 'Reservations[*].Instances[*].[InstanceId]' --output text)
