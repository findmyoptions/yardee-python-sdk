# Yardee Python SDK

🚀 **The fastest way to add AI-powered search to your Python applications**

[![PyPI version](https://badge.fury.io/py/yardee.svg)](https://badge.fury.io/py/yardee)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Turn your documents into intelligent search endpoints in minutes. The Yardee Python SDK provides seamless access to our vector database API, letting you build ChatGPT-style question answering over your own data.

## ⚡ Quick Start

```bash
pip install yardee
```

```python
from yardee import Client

# Initialize client
client = Client(api_key="sk-your-api-key")

# Search your knowledge base
results = client.search(
    knowledge_base_id=123,
    query="How do I reset my password?"
)

# Get intelligent answers
for result in results['results']:
    print(f"📄 {result['content']}")
    print(f"🎯 Relevance: {result['similarity_score']:.2f}")
```

**Get your free API key at [app.yardee.ai](https://app.yardee.ai) →**

## 🎯 Why Yardee?

- **⚡ Instant Setup**: Upload PDFs, get searchable API in 30 seconds
- **🧠 Smart Results**: Vector similarity + metadata filtering + MMR diversity  
- **🔗 Connect Everything**: HubSpot CRM, live databases, CSV files
- **🌍 Built for Scale**: Used by developers in 50+ countries
- **💰 Developer-Friendly Pricing**: Free tier + pay-per-query

## 🛠 Core Features

### 📚 Knowledge Base Management

```python
# Create a knowledge base
kb = client.create_knowledge_base(
    name="Customer Support",
    description="FAQ and help articles"
)

# Upload documents
result = client.upload_document(
    knowledge_base_id=kb['id'],
    file_path="./support_docs.pdf"
)

# List all knowledge bases
knowledge_bases = client.list_knowledge_bases()
```

### 🔍 Advanced Search

```python
# Basic search
results = client.search(
    knowledge_base_id=123,
    query="pricing plans",
    top_k=5
)

# Advanced filtering
results = client.search(
    knowledge_base_id=123,
    query="enterprise features",
    similarity_threshold=0.8,
    metadata_filters={"department": "sales"},
    use_mmr=True  # Maximum Marginal Relevance for diversity
)

# Conversational search with context
results = client.search(
    knowledge_base_id=123,
    query="What about enterprise pricing?",
    chat_history=[
        {"role": "user", "content": "Tell me about your pricing"},
        {"role": "assistant", "content": "We have three pricing tiers..."}
    ]
)
```

### 📊 Document Management

```python
# List documents
documents = client.list_documents(knowledge_base_id=123)

# Delete document
client.delete_document(document_id=456)
```

### 🗃️ Live Database Connections

```python
# Connect PostgreSQL database
db_conn = client.create_database_connection(
    knowledge_base_id=123,
    name="Production PostgreSQL",
    db_type="postgres",
    host="db.mycompany.com",
    port=5432,
    database="analytics",
    username="readonly_user",
    password="secure_password"
)

# Connect with SSH tunnel for security
secure_conn = client.create_database_connection(
    knowledge_base_id=123,
    name="Secure MySQL",
    db_type="mysql",
    host="internal-db",
    port=3306,
    database="sales",
    username="api_user", 
    password="password",
    use_ssh_tunnel=True,
    ssh_host="bastion.company.com",
    ssh_port=22,
    ssh_user="ubuntu",
    ssh_private_key="-----BEGIN RSA PRIVATE KEY-----\n..."
)

# Test connection
test_result = client.test_connection(123, db_conn['id'])
print(f"Connection status: {'✅ Working' if test_result['success'] else '❌ Failed'}")

# Query database with natural language (uses same search endpoint)
results = client.search(
    knowledge_base_id=123,
    query="How many customers signed up last month?"
)
```

### 🚀 HubSpot CRM Integration

```python
# Connect HubSpot CRM
hubspot_conn = client.create_hubspot_connection(
    knowledge_base_id=123,
    name="HubSpot CRM",
    private_app_token="pat-na1-your-private-app-token"
)

# Query HubSpot data with natural language
crm_results = client.search(
    knowledge_base_id=123,
    query="Show me deals in the proposal stage with value over $50k"
)

# Mixed queries across documents + CRM + databases
comprehensive_results = client.search(
    knowledge_base_id=123,
    query="Compare our pricing from the docs with actual deal values in HubSpot"
)

# List all connections
connections = client.list_connections(123)
for conn in connections['connections']:
    print(f"- {conn['name']} ({conn['db_type']}) - {conn['status']}")
```

## 🚀 Real-World Examples

### Customer Support Chatbot

```python
from yardee import Client

def answer_support_question(question: str) -> str:
    client = Client(api_key="sk-your-key")
    
    results = client.search(
        knowledge_base_id=123,  # Your support docs
        query=question,
        top_k=3,
        similarity_threshold=0.7
    )
    
    if not results['results']:
        return "I couldn't find relevant information. Please contact support."
    
    # Combine top results into answer
    context = "\n".join([r['content'] for r in results['results']])
    return f"Based on our documentation:\n\n{context}"

# Use it
answer = answer_support_question("How do I cancel my subscription?")
print(answer)
```

### Content Discovery API

```python
from flask import Flask, request, jsonify
from yardee import Client

app = Flask(__name__)
client = Client(api_key="sk-your-key")

@app.route('/search')
def search_content():
    query = request.args.get('q')
    
    results = client.search(
        knowledge_base_id=456,  # Your content KB
        query=query,
        top_k=10,
        use_mmr=True  # Diverse results
    )
    
    return jsonify({
        'query': query,
        'results': results['results'],
        'count': len(results['results'])
    })

if __name__ == '__main__':
    app.run()
```

### Complete Business Intelligence Setup

```python
from yardee import Client
import os

def setup_complete_intelligence_system():
    """
    Set up a complete business intelligence system with documents, 
    database, and CRM integration.
    """
    client = Client(api_key="sk-your-key")
    
    # 1. Create knowledge base
    kb = client.create_knowledge_base(
        name="Business Intelligence Hub",
        description="Complete business data: docs + database + CRM"
    )
    kb_id = kb['id']
    print(f"✅ Created knowledge base: {kb['name']}")
    
    # 2. Upload documentation
    doc_results = []
    doc_folder = "./business_docs"
    if os.path.exists(doc_folder):
        for filename in os.listdir(doc_folder):
            if filename.endswith(('.pdf', '.docx', '.txt')):
                try:
                    result = client.upload_document(kb_id, os.path.join(doc_folder, filename))
                    doc_results.append(result)
                    print(f"✅ Uploaded: {filename}")
                except Exception as e:
                    print(f"❌ Failed to upload {filename}: {e}")
    
    # 3. Connect production database
    try:
        db_conn = client.create_database_connection(
            knowledge_base_id=kb_id,
            name="Production Database",
            db_type="postgres",
            host=os.getenv("DB_HOST", "db.company.com"),
            port=5432,
            database=os.getenv("DB_NAME", "analytics"), 
            username=os.getenv("DB_USER", "readonly_user"),
            password=os.getenv("DB_PASS", "secure_password"),
            ssl_required=True
        )
        print(f"✅ Connected database: {db_conn['name']}")
        
        # Test database connection
        test_result = client.test_connection(kb_id, db_conn['id'])
        if test_result['success']:
            print("✅ Database connection verified")
        else:
            print(f"⚠️  Database test failed: {test_result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
    
    # 4. Connect HubSpot CRM
    hubspot_token = os.getenv("HUBSPOT_TOKEN")
    if hubspot_token:
        try:
            crm_conn = client.create_hubspot_connection(
                knowledge_base_id=kb_id,
                name="HubSpot CRM",
                private_app_token=hubspot_token
            )
            print(f"✅ Connected HubSpot: {crm_conn['name']}")
            
            # Test HubSpot connection  
            test_result = client.test_connection(kb_id, crm_conn['id'])
            if test_result['success']:
                print("✅ HubSpot connection verified")
            else:
                print(f"⚠️  HubSpot test failed: {test_result.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"❌ HubSpot connection failed: {e}")
    else:
        print("⚠️  No HUBSPOT_TOKEN environment variable found")
    
    # 5. Test comprehensive queries
    print("\n🧠 Testing AI queries across all data sources...")
    
    test_queries = [
        "How many customers do we have in our database?",
        "What are our top 3 selling products this quarter?", 
        "Show me recent deals over $10k from HubSpot",
        "According to our documentation, what is our refund policy?",
        "Compare actual sales numbers with our pricing strategy from the docs"
    ]
    
    for query in test_queries:
        try:
            results = client.search(kb_id, query, top_k=3)
            print(f"\n📊 Query: '{query}'")
            print(f"   Results: {len(results['results'])} found")
            
            for i, result in enumerate(results['results'][:2], 1):
                source = result.get('document_title', 'Unknown source')
                content_preview = result['content'][:100] + "..." if len(result['content']) > 100 else result['content']
                print(f"   {i}. {source}: {content_preview}")
                
        except Exception as e:
            print(f"   ❌ Query failed: {e}")
    
    # 6. Summary
    connections = client.list_connections(kb_id)
    documents = client.list_documents(kb_id)
    
    print(f"\n🎉 Setup Complete!")
    print(f"   📚 Knowledge Base ID: {kb_id}")
    print(f"   📄 Documents: {documents['count']}")
    print(f"   🔗 Connections: {len(connections.get('connections', []))}")
    print(f"   🚀 Ready for AI-powered business intelligence!")
    
    return kb_id

# Run the setup
if __name__ == "__main__":
    setup_complete_intelligence_system()
```

## 🔧 Advanced Configuration

```python
from yardee import Client

# Custom configuration
client = Client(
    api_key="sk-your-key",
    base_url="https://app.yardee.ai/api/v1",  # Custom endpoint
    timeout=60,  # Request timeout
    max_retries=5  # Retry failed requests
)

# Using context manager (auto-closes connections)
with Client(api_key="sk-your-key") as client:
    results = client.search(123, "your query")
```

## 🚨 Error Handling

```python
from yardee import Client, YardeeError, AuthenticationError, RateLimitError

client = Client(api_key="sk-your-key")

try:
    results = client.search(123, "test query")
    
except AuthenticationError:
    print("❌ Invalid API key")
    
except RateLimitError:
    print("⏳ Rate limit exceeded, please wait")
    
except YardeeError as e:
    print(f"❌ API Error: {e}")
    
except Exception as e:
    print(f"💥 Unexpected error: {e}")
```

## 📖 API Reference

### Client Class

#### `Client(api_key, base_url=None, timeout=30, max_retries=3)`

Main client class for interacting with Yardee API.

**Parameters:**
- `api_key` (str): Your Yardee API key (required)
- `base_url` (str): Custom API endpoint (optional)  
- `timeout` (int): Request timeout in seconds (default: 30)
- `max_retries` (int): Max retry attempts (default: 3)

### Search Methods

#### `search(knowledge_base_id, query, top_k=5, similarity_threshold=0.1, use_mmr=True, metadata_filters=None, chat_history=None)`

Perform semantic search across a knowledge base.

**Returns:** Dictionary with `results` list and `total_results` count.

### Knowledge Base Methods

#### `list_knowledge_bases()`
Get all knowledge bases in your account.

#### `create_knowledge_base(name, description=None)`
Create a new knowledge base.

#### `get_knowledge_base(knowledge_base_id)`
Get details of a specific knowledge base.

### Document Methods

#### `upload_document(knowledge_base_id, file_path, filename=None)`
Upload a document to a knowledge base.

#### `list_documents(knowledge_base_id)`
List all documents in a knowledge base.

#### `delete_document(document_id)`
Delete a document.

### Connection Methods

#### `create_database_connection(knowledge_base_id, name, db_type, host, port, database, username, password, **options)`
Create a live database connection (PostgreSQL, MySQL, SQL Server).

#### `create_hubspot_connection(knowledge_base_id, name, private_app_token)`
Create a HubSpot CRM connection.

#### `list_connections(knowledge_base_id)`
List all connections for a knowledge base.

#### `get_connection(knowledge_base_id, connection_id)`
Get details of a specific connection.

#### `update_connection(knowledge_base_id, connection_id, **updates)`
Update connection settings.

#### `delete_connection(knowledge_base_id, connection_id)`
Delete a connection.

#### `test_connection(knowledge_base_id, connection_id)`
Test if a connection is working.

## 🌟 What Developers Are Building

> *"Yardee turned our 500-page manual into a ChatGPT for our support team. Setup took 5 minutes."*  
> **— SaaS Startup, 50k users**

> *"We connected our CRM and now our sales team has instant access to all customer context."*  
> **— E-commerce Platform, India**

> *"The Python SDK made integration trivial. Our chatbot now answers technical questions from our docs."*  
> **— Fintech Company, Pakistan**

## 🤝 Support & Community

- **📚 [Full Documentation](https://docs.yardee.ai)**
- **📧 [Email Support](mailto:support@yardee.ai)**

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🚀 Get Started Now

1. **Get your API key**: [Sign up at app.yardee.ai](https://app.yardee.ai)
2. **Install the SDK**: `pip install yardee`
3. **Upload your first document**
4. **Start searching!**

```python
from yardee import Client

client = Client(api_key="sk-your-key")
# Your AI-powered search is ready! 🎉
```

---

Made with ❤️ by the [Yardee Team](https://yardee.ai) | Star us on [GitHub](https://github.com/yardee/yardee-python-sdk) ⭐
