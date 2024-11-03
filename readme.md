# Chunker

Creates chunks starting from MD documents using specified delimiter

<img src="https://i.ibb.co/mSTjxw1/chunker.webp" alt="Chunker Profile"/>

## Setup

If using [conda](https://docs.anaconda.com/miniconda/#miniconda):
```python
conda create -n chunker python=3.12.7
```

### 1 install dependencies

```python
pip install -r requirements.txt
```

### 2 setup environment variables

create .env file with:

```.env
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENVIRONMENT=your_pinecone_environment
OPENAI_API_KEY=your_openai_api_key
```

## Usage

Run the script from the command line:
```python
python main.py
```

## Documentation

use the following references:
- [langchain text_splitter](https://api.python.langchain.com/en/latest/character/langchain_text_splitters.character.RecursiveCharacterTextSplitter.html)
- [pinecone upsert vectors](https://docs.pinecone.io/guides/data/upsert-data)

## Credits
Made with ❤️ by [Massimo Olivieri](https://linktr.ee/maxvaega) 🪂