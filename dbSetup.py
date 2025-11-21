from dbcmSqlite import Database
import sys

def dbSetup (dbname):
    # skullData={"name":skullName,"description":"","skullType":"","damageType":"","skullInfo":"","basicAttackInfo":"","passiveSkill":"","swapSkillName":"","swapSkillInfo":"","activeSkill":[]}
    with Database(dbname) as cur:
        # Skulls table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS skulls (
            name TEXT PRIMARY KEY,
            description TEXT,
            skullType TEXT,
            damageType TEXT,
            skullInfo TEXT,
            basicAttackInfo TEXT,
            passiveSkill TEXT,
            swapSkillName TEXT,
            swapSkillInfo TEXT
        )
        """)
        # Skills table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS activatedSkills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            info TEXT,
            cooldown TEXT
        )
        """)
        # Skull to Skull table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS skullToSkills (
            skull_name TEXT,
            skill_id INTEGER,
            FOREIGN KEY(skull_name) REFERENCES skull(name),
            FOREIGN KEY(skill_id) REFERENCES activatedSkills(id),
            PRIMARY KEY(skull_name, skill_id)
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
