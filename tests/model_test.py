from api/application import application, FakeNewsDetector
import pytest

@pytest.mark.parametrize("input, result", [
    ("Emperor of Mars has declared war on Earth", 1),
    ("Messi leads argentina for the round of super 16", 0),
    ("LeBron James is best ever to touch a basketball", 0),
    ("Elon Musk is the president of the US$", 1)
    ])
def model_tester(input: str, result: int):
    tester = application.test_client()
    fake_news_model = FakeNewsDetector()
    prediction = fake_news_model.predict(input)
    assert result == prediction 