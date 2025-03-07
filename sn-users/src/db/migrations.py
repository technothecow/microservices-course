import os
import psycopg2
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def run_migrations():
    """Run all SQL migration files in order."""
    # Database connection parameters
    conn_params = {
        'dbname': os.environ.get('DB_NAME', 'users'),
        'user': os.environ.get('DB_USER', 'postgres'),
        'password': os.environ.get('DB_PASSWORD', 'postgres'),
        'host': os.environ.get('DB_HOST', 'localhost'),
        'port': os.environ.get('DB_PORT', '5432'),
    }
    
    try:
        # Connect to the database
        conn = psycopg2.connect(**conn_params)
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Create migrations table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS migrations (
                id SERIAL PRIMARY KEY,
                version VARCHAR(255) NOT NULL UNIQUE,
                applied_at TIMESTAMP NOT NULL DEFAULT NOW()
            )
        """)
        
        # Get list of applied migrations
        cursor.execute("SELECT version FROM migrations")
        applied_migrations = {row[0] for row in cursor.fetchall()}
        
        # Find all migration files
        migrations_dir = Path(__file__).parent.parent.parent / "postgresql/migrations"
        migration_files = sorted(migrations_dir.glob("V*__*.sql"))
        
        for migration_file in migration_files:
            # Extract version from filename (V001__description.sql -> 001)
            version = migration_file.name.split('__')[0][1:]
            
            if version not in applied_migrations:
                logger.info(f"Applying migration: {migration_file.name}")
                
                # Read and execute migration
                with open(migration_file, 'r') as f:
                    sql = f.read()
                    cursor.execute(sql)
                
                # Record the migration
                cursor.execute(
                    "INSERT INTO migrations (version) VALUES (%s)",
                    (version,)
                )
                
                logger.info(f"Successfully applied migration: {migration_file.name}")
            else:
                logger.info(f"Skipping already applied migration: {migration_file.name}")
                
    except Exception as e:
        logger.error(f"Migration failed: {str(e)}")
        raise
    finally:
        if 'conn' in locals():
            conn.close()
    
    logger.info("Migrations completed successfully")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_migrations()
