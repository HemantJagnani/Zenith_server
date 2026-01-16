from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
import sys

# The connection string I have from previous context
DATABASE_URL = "postgresql://postgres.bpcuynlliomdtlbmahxw:Nexus%40211421@aws-0-ap-south-1.pooler.supabase.com:5432/postgres"

print(f"Testing connection to: {DATABASE_URL.split('@')[1]}") # Hide credentials in output

try:
    engine = create_engine(DATABASE_URL)
    connection = engine.connect()
    print("✅ Connection successful!")
    connection.close()
    sys.exit(0)
except OperationalError as e:
    print(f"❌ Connection failed: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ An error occurred: {e}")
    sys.exit(1)
