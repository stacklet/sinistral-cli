provider "aws" {
  region = "us-east-2"
}

module "a" {
  source = "./moda"
}
