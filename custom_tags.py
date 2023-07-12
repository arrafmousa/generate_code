import re

import nltk
import spacy
from nltk import Tree
from nltk.corpus import brown

sentence = "A solution of piperidin-4-ol (100 mg, 0.989 mmol) and 3-((phenylsulfonyl)methylene)oxetane (prepared according to a published literature procedure: Wuitschik et al. J. Med. Chem. 53(8) 3227-3246, 2010, 416 mg, 1.977 mmol) in methanol (5 mL) was heated at 50Â° C. for 20 h. Solvent was evaporated in vacuo and the crude product was purified by flash chromatography on silica gel using an automated ISCO system (40 g column, eluting with 0-8% 2 N ammonia in methanol/dichloromethane). 1-(3-((phenylsulfonyl)methyl)oxetan-3-yl)piperidin-4-ol (300 mg) was obtained as a colorless oil.  If the temperature exceed 64 degrees when heating methanol it will result in 3% decrease in the final products."


def clean_sentence(example):
    cleaned_sentence = example
    mmole_qnuatities = re.findall("(\d+\.\d* mmol)", cleaned_sentence)
    for x in mmole_qnuatities:
        cleaned_sentence = cleaned_sentence.replace(x, '')
    return cleaned_sentence


sentence = clean_sentence(sentence)


def tok_format(tok, is_quantity=False, is_unit=False):
    if is_quantity:
        return "_".join([tok.orth_, "QNTTY"])
    if is_unit:
        return "_".join([tok.orth_, "UNIT"])

    return "_".join([tok.orth_, tok.tag_])


def to_nltk_tree(node, is_quantity=False, is_unit=False):
    if node.n_lefts + node.n_rights > 0:
        if is_quantity:
            return Tree(tok_format(node, is_quantity=True),
                        [to_nltk_tree(child) for child in node.children])
        if node.text in units_list:
            return Tree(tok_format(node, is_unit=True), [to_nltk_tree(child, is_quantity=True) for child in node.children])
        return Tree(tok_format(node), [to_nltk_tree(child) for child in node.children])
    else:
        if is_quantity and node.text.isnumeric():
            return Tree(tok_format(node, is_quantity=True),
                        [to_nltk_tree(child) for child in node.children])

        return tok_format(node)


parser = spacy.load("en_core_web_sm")
doc = parser(' '.join(sentence.split()))
units_list = ['mg', 'g', 'gr', 'gram', 'grams', 'kg', 'milligrams', 'milligram', 'mmol', 'ml', 'mL', 'L', 'millilitre']

uni_tags = []
for sent in doc.sents:
    for idx, token in enumerate(sent):
        if token.text in units_list:
            uni_tags.append((token.text, 'UNT'))
        elif token.text.isnumeric() and idx < len(sent) - 1 and sent[idx + 1].text in units_list:
            uni_tags.append((token.text, 'QNTY'))
        else:
            uni_tags.append((token.text, token.tag_))

# t0 = nltk.DefaultTagger('NN')
# t1 = nltk.UnigramTagger(uni_tags, backoff=t0)

[to_nltk_tree(sent.root).pretty_print() for sent in doc.sents]

# def tag_sentence(sentence):
#     for word in se
