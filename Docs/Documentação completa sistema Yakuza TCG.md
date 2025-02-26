# Yakuza TCG - Documentação Completa do Projeto

## 1. Visão Geral
Sistema web para gerenciamento e jogo de cartas colecionáveis baseado na série Yakuza.

### 1.1. Objetivos
- Criar plataforma para gerenciamento de cartas e decks
- Permitir jogos online entre jogadores
- Fornecer ferramentas de análise e estatísticas
- Manter sistema modular e fácil de manter

### 1.2. Arquitetura Híbrida
- **Ambiente de Desenvolvimento/Produção**
  - Local: PostgreSQL + FastAPI
  - Produção: Supabase (futuro)
- **Sistema de Jogo**
  - Servidor Local (PC/Notebook)
  - Specs mínimas:
    - i5 3ª geração
    - 10GB RAM
    - 40GB HD livre
    - Internet estável

## 2. Estrutura do Projeto

### 2.1. Organização de Arquivos
```
yakuza_tcg/
├── src/
│   ├── api/                    # Endpoints
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── cards.py
│   │   ├── decks.py
│   │   └── game.py
│   │
│   ├── core/                   # Lógica central
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── cards.py
│   │   └── game_logic.py
│   │
│   ├── database/              # Banco de dados
│   │   ├── __init__.py
│   │   ├── connection.py
│   │   ├── models.py
│   │   └── repositories/
│   │
│   ├── services/              # Serviços
│   │   ├── __init__.py
│   │   ├── card_service.py
│   │   └── game_service.py
│   │
│   └── utils/                 # Utilitários
│       ├── __init__.py
│       ├── validators.py
│       └── helpers.py
│
├── static/                    # Frontend
│   ├── css/
│   ├── js/
│   │   ├── components/
│   │   ├── services/
│   │   └── utils/
│   └── images/
│
├── templates/                 # HTML
├── tests/                    # Testes
└── config/                   # Configurações
```

### 2.2. Tecnologias Principais
- Backend: Python + FastAPI
- Banco: PostgreSQL
- Frontend: HTML + CSS (Tailwind) + JavaScript
- Testes: pytest
- Documentação: Markdown

## 3. Funcionalidades

### 3.1. Sistema de Cartas
- CRUD completo de cartas
- Upload e gestão de imagens
- Sistema de layouts customizáveis
- Versionamento de cartas
- Tags e categorias

### 3.2. Editor de Layout
- Interface gráfica para criação de templates
- Zonas configuráveis (texto, números, imagens)
- Preview em tempo real
- Validação de espaços e textos
- Sistema de camadas

### 3.3. Deck Builder
- Construção de decks
- Validação de regras
- Análise de curva de mana
- Sugestões de cartas
- Exportação/Importação

### 3.4. Sistema de Jogo
- Interface web via navegador
- Controles manuais para:
  - Vida
  - Heat
  - Posicionamento de cartas
  - Virar/desvirar
- Log de ações
- Chat entre jogadores

### 3.5. Sistema de Usuários
- Autenticação
- Perfis
- Níveis de acesso (admin/user)
- Histórico de jogos
- Estatísticas

### 3.6. Análise de Dados
- Winrate de decks/cartas
- Cartas mais usadas
- Tendências de meta
- Relatórios para balanceamento

## 4. Processo de Desenvolvimento

### 4.1 Fase Local (Notebook)
```python
# Configuração do servidor local
uvicorn main:app --host 0.0.0.0 --port 8000
```

#### 4.1.1 Ambiente Inicial
- PostgreSQL local
- FastAPI backend
- Interface web básica
- Autenticação simples

#### 4.1.2 Desenvolvimento Base
- CRUD completo
- Interface inicial
- Sistema base de jogo
- Testes locais

### 4.2 Sistema de Compartilhamento

#### 4.2.1 Gerenciador GitHub
```python
class GitHubManager:
    def __init__(self):
        self.token = os.getenv('GITHUB_TOKEN')
        self.repo = "yakuza-tcg"
        
    def sanitize_sensitive_data(self):
        """Protege dados sensíveis"""
        sensitive_files = [
            'card_data.json',
            'config/secrets.py'
        ]
        # Processo de sanitização
        
    def toggle_visibility(self, make_public=False):
        """Controle de visibilidade"""
        if make_public:
            self.sanitize_sensitive_data()
            # Torna público
        else:
            # Reverte sanitização
            # Torna privado
```

#### 4.2.2 Interface Admin
```python
@app.route("/admin/repo-control")
def repo_control():
    return {
        "status": "private/public",
        "last_changed": timestamp,
        "temp_link": "github.com/...",
        "auto_private_in": "2 hours"
    }
```

