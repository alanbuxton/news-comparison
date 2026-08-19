# Rows commented out with "# CUT:" were removed on 2026-08-19 after scoring the
# 2026-05-28, 2026-07-05 and 2026-08-09 runs: an LLM judge rated each provider's
# returned headlines for genuine relevance, and these queries put every provider
# in the same bucket (all junk, all good, or a duplicate of another row), so they
# cost API calls and prompt budget without separating the providers. Re-check
# occasionally - a provider improving could make some of them discriminating again.

industry_location_examples = [
    {"industry": "PE Resins", "industry_context": "Elastomer, HDPE Bio, LDPE C4", "location": "US"},
    # CUT: flat: every provider 0.00-0.30, no separation
    # {"industry": "Film Distribution", "industry_context": "Movies", "location": "Midwest" },
    {"industry": "Packaging Boxes", "industry_context": "Carton Boxes, Metal Boxes, Plastic Boxes", "location": "IN" },
    {"industry": "Road Freight", "industry_context": "Flatbed Truckload, Less than Truckload (LTL), Tanker Truckings", "location": "Europe"},
    {"industry": "Film", "industry_context": "BOPP Film, BOPET, PE Film", "location": "CN" },
    # CUT: all 5 providers junk (rel 0.00-0.20); Film|CN covers the same ground and does separate them
    # {"industry": "BOPET", "industry_context": "Film", "location": "CN" },
    # CUT: flat: every provider 0.00-0.40; cited in 2 of 4 analyses
    # {"industry": "Distribution Services", "industry_context": "Distribution, Mastering, Localization", "location": "Northern America"},
    # CUT: duplicate of the Northern America variant, which separates providers more
    # {"industry": "Converter Foil", "industry_context": "Aluminium", "location": "" },
    {"industry": "Converter Foil", "industry_context": "Aluminium", "location": "Northern America" },
    # CUT: all 5 providers junk (rel 0.00-0.25) in every run
    # {"industry": "BOARD", "industry_context": "Chemi Thermo Mechanical Pulp Board, Folding Box Board, Formable Board", "location": "Eastern Asia" },
    {"industry": "CONSTRUCTION", "industry_context": "BUILDING CONSTRUCTION, ELECTRICAL INSTALLATION, HVAC INSTALLATION", "location": "Europe" },
    # CUT: flat: every provider mixed 0.40-0.67; never cited in any analysis
    # {"industry": "OIL/ FUEL", "industry_context": "BIO FUEL, DIESEL, GASOLINE OR PETROL", "location": "South-eastern Asia" },
    {"industry": "CONVERTING AND FINISHING MACHINES", "industry_context": "BLENDER EQUIPMENT, CNC MACHINING CENTERS, CONVERTING LINES/MACHINES", "location": "Southern Asia" },
    {"industry": "EXTERNAL MANUFACTURING / TOLLING", "industry_context": "ASSEMBLY SERVICES, METALIZATION SERVICES, POUCHING/BAGGING SERVICES", "location": "Northern America" },
    # CUT: all 5 providers junk (rel 0.00-0.10) in every run
    # {"industry": "CLEANING SUPPLIES", "industry_context": "CLEANING EQUIPMENT, SOAPS AND SANITIZERS CLEANING SUPPLIES, TOILET PAPER", "location": "New England" },
    {"industry": "HR SERVICES", "industry_context": "CORPORATE SOCIAL RESPONSIBILITY (CSR), EMPLOYEE HEALTH INSURANCE, FLEET MANAGEMENT", "location": "Mid Atlantic" },
    {"industry": "IT & TELECOM", "industry_context": "IT HARDWARE, IT NETWORK & TELECOM, IT SERVICES, IT SOFTWARE", "location": "Northern Africa" },
    {"industry": "LIQUIDS", "industry_context": "Adhesives, Inks, Solvents", "location": "Southern Africa" },
    {"industry": "LOGISTICS", "industry_context": "AIR FREIGHT, DELIVERY FLEET, OCEAN FREIGHT", "location": "Western Africa" },
    {"industry": "LABORATORY", "industry_context": "LAB EQUIPMENT MAINTENANCE AND REPAIR, POLYMER CHARACTERIZATION, THERMAL ANALYSIS", "location": "Africa" },
    {"industry": "PACKAGING", "industry_context": "BAGS, BOXES, CORRUGATED", "location": "Oceania" },
    {"industry": "PAPER", "industry_context": "", "location": "Northern Europe" },
    {"industry": "SOLVENTS", "industry_context": "Ethyl Acetate, Acetone, MEK", "location": ""},
    # CUT: duplicate profile of the no-location SOLVENTS row
    # {"industry": "SOLVENTS", "industry_context": "Ethyl Acetate, Acetone, MEK", "location": "Northern Europe"},
    {"industry": "PROFESSIONAL SERVICES", "industry_context": "CONSULTING, FINANCIAL SERVICES, LEGAL SERVICES", "location": "LATAM" },
    # CUT: flat: every provider mixed 0.20-0.50; cited in only 1 of 4 analyses
    # {"industry": "Cocoa, Nuts & Seeds", "industry_context": "Food Ingredients", "location": "Asia Pacific"},
    {"industry": "Cheese, Cultures, Milk Powders", "industry_context": "Food Ingredients", "location": "US"},
    {"industry": "Whey Ingredients", "industry_context": "Dairy Inputs", "location": "Northern Europe"},
    {"industry": "Molasses", "industry_context": "Sugar & Sweeteners", "location": "Oceania"},
]

