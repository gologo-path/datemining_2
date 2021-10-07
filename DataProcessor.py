class DataProcessor:
    file_path = ""
    ham = []
    spam = []
    words = []
    result = dict()

    def set_file(self, file_path : str):
        if not self.file_path == file_path:
            self.file_path = file_path

    def set_word(self, words: list):
        if not self.words == words:
            self.words = words

    def get_result(self) -> dict:
        return result

    def start_processing(self):
        categories = self._load_from_file()

        for line in categories["ham"]:
            self._ham.append(self._stemming(self._remove_stopwords(self._tokenization(self._clean_str(line)))))

        for line in categories["spam"]:
            self._spam.append(self._stemming(self._remove_stopwords(self._tokenization(self._clean_str(line)))))



    def get_P(self, length: int, total_length: int) -> float:
        return length / total_length

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

