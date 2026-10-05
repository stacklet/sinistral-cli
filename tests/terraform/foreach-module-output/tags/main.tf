variable "environment" {
  type = string
}

output "out" {
  value = {
    Environment = var.environment
  }
}
