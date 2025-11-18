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

resource "aws_lambda_permission" "apigw_invoke" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.this.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.http_api.execution_arn}/*/*"
}

resource "aws_cloudwatch_log_group" "lambda" {
  name              = "/aws/lambda/${var.function_name}"
  retention_in_days = 14
}
