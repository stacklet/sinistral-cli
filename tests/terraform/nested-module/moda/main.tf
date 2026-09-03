# Regression fixture: the for_each collection is built by reading a file
# through path.module from inside a non-root module. Path-based functions
# used to resolve relative to the module directory, so composing them with
# the project-root-relative path.module produced a duplicated module prefix,
# the read returned null, the for_each expanded to nothing, and this resource
# never reached policy evaluation at all.
locals {
  items = yamldecode(file("${path.module}/data.yml"))
}

resource "aws_sqs_queue" "x" {
  for_each = local.items
  name     = each.value.name
}