### 4.3 Arquitetura Híbrida

#### 4.3.1 Estrutura de Dados
```sql
-- Supabase (24/7)
CREATE TABLE auth.users (
    id UUID PRIMARY KEY,
    username TEXT UNIQUE,
    email TEXT UNIQUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE public.decks (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES auth.users,
    name TEXT,
    cards JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Local (Jogos)
CREATE TABLE game_sessions (
    id UUID PRIMARY KEY,
    players JSONB,
    current_state JSONB,
    started_at TIMESTAMPTZ DEFAULT NOW()
);
```

#### 4.3.2 Sistema de Sincronização
```python
class DataSync:
    def __init__(self):
        self.supabase = create_client(...)
        self.local_db = PostgresDB(...)
    
    async def sync_from_supabase(self):
        """Sincroniza dados do Supabase"""
        updates = await self.supabase.fetch_updates()
        await self.local_db.apply_updates(updates)
    
    async def push_game_data(self):
        """Envia dados de jogos"""
        game_data = await self.local_db.get_new_games()
        await self.supabase.store_game_data(game_data)
```

#### 4.3.3 Sistema de Cache
```python
class GameCache:
    def __init__(self):
        self.deck_cache = {}
        self.card_cache = {}
        
    async def get_deck(self, deck_id):
        """Busca deck (cache ou Supabase)"""
        if deck_id in self.deck_cache:
            return self.deck_cache[deck_id]
        
        deck = await supabase.get_deck(deck_id)
        self.deck_cache[deck_id] = deck
        return deck
```

### 4.4 Fluxo de Operação

#### 4.4.1 Servidor de Jogo
```python
async def server_startup():
    """Inicialização do servidor"""
    # 1. Sincronização inicial
    await sync_latest_data()
    
    # 2. Preparação de cache
    await warm_up_cache()
    
    # 3. Início de listeners
    start_sync_listeners()
    
    # 4. Abertura de conexões
    start_game_server()
```

#### 4.4.2 Ambientes
- **Supabase (24/7)**
  - Autenticação
  - Dados persistentes
  - Estatísticas
  
- **Local (Jogos)**
  - Sistema de jogo
  - Matchmaking
  - Chat
  - Logs

### 4.5 Sistema de Backup

#### 4.5.1 Backup Automático
```python
class BackupSystem:
    def __init__(self):
        self.backup_paths = {
            'local': 'backups/local/',
            'supabase': 'backups/supabase/'
        }
    
    async def create_backup(self):
        """Backup completo"""
        timestamp = datetime.now()
        await self.backup_local_db(timestamp)
        await self.backup_supabase_data(timestamp)
    
    async def restore_point(self, timestamp):
        """Restauração específica"""
```

#### 4.5.2 Logging
```python
class SyncLogger:
    def log_sync_event(self, event_type, details):
        """Log de eventos"""
        log_entry = {
            'timestamp': datetime.now(),
            'type': event_type,
            'details': details,
            'status': 'success/error'
        }
        await self.store_log(log_entry)
```

## 5. Segurança e Privacidade

### 5.1. Repositório
- Controle de visibilidade GitHub
- Sanitização automática
- Permissões granulares

### 5.2. Dados
- Criptografia em repouso
- Backups seguros
- Logs de acesso

## 6. Fases de Implementação

### 6.1. Fase 1 - Base (2-3 semanas)
- Setup inicial
- CRUD básico
- Interface administrativa
- Autenticação

### 6.2. Fase 2 - Core (2-3 semanas)
- Sistema de layouts
- Deck builder
- Análises básicas

### 6.3. Fase 3 - Jogo (2-3 semanas)
- Interface de jogo
- Sistema de salas
- Chat e logs

## 7. Manutenção

### 7.1. Código
- Arquivos modulares
- Documentação inline
- Testes unitários

### 7.2. Monitoramento
- Logs de sistema
- Métricas de uso
- Backups automáticos

### 7.3. Updates
- Patches semanais
- Updates mensais
- Hotfixes quando necessário

## 8. Recursos Necessários

### 8.1. Desenvolvimento
- VSCode
- Python 3.9+
- PostgreSQL
- Git

### 8.2. Produção
- Servidor dedicado
- Backup externo
- Monitoramento 24/7

## 9. Métricas de Sucesso

### 9.1. Performance
- Tempo de resposta < 200ms
- Uptime > 99%
- Zero perda de dados

### 9.2. Usuários
- Retenção > 70%
- Satisfação > 4/5
- Crescimento mensal > 10%