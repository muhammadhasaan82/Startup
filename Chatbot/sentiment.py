"""
LLM-based analysis for the NexGenTeck AI Chatbot.
Uses Groq LLM for all interpretation - NO hardcoded patterns.
This is a fully softcoded approach where the LLM understands intent dynamically.
"""

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from typing import Dict
import logging
import json

from config import config

logger = logging.getLogger(__name__)


class LLMAnalyzer:
    """
    Analyzes user messages using LLM - fully softcoded approach.
    No regex patterns or keyword matching - LLM interprets everything.
    """
    
    _instance = None
    _llm = None
    
    def __new__(cls):
        """Singleton pattern."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize the LLM for analysis."""
        if LLMAnalyzer._llm is None:
            logger.info("Initializing LLM analyzer")
            try:
                LLMAnalyzer._llm = ChatGroq(
                    api_key=config.GROQ_API_KEY,
                    model=config.LLM_MODEL,
                    temperature=0.1,  # Low temperature for consistent analysis
                    max_tokens=256
                )
                logger.info("LLM analyzer initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize LLM analyzer: {e}")
                LLMAnalyzer._llm = None
    
    async def analyze(self, message: str) -> Dict[str, any]:
        """
        Analyze the user message using LLM.
        The LLM determines intent, sentiment, and whether it's a greeting.
        
        Args:
            message: User message to analyze
            
        Returns:
            Dict with analysis results
        """
        if LLMAnalyzer._llm is None:
            return self._get_default_analysis()
        
        try:
            analysis_prompt = self._build_analysis_prompt(message)
            
            response = LLMAnalyzer._llm.invoke([
                SystemMessage(content=analysis_prompt),
                HumanMessage(content=f"Analyze this message: \"{message}\"")
            ])
            
            # Parse JSON response
            result = self._parse_analysis(response.content)
            logger.info(f"LLM analysis result: {result}")
            return result
            
        except Exception as e:
            logger.error(f"LLM analysis error: {e}")
            return self._get_default_analysis()
    
    def _build_analysis_prompt(self, message: str) -> str:
        """
        Build the analysis prompt for the LLM.
        The LLM will interpret the message without any hardcoded rules.
        """
        return """You are an intelligent message analyzer. Analyze the user's message and determine:

1. **is_greeting**: Is this a greeting or casual hello? (true/false)
2. **intent**: What does the user want? One of: "greeting", "question", "request", "complaint", "feedback", "general"
3. **sentiment**: The emotional tone. One of: "positive", "negative", "neutral"
4. **needs_context**: Does this message need information from our knowledge base to answer properly? (true/false)
   - Greetings and casual chat do NOT need context
   - Questions about services, pricing, etc. DO need context
5. **context_topics**: If needs_context is true, what topics should we search for? (list of keywords)

IMPORTANT: 
- You are analyzing for a business website chatbot (NexGenTeck - a tech company)
- Be intelligent about understanding what the user wants
- Do not use rigid rules - understand the intent naturally

Respond ONLY with valid JSON in this exact format:
{
    "is_greeting": true/false,
    "intent": "greeting|question|request|complaint|feedback|general",
    "sentiment": "positive|negative|neutral",
    "needs_context": true/false,
    "context_topics": ["topic1", "topic2"]
}"""
    
    def _parse_analysis(self, response: str) -> Dict[str, any]:
        """
        Parse the LLM's JSON response.
        
        Args:
            response: LLM response string
            
        Returns:
            Parsed analysis dict
        """
        try:
            # Try to extract JSON from response
            response = response.strip()
            
            # Handle markdown code blocks
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0]
            elif "```" in response:
                response = response.split("```")[1].split("```")[0]
            
            result = json.loads(response.strip())
            
            # Ensure required fields exist
            return {
                "is_greeting": result.get("is_greeting", False),
                "intent": result.get("intent", "general"),
                "sentiment": result.get("sentiment", "neutral"),
                "needs_context": result.get("needs_context", True),
                "context_topics": result.get("context_topics", []),
                "confidence": 0.9  # LLM analysis is high confidence
            }
            
        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse LLM response as JSON: {e}")
            return self._get_default_analysis()
    
    def _get_default_analysis(self) -> Dict[str, any]:
        """
        Return default analysis when LLM fails.
        Assumes it needs context to be safe.
        """
        return {
            "is_greeting": False,
            "intent": "general",
            "sentiment": "neutral",
            "needs_context": True,
            "context_topics": [],
            "confidence": 0.5
        }
    
    def should_retrieve_context(self, analysis: Dict) -> bool:
        """
        Determine if we should retrieve context - based on LLM's decision.
        
        Args:
            analysis: Result from analyze()
            
        Returns:
            True if context retrieval is needed
        """
        return analysis.get("needs_context", True)
    
    def get_search_query(self, message: str, analysis: Dict) -> str:
        """
        Build the search query for vector store.
        Uses LLM-identified topics if available.
        
        Args:
            message: Original user message
            analysis: Analysis result
            
        Returns:
            Search query string
        """
        topics = analysis.get("context_topics", [])
        
        if topics:
            # Use LLM-identified topics for better search
            return f"{message} {' '.join(topics)}"
        
        return message


# Singleton instance
llm_analyzer = LLMAnalyzer()
