import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
from nltk.tokenize import word_tokenize
import joblib


class SpamModelTrain:

    def train_model(self):
        data = pd.read_csv("./spam.csv")
        data.drop_duplicates(inplace=True)
        text = data['text']
        spam = data['spam_id']
        text_train, text_test, spam_train, spam_test = train_test_split(text, spam, test_size=0.2, random_state=42)
        # Uzbek stopwords
        uzbek_stopwords = {
            'va', 'ham', 'bilan', 'shu', 'bu', 'u', 'bir', 'siz', 'biz', 'ular',
            'nima', 'nega', 'nimaga', 'bordi', 'keldi', 'qildi', 'edi', 'edi',
            'yoki', 'bor', 'yoq', 'to', 'deb', 'buni', 'uning', 'o\'z','salom'
        }

        def preprocess_text(text):
            tokens = word_tokenize(text.lower())
            tokens = [word for word in tokens if word.isalpha() and word not in uzbek_stopwords]
            return ' '.join(tokens)

        text_train = text_train.apply(preprocess_text)
        text_test = text_test.apply(preprocess_text)

        # Vectorize text data
        cv = CountVectorizer()
        features_train = cv.fit_transform(text_train)
        features_test = cv.transform(text_test)

        model = MultinomialNB()
        model.fit(features_train, spam_train)

        spam_pred = model.predict(features_test)
        accuracy = accuracy_score(spam_test, spam_pred)
        report = classification_report(spam_test, spam_pred, zero_division=0)

        print("Accuracy:", accuracy)
        print("Classification Report:")
        print(report)

        # Save the model and the vectorizer
        joblib.dump(model, 'spam_detector_model.pkl')
        joblib.dump(cv, 'count_vectorizer.pkl')

        return model


# Example usage
if __name__ == "__main__":
    model_trainer = SpamModelTrain()
    trained_model = model_trainer.train_model()
    print(trained_model)
