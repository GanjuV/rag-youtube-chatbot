"""LangChain LCEL RAG chain assembly."""

from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser


def format_docs(docs: list) -> str:
    return "\n\n".join(doc.page_content for doc in docs)


def build_simple_chain(retriever):
    """Build a simple RAG chain that returns formatted context without LLM complexity."""
    
    def generate_answer(inputs):
        """Generate answer from context and question."""
        context = inputs.get("context", "")
        question = inputs.get("question", "")
        
        if not context:
            return "I couldn't find relevant information in the video to answer your question."
        
        # Simple answer construction from context
        return f"Based on the video transcript:\n\n{context[:500]}..."
    
    parallel_chain = RunnableParallel({
        "context": retriever | RunnableLambda(format_docs),
        "question": RunnablePassthrough()
    })
    
    return parallel_chain | RunnableLambda(generate_answer) | StrOutputParser()


def build_chain(retriever):
    """Build and return the full RAG chain (simplified version without LLM)."""
    return build_simple_chain(retriever)