company_name_examples = [
    "ExxonMobil",
    "Borouge",
    "Sigma Chemtrade",
    "HPCL Mittal Energy",
    # CUT: no provider ever finds it (rel 0.00 everywhere)
    # "L M Goes Embalagens",
    "Westrock",
    "International Paper",
    "Dine Cartonnages",
    # CUT: no provider ever finds it (name is also misspelt - Jiangyin)
    # "Jiangin Yonghe Packaging Products",
    "Fritz Foss",
    "Husky Technologies",
    # CUT: no provider ever finds it (rel 0.00 everywhere)
    # "KRC Custom Manufacturing",
    # CUT: no provider ever finds it (rel 0.00 everywhere)
    # "Braroll Acessorios Industriais",
    "Jindal Films",
    # Deliberate spelling-variant pair: same company, with and without the
    # umlaut. analyse.py detects the pair and reports per-provider overlap
    # between the two result sets (SPELLING-VARIANT CONSISTENCY), so keep both.
    "Klöckner Pentaplast",
    "Klockner Pentaplast",
    "Entertainment Partners",
    "Universal McCann",
    "Little Island Productions",
    # CUT: all 5 providers score GOOD (0.80-1.00) - the only zero-signal query in the set
    # "Commerzbank AG",
    "Linklaters",
    "CBS News",
    "Deloitte",
    "Bloomberg",
    "ALPEK POLYESTER",
    "COLES",
    "CONSTELLIUM",
    "SNOWFLAKE",
    "HAIER",
    # CUT: no provider ever finds it (rel 0.00 everywhere)
    # "AURIGA POLYMERS",
    "FLINT GROUP",
    # CUT: no provider ever finds it; never cited in any analysis
    # "ZHEJIANG KINGSAFE IMPORT",
    "ZETA TECHNICAL SERVICES",
    # CUT: 4 GOOD + Tavily; same story as ExxonMobil/Borouge/International Paper
    # "CVS PHARMACY",
    "BERKSHIRE LABELS",
    "CHEP",
    "TRICON DRY CHEMICALS",
    "RAINFOCUS",
    "GANDHAR OIL REFINERY",
    "IMPACT RETAIL",
    "REGUS BUSINESS CENTERS",
    # CUT: 4 GOOD + Tavily; same story as ExxonMobil/Borouge/International Paper
    # "SODEXO",
    "NECTAR 360 SERVICES",
    "DOMINION ENERGY",
    "LUSHA SYSTEMS",
    "MISTRAL AI SAS",
    "CHARTER NEX FILMS",
    "GREEN BAY PACKAGING",
    "ICOF EUROPE",
    # CUT: 4 GOOD + Tavily; same story as ExxonMobil/Borouge/International Paper
    # "TRANE",
    "SEERTECH SOLUTIONS",
    "NUBIZ PLASTIC",
]
