from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Dict, Any, Optional
from .config import settings
import uuid

class VectorDB:
    def __init__(self):
        self.client = QdrantClient(
            host=settings.qdrant_host,
            port=settings.qdrant_port
        )
        self.collection_name = "educational_content"
        self._initialize_collection()
    
    def _initialize_collection(self):
        """Initialize the collection if it doesn't exist"""
        try:
            # Check if collection exists
            self.client.get_collection(self.collection_name)
        except:
            # Create collection if it doesn't exist
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=384,  # Size for sentence-transformers/all-MiniLM-L6-v2
                    distance=models.Distance.COSINE
                )
            )
    
    def add_content(self, content_id: str, content: str, vector: List[float], metadata: Dict[str, Any] = None):
        """Add educational content to the vector database"""
        if metadata is None:
            metadata = {}
            
        self.client.upsert(
            collection_name=self.collection_name,
            points=[
                models.PointStruct(
                    id=content_id,
                    vector=vector,
                    payload={
                        "content": content,
                        "metadata": metadata
                    }
                )
            ]
        )
    
    def search_content(self, query_vector: List[float], limit: int = 5) -> List[Dict[str, Any]]:
        """Search for relevant content based on the query vector"""
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=limit
        )
        
        return [
            {
                "id": result.id,
                "content": result.payload.get("content", ""),
                "metadata": result.payload.get("metadata", {}),
                "score": result.score
            }
            for result in results
        ]
    
    def get_content_by_id(self, content_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve content by its ID"""
        results = self.client.retrieve(
            collection_name=self.collection_name,
            ids=[content_id]
        )
        
        if results:
            result = results[0]
            return {
                "id": result.id,
                "content": result.payload.get("content", ""),
                "metadata": result.payload.get("metadata", {})
            }
        
        return None
    
    def update_content(self, content_id: str, content: str = None, vector: List[float] = None, metadata: Dict[str, Any] = None):
        """Update existing content in the vector database"""
        current = self.get_content_by_id(content_id)
        if not current:
            raise ValueError(f"Content with ID {content_id} not found")
        
        updated_payload = current.get("payload", {})
        if content:
            updated_payload["content"] = content
        if metadata:
            updated_payload["metadata"] = metadata
        
        self.client.upsert(
            collection_name=self.collection_name,
            points=[
                models.PointStruct(
                    id=content_id,
                    vector=vector or current.get("vector", []),
                    payload=updated_payload
                )
            ]
        )
    
    def delete_content(self, content_id: str):
        """Remove content from the vector database"""
        self.client.delete(
            collection_name=self.collection_name,
            points_selector=models.PointIdsList(
                points=[content_id]
            )
        )

# Global instance
vector_db = VectorDB()

def get_vector_db():
    """Dependency function for FastAPI"""
    return vector_db