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

# Who each queried company actually is. Shown only to the judge and the row
# labeller (analyse.py), never sent to providers — they get the bare name, as a
# real caller would. Without it the judge guessed identities (it called ZETA
# TECHNICAL SERVICES "a Dubai firm" and Tricon Dry Chemicals "Indian", and
# labelled Tricon Energy, the actual parent, as a wrong entity). Names absent
# here could not be identified with confidence (checked 2026-10-26): a wrong
# profile is worse than none, because it turns correct rows into "wrong entity".
# TODO identify: Sigma Chemtrade, Fritz Foss, ZETA TECHNICAL SERVICES,
# ICOF EUROPE, IMPACT RETAIL.
company_profiles = {
    "ExxonMobil": "US oil and gas major (Exxon Mobil Corporation), Irving, Texas.",
    "Borouge": "UAE polyolefins producer, ADNOC/Borealis joint venture; includes Borouge Group International.",
    "HPCL Mittal Energy": "Indian refining and petrochemicals JV of HPCL and Mittal Energy (HMEL); Guru Gobind Singh Refinery, Bathinda.",
    "Westrock": "US paper and packaging company, merged with Smurfit Kappa in 2024 to form Smurfit Westrock.",
    "International Paper": "US paper and packaging company; acquired DS Smith in 2025.",
    "Dine Cartonnages": "Cartonnages Dine, small French corrugated-cardboard packaging maker in Ingersheim (Haut-Rhin), cartonnages-dine.fr.",
    "Husky Technologies": "Canadian maker of injection-moulding systems (PET preform and closure tooling), Bolton, Ontario.",
    "Jindal Films": "Flexible packaging films business (BOPP, BOPET, coated films) of India's Jindal Poly Films / B C Jindal Group; Jindal Poly Films news counts.",
    "Klöckner Pentaplast": "Plastic films and packaging maker (kp), Luxembourg/Germany.",
    "Klockner Pentaplast": "Plastic films and packaging maker (kp), Luxembourg/Germany.",
    "Entertainment Partners": "US payroll, residuals and production-finance services provider to the film and TV industry (EP), Burbank.",
    "Universal McCann": "UM, global media-buying agency, formerly of IPG Mediabrands (IPG acquired by Omnicom).",
    "Little Island Productions": "London-based film and TV production company (credits include Patrick Melrose).",
    "Linklaters": "Global law firm headquartered in London.",
    "CBS News": "US broadcast news division of CBS (Paramount).",
    "Deloitte": "Global professional services and audit firm.",
    "Bloomberg": "Bloomberg L.P., financial data and media company (includes Bloomberg Beta, its VC arm).",
    "ALPEK POLYESTER": "Polyester/PET business of Mexico's Alpek S.A.B. de C.V. (Alfa group); Alpek news counts.",
    "COLES": "Coles Group, Australian supermarket and liquor retailer.",
    "CONSTELLIUM": "Aluminium rolled and extruded products maker, Paris/US listed.",
    "SNOWFLAKE": "Snowflake Inc., US cloud data platform company.",
    "HAIER": "Haier Group / Haier Smart Home, Chinese household appliance maker.",
    "FLINT GROUP": "Luxembourg-based supplier of printing and packaging inks and print consumables.",
    "BERKSHIRE LABELS": "UK self-adhesive label and shrink-sleeve printer, Hungerford; part of the Asteria group.",
    "CHEP": "Pallet and container pooling company owned by Brambles; Brambles news counts.",
    "TRICON DRY CHEMICALS": "Dry chemicals / polymers trading arm of Tricon Energy, Houston; Tricon Energy news counts.",
    "RAINFOCUS": "US event-management software company (RainFocus), Utah.",
    "GANDHAR OIL REFINERY": "Gandhar Oil Refinery (India) Ltd, maker of white oils, lubricants and process oils (Divyol brand), Mumbai.",
    "REGUS BUSINESS CENTERS": "Regus, flexible office brand of IWG plc; IWG news counts.",
    "NECTAR 360 SERVICES": "Nectar360, Sainsbury's loyalty, retail-media and data subsidiary (Nectar card), UK.",
    "DOMINION ENERGY": "US electric and gas utility, Richmond, Virginia.",
    "LUSHA SYSTEMS": "Lusha, Israeli B2B contact-data and sales-intelligence company.",
    "MISTRAL AI SAS": "Mistral AI, French AI model developer, Paris.",
    "CHARTER NEX FILMS": "US plastic film manufacturer, part of Charter Next Generation (CNG); CNG news counts.",
    "GREEN BAY PACKAGING": "US paper, containerboard and corrugated packaging company, Green Bay, Wisconsin.",
    "SEERTECH SOLUTIONS": "Learning-management-system software provider (iLearning PLUS), Lakewood, Colorado.",
    "NUBIZ PLASTIC": "Nubiz Plastic (Nantong) Co., Chinese maker of dispensing pumps and sprayers for packaging.",
}

# Made-up companies: every article returned for one is a false positive by
# construction, with no judging needed. Queried like any other company; the
# analysis keeps them away from the judge and counts hits mechanically.
#
# The names are invented afresh for every run and recorded only in that run's
# queries.json. A fixed list would stop working once this repo is pushed: the
# names would then exist on the web (in this file), and a provider returning
# the GitHub page would be "right". Names are two random syllable pairs plus a
# sector suffix from this benchmark's own industries, so they look like the
# obscure manufacturers the real list is full of.
_CONTROL_ONSETS = ["Kor", "Dray", "Vel", "Trem", "Bral", "Ost", "Quen", "Mar",
                   "Fen", "Gal", "Ister", "Lom", "Prav", "Sel", "Thal", "Vor"]
# No English-word codas ("brook", "dale"): those make real firm names.
_CONTROL_CODAS = ["vessa", "quist", "ora", "eth", "anza", "isca", "ondra",
                  "ivo", "esk", "umbra", "iel", "axa"]
_CONTROL_SECTORS = ["Polymer Films", "Industrial Coatings", "Packaging",
                    "Labels", "Specialty Chemicals", "Corrugated", "Plastics",
                    "Flexible Packaging", "Resins", "Paperboard"]
CONTROL_COUNT = 3


def make_control_companies(rng, n: int = CONTROL_COUNT) -> list[str]:
    """Invent n distinct company names that clash with no real queried name."""
    real = {name.lower() for name in company_name_examples}
    names: list[str] = []
    while len(names) < n:
        name = (f"{rng.choice(_CONTROL_ONSETS)}{rng.choice(_CONTROL_CODAS)} "
                f"{rng.choice(_CONTROL_SECTORS)}")
        if name.lower() not in real and name not in names:
            names.append(name)
    return names
