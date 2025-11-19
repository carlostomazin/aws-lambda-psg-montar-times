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

# GET /games
resource "aws_apigatewayv2_route" "games" {
  api_id    = aws_apigatewayv2_api.http_api.id
  route_key = "GET /games"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}

# GET /games/{date}
resource "aws_apigatewayv2_route" "games_por_date" {
  api_id    = aws_apigatewayv2_api.http_api.id
  route_key = "GET /games/{gameId}"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}

# POST /games/create
resource "aws_apigatewayv2_route" "games_create" {
  api_id    = aws_apigatewayv2_api.http_api.id
  route_key = "POST /games/create"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}
