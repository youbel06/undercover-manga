-- LELOX Loup-Garou — Schéma Supabase
-- Exécuter dans l'éditeur SQL Supabase

CREATE TABLE IF NOT EXISTS lw_rooms (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  code TEXT UNIQUE NOT NULL,
  host_id UUID,
  status TEXT DEFAULT 'waiting',
  phase TEXT DEFAULT 'lobby',
  config JSONB DEFAULT '{}',
  roles JSONB DEFAULT '{}',
  night_count INTEGER DEFAULT 0,
  eliminated JSONB DEFAULT '[]',
  lovers JSONB DEFAULT '[]',
  night_actions JSONB DEFAULT '{}',
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS lw_players (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  room_id UUID,
  player_id UUID,
  username TEXT,
  avatar_emoji TEXT DEFAULT '🐺',
  role TEXT DEFAULT '',
  is_alive BOOLEAN DEFAULT TRUE,
  is_host BOOLEAN DEFAULT FALSE,
  is_ready BOOLEAN DEFAULT FALSE,
  joined_at TIMESTAMP DEFAULT NOW()
);
ALTER TABLE lw_rooms DISABLE ROW LEVEL SECURITY;
ALTER TABLE lw_players DISABLE ROW LEVEL SECURITY;
ALTER PUBLICATION supabase_realtime ADD TABLE lw_rooms;
ALTER PUBLICATION supabase_realtime ADD TABLE lw_players;
