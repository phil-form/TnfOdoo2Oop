CREATE TABLE hero_races (
    id              SERIAL PRIMARY KEY,
    name            VARCHAR(50) UNIQUE NOT NULL,
    description     VARCHAR(100) NOT NULL DEFAULT '',
    stamina_bonus   INTEGER NOT NULL DEFAULT 0,
    strength_bonus  INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE monster_types (
    id              SERIAL PRIMARY KEY,
    name            VARCHAR(50) UNIQUE NOT NULL,
    stamina_bonus   INTEGER NOT NULL DEFAULT 0,
    strength_bonus  INTEGER NOT NULL DEFAULT 0,
    drops_gold      BOOLEAN NOT NULL DEFAULT FALSE,
    drops_leather   BOOLEAN NOT NULL DEFAULT FALSE,
    token           CHAR(1) NOT NULL
);

CREATE TABLE maps (
    id                   SERIAL PRIMARY KEY,
    map_type             VARCHAR(50) UNIQUE NOT NULL,
    display_name         VARCHAR(50) NOT NULL,
    description          VARCHAR(100) NOT NULL DEFAULT '',
    default_size         INTEGER NOT NULL,
    default_nb_monsters  INTEGER NOT NULL,
    empty_token          VARCHAR(3) NOT NULL DEFAULT ' . '
);

-- Per-map spawn weights: higher weight = more frequent.
-- The Map model uses these to pick a random monster type on each spawn.
CREATE TABLE map_monster_weights (
    map_id          INTEGER NOT NULL REFERENCES maps(id),
    monster_type_id INTEGER NOT NULL REFERENCES monster_types(id),
    weight          INTEGER NOT NULL DEFAULT 1 CHECK (weight > 0),
    PRIMARY KEY (map_id, monster_type_id)
);

-- ── Seed data ────────────────────────────────────────────────────────────────

INSERT INTO hero_races (name, description, stamina_bonus, strength_bonus) VALUES
    ('Human', '+1 STR  +1 STAM', 1, 1),
    ('Dwarf', '+2 STAM  tougher', 2, 0);

INSERT INTO monster_types (name, stamina_bonus, strength_bonus, drops_gold, drops_leather, token) VALUES
    ('Wolf',   0, 0, FALSE, TRUE,  'W'),
    ('Orc',    0, 1, TRUE,  FALSE, 'O'),
    ('Dragon', 1, 0, TRUE,  TRUE,  'D');

INSERT INTO maps (map_type, display_name, description, default_size, default_nb_monsters, empty_token) VALUES
    ('forest', 'Forest', '15x15  balanced enemies', 15, 15, ' . '),
    ('castle', 'castle', '20x20 balanced enemies', 20, 20, ' # '),
    ('cave',   'Cave',   '12x12  dragon-heavy',     12, 12, ' : ');

-- Forest: Wolf / Orc / Dragon each at weight 1  →  equal probability
INSERT INTO map_monster_weights (map_id, monster_type_id, weight) VALUES
    (1, 1, 1),
    (1, 2, 1),
    (1, 3, 1);

-- Cave: Wolf 1, Orc 1, Dragon 2  →  Dragon spawns ~50 % of the time
INSERT INTO map_monster_weights (map_id, monster_type_id, weight) VALUES
    (2, 1, 1),
    (2, 2, 1),
    (2, 3, 2);
