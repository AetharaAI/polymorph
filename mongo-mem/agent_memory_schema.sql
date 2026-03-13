-- ═══════════════════════════════════════════════════════════════════
-- AETHER-MAX AGENT MEMORY SCHEMA
-- Database: operations | Schema: agent_memory
-- Run: docker exec -it redwatch-postgres psql -U redwatch_ops -d operations
-- ═══════════════════════════════════════════════════════════════════

CREATE SCHEMA IF NOT EXISTS agent_memory;

-- ─────────────────────────────────────────────
-- CORE MEMORY: Always-on identity/profile layer
-- Loaded at agent startup, injected every prompt
-- ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS agent_memory.core_memory (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id        VARCHAR(100) NOT NULL DEFAULT 'aether-max',
    key             VARCHAR(255) NOT NULL,
    value           TEXT NOT NULL,
    category        VARCHAR(50) NOT NULL,  -- 'user_profile' | 'agent_identity' | 'preference' | 'permanent_fact'
    priority        INTEGER DEFAULT 5,     -- 1-10, higher = inject first
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(agent_id, key)
);

-- ─────────────────────────────────────────────
-- SESSIONS: Lifecycle tracking for every session
-- ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS agent_memory.sessions (
    session_id          VARCHAR(100) PRIMARY KEY,
    agent_id            VARCHAR(100) NOT NULL DEFAULT 'aether-max',
    user_id             VARCHAR(100) NOT NULL DEFAULT 'cory',
    title               VARCHAR(255),
    status              VARCHAR(20) DEFAULT 'active',  -- active | completed | archived
    model               VARCHAR(100),
    total_input_tokens  BIGINT DEFAULT 0,
    total_output_tokens BIGINT DEFAULT 0,
    tool_call_count     INTEGER DEFAULT 0,
    iteration_count     INTEGER DEFAULT 0,
    started_at          TIMESTAMPTZ DEFAULT NOW(),
    ended_at            TIMESTAMPTZ,
    metadata            JSONB DEFAULT '{}'
);

