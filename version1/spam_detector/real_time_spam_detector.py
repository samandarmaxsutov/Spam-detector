import os
import joblib
import asyncio


class RealTimeSpamDetector:
    def __init__(self):
        current_dir = os.path.dirname(__file__)
        self.model_path = os.path.join(current_dir, 'spam_detector_model.pkl')
        self.vectorizer_path = os.path.join(current_dir, 'count_vectorizer.pkl')

        self.model = joblib.load(self.model_path)
        self.vectorizer = joblib.load(self.vectorizer_path)

    async def predict(self, message):
        loop = asyncio.get_event_loop()
        # Perform prediction in the event loop executor
        return await loop.run_in_executor(None, self._predict_proba, message)

    def _predict_proba(self, message):
        features = self.vectorizer.transform([message])
        proba = self.model.predict_proba(features)[0]
        confidence = {
            'not_spam': proba[0] * 100,
            'spam': proba[1] * 100
        }
        prediction = 'Spam xabar ❌' if proba[1] > proba[0] else 'Spam xabar emas ✅'
        return prediction, confidence

    def detect_spam(self, text):
        features = self.vectorizer.transform([text])
        proba = self.model.predict_proba(features)[0]
        confidence = {
            'not_spam': proba[0] * 100,
            'spam': proba[1] * 100
        }
        prediction = 'Spam xabar' if proba[1] > proba[0] else 'Spam xabar emas ✅'
        return prediction, confidence


if __name__ == '__main__':
    spam_detector = RealTimeSpamDetector()
    print(spam_detector.detect_spam("Salom, 1000 yutib olishingiz mumkin"))
