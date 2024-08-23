
COMPANY_SECTOR_OPTIONS = [
    "Corporates", "Financial Institutions", "Funds & Asset Management", 
    "Infrastructure & Project Finance", "Insurance", "Other"
]

COMPANY_SIZE_OPTIONS = ["Small", "Medium", "Large"]


MAPPED_RATINGS = [
    ("Aaa", 2.5),
    ("Aa", 3.5),
    ("A", 4.5),
    ("Baa", 5.5),
    ("Ba", 6.5),
    ("B", 7.5),
    ("Caa", 8.5),
    ("Ca", 9.5),
    ("C", float("inf")),
]

MAPPED_RATINGS_DICT = {rating: value for rating, value in MAPPED_RATINGS}


RATING_META = {
    "Score Range": ["≤ 2.5", "≤ 3.5", "≤ 4.5", "≤ 5.5", "≤ 6.5", "≤ 7.5", "≤ 8.5", "≤ 9.5", "> 9.5"],
    "Rating": ["Aaa", "Aa", "A", "Baa", "Ba", "B", "Caa", "Ca", "C"],
    "Rating Agencies Scale": [
        "AAA",
        "AA+, AA, AA-",
        "A+, A, A-",
        "BBB+, BBB, BBB-",
        "BB+, BB, BB-",
        "B+, B, B-",
        "CCC",
        "CC",
        "D",
    ],
    "Description": [
        "Issuers assessed Aaa are judged to have the highest intrinsic, or standalone, financial strength, and thus subject to the lowest level of credit risk absent any possibility of extraordinary support from an affiliate or a government.",
        "Issuers assessed Aa are judged to have high intrinsic, or standalone, financial strength, and thus subject to very low credit risk absent any possibility of extraordinary support from an affiliate or a government.",
        "Issuers assessed A are judged to have upper-medium-grade intrinsic, or standalone, financial strength, and thus subject to low credit risk absent any possibility of extraordinary support from an affiliate or a government.",
        "Issuers assessed Baa are judged to have medium-grade intrinsic, or standalone, financial strength, and thus subject to moderate credit risk and, as such, may possess certain speculative credit elements absent any possibility of extraordinary support from an affiliate or a government.",
        "Issuers assessed Ba are judged to have speculative intrinsic, or standalone, financial strength, and are subject to substantial credit risk absent any possibility of extraordinary support from an affiliate or a government.",
        "Issuers assessed B are judged to have speculative intrinsic, or standalone, financial strength, and are subject to high credit risk absent any possibility of extraordinary support from an affiliate or a government.",
        "Issuers assessed Caa are judged to have speculative intrinsic, or standalone, financial strength, and are subject to very high credit risk absent any possibility of extraordinary support from an affiliate or a government.",
        "Issuers assessed Ca have highly speculative intrinsic, or standalone, financial strength, and are likely to be either in, or very near, default, with some prospect for recovery of principal and interest; or, these issuers have avoided default or are expected to avoid default through the provision of extraordinary support from an affiliate or a government.",
        "Issuers assessed C are typically in default, with little prospect for recovery of principal or interest; or, these issuers are benefiting from a government or affiliate support but are likely to be liquidated over time; without support there would be little prospect for recovery of principal or interest."
    ],
    "Meaning": [
        "**Investment Grade** - Prime",
        "**Investment Grade** - High Grade",
        "**Investment Grade** - Upper Medium Grade",
        "**Investment Grade** - Lower Medium Grade",
        "**Speculative Grade** - Speculative",
        "**Speculative Grade** - Highly Speculative",
        "**Speculative Grade** - Substantial Risks",
        "**Speculative Grade** - Extremely Speculative",
        "In Default with Little Prospect for Recovery"
        ],
    "Probability of Default": ["0.00%", "0.01%", "0.10%", "0.46%", "2.31%", "7.62%", "17.86%", "50.00%", "100.00%"]
}


COLOR_MAPPING = {
    "Aaa": "#6aa84f", "Aa": "#93c47d", "A": "#b6d7a8", "Baa": "#ffd966", 
    "Ba": "#f6b26b", "B": "#e69138", "Caa": "#e06666", "Ca": "#cc0000", 
    "C": "#990000",
}