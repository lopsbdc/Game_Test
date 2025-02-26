# Guia do Projeto Yakuza TCG

## NOTA PARA CLAUDE:
Este documento serve como guia para retomar o desenvolvimento do projeto após um reset de memória. O projeto é um sistema de cartas colecionáveis baseado na série Yakuza, desenvolvido em Python/FastAPI.

### INSTRUÇÕES DE CONTINUIDADE:
1. Analise o código fonte no ZIP anexado
2. Revise o estado atual documentado abaixo
3. Confirme compreensão do projeto antes de prosseguir
4. Retome desenvolvimento da última funcionalidade em progresso

## 1. Estado Atual do Projeto

### 1.1. Funcionalidades Implementadas
- CRUD completo de cartas
- Upload e gerenciamento de imagens
- Sistema de filtros e busca
- Validação de campos (ID/nome duplicados)
- Visualização responsiva de cartas
- Preview de imagens na listagem
- Filtros avançados (tipo, cor, raridade, custo, poder)

### 1.2. Última Implementação
- Sistema de filtros avançados
- Busca por texto com suporte a custo e poder específicos (custo:X, poder:X)
- Validação de IDs e nomes duplicados

### 1.3. Em Progresso
- Ajustes no layout dos filtros
- Remoção de flavor text do filtro
- Alinhamento dos campos de filtro

## 2. Estrutura do Projeto

### 2.1. Organização (Manter esta estrutura no ZIP)
```
yakuza_tcg/
├── src/
│   ├── api/
│   │   ├── __init__.py
│   │   └── cards.py          # Rotas e handlers
│   ├── database/
│   │   ├── __init__.py
│   │   ├── connection.py     # Conexão com banco
│   │   ├── models.py         # Modelos SQLAlchemy
│   │   └── repositories/
│   │       └── card_repository.py
│   └── utils/
├── static/
│   └── images/               # Imagens das cartas
├── templates/
│   ├── base.html
│   └── cards/
│       ├── list.html        # Lista com filtros
│       ├── form.html        # Formulário com validação
│       └── view.html        # Visualização detalhada
├── .env
├── main.py
└── requirements.txt
```

### 2.2. Dependências Principais
```
fastapi
uvicorn
sqlalchemy
python-multipart
psycopg2-binary
python-dotenv
```

## 3. Próximas Funcionalidades Planejadas

### 3.1. Prioridade Imediata
1. Sistema de Decks
   - Modelo de dados
   - Interface de construção
   - Validação de regras
   - Análise de curva de mana

### 3.2. Médio Prazo
1. Sistema de Jogo
   - Interface básica
   - Manipulação de cartas
   - Sistema de turnos

### 3.3. Longo Prazo
1. Autenticação
2. Estatísticas
3. Multiplayer

## 4. Convenções e Padrões

### 4.1. Código
- Tipo hints em Python
- Documentação em funções complexas
- Arquivos pequenos e focados
- Seguir PEP 8

### 4.2. Git
- Commits descritivos
- Uma feature por branch
- Merge apenas com testes OK

## 5. Informações do Sistema

### 5.1. Banco de Dados
- PostgreSQL local
- Tabelas principais:
  - cards (cartas)
  - decks (futuro)
  - users (futuro)

### 5.2. Endpoints Principais
```
GET  /cards          # Lista de cartas
POST /cards/new      # Nova carta
GET  /cards/{id}     # Visualizar carta
POST /cards/{id}/edit # Editar carta
```

## 6. Como Continuar o Desenvolvimento

### 6.1. Para o Desenvolvedor
1. Fornecer o ZIP do projeto atualizado
2. Fornecer este documento
3. Especificar qual funcionalidade continuar

### 6.2. Para Claude
1. Analisar código no ZIP
2. Verificar estado no documento
3. Confirmar entendimento
4. Prosseguir com desenvolvimento

## 7. Testes e Validações

### 7.1. Teste Manual
1. Criar carta nova
2. Editar carta existente
3. Testar filtros
4. Verificar uploads

### 7.2. Logs
- Manter logs detalhados
- Registrar erros
- Monitorar uploads

## NOTA FINAL PARA CLAUDE:
Este projeto está em desenvolvimento ativo. Ao retomar, confirme o entendimento e peça esclarecimentos se necessário. O desenvolvedor fornecerá o código fonte via ZIP junto com este documento para contextualização completa.