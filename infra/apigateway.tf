resource "aws_apigatewayv2_api" "http_api" {
  name          = var.aws_apigateway_name
  protocol_type = "HTTP"

  # Se quiser já deixar CORS redondo:
  cors_configuration {
    allow_origins = ["*"]             # ajuste pra seu domínio em produção
    allow_methods = ["GET", "POST", "OPTIONS"]
    allow_headers = ["content-type", "x-requested-with"]
  }
}

resource "aws_apigatewayv2_stage" "default" {
  api_id = aws_apigatewayv2_api.http_api.id

  name        = "$default"
  auto_deploy = true
}

resource "aws_apigatewayv2_integration" "lambda_integration" {
  api_id = aws_apigatewayv2_api.http_api.id

  integration_type        = "AWS_PROXY"
  integration_uri         = aws_lambda_function.this.arn
  integration_method      = "POST"
  payload_format_version  = "2.0"
}

#########################
# ROTAS DA TUA API
#########################

# GET /health
resource "aws_apigatewayv2_route" "health" {
  api_id    = aws_apigatewayv2_api.http_api.id
  route_key = "GET /health"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}

# GET /jogos
resource "aws_apigatewayv2_route" "jogos" {
  api_id    = aws_apigatewayv2_api.http_api.id
  route_key = "GET /jogos"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}

# GET /jogos/{date}
resource "aws_apigatewayv2_route" "jogos_por_date" {
  api_id    = aws_apigatewayv2_api.http_api.id
  route_key = "GET /jogos/{date}"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}

# POST /jogos/gerar
resource "aws_apigatewayv2_route" "jogos_gerar" {
  api_id    = aws_apigatewayv2_api.http_api.id
  route_key = "POST /jogos/gerar"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}
