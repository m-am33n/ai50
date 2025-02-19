import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    linked_pages = corpus[page]
    prob_dist = dict()
    for page in linked_pages:
        prob_dist[page] = damping_factor / len(linked_pages)
    
    all_pages = set(corpus.keys())
    
    remaining_prob = 1
    if len(linked_pages) != 0:
        remaining_prob = 1 - damping_factor
    prob_to_distribute = remaining_prob / len(all_pages)
    
    # First distribute probabilities without rounding
    for page in all_pages:
        if page in prob_dist:
            prob_dist[page] += prob_to_distribute
        else:
            prob_dist[page] = prob_to_distribute

    # Ensure the sum is exactly 1 by adjusting the last value
    total = sum(prob_dist.values())
    if total != 1:
        last_page = list(prob_dist.keys())[-1]
        prob_dist[last_page] += (1 - total)
    
    # Round all probabilities to 5 decimal places
    for page in prob_dist:
        prob_dist[page] = round(prob_dist[page], 5)
    
    # Final adjustment if needed after rounding
    total = sum(prob_dist.values())
    if total != 1:
        last_page = list(prob_dist.keys())[-1]
        prob_dist[last_page] += round(1 - total, 5)

    return prob_dist



def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    page = random.choice(list(corpus.keys()))
    occurences = dict()
    occurences[page] = 1
    for i in range(n):
        page = sample(corpus, damping_factor, page)
        if page in occurences:
            occurences[page] += 1
        else:
            occurences[page] = 1

    page_ranks = dict()
    for page in occurences:
        page_ranks[page] = occurences[page] / n

    # Final adjustment if needed after rounding
    total = sum(page_ranks.values())
    if total != 1:
        last_page = list(page_ranks.keys())[-1]
        page_ranks[last_page] += round(1 - total, 5)
    return page_ranks


def sample(corpus, damping_factor, page):
    prob_dist = transition_model(corpus, page, damping_factor)

    random_factor = random.random()
    if random_factor < damping_factor:
        return random.choices(list(corpus.keys()), weights=prob_dist)[0]
    else:
        return random.choice(list(corpus.keys()))

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    """
    page_ranks = dict()
    for page in corpus.keys():
        page_ranks[page] = 1 / len(corpus.keys())

    page = random.choice(list(corpus.keys()))

    for i in range(n):
        pagerank = (1 - damping_factor) / len(corpus.keys()) + damping_factor
    """




if __name__ == "__main__":
    main()
