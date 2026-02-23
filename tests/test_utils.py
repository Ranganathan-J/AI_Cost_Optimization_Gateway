from aicog_v2.core.utils import TokenEstimator

def test_estimate_empty():
    assert TokenEstimator.estimate("") == 0

def test_estimate_short_sentence():
    # "Hello world" is 11 chars, 2 words
    # int(11/4) = 2, int(2*1.3) = 2 -> 2
    assert TokenEstimator.estimate("Hello world") >= 2

def test_estimate_longer_text():
    text = "This is a longer sentence intended to test the token estimation logic."
    estimate = TokenEstimator.estimate(text)
    assert estimate > 5
    assert isinstance(estimate, int)
