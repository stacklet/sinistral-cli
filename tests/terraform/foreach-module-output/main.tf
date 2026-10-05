# Regression fixture: the for_each collection holds a module output reference.
# The collection itself used to resolve, but each.value.<attr> inside the
# resource body stayed an unresolved reference marker, so policies matching
# on that attribute evaluated the marker instead of the real value.
provider "aws" {
  region = "us-east-2"
}

module "tags" {
  source      = "./tags"
  environment = "prod"
}

locals {
  queues = {
    # tags come from the module output and include Environment: compliant
    tagged = {
      tags = module.tags.out
    }
    # static tags without Environment: a genuine violation
    untagged = {
      tags = { Team = "platform" }
    }
  }
}

resource "aws_sqs_queue" "x" {
  for_each = local.queues
  name     = "queue-${each.key}"
  tags     = each.value.tags
}
