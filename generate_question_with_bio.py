import random
import json
from Bio.Seq import Seq
from Bio.SeqUtils import GC, six_frame_translations
from Bio.Blast import NCBIWWW, NCBIXML
from Bio import Entrez, SeqIO
import random
from Bio.SeqUtils.ProtParam import ProteinAnalysis
from tqdm import tqdm

def execute_code(code_str):
    try:
        # Create a namespace to hold the variables from executed code
        namespace = {}

        # Execute the code in the given namespace
        exec(code_str, namespace)

        # Retrieve the return value from the namespace
        return_value = namespace.get('result', None)

        return return_value
    except Exception as e:
        print("Error:", e)
        return "NAA"


# Generate random DNA sequence
def generate_random_dna(length=40):
    return ''.join(random.choice('ACGT') for _ in range(length))


# Generate random protein sequence
def generate_random_protein(length=22):
    return ''.join(random.choice('ACDEFGHIKLMNPQRSTVWY') for _ in range(length))


# Initialize dataset
dataset = []

# Number of entries to generate
diffrent_proteins = 250  # adjust as required

for _ in tqdm(range(diffrent_proteins)):
    dna_sequence = generate_random_dna()
    protein_sequence = generate_random_protein()

    # Sample Questions and Answers for DNA sequences
    question_1 = f"Given the DNA sequence '{dna_sequence}', which portion of the sequence has the highest GC content?"
    code_1 = f"""
from Bio.Seq import Seq
from Bio.SeqUtils import GC

dna_sequence = Seq("{dna_sequence}")
window_size = 10
highest_gc = 0
segment_start = 0
for i in range(len(dna_sequence) - window_size + 1):
    window_sequence = dna_sequence[i:i+window_size]
    current_gc = GC(window_sequence)
    if current_gc > highest_gc:
        highest_gc = current_gc
        segment_start = i
segment = dna_sequence[segment_start:segment_start+window_size]
result = segment
    """
    print("answering")
    answer_1 = execute_code(code_1)
    print(1)
    question_2 = f"Using the DNA sequence '{dna_sequence}', which potential protein sequence(s) can be derived using the three possible reading frames on the forward strand?"
    code_2 = f"""
from Bio.Seq import Seq

dna_sequence = Seq("{dna_sequence}")
protein_result = []
for frame in range(3):
    protein = dna_sequence[frame:].translate(to_stop=True)
    protein_result.append(protein)
result = protein_result
    """
    print("asnwering")
    answer_2 = execute_code(code_2)
    print(2)

    # Sample Questions and Answers for Protein sequences
    question_3 = f"For the protein sequence '{protein_sequence}', which amino acid is predicted to be the most flexible?"
    code_3 = f"""
from Bio.SeqUtils.ProtParam import ProteinAnalysis

analysis = ProteinAnalysis("{protein_sequence}")
flexibility_scores = analysis.flexibility()
most_flexible_aa = "{protein_sequence}"[flexibility_scores.index(max(flexibility_scores))]
result = most_flexible_aa
    """
    print("asnwering")
    answer_3 = execute_code(code_3)
    print(3)

#     question_4 = f"Given the protein sequence '{protein_sequence}', can you find closely related protein sequences ?"
#     code_4 = f"""
# from Bio.Blast import NCBIWWW, NCBIXML
#
# result_handle = NCBIWWW.qblast("blastp", "nr", "{protein_sequence}")
# blast_record = NCBIXML.read(result_handle)
# top_matches = [alignment.title for alignment in blast_record.alignments[:5]]
# result = top_matches
#     """
#     print("asnwering")
#     answer_4 = "4" #execute_code(code_4)
#     print(4)

    # Question 1: Most and least flexible amino acid
    question_5 = f"Given the protein sequence '{protein_sequence}', which amino acid is predicted to be the most flexible and which one is the least flexible?"
    code_5 = f"""
from Bio.SeqUtils.ProtParam import ProteinAnalysis

protein_sequence = "{protein_sequence}"
analysis = ProteinAnalysis(protein_sequence)
flexibility_scores = analysis.flexibility()

most_flexible_index = flexibility_scores.index(max(flexibility_scores))
least_flexible_index = flexibility_scores.index(min(flexibility_scores))

result = most_flexible_index , least_flexible_index
    """
    print("asnwering")
    answer_5 = execute_code(code_5)
    print(5)

    # Question 2: Segment of three amino acids with the highest average flexibility
    question_6 = f"For the protein sequence '{protein_sequence}', which segment of three consecutive amino acids has the highest average flexibility?"
    code_6 = f"""
from Bio.SeqUtils.ProtParam import ProteinAnalysis

protein_sequence = "{protein_sequence}"
analysis = ProteinAnalysis(protein_sequence)
flexibility_scores = analysis.flexibility()

highest_avg_flexibility = 0
segment_start = 0

for i in range(len(flexibility_scores) - 2):
    avg_flexibility = sum(flexibility_scores[i:i+3]) / 3
    if avg_flexibility > highest_avg_flexibility:
        highest_avg_flexibility = avg_flexibility
        segment_start = i
result = segment_start
    """
    print("answering")
    answer_6 = execute_code(code_6)
    print(6)

    # Question 3: Proportion of polar vs non-polar amino acids
    question_7 = f"Given the protein sequence '{protein_sequence}', how does the proportion of polar amino acids compare to the proportion of non-polar amino acids?"
    code_7 = f"""
from Bio.SeqUtils.ProtParam import ProteinAnalysis

protein_sequence = "{protein_sequence}"
analysis = ProteinAnalysis(protein_sequence)
aa_count = analysis.count_amino_acids()

polar_amino_acids = ['Q', 'N', 'H', 'K', 'D', 'E', 'S', 'T', 'R', 'Y']
polar_count = sum(aa_count[aa] for aa in polar_amino_acids)
non_polar_count = sum(aa_count[aa] for aa in set(aa_count.keys()) - set(polar_amino_acids))
result = polar_count / non_polar_count
    """
    print("answering")
    answer_7 = execute_code(code_7)
    print(7)

    dataset.append({
        "question": question_1,
        "code": code_1,
        "answer": str(answer_1)
    })

    dataset.append({
        "question": question_2,
        "code": code_2,
        "answer": [str(a) for a in answer_2]
    })

    dataset.append({
        "question": question_3,
        "code": code_3,
        "answer": answer_3
    })

    # dataset.append({
    #     "question": question_4,
    #     "code": code_4,
    #     "answer": answer_4
    # })

    dataset.append({
        "question": question_5,
        "code": code_5,
        "answer": answer_5
    })

    dataset.append({
        "question": question_6,
        "code": code_6,
        "answer": answer_6
    })

    dataset.append({
        "question": question_7,
        "code": code_7,
        "answer": answer_7
    })

# Now, you have a dataset with randomized DNA and protein sequences in the questions and corresponding code answers.
print(dataset)
dataset_json = json.dumps(dataset, indent=4)
with open("package_questions/bio.json", "w") as outfile:
    outfile.write(dataset_json)

print(len(dataset))