# aws-lambda-psg-montar-times

Pipeline de CI/CD com GitHub Actions e infraestrutura com Terraform para fazer deploy de uma AWS Lambda (Python).

**Resumo**
- Código da Lambda em `app/` (handler: `lambda_function.lambda_handler`).
- Dependências Python em `app/requirements.txt` (empacotadas no build).
- Infra Terraform em `infra/` (IAM role, logs e Lambda).
- Workflow do GitHub em `.github/workflows/deploy.yml` (build + terraform apply).

## Pré‑requisitos
- AWS credenciais com permissões para IAM, Lambda, CloudWatch Logs e acesso ao bucket de state S3.
- Bucket S3 e tabela DynamoDB para o backend do Terraform (state/lock).
- Secrets no repositório GitHub:
  - `AWS_ACCESS_KEY_ID`
  - `AWS_SECRET_ACCESS_KEY`
  - `AWS_REGION` (ex: `us-east-1`)
  - `TF_STATE_BUCKET` (bucket S3 do state)
  - `TF_STATE_LOCK_TABLE` (tabela DynamoDB do lock)
  - `SUPABASE_URL` e `SUPABASE_KEY` (variáveis de ambiente usadas pelo app)

## Estrutura
- `app/`
  - `lambda_function.py` (handler)
  - `src/` (módulos auxiliares)
  - `requirements.txt` (dependências)
- `infra/`
  - `main.tf`, `variables.tf` (Lambda, IAM, Logs)
- `.github/workflows/deploy.yml` (pipeline)

## Como funciona o pipeline
1. Faz checkout do código e configura Python 3.13.
2. Instala dependências do `app/requirements.txt` e empacota tudo em `dist/function.zip` (inclui `app/` e libs).
3. Configura credenciais AWS.
4. Gera `infra/ci.auto.tfvars.json` com variáveis sensíveis (de Secrets) e roda:
   - `terraform init` usando backend S3 + DynamoDB.
   - `terraform validate` e `plan` (em PRs) ou `apply` (no branch `main`).

## Variáveis principais (Terraform)
- `function_name` (default: `psg-montar-times`)
- `lambda_runtime` (default: `python3.13`)
- `lambda_handler` (default: `lambda_function.lambda_handler`)
- `artifact_path` (default: `../dist/function.zip`)
- `environment` (map com envs, preenchido no CI via `ci.auto.tfvars.json`)

## Observações
- O backend do Terraform requer bucket S3 e tabela DynamoDB já existentes. Crie-os manualmente ou via um stack separado antes do primeiro deploy.
- Se quiser expor a Lambda via HTTP, podemos adicionar API Gateway (HTTP API) e permissões — peça que eu incluo.

## URL pública da Lambda
- O Terraform cria uma "Lambda Function URL" pública por padrão (auth `NONE`).
- A URL é exposta no output `lambda_function_url` após o `terraform apply`.
- Para ver no GitHub Actions: cheque os logs do job de `apply` ou rode localmente `terraform output lambda_function_url` dentro de `infra/`.
- Segurança: `NONE` permite acesso anônimo. Para restringir, defina `function_url_auth_type = "AWS_IAM"` em variáveis do Terraform e proteja com IAM/assinatura SigV4.
