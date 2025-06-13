import os
from fonctions import list_of_files, lower_folder, punctuation, calcul_tf, calcul_idf, calcul_tf_idf, tokenize_question, similarite

BASE_DIR = os.path.dirname(__file__)
DIRECTORY = os.path.join(BASE_DIR, "speeches")
CLEANED = os.path.join(BASE_DIR, "cleaned")


def prepare_data():
    files = list_of_files(DIRECTORY, "txt")
    lower_folder(DIRECTORY, CLEANED, files)
    punctuation(CLEANED, files)
    tf = calcul_tf(files)
    idf = calcul_idf(tf)
    tf_idf = calcul_tf_idf(tf, idf)
    return files, tf_idf, idf


def build_vocab_matrix(tf_idf):
    vocab = sorted({word for d in tf_idf.values() for word in d})
    ordered_files = sorted(tf_idf.keys())
    matrix = []
    for name in ordered_files:
        vector = [tf_idf[name].get(word, 0) for word in vocab]
        matrix.append(vector)
    return vocab, matrix, ordered_files


def vectorize_question(question, vocab, idf_global):
    tokens = tokenize_question(question)
    tf_q = {}
    for t in tokens:
        tf_q[t] = tf_q.get(t, 0) + 1
    return [tf_q.get(w, 0) * idf_global.get(w, 0) for w in vocab]


def get_sentence_with_word(file_path, word):
    with open(file_path, "r") as f:
        content = f.read().lower()
    for sent in content.split('.'):
        if word in sent:
            return sent.strip()
    return ""


def main():
    os.chdir(BASE_DIR)
    files, tf_idf, idf = prepare_data()
    idf_global = next(iter(idf.values()))
    vocab, matrix, ordered_files = build_vocab_matrix(tf_idf)

    while True:
        question = input("Posez votre question ('exit' pour quitter): ")
        if question.lower() == 'exit':
            break
        vec_q = vectorize_question(question, vocab, idf_global)
        sims = [similarite(vec_q, v) for v in matrix]
        best_idx = sims.index(max(sims))
        best_file = ordered_files[best_idx]

        if max(vec_q) > 0:
            word = vocab[vec_q.index(max(vec_q))]
            sentence = get_sentence_with_word(os.path.join(DIRECTORY, best_file), word)
            if sentence:
                print(sentence)
                continue
        print(f"Voir le discours: {best_file}")


if __name__ == "__main__":
    main()
