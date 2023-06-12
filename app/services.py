import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


LOADED_MODELS = {}


def load_clf_and_vectorizer(lang: str) -> tuple[LogisticRegression, TfidfVectorizer]:
    if not LOADED_MODELS.get(lang):
        clf = joblib.load(f'app/classifiers/{lang}_classifier.joblib')
        vectorizer = joblib.load(f'app/classifiers/{lang}_vectorizer.joblib')
        LOADED_MODELS[lang] = (clf, vectorizer)
        print(f'loading CLF-{lang}')
        return clf, vectorizer
    return LOADED_MODELS.get(lang)


def compare_styles(phrase: str, lang: str) -> bool:
    phrase = phrase.strip()

    # load from joblib classifier and vectorizer
    clf, vectorizer = load_clf_and_vectorizer(lang)

    # Use the classifier to predict the style of new text
    new_vectorized = vectorizer.transform([phrase])
    defined_style = clf.predict(new_vectorized)[0]

    return defined_style


def get_styles_from_file(file, lang: str) -> list[tuple[str, bool]]:
    clf, vectorizer = load_clf_and_vectorizer(lang)
    results = []
    for line in file.file:
        phrase, _ = line.decode('utf-8').strip().split('|')
        phrase = phrase.strip()

        new_vectorized = vectorizer.transform([phrase])
        defined_style = clf.predict(new_vectorized)[0]
        results.append((phrase, defined_style))
    return results
