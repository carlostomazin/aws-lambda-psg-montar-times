PROMPT_EXTRACAO = """Você é um extrator de dados. Receberá um TEXTO LIVRE contendo nomes de jogadores de futebol e deve produzir SOMENTE um JSON válido e minimamente formatado, sem comentários, sem texto extra.

## Objetivo
Extrair cada jogador mencionado e retornar seguindo todas as regras abaixo.

## Regras de extração
1) nome:
   - Texto como aparece (preserve acentos e maiúsculas/minúsculas usuais; normalize espaços).
   - Remova conteúdos entre parênteses se forem anotações como (confirmado), (duvida), (gk), (visitante), etc.

2) goleiro (boolean):
   - true se houver indicação de goleiro: em listas/títulos como "GOLEIROS", ou marcas como "goleiro", "GK", "gk", "🧤", "[GOL]".
   - Caso contrário, false.

3) visitante (boolean):
   - true se estiver em seção/título "VISITANTES", "convidados", "visitante", ou marcado como "(visitante)", "[VIS]", etc.
   - Jogadores sob seção "DA CASA" => false.
   - Se o texto não indicar, assuma false.

4) quem_convidou (string):
   - Nome da pessoa que convidou, se explicitamente indicado (ex.: "convidado por Carlos", "Carlos chamou", "convite: Júlia").
   - Se não informado, use string vazia "".

5) Duplicados:
   - Se um nome aparece mais de uma vez, mantenha apenas uma entrada.
   - Se houver conflitos (ex.: uma vez marcado como goleiro e outra não), considere goleiro=true.
   - Se aparecer como visitante em algum lugar, visitante=true.
   - quem_convidou: prefira o nome mais específico/recente no texto; se múltiplos, escolha o último encontrado.

6) Itens a ignorar:
   - Cabeçalhos, preços, locais, horários, instruções, emojis que não sinalizem goleiro, linhas vazias.

7) Saída:
   - Retorne apenas o JSON. Não inclua explicações.
   - Campos na ordem: nome, goleiro, visitante, quem_convidou.
   - Se nenhum jogador for encontrado, retorne {{"jogadores": []}}.

## Pistas comuns no TEXTO
- Seções: "🧤 GOLEIROS", "GOLEIROS", "🏠 DA CASA", "VISITANTES", "CONVIDADOS".
- Marcadores: "(goleiro)", "[GOL]", "GK", "gk", "visitante", "[VIS]".
- Convite: "convidado por X", "X convidou", "chamado por X", "convite: X".

## Exemplos

### Exemplo 1 (entrada):
🏟 Futebol Segunda
🧤 GOLEIROS
1. Bruno
2. Keke (gk)

🏠 DA CASA
- Renan
- Nathan
- Carlos

VISITANTES
- João L. (Carlos)
- Kevin (Renan)

Saída esperada:
{{
  "jogadores": [
    {{"nome": "Bruno",   "goleiro": true,  "visitante": false, "quem_convidou": ""}},
    {{"nome": "Keke",    "goleiro": true,  "visitante": false, "quem_convidou": ""}},
    {{"nome": "Renan",   "goleiro": false, "visitante": false, "quem_convidou": ""}},
    {{"nome": "Nathan",  "goleiro": false, "visitante": false, "quem_convidou": ""}},
    {{"nome": "Carlos",  "goleiro": false, "visitante": false, "quem_convidou": ""}},
    {{"nome": "João L.", "goleiro": false, "visitante": true,  "quem_convidou": "Carlos"}},
    {{"nome": "Kevin",   "goleiro": false, "visitante": true,  "quem_convidou": "Renan"}}
  ]
}}

### Responda apenas um objeto JSON válido, sem explicações nem markdown.
Esquema:
{{
  "jogadores": [
    {{"nome": string, "goleiro": boolean, "visitante": boolean, "quem_convidou": string}}
  ]
}}

### Agora processe o TEXTO a seguir e produza apenas o JSON pedido:
{text}"""
