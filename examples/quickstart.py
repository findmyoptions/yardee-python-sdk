"""
Yardee Python SDK - Quickstart Example

This example demonstrates core functionality of the Yardee Python SDK.
Replace 'your-api-key-here' with your actual API key from app.yardee.ai
"""

import os
from yardee import Client, YardeeError

def main():
    # Initialize the client
    api_key = os.getenv("YARDEE_API_KEY", "sk-your-api-key-here")
    
    if api_key == "sk-your-api-key-here":
        print("⚠️  Please set your API key!")
        print("   Option 1: Set environment variable: export YARDEE_API_KEY=sk-your-key")
        print("   Option 2: Replace 'sk-your-api-key-here' in this file")
        print("   Get your API key at: https://app.yardee.ai")
        return
    
    # Create client
    client = Client(api_key=api_key)
    print("🚀 Yardee SDK Quickstart Example")
    print("=" * 50)
    
    try:
        # 1. List existing knowledge bases
        print("\n📚 Your Knowledge Bases:")
        kb_list = client.list_knowledge_bases()
        
        if kb_list['count'] == 0:
            print("   No knowledge bases found. Let's create one!")
            
            # Create a new knowledge base
            new_kb = client.create_knowledge_base(
                name="SDK Test KB",
                description="Test knowledge base created by Python SDK"
            )
            print(f"✅ Created knowledge base: {new_kb['name']} (ID: {new_kb['id']})")
            kb_id = new_kb['id']
            
        else:
            # Use the first existing knowledge base
            kb = kb_list['knowledge_bases'][0]
            kb_id = kb['id']
            print(f"📖 Using existing KB: {kb['name']} (ID: {kb_id})")
            
            # Show all knowledge bases
            for kb in kb_list['knowledge_bases']:
                print(f"   - {kb['name']} (ID: {kb['id']}) - {kb.get('document_count', 0)} documents")
        
        # 2. List documents in the knowledge base
        print(f"\n📄 Documents in Knowledge Base {kb_id}:")
        documents = client.list_documents(kb_id)
        
        if documents['count'] == 0:
            print("   No documents found in this knowledge base.")
            print("   💡 Upload some documents to enable search functionality!")
        else:
            for doc in documents['documents']:
                print(f"   - {doc['filename']} (ID: {doc['id']}) - {doc.get('chunk_count', 0)} chunks")
        
        # 3. Perform a search (even if no documents - will show empty results)
        print(f"\n🔍 Testing Search Functionality:")
        
        test_queries = [
            "How do I get started?",
            "What are the pricing plans?", 
            "API documentation",
            "customer support contact"
        ]
        
        for query in test_queries[:2]:  # Test first 2 queries
            print(f"\n   Query: '{query}'")
            
            try:
                results = client.search(
                    knowledge_base_id=kb_id,
                    query=query,
                    top_k=3,
                    similarity_threshold=0.1
                )
                
                if results['results']:
                    print(f"   ✅ Found {len(results['results'])} results:")
                    for i, result in enumerate(results['results'], 1):
                        score = result.get('similarity_score', 'N/A')
                        content_preview = result['content'][:100] + "..." if len(result['content']) > 100 else result['content']
                        print(f"      {i}. Score: {score}")
                        print(f"         Preview: {content_preview}")
                        
                        # Show metadata if available
                        if 'metadata' in result and result['metadata']:
                            metadata = result['metadata']
                            if isinstance(metadata, dict):
                                for key, value in list(metadata.items())[:2]:  # Show first 2 metadata fields
                                    print(f"         {key}: {value}")
                else:
                    print("   📭 No results found (knowledge base may be empty)")
                    
            except YardeeError as e:
                print(f"   ❌ Search error: {e}")
        
        print(f"\n🎉 Quickstart Complete!")
        print("   Next steps:")
        print("   1. Upload documents to your knowledge base")
        print("   2. Connect databases or HubSpot for live data")
        print("   3. Try different search queries")
        print("   4. Integrate into your application")
        
    except YardeeError as e:
        print(f"❌ Yardee API Error: {e}")
        print("   Check your API key and network connection")
        
    except Exception as e:
        print(f"💥 Unexpected Error: {e}")
        print("   Please check the error details and try again")


if __name__ == "__main__":
    print("Yardee Python SDK - Quickstart Example")
    print("Get your API key at: https://app.yardee.ai")
    print()
    
    main()