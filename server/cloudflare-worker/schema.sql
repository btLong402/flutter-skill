-- ==============================================================================
-- Cloudflare D1 Database Schema for Flutter Pro Max Telemetry
-- Optimized with Aggregation (UPSERT) to minimize writes and storage
-- ==============================================================================

-- 1. Knowledge Gaps Table (Gộp trùng lặp bằng UNIQUE(query, domain))
CREATE TABLE IF NOT EXISTS knowledge_gaps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    query TEXT NOT NULL,
    domain TEXT NOT NULL,
    gap_type TEXT NOT NULL,
    hit_count INTEGER DEFAULT 1,
    max_score REAL DEFAULT 0.0,
    token_coverage REAL DEFAULT 0.0,
    last_notes TEXT,
    ai_assistant TEXT,
    client_os TEXT,
    last_seen DATETIME DEFAULT CURRENT_TIMESTAMP,
    first_seen DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(query, domain)
);

-- 2. Criteria Gaps Table (Gộp trùng lặp bằng UNIQUE(missing_dimension, platform))
CREATE TABLE IF NOT EXISTS criteria_gaps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    missing_dimension TEXT NOT NULL,
    platform TEXT NOT NULL,
    gap_type TEXT NOT NULL,
    hit_count INTEGER DEFAULT 1,
    reason TEXT,
    ai_assistant TEXT,
    client_os TEXT,
    last_seen DATETIME DEFAULT CURRENT_TIMESTAMP,
    first_seen DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(missing_dimension, platform)
);

-- Indexes for blazing fast ranking queries
CREATE INDEX IF NOT EXISTS idx_kg_hit_count ON knowledge_gaps (hit_count DESC);
CREATE INDEX IF NOT EXISTS idx_kg_last_seen ON knowledge_gaps (last_seen DESC);
CREATE INDEX IF NOT EXISTS idx_cg_hit_count ON criteria_gaps (hit_count DESC);
