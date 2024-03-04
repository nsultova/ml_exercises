
def count_bigrams(text):
    bigram_occurence = {}
    for i in range(len(text) -1):
        bigram = text[i:i+2]
        if not bigram in bigram_occurence:
            bigram_occurence[bigram] = 0
        bigram_occurence[bigram] += 1
    return bigram_occurence

def find_max_occurence(text):
    max_count = 0
    max_bigram = None
    for bigram, count in count_bigrams(text).items():
        #print(bigram, count)
        if count > max_count:
            max_count = count
            max_bigram = bigram
        
    return max_bigram

class DummyTokenizer():

    def __init__(self, vocab_size=256, num_merges=3):
        self.vocab_size = vocab_size
        self.merges = num_merges
        self.vocab_map = dict([(i,chr(i)) for i in range(256)])

    def _find_next_vocab_idx(self):
        return len(self.vocab_map)
    
    def _non_terminal_symbol(self, vocab_map_idx):
        symbol_idx = vocab_map_idx - self.vocab_size
        ASCII_Z = 90
        return chr(ASCII_Z - symbol_idx) 

    def merge(self, text):
        max_bigram = find_max_occurence(text)
        next_substitution = self._non_terminal_symbol(self._find_next_vocab_idx())
        text = text.replace(max_bigram, next_substitution)
        self.vocab_map[self._find_next_vocab_idx()] = max_bigram
        return text

    def train(self, text):
        for i in range(self.merges):
            text = self.merge(text)
        return text 

    def encode(self, text):
        #return [258, 100, 258, 97, 99]
        for (idx, bigram ) in list(self.vocab_map.items())[256:]:
        #print(idx,bigram, non_terminal_symbol(idx))
            text = text.replace(bigram, self._non_terminal_symbol(idx))
        return text
    
    def decode(self, text):
        reversed_mapping = list(self.vocab_map.items())[256:]; reversed_mapping.reverse()
        for (idx, bigram ) in reversed_mapping:
            text = text.replace(self._non_terminal_symbol(idx), bigram)
        #print(idx,bigram, non_terminal_symbol(idx))
        return text


def test():
    tokenizer = DummyTokenizer()
    #print(tokenizer.vocab_map)
    #print(tokenizer._find_next_vocab_idx())
    #print(tokenizer._non_terminal_symbol(257))
    print(tokenizer.merge("xyzxyzxyz"))
    text = "aaabdaaabac"
    tokenizer.train(text) # 256 are the byte tokens, then do 3 merges
    print(tokenizer.encode(text))
    # [258, 100, 258, 97, 99]
    print(tokenizer.decode("ddddddd"))
    # aaabdaaabac
    

if __name__ == "__main__":
    test()