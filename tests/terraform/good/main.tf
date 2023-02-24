provider "aws" {
  region = "us-east-2"
}

resource "aws_sqs_queue" "test_sqs" {
  name = uuid()
  sqs_managed_sse_enabled = true
  tags = {
    Environment = "dev"
  }
}

module "sqs" {
  source  = "terraform-aws-modules/sqs/aws"
  version = "4.0.1"
  sqs_managed_sse_enabled = true
  tags = {
    Environment = "dev"
  }
}
