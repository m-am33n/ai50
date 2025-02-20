import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    zero_gene = []
    dont_have_trait = []

    for person in people:
        if person not in one_gene and person not in two_genes:
            zero_gene.append(person)
        if person not in have_trait:
            dont_have_trait.append(person)
    
    total_prob = 1
    for person in people:
        if people[person]["mother"] is None and people[person]["father"] is None:
            total_prob *= getTraitProbabilityForNonChild(people, person, one_gene, two_genes, have_trait, zero_gene)
        else:
            total_prob *= getTraitProbabilityForChild(people, person, one_gene, two_genes, have_trait, zero_gene)
    
    return total_prob

def getTraitProbabilityForNonChild(people, person, one_gene, two_genes, have_trait, zero_gene):
    prob_gene = 1
    num_genes = 0
    if person in zero_gene:
        prob_gene = PROBS["gene"][0]
        num_genes = 0
    if person in one_gene:
        prob_gene = PROBS["gene"][1]
        num_genes = 1
    if person in two_genes:
        prob_gene = PROBS["gene"][2]
        num_genes = 2
    
    prob_trait = 1
    if person in have_trait:
        prob_trait = PROBS["trait"][num_genes][True]
    else:
        prob_trait = PROBS["trait"][num_genes][False]

    return prob_gene * prob_trait

def getTraitProbabilityForChild(people, person, one_gene, two_genes, have_trait, zero_gene):
    mother = people[person]["mother"]
    father = people[person]["father"]

    prob_gene = 1
    if mother in zero_gene:
        mother_inherited_gene = PROBS["mutation"]
    else:
        mother_inherited_gene = 1 - PROBS["mutation"]
        
    if father in zero_gene:
        father_inherited_gene = PROBS["mutation"]
    else:
        father_inherited_gene = 1 - PROBS["mutation"]

    if person in zero_gene:
        num_genes = 0
        prob_gene = (1- mother_inherited_gene) * (1- father_inherited_gene)
    if person in one_gene:
        num_genes = 1
        prob_gene = mother_inherited_gene * (1- father_inherited_gene) + father_inherited_gene * (1- mother_inherited_gene)
    if person in two_genes:
        num_genes = 2
        prob_gene = mother_inherited_gene * father_inherited_gene
        
    want_trait = person in have_trait
    prob_trait = PROBS["trait"][num_genes][want_trait]
            
    return prob_gene * prob_trait

def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        # Update gene probabilities
        if person in two_genes:
            probabilities[person]["gene"][2] += p
        elif person in one_gene:
            probabilities[person]["gene"][1] += p
        else:
            probabilities[person]["gene"][0] += p
            
        # Update trait probabilities
        probabilities[person]["trait"][person in have_trait] += p

def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        normalize = 0
        sum_gene_probabilities = sum(probabilities[person]["gene"].values())
        sum_trait_probabilities = sum(probabilities[person]["trait"].values())
        for gene_count in probabilities[person]["gene"]:
            probabilities[person]["gene"][gene_count] /= sum_gene_probabilities
        for want_trait in probabilities[person]["trait"]:
            probabilities[person]["trait"][want_trait] /= sum_trait_probabilities

    total_gene_probability = sum(probabilities[person]["gene"].values())
    if total_gene_probability != 1:
        last_gene = list(probabilities[person]["gene"].keys())[-1]
        probabilities[person]["gene"][last_gene] += round(1 - total_gene_probability, 5)
        
    total_trait_probability = sum(probabilities[person]["trait"].values())
    if total_trait_probability != 1:
        last_trait = list(probabilities[person]["trait"].keys())[-1]
        probabilities[person]["trait"][last_trait] += round(1 - total_trait_probability, 5)
        
    

if __name__ == "__main__":
    main()
