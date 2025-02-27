# Implementação do Sistema de Decks

Implementamos com sucesso o sistema de Decks para o jogo Yakuza TCG, seguindo as regras estabelecidas no documento Regras.txt. 

## Componentes Implementados

1. **Modelo de Dados**
   - Tabela `decks` para armazenar informações básicas dos decks
   - Tabela de relação `deck_cards` para armazenar as cartas de cada deck
   - Campos para identificar cartas de dinheiro e heat

2. **Repositório de Decks**
   - Métodos CRUD completos
   - Validação de regras do jogo
   - Cálculo de estatísticas e análises

3. **Rotas da API**
   - Listagem de decks
   - Criação e edição de decks
   - Visualização detalhada de deck com análises
   - Exportação de deck

4. **Interface do Usuário**
   - Formulário de criação/edição de deck
   - Visualização detalhada do deck
   - Análises visuais (curva de mana, distribuição de tipos/cores)
   - Validação interativa das regras do jogo

## Regras do Jogo Implementadas

O sistema valida automaticamente as seguintes regras:

- **Composição do Deck:**
  - 40-50 cartas principais
  - 10-30 cartas de dinheiro
  - 5 cartas de heat (exatamente)
  - Total de 50-80 cartas no deck
  - Máximo de 3 cópias de cada carta
  - 1 Leader Card obrigatório

## Análises Disponíveis

O sistema oferece as seguintes análises automáticas:

1. **Curva de Mana**
   - Distribuição de custos das cartas do deck principal
   - Visualização gráfica para facilitar análise

2. **Distribuição de Tipos**
   - Proporção de cada tipo de carta no deck (Combat, Action, Support, Equipment)
   - Representação visual com barras coloridas

3. **Distribuição de Cores**
   - Proporção de cada cor de carta no deck (Purple, Blue, Red, Green, Gold)
   - Representação visual com barras coloridas

## Próximos Passos

Para futuras implementações, podemos considerar:

1. **Sistema de Jogo**
   - Interface de jogo com movimentação de cartas
   - Sistema de turnos
   - Resolução de combate

2. **Compartilhamento de Decks**
   - Exportação/importação em formatos padrão (JSON, texto)
   - Visualização pública de decks

3. **Análises Avançadas**
   - Sugestões de melhorias para decks
   - Comparação de estatísticas com outros decks
   - Recomendações de cartas baseadas na identidade do deck

## Instruções para Execução

1. Execute a migração do banco de dados:
   ```bash
   alembic upgrade head
   ```

2. Inicie o servidor:
   ```bash
   uvicorn main:app --reload
   ```

3. Acesse a interface web:
   ```
   http://localhost:8000/decks
   ```