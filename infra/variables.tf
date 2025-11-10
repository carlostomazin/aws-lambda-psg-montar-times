variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-east-1"
}

variable "function_name" {
  description = "Lambda function name"
  type        = string
  default     = "lambda-psg-montar-times"
}

variable "lambda_runtime" {
  description = "Lambda runtime"
  type        = string
  default     = "python3.13"
}

variable "lambda_handler" {
  description = "Lambda handler"
  type        = string
  default     = "lambda_function.lambda_handler"
}

variable "memory_size" {
  description = "Lambda memory in MB"
  type        = number
  default     = 256
}

variable "timeout" {
  description = "Lambda timeout in seconds"
  type        = number
  default     = 30
}

variable "environment" {
  description = "Environment variables for Lambda"
  type        = map(string)
  default     = {}
}

variable "artifact_path" {
  description = "Path to the built Lambda zip"
  type        = string
  default     = "../dist/function.zip"
}
