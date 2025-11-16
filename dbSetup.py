from dbcmSqlite import Database
import sys

def dbSetup (dbname):
    with Database(dbname) as cur:
        # Skulls table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS skulls (
            name TEXT PRIMARY KEY,
            rarity TEXT,
            skull_type TEXT,
            damage_type TEXT,
            passive_skill TEXT,
            swap_skill1 TEXT,
            swap_skill2 TEXT,
            skill_names TEXT,
            skill_descriptions TEXT,
            skill_cooldowns TEXT
        )
        """)
        # Items table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS equipment (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            rarity TEXT,
            description TEXT,
            effect TEXT,
            recommended_skulls TEXT
        )
        """)
        # Inscriptions table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS inscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            description TEXT,
            thresholds TEXT
        )
        """)
        # Inscription Effects Table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS inscriptions_effects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            requirement TEXT,
            effect TEXT
        )
        """)
        # Join table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS item_inscriptions (
            item_id INTEGER,
            inscription_id INTEGER,
            FOREIGN KEY(item_id) REFERENCES items(id),
            FOREIGN KEY(inscription_id) REFERENCES inscriptions(id),
            PRIMARY KEY(item_id, inscription_id)
        )
        """)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage python -m dbSetup <dbname>")
    else:
        dbSetup(sys.argv[1])
