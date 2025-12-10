from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer
from ..vector_db import vector_db
from ..models.chapter import Chapter
from ..models.learning_step import LearningStep
from sqlalchemy.orm import Session
import json

class RAGService:
    def __init__(self):
        # Initialize the sentence transformer model for creating embeddings
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def index_educational_content(self, db: Session):
        """Index all educational content (chapters and steps) into the vector database"""
        # Get all chapters
        chapters = db.query(Chapter).all()
        
        for chapter in chapters:
            # Index chapter content
            chapter_content = f"Chapter: {chapter.title}. {chapter.description}"
            chapter_vector = self.model.encode(chapter_content).tolist()
            
            vector_db.add_content(
                content_id=f"chapter_{chapter.id}",
                content=chapter_content,
                vector=chapter_vector,
                metadata={
                    "type": "chapter",
                    "title": chapter.title,
                    "id": str(chapter.id),
                    "order_index": chapter.order_index
                }
            )
            
            # Get steps for this chapter and index them
            steps = db.query(LearningStep).filter(LearningStep.chapter_id == chapter.id).all()
            for step in steps:
                step_content = f"Step: {step.title}. {step.content}"
                step_vector = self.model.encode(step_content).tolist()
                
                vector_db.add_content(
                    content_id=f"step_{step.id}",
                    content=step_content,
                    vector=step_vector,
                    metadata={
                        "type": "step",
                        "title": step.title,
                        "chapter_id": str(chapter.id),
                        "chapter_title": chapter.title,
                        "step_order": step.order_index,
                        "id": str(step.id)
                    }
                )
    
    def query_educational_content(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search for relevant educational content based on the query"""
        # Convert the query to a vector
        query_vector = self.model.encode(query).tolist()
        
        # Search the vector database
        results = vector_db.search_content(query_vector, limit=limit)
        
        return results
    
    def get_answer_with_context(self, query: str, limit: int = 3) -> Dict[str, Any]:
        """Get an answer with relevant context from the educational content"""
        # Search for relevant content
        search_results = self.query_educational_content(query, limit)
        
        if not search_results:
            return {
                "answer": "I couldn't find relevant information in the textbook for your query.",
                "context": [],
                "references": []
            }
        
        # Create context from the search results
        context = [result["content"] for result in search_results]
        
        # Generate a response based on the context
        # In a real implementation, this would use a more sophisticated approach
        # to generate an answer based on the context
        answer = self._generate_answer(query, context)
        
        # Extract reference information
        references = [
            {
                "title": result["metadata"].get("title", "Unknown"),
                "type": result["metadata"].get("type", "Unknown"),
                "id": result["metadata"].get("id", ""),
                "score": result["score"]
            }
            for result in search_results
        ]
        
        return {
            "answer": answer,
            "context": context,
            "references": references
        }
    
    def _generate_answer(self, query: str, context: List[str]) -> str:
        """Generate an answer based on the query and context"""
        # In a full implementation, this would use a language model to generate
        # a comprehensive answer based on the context.
        # For now, we'll return a simple response indicating what was found.
        if len(context) == 1:
            return f"Based on the textbook content: {context[0][:500]}{'...' if len(context[0]) > 500 else ''}"
        else:
            return f"I found {len(context)} relevant sections in the textbook that might answer your question. The content covers topics related to your query: {query}"