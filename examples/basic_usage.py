"""
Yardee Python SDK - Basic Usage Examples

Simple, copy-paste ready examples for common operations.
"""

import os
from yardee import Client

def setup_client():
    """Initialize the Yardee client with your API key."""
    api_key = os.getenv("YARDEE_API_KEY", "sk-your-api-key-here")
    
    if api_key == "sk-your-api-key-here":
        print("⚠️  Please set YARDEE_API_KEY environment variable")
        return None
        
    return Client(api_key=api_key)


def create_knowledge_base_example():
    """Example: Create a new knowledge base"""
    client = setup_client()
    if not client:
        return
    
    try:
        kb = client.create_knowledge_base(
            name="Company Documentation",
            description="Internal docs, policies, and procedures"
        )
        print(f"✅ Created knowledge base: {kb['name']} (ID: {kb['id']})")
        return kb['id']
    except Exception as e:
        print(f"❌ Failed to create KB: {e}")
        return None


def list_knowledge_bases_example():
    """Example: List all your knowledge bases"""
    client = setup_client()
    if not client:
        return
    
    try:
        result = client.list_knowledge_bases()
        print(f"📚 Found {result['count']} knowledge bases:")
        
        for kb in result['knowledge_bases']:
            print(f"   - {kb['name']} (ID: {kb['id']})")
            print(f"     Documents: {kb.get('document_count', 0)}")
            print(f"     Created: {kb.get('created_at', 'Unknown')}")
        
        return result['knowledge_bases']
    except Exception as e:
        print(f"❌ Failed to list KBs: {e}")
        return []


def upload_document_example(kb_id, file_path):
    """Example: Upload a document to a knowledge base"""
    client = setup_client()
    if not client:
        return
    
    try:
        result = client.upload_document(
            knowledge_base_id=kb_id,
            file_path=file_path,
            title="Important Document"
        )
        print(f"✅ Uploaded document: {result['filename']} (ID: {result['id']})")
        return result['id']
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        return None


def search_example(kb_id, query):
    """Example: Search within a knowledge base"""
    client = setup_client()
    if not client:
        return
    
    try:
        results = client.search(
            knowledge_base_id=kb_id,
            query=query,
            top_k=5
        )
        
        print(f"🔍 Search results for: '{query}'")
        print(f"   Found {len(results['results'])} results")
        
        for i, result in enumerate(results['results'], 1):
            score = result.get('similarity_score', 'N/A')
            preview = result['content'][:150] + "..." if len(result['content']) > 150 else result['content']
            print(f"   {i}. Score: {score}")
            print(f"      {preview}")
        
        return results
    except Exception as e:
        print(f"❌ Search failed: {e}")
        return None


def connect_database_example(kb_id):
    """Example: Connect a PostgreSQL database"""
    client = setup_client()
    if not client:
        return
    
    try:
        connection = client.connect_database(
            knowledge_base_id=kb_id,
            name="Production Database",
            db_type="postgresql",
            host="localhost",
            port=5432,
            database="myapp",
            username="dbuser",
            password="dbpass"
        )
        print(f"✅ Connected database: {connection['name']} (ID: {connection['id']})")
        return connection['id']
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return None


def connect_hubspot_example(kb_id):
    """Example: Connect HubSpot CRM"""
    client = setup_client()
    if not client:
        return
    
    hubspot_token = os.getenv("HUBSPOT_PRIVATE_APP_TOKEN")
    if not hubspot_token:
        print("⚠️  Set HUBSPOT_PRIVATE_APP_TOKEN environment variable")
        return None
    
    try:
        connection = client.connect_hubspot(
            knowledge_base_id=kb_id,
            name="HubSpot CRM",
            private_app_token=hubspot_token
        )
        print(f"✅ Connected HubSpot: {connection['name']} (ID: {connection['id']})")
        return connection['id']
    except Exception as e:
        print(f"❌ HubSpot connection failed: {e}")
        return None


def main():
    """Run all basic examples"""
    print("🚀 Yardee SDK - Basic Usage Examples")
    print("=" * 45)
    
    # 1. List existing knowledge bases
    print("\n1️⃣ Listing Knowledge Bases:")
    kbs = list_knowledge_bases_example()
    
    # 2. Create a new knowledge base if none exist
    if not kbs:
        print("\n2️⃣ Creating Knowledge Base:")
        kb_id = create_knowledge_base_example()
    else:
        kb_id = kbs[0]['id']
        print(f"\n2️⃣ Using existing KB: {kbs[0]['name']} (ID: {kb_id})")
    
    if not kb_id:
        print("❌ Cannot continue without a knowledge base")
        return
    
    # 3. Search example
    print("\n3️⃣ Testing Search:")
    search_example(kb_id, "getting started guide")
    
    # 4. Connection examples (commented out - require real credentials)
    print("\n4️⃣ Connection Examples:")
    print("   💡 Database and HubSpot examples available (see source code)")
    print("   📝 Set environment variables to test connections:")
    print("      - HUBSPOT_PRIVATE_APP_TOKEN for HubSpot")
    print("      - Update database credentials in connect_database_example()")
    
    print(f"\n🎉 Basic examples complete!")
    print("   📚 Check examples/advanced_features.py for more capabilities")


if __name__ == "__main__":
    main()