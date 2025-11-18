data "aws_region" "current" {}
data "aws_caller_identity" "current" {}

# ------------------------------------------------------
# 1 Role de execução da Lambda
# ------------------------------------------------------
resource "aws_iam_role" "lambda_exec" {
  name               = "${var.function_name}-exec-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "basic" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# ------------------------------------------------------
# 2 Função Lambda
# ------------------------------------------------------
resource "aws_lambda_function" "this" {
  function_name    = var.function_name
  role             = aws_iam_role.lambda_exec.arn
  runtime          = var.lambda_runtime
  handler          = var.lambda_handler
  filename         = var.artifact_path
  source_code_hash = filebase64sha256(var.artifact_path)

  architectures = ["arm64"]

  memory_size = var.memory_size
  timeout     = var.timeout

  environment {
    variables = var.environment
  }
}

resource "aws_lambda_function_url" "this" {
  function_name      = aws_lambda_function.this.function_name
  authorization_type = var.function_url_auth_type
}

resource "aws_cloudwatch_log_group" "lambda" {
  name              = "/aws/lambda/${var.function_name}"
  retention_in_days = 14
}

# ------------------------------------------------------
# 3 API Gateway HTTP API
# ------------------------------------------------------
resource "aws_apigatewayv2_api" "http_api" {
  name          = var.aws_apigateway_name
  protocol_type = "HTTP"

  body = templatefile("${path.module}/openapi.yaml", {
    region     = data.aws_region.current.name
    lambda_arn = aws_lambda_function.this.arn
  })
}

# ------------------------------------------------------
# 5 Integração HTTP API -> Lambda
# ------------------------------------------------------
resource "aws_apigatewayv2_integration" "lambda_integration" {
  api_id = aws_apigatewayv2_api.http_api.id

  integration_type = "AWS_PROXY"
  integration_uri  = aws_lambda_function.this.arn

  integration_method = "POST" # obrigatório na integração com Lambda
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "hello_route" {
  api_id = aws_apigatewayv2_api.http_api.id

  route_key = "GET /hello"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}

resource "aws_apigatewayv2_stage" "default" {
  api_id = aws_apigatewayv2_api.http_api.id

  name        = "$default"
  auto_deploy = true
}

# ------------------------------------------------------
# 4 Permissão para API Gateway invocar a Lambda
# ------------------------------------------------------
resource "aws_lambda_permission" "apigw_invoke" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.this.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.http_api.execution_arn}/*/*"
}