-- ─────────────────────────────────────────────
-- MEMORY OPERATIONS: Full audit trail
-- Every read/write to any memory layer logged here
-- ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS agent_memory.memory_ops (
    id              BIGSERIAL PRIMARY KEY,
    session_id      VARCHAR(100),
    agent_id        VARCHAR(100) NOT NULL DEFAULT 'aether-max',
    op_type         VARCHAR(30) NOT NULL,
    -- 'write_episode' | 'read_episode'
    -- 'write_semantic' | 'read_semantic'
    -- 'write_procedure' | 'read_procedure'
    -- 'read_core' | 'write_core'
    -- 'write_working' | 'read_working'
    collection      VARCHAR(50),   -- MongoDB collection hit (if applicable)
    query_text      TEXT,          -- what was searched
    results_count   INTEGER,       -- results returned
    latency_ms      INTEGER,
    tokens_used     INTEGER,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- ─────────────────────────────────────────────
-- TOKEN USAGE: Per-session cost tracking
-- ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS agent_memory.token_usage (
    id              BIGSERIAL PRIMARY KEY,
    session_id      VARCHAR(100) NOT NULL,
    agent_id        VARCHAR(100) NOT NULL DEFAULT 'aether-max',
    model           VARCHAR(100),
    input_tokens    INTEGER NOT NULL DEFAULT 0,
    output_tokens   INTEGER NOT NULL DEFAULT 0,
    operation       VARCHAR(50),
    -- 'chat' | 'summarize' | 'embed' | 'rerank' | 'consolidate'
    cost_usd        NUMERIC(10, 6),
    recorded_at     TIMESTAMPTZ DEFAULT NOW()
);

-- ─────────────────────────────────────────────
-- PROCEDURE REGISTRY: Index of learned playbooks
-- Full docs live in MongoDB procedures collection
-- This is the fast lookup index
-- ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS agent_memory.procedure_registry (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id        VARCHAR(100) NOT NULL DEFAULT 'aether-max',
    task_type       VARCHAR(100) NOT NULL,
    description     TEXT NOT NULL,
    mongo_doc_id    VARCHAR(100),   -- foreign ref to MongoDB _id
    success_count   INTEGER DEFAULT 1,
    failure_count   INTEGER DEFAULT 0,
    last_used       TIMESTAMPTZ DEFAULT NOW(),
    avg_iterations  NUMERIC(5,2),
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- ─────────────────────────────────────────────
-- INDEXES
-- ─────────────────────────────────────────────
CREATE INDEX IF NOT EXISTS idx_sessions_agent      ON agent_memory.sessions(agent_id);
CREATE INDEX IF NOT EXISTS idx_sessions_status     ON agent_memory.sessions(status);
CREATE INDEX IF NOT EXISTS idx_sessions_started    ON agent_memory.sessions(started_at DESC);
CREATE INDEX IF NOT EXISTS idx_sessions_user       ON agent_memory.sessions(user_id);

CREATE INDEX IF NOT EXISTS idx_memory_ops_session  ON agent_memory.memory_ops(session_id);
CREATE INDEX IF NOT EXISTS idx_memory_ops_type     ON agent_memory.memory_ops(op_type);
CREATE INDEX IF NOT EXISTS idx_memory_ops_created  ON agent_memory.memory_ops(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_memory_ops_agent    ON agent_memory.memory_ops(agent_id);

CREATE INDEX IF NOT EXISTS idx_token_session       ON agent_memory.token_usage(session_id);
CREATE INDEX IF NOT EXISTS idx_token_agent         ON agent_memory.token_usage(agent_id);
CREATE INDEX IF NOT EXISTS idx_token_recorded      ON agent_memory.token_usage(recorded_at DESC);

CREATE INDEX IF NOT EXISTS idx_core_agent          ON agent_memory.core_memory(agent_id);
CREATE INDEX IF NOT EXISTS idx_core_category       ON agent_memory.core_memory(category);

CREATE INDEX IF NOT EXISTS idx_proc_agent          ON agent_memory.procedure_registry(agent_id);
CREATE INDEX IF NOT EXISTS idx_proc_type           ON agent_memory.procedure_registry(task_type);

-- ─────────────────────────────────────────────
-- SEED: Cory's core memory profile
-- ─────────────────────────────────────────────
INSERT INTO agent_memory.core_memory (agent_id, key, value, category, priority) VALUES
('aether-max', 'user_name',         'Cory',                                                                                        'user_profile',   10),
('aether-max', 'user_role',         'Founder and CEO of AetherPro Technologies LLC',                                               'user_profile',   10),
('aether-max', 'user_expertise',    'Licensed master electrician 15+ years commercial. Self-taught AI developer since April 2024', 'user_profile',   9),
('aether-max', 'agent_name',        'Aether-Max',                                                                                  'agent_identity', 10),
('aether-max', 'agent_purpose',     'Autonomous AI worker agent for AetherPro Technologies. Powered by MiniMax M2.5.',             'agent_identity', 10),
('aether-max', 'infra_stack',       'OVHcloud L40S GPUs, Redis Stack, PostgreSQL, MongoDB, Qdrant, NATS x3, BGE embed+rerank',    'user_profile',   8),
('aether-max', 'active_projects',   'RedWatch (CMMC 2.0/cybersec), AetherPro federal (CAGE 174V7), BlackBox Audio, Perceptor, AetherAgentForge', 'user_profile', 9),
('aether-max', 'coding_preference', 'Python backend, Next.js frontend. Claude Sonnet 4.6 is primary coding assistant.',           'preference',     7),
('aether-max', 'comms_style',       'Direct, no-nonsense. Electrical engineering background. First-principles reasoning.',        'preference',     7),
('aether-max', 'company_cage',      'AetherPro CAGE code 174V7, SAM.gov registered, targeting federal contracts',                 'permanent_fact', 8)
ON CONFLICT (agent_id, key) DO UPDATE
    SET value = EXCLUDED.value,
        updated_at = NOW();

-- ─────────────────────────────────────────────
-- VERIFY
-- ─────────────────────────────────────────────
SELECT schemaname, tablename
FROM pg_tables
WHERE schemaname = 'agent_memory'
ORDER BY tablename;

SELECT key, category, priority
FROM agent_memory.core_memory
ORDER BY priority DESC, category;
