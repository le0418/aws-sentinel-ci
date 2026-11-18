terraform {
  required_version = ">= 1.17.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"

  default_tags {
    tags = {
      Project     = "AWS-Sentinel-CI"
      Environment = "Lab"
      ManagedBy   = "Terraform"
      Purpose     = "Cloud-Security-Portfolio"
    }
  }
}
