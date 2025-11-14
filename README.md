# AWS Lambda - PSG Montar Times

Lambda function para montar times de futebol baseado em uma lista de jogadores, zagueiros fixos e habilidades.

## Contrato da Lambda

### Entrada (Request Body)

A lambda espera receber um evento com a seguinte estrutura:

```json
{
  "body": "{\"jogadores_raw\": [...], \"zagueiros_fixo\": [...], \"habilidasos\": [...]}"
}
```

O `body` deve ser uma string JSON contendo:

#### Campos Obrigatórios:

- **jogadores_raw** (string): Texto contendo a lista de jogadores em formato estruturado
  - Deve conter seções identificadas por emojis ou palavras-chave: `🧤 GOLEIROS`, `🏠 DA CASA`, `🎟 VISITANTES`, `🚫 NÃO VÃO`
  - Cada jogador é extraído das seções, com suporte a nomes entre parênteses indicando quem convidou: `Nome (Convidou por)`
  - A lambda remove automaticamente emojis e caracteres especiais

- **zagueiros_fixo** (array de strings): Lista com os nomes dos zagueiros que DEVEM estar nos times
  - Os zagueiros fixos serão distribuídos nos times de forma equilibrada
  - Sensível a caso (case-insensitive na comparação)

- **habilidasos** (array de strings): Lista com os nomes dos jogadores com maior habilidade/força
  - Usada pela lógica de montagem de times para equilibrar a qualidade entre os times
  - Sensível a caso (case-insensitive na comparação)

#### Exemplo de Requisição Completa:

```json
{
  "body": "{\"jogadores_raw\": \"\\n🏟 Futebol Segunda - 20h\\n📍 Society Hidrofit\\n💰 R$ 12,00 por jogador\\n📲 Pix (chave aleatória): 40165266-dfa1-4e35-ae05-efdf2b5b8a6e\\n👤 Carlos Augusto \\n\\n⚠ CONFIRMAÇÃO OBRIGATÓRIA ATÉ 12H DE SEGUNDA PARA OS DA CASA ⚠\\nApós esse horário, abrimos vaga pros visitantes.\\n\\n🧤 GOLEIROS\\n1. Ryan (guilherme)\\n2.\\n\\n🏠 DA CASA\\n1. Renan\\n2. Gustaa\\n3. Johnny\\n4. Octávio \\n5. Leozin\\n6. Nathan \\n7. beligui \\n8. Igão\\n9. Matheus\\n10. Kevin\\n11. Rodrigo ✅©\\n12.\\n13.\\n14.\\n15.\\n16.\\n17.\\n18.\\n\\n🎟 VISITANTES\\n1. vinicius (Guilherme)\\n2. Murilo (Octávio)\\n3. Kovacs (Octávio)\\n4. Xoxolim (Leozin)\\n5. Yago (Leozin)\\n\\n🚫 NÃO VÃO\\n* Caio Maia\\n* Alex\\n* Rafael\\n* Carlos\\n* Jeh bass\\n* Fernando\\n* Yan\\n* Vitinho\\n* Rodrigo\\n* Gusin\\n\", \"zagueiros_fixo\": [\"rodrigo\", \"fernando\", \"leozin\"], \"habilidasos\": [\"caio maia\", \"nathan\", \"carlos\", \"alex\", \"gusta\", \"renan\"]}"
}
```

#### Formato Legível do Body (para referência):

```json
{
  "jogadores_raw": "\n🏟 Futebol Segunda - 20h\n📍 Society Hidrofit\n💰 R$ 12,00 por jogador\n📲 Pix (chave aleatória): 40165266-dfa1-4e35-ae05-efdf2b5b8a6e\n👤 Carlos Augusto \n\n⚠ CONFIRMAÇÃO OBRIGATÓRIA ATÉ 12H DE SEGUNDA PARA OS DA CASA ⚠\nApós esse horário, abrimos vaga pros visitantes.\n\n🧤 GOLEIROS\n1. Ryan (guilherme)\n2.\n\n🏠 DA CASA\n1. Renan\n2. Gustaa\n3. Johnny\n4. Octávio \n5. Leozin\n6. Nathan \n7. beligui \n8. Igão\n9. Matheus\n10. Kevin\n11. Rodrigo ✅©\n12.\n13.\n14.\n15.\n16.\n17.\n18.\n\n🎟 VISITANTES\n1. vinicius (Guilherme)\n2. Murilo (Octávio)\n3. Kovacs (Octávio)\n4. Xoxolim (Leozin)\n5. Yago (Leozin)\n\n🚫 NÃO VÃO\n* Caio Maia\n* Alex\n* Rafael\n* Carlos\n* Jeh bass\n* Fernando\n* Yan\n* Vitinho\n* Rodrigo\n* Gusin\n",
  "zagueiros_fixo": ["rodrigo", "fernando", "leozin"],
  "habilidasos": ["caio maia", "nathan", "carlos", "alex", "gusta", "renan"]
}
```

### Saída (Response)

A lambda retorna uma resposta com status HTTP e um JSON contendo os times montados:

#### Resposta de Sucesso (HTTP 200):

```json
{
  "statusCode": 200,
  "body": "{\"times\": {\"a\": [\"João Silva\", \"Lucas Oliveira\", \"...\"], \"b\": [\"Pedro Santos\", \"Marcus Vinicius\", \"...\"], \"c\": []}}"
}
```

O body contém um objeto `times` com três arrays:
- **a**: Jogadores do time A
- **b**: Jogadores do time B
- **c**: Jogadores do time C

#### Resposta de Erro (HTTP 400/500):

```json
{
  "statusCode": 400,
  "body": "{\"error\": \"mensagem de erro descritiva\"}"
}
```

### Códigos de Erro

| Código | Descrição |
|--------|-----------|
| 400 | JSON inválido no body, campos obrigatórios faltando, ou erro ao processar jogadores/times |
| 500 | Erro ao salvar dados do jogo no banco de dados |


## Funcionalidades

- ✅ Extração de jogadores a partir de JSON
- ✅ Remoção automática de emojis dos dados de entrada
- ✅ Montagem inteligente de times
- ✅ Suporte a zagueiros fixos
- ✅ Consideração de habilidades dos jogadores
- ✅ Persistência dos dados em Supabase
