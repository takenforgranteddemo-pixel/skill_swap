import sqlite3
import os
import shutil

OLD_DB = "db.sqlite3"
BACKUP_DB = "db.sqlite3.bak"
NEW_DB = "new_db.sqlite3"

# Step 1: Backup corrupted DB
if os.path.exists(OLD_DB):
    print(f"[+] Backing up {OLD_DB} to {BACKUP_DB}...")
    shutil.copy2(OLD_DB, BACKUP_DB)
else:
    print(f"[!] {OLD_DB} not found. Exiting.")
    exit(1)

# Step 2: Connect in read-only mode to avoid further damage
print("[+] Connecting to corrupted DB...")
try:
    conn_old = sqlite3.connect(f"file:{OLD_DB}?mode=ro", uri=True)
except Exception as e:
    print(f"[!] Could not open DB: {e}")
    exit(1)

# Step 3: Get list of tables
tables = []
try:
    cur = conn_old.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cur.fetchall()]
    print(f"[+] Found tables: {tables}")
except Exception as e:
    print(f"[!] Could not read table list: {e}")
    conn_old.close()
    exit(1)

# Step 4: Create new DB
conn_new = sqlite3.connect(NEW_DB)
cur_new = conn_new.cursor()

# Step 5: Copy tables one-by-one
for table in tables:
    try:
        # Get table schema
        schema = conn_old.execute(
            f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table}'"
        ).fetchone()[0]
        cur_new.execute(schema)
        conn_new.commit()

        # Copy data
        rows = conn_old.execute(f"SELECT * FROM {table}").fetchall()
        placeholders = ",".join(["?"] * len(rows[0])) if rows else ""
        if rows:
            cur_new.executemany(f"INSERT INTO {table} VALUES ({placeholders})", rows)
            conn_new.commit()

        print(f"[+] Recovered table: {table} ({len(rows)} rows)")
    except Exception as e:
        print(f"[!] Skipping table {table}: {e}")

# Step 6: Close connections
conn_old.close()
conn_new.close()

# Step 7: Replace old DB
os.remove(OLD_DB)
os.rename(NEW_DB, OLD_DB)

print("[✅] Recovery attempt finished")
print(f"[💾] Backup saved as {BACKUP_DB}")
