"""
Marcus Graves
Csci 191T Bioinformatics
2/1/17

Programming Assignment 1
Extract the first 500 non-redundant RefSeq gene sequences from human genome(HG38) chromosome1 and make a fasta file.

Example Output:
>chr1.11873.14409.NR_046018.+
CTTGCCGTCAGCCTTTTCTTT...

Assuming fasta format is a list of 'fasta objects' of schema:
>[chromosome name].[start position].[end position].[gene ID].[strand]
[Sequence]
"""

import csv
def find_gene(start_pos, end_pos):
    line_number_start = ((start_pos + 1) / 50)  #start line
    line_number_end = ((end_pos + 1) / 50)      #end line
    char_start = start_pos % 50                 #start char
    char_end = end_pos % 50                     #end char

    gene = content[line_number_start][char_start:] #first line of gene

    counter = line_number_start + 1                #counter to keep track of fa line. +1 because we already have first line
    while counter < line_number_end:               #middle of gene
        gene += content[counter]
        counter += 1

    gene += content[line_number_end + 1][:char_end]#end of gene

    return gene

def reverse_complement(gene): #assuming A->T, T->A, U->A, G->C, C->G via http://arep.med.harvard.edu/labgc/adnan/projects/Utilities/revcomp.html
    gene = list(gene) #convert to list because python strings are immutable
    for index, each_char in enumerate(gene):
        if each_char.upper() == "A":
            gene[index] = "T"
        elif each_char.upper() == "T":
            gene[index] = "A"
        elif each_char.upper() == "U":
            gene[index] = "A"
        elif each_char.upper() == "G":
            gene[index] = "C"
        elif each_char.upper() == "C":
            gene[index] = "G"
    return ''.join(gene) #convert back to string

#initialize counter to zero. When non-redundant RefSeq gene is found, increment by 1
counter = 0

#list containing first 500 RefSeq genes
new_list = []

with open("hg38-chr1.fa") as f:                    #opening fa file
    content = f.readlines()                        #assigning to list

#read list
with open("HG38-refseq-annot-chr1-6col") as tsv:        #opening file
    for line in csv.reader(tsv, dialect="excel-tab"):   #file is delimited by tabs
        if counter < 500:                               #Only looking for first 500
            if line not in new_list:                    #if RefSeq gene is already added, do nothing
                new_list.append(line)
                counter += 1

text_file = open("CS191T-prog1-MarcusGraves.fa", "w")
for each_gene in new_list: #for each RefSeq gene, find the sequence and add it to the fasta object
    sequence = find_gene(int(each_gene[1]), int(each_gene[2])) #find sequence
    if each_gene[5] == "-":
        sequence = reverse_complement(sequence)                #if negative, reverse complement
    fasta_object = [">%s.%s.%s.%s.%s" %(each_gene[0],
                                        each_gene[1],
                                        each_gene[2],
                                        each_gene[3],
                                        each_gene[5]), sequence]

    text_file.write(fasta_object[0])                           #label
    text_file.write("\n")
    text_file.write(fasta_object[1])                           #sequence
    text_file.write("\n")
text_file.close()
