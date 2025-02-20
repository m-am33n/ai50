import heredity

people = {
  'Harry': {'name': 'Harry', 'mother': 'Lily', 'father': 'James', 'trait': None},
  'James': {'name': 'James', 'mother': None, 'father': None, 'trait': True},
  'Lily': {'name': 'Lily', 'mother': None, 'father': None, 'trait': False}
}

one_gene = set(["Harry"])
two_genes = set(["James"])
have_trait = set(["James"])

print(heredity.joint_probability(people, one_gene, two_genes, have_trait))