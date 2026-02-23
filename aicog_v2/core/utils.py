import re

class TokenEstimator:
    """
    Simplified heuristic-based token estimator for routing decisions.
    Approximates tokens based on character count and common word patterns.
    """
    @staticmethod
    def estimate(text: str) -> int:
        if not text:
            return 0
        
        # Heuristic: ~4 characters per token for English
        char_count = len(text)
        
        # Word count heuristic
        words = re.findall(r'\w+', text)
        word_count = len(words)
        
        # Average of char-based and word-based estimates
        return max(int(char_count / 4), int(word_count * 1.3))
