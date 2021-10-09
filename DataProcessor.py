import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer


class DataProcessor:
    file_path = ""
    ham = []
    spam = []
    words = []
    result = dict()

    def get_result(self) -> dict:
        return self.result

    def start_processing(self, file_path: str, words: list):
        if file_path != self.file_path or words != self.words:

            self.file_path = file_path
            self.words = words

            categories = self._load_from_file()

            for line in categories["ham"]:
                self.ham.append(self._stemming(self._remove_stopwords(self._tokenization(self._clean_str(line)))))

            for line in categories["spam"]:
                self.spam.append(self._stemming(self._remove_stopwords(self._tokenization(self._clean_str(line)))))

            ham = self._to_single_list(self.ham.copy())
            spam = self._to_single_list(self.spam.copy())

            for word in words:
                if word not in ham:
                    ham.append(self._stemming([word.lower()])[0])

                if word not in spam:
                    spam.append(self._stemming([word.lower()])[0])

            length = len(categories["ham"]) + len(categories["spam"])
            Pham = len(categories["ham"]) / length
            Pspam = len(categories["spam"]) / length

            test_message_ham = 0
            test_message_spam = 0

            for word in words:
                test_message_spam += self.get_word_count(word.lower(), spam)
                test_message_ham += self.get_word_count(word.lower(), ham)

            test_message_ham = (Pham * test_message_ham) / length
            test_message_spam = (Pspam * test_message_spam) / length

            self.result = {"ham": test_message_ham, "spam": test_message_spam}

    def get_P(self, amount: int, total_amount: int) -> float:
        return amount / total_amount

    def get_word_count(self, word: str, collection: list):
        return self._count_words(collection)[word] / len(collection)

    def _load_from_file(self) -> dict:
        _inp = pd.read_csv(self.file_path, encoding="cp1251")

        _ham = []
        for line in _inp[_inp.v1 == "ham"].values:
            _tmp = ""
            for item in line[1:]:
                if isinstance(item, str):
                    _tmp += item
            _ham.append(_tmp)

        _spam = []
        for line in _inp[_inp.v1 == "spam"].values:
            _tmp = ""
            for item in line[1:]:
                if isinstance(item, str):
                    _tmp += item
            _spam.append(_tmp)

        return {"ham": _ham, "spam": _spam}

    def _clean_str(self, _inp: str) -> str:
        _out = ""
        for char in _inp:
            if char.isalpha():
                _out += char.lower()
            else:
                _out += " "
        return _out

    def _tokenization(self, _inp: str) -> list:
        ls = []
        for word in _inp.split(" "):
            if word != "":
                ls.append(word)
        return ls

    def _remove_stopwords(self, _tokens: list) -> list:
        stops = stopwords.words("english")
        _out = [token.strip() for token in _tokens if token not in stops]
        return _out

    def _stemming(self, _inp: list) -> list:
        ps = PorterStemmer()
        arr = []
        for word in _inp:
            arr.append(ps.stem(word))
        return arr

    def _get_av(self, _inp: dict) -> int:
        all = 0
        for k, v in _inp.items():
            all += k * v
        return all / sum(_inp.values())

    def _to_single_list(self, _inp: list) -> list:
        _arr = []
        for subarr in _inp:
            _arr.extend(subarr)

        return _arr

    def _count_words(self, _inp: list) -> dict:
        """Note: need to_single_list before"""
        _dict = dict()
        for word in _inp:
            try:
                _dict[word] += 1
            except KeyError:
                _dict[word] = 1

        return _dict

    def _count_len_words(self, _inp: list) -> dict:
        """Note: need to_single_list before"""
        _dict = dict()
        for word in _inp:
            try:
                _dict[len(word)] += 1
            except KeyError:
                _dict[len(word)] = 1

        return _dict

    def _count_message_len(self, _inp: list) -> dict:
        _dict = dict()
        for message in _inp:
            try:
                _dict[len(message)] += 1
            except KeyError:
                _dict[len(message)] = 1

        return _dict

    def _normalize(self, _inp: dict) -> list:
        s = 0
        ls = []
        for k, v in _inp.items():
            s += k * v

        for i in _inp.values():
            ls.append(i / s)

        return ls

