# Yardee Python SDK Examples

This directory contains practical examples showing how to use the Yardee Python SDK.

## 🚀 Getting Started

1. **Install the SDK**: `pip install yardee`
2. **Get your API key**: https://app.yardee.ai/settings
3. **Run examples**: `python quickstart.py`

## 📁 Examples

### [`quickstart.py`](./quickstart.py)
**Complete beginner-friendly walkthrough** that covers:
- ✅ Client setup and authentication
- 📚 Creating and managing knowledge bases
- 📄 Document operations
- 🔍 Search functionality (basic and advanced)
- 🔗 Database and HubSpot connections
- 🛡️ Error handling

**Perfect for**: First-time users, learning the basics

### [`basic_usage.py`](./basic_usage.py) 
**Essential operations** in minimal code:
- Client initialization
- Knowledge base creation
- Document upload
- Simple search

**Perfect for**: Quick integration, copy-paste snippets

### [`advanced_features.py`](./advanced_features.py)
**Advanced SDK capabilities**:
- Advanced search with filters
- Database connections (PostgreSQL, MySQL, SQL Server)
- HubSpot CRM integration
- Batch operations
- Connection management

**Perfect for**: Production applications, complex integrations

## 🔧 Setup

### Environment Variables (Recommended)
```bash
export YARDEE_API_KEY="sk-your-api-key-here"
export HUBSPOT_PRIVATE_APP_TOKEN="your-hubspot-token" # Optional
```

### Direct API Key
Replace `"sk-your-api-key-here"` in the example files.

## 🏃‍♂️ Quick Run

```bash
# Install SDK
pip install yardee

# Set your API key
export YARDEE_API_KEY="sk-your-api-key-here"

# Run the quickstart
python examples/quickstart.py

# Try basic usage
python examples/basic_usage.py
```

## 📚 Key Concepts

### Knowledge Bases
Central containers for your documents and data connections. Create separate knowledge bases for different projects or data domains.

### Documents & Chunks
Upload documents (PDF, TXT, DOCX) which get automatically chunked and vectorized for semantic search.

### Connections
Integrate live data sources:
- **Databases**: PostgreSQL, MySQL, SQL Server
- **CRM**: HubSpot (contacts, deals, companies)
- Query them all through the same search interface!

### Search Methods
- **Basic Search**: Simple query against your knowledge base
- **Advanced Search**: With filters, MMR, similarity thresholds
- **Cross-Connection**: Search across documents AND live database data

## 🔗 Resources

- **📖 Full Documentation**: [GitHub Repository](https://github.com/findmyoptions/yardee-python-sdk)
- **🌐 Get API Key**: [Yardee Dashboard](https://app.yardee.ai)
- **📦 PyPI Package**: [yardee](https://pypi.org/project/yardee/)
- **🐛 Issues & Support**: [GitHub Issues](https://github.com/findmyoptions/yardee-python-sdk/issues)

## 🆘 Need Help?

1. **Check the quickstart example** - Covers most common scenarios
2. **Review error messages** - SDK provides detailed error information
3. **Verify API key** - Must start with `sk-` and be from app.yardee.ai
4. **Check network connection** - SDK requires internet access
5. **Open an issue** - We're here to help!

Happy coding! 🎉