#!/bin/bash
echo "🔍 Running IaC scan with Bandit..."
bandit -r cdk/
