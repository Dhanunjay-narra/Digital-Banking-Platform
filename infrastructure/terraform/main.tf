terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

resource "aws_vpc" "finx_vpc" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true
  tags = {
    Name        = "finxcore-vpc"
    Environment = var.environment
  }
}

resource "aws_db_instance" "finx_postgres" {
  allocated_storage      = 100
  max_allocated_storage  = 500
  engine                 = "postgres"
  engine_version         = "16.1"
  instance_class         = "db.r6g.xlarge"
  db_name                = "finx_core_db"
  username               = "finx_admin"
  password               = var.db_password
  multi_az               = true
  storage_encrypted      = true
  skip_final_snapshot    = false
  deletion_protection    = true
}
