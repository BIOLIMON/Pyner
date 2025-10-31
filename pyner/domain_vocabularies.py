"""
Domain-specific vocabularies for plant bioinformatics data mining.

Provides synonyms and keywords for:
- Multiple plant species
- Diverse experimental conditions (abiotic stress, biotic stress, development)
- Various experiment types (RNA-seq, genomics, epigenomics, proteomics)
- Tissue/sample types across plant organs and developmental stages
"""

# Condition/Treatment Synonyms for Plant Research
CONDITION_SYNONYMS = {
    # ===== ABIOTIC STRESS =====
    "salt_stress": ["salt stress", "salt", "NaCl", "salinity", "sodium chloride", "saline", "ionic stress"],
    "drought": ["drought", "water deficit", "water stress", "dehydration", "osmotic stress"],
    "cold": ["cold stress", "cold", "low temperature", "chilling", "freezing", "frost"],
    "heat": ["heat stress", "heat", "high temperature", "thermal stress", "elevated temperature"],
    "uv": ["UV", "UV-B", "UV-A", "ultraviolet", "UV radiation", "light stress"],
    "oxidative": ["oxidative stress", "H2O2", "hydrogen peroxide", "ROS", "reactive oxygen"],
    "heavy_metal": ["heavy metal", "cadmium", "lead", "mercury", "aluminum", "metal toxicity"],
    "flooding": ["flooding", "waterlogging", "submergence", "hypoxia", "anoxia"],
    "nutrient_deficiency": ["nutrient deficiency", "nitrogen", "phosphorus", "potassium", "iron", "starvation"],
    "ph_stress": ["pH stress", "acidic", "alkaline", "low pH", "high pH"],

    # ===== BIOTIC STRESS =====
    "pathogen": ["pathogen", "infection", "disease", "bacterial", "fungal", "viral", "infected"],
    "herbivory": ["herbivory", "insect", "pest", "aphid", "caterpillar", "feeding"],
    "elicitor": ["elicitor", "PAMP", "MAMP", "flagellin", "chitin", "immune"],

    # ===== HORMONES =====
    "auxin": ["auxin", "IAA", "indole acetic acid", "2,4-D"],
    "cytokinin": ["cytokinin", "CK", "6-BA", "kinetin"],
    "gibberellin": ["gibberellin", "GA", "GA3"],
    "abscisic_acid": ["abscisic acid", "ABA"],
    "ethylene": ["ethylene", "ACC", "ethylene treatment"],
    "jasmonic_acid": ["jasmonic acid", "JA", "jasmonate", "MeJA"],
    "salicylic_acid": ["salicylic acid", "SA", "salicylate"],
    "brassinosteroid": ["brassinosteroid", "BR", "brassinolide"],

    # ===== DEVELOPMENT =====
    "flowering": ["flowering", "floral", "flower development", "photoperiod"],
    "germination": ["germination", "seed germination", "imbibition"],
    "senescence": ["senescence", "aging", "leaf senescence"],
    "fruit_ripening": ["fruit ripening", "ripening", "maturation"],
    "root_development": ["root development", "lateral root", "root hair", "root growth"],

    # ===== TREATMENTS =====
    "chemical_treatment": ["chemical treatment", "compound", "inhibitor", "chemical"],
    "light": ["light", "dark", "photoperiod", "shade", "blue light", "red light"],
    "circadian": ["circadian", "diurnal", "clock", "rhythm"],
}

# Experiment Type Synonyms for Plant Studies
EXPERIMENT_SYNONYMS = {
    # ===== TRANSCRIPTOMICS =====
    "rna_seq": ["RNA-seq", "RNAseq", "RNA seq", "transcriptome", "transcriptomic", "transcriptomics"],
    "single_cell_rna": ["single-cell", "scRNA-seq", "single cell RNA-seq", "droplet-based", "10x Genomics"],
    "microarray": ["microarray", "gene chip", "expression array", "Affymetrix", "Agilent"],
    "small_rna": ["small RNA", "miRNA", "sRNA", "microRNA", "siRNA"],

    # ===== GENOMICS =====
    "wgs": ["whole genome sequencing", "WGS", "genome sequencing", "complete genome", "de novo"],
    "resequencing": ["resequencing", "variant calling", "SNP", "mutation", "GWAS"],
    "targeted_sequencing": ["targeted sequencing", "amplicon", "panel sequencing", "targeted"],
    "ddrad": ["ddRAD", "RAD-seq", "GBS", "genotyping by sequencing"],

    # ===== EPIGENOMICS =====
    "chip_seq": ["ChIP-seq", "ChIPseq", "ChIP seq", "chromatin immunoprecipitation"],
    "atac_seq": ["ATAC-seq", "ATACseq", "ATAC seq", "chromatin accessibility"],
    "bisulfite_seq": ["bisulfite", "WGBS", "methylation", "BS-seq", "methylome", "DNA methylation"],
    "dnase_seq": ["DNase-seq", "DNase hypersensitivity", "DHS"],
    "mnase_seq": ["MNase-seq", "nucleosome", "nucleosome positioning"],

    # ===== PROTEOMICS =====
    "proteomics": ["proteomics", "mass spectrometry", "LC-MS", "protein", "peptide", "iTRAQ", "TMT"],
    "phosphoproteomics": ["phosphoproteomics", "phosphorylation", "PTM"],

    # ===== OTHER =====
    "hi_c": ["Hi-C", "chromatin conformation", "3C", "chromosome conformation", "3D genome"],
    "clip_seq": ["CLIP-seq", "CLIP", "RNA-protein interaction", "RIP"],
    "ribosome_profiling": ["ribosome profiling", "Ribo-seq", "translation", "translat"],
    "degradome": ["degradome", "PARE", "degradome-seq"],
    "chia_pet": ["ChIA-PET", "chromatin interaction"],
}

# Plant Sample/Tissue Type Keywords
SAMPLE_TYPE_KEYWORDS = [
    # ===== VEGETATIVE ORGANS =====
    # Roots
    "root", "roots", "root tip", "lateral root", "primary root", "adventitious root",
    "root hair", "root cap", "radicle",

    # Shoots
    "shoot", "stem", "hypocotyl", "epicotyl", "internode", "node",

    # Leaves
    "leaf", "leaves", "cotyledon", "true leaf", "rosette", "blade",

    # Apical structures
    "meristem", "SAM", "shoot apical meristem", "RAM", "root apical meristem",
    "apical meristem", "cambium", "vascular cambium",

    # ===== REPRODUCTIVE ORGANS =====
    # Flowers
    "flower", "floral", "inflorescence", "bud", "floral bud",
    "petal", "sepal", "stamen", "carpel", "pistil", "anther", "stigma", "style", "ovary",

    # Seeds and fruits
    "seed", "fruit", "berry", "silique", "pod", "grain", "kernel",
    "embryo", "endosperm", "pericarp", "testa", "seed coat",

    # Pollen
    "pollen", "pollen grain", "microspore",

    # ===== TISSUES =====
    "epidermis", "cortex", "endodermis", "pericycle", "stele",
    "xylem", "phloem", "vascular tissue", "parenchyma", "mesophyll",
    "palisade", "spongy mesophyll", "guard cell", "stomata",

    # ===== CELL TYPES =====
    "protoplast", "cell culture", "suspension culture", "callus",
    "mesophyll cell", "guard cells", "trichome",

    # ===== DEVELOPMENTAL STAGES =====
    "seedling", "germinating seed", "mature plant", "flowering plant",
    "whole plant", "aerial tissue", "above ground", "below ground",

    # ===== SPECIALIZED STRUCTURES =====
    "tuber", "bulb", "rhizome", "stolon", "corm",
    "nodule", "root nodule", # for legumes

    # ===== GENERAL =====
    "mixed tissue", "pooled", "combined tissue", "whole",
]

# Model Plant Organisms
MODEL_PLANT_ORGANISMS = [
    # ===== MODEL SYSTEMS =====
    "Arabidopsis thaliana",      # Primary model plant
    "Oryza sativa",              # Rice - monocot model
    "Zea mays",                  # Maize/Corn
    "Medicago truncatula",       # Legume model
    "Brachypodium distachyon",   # Grass model

    # ===== MAJOR CROPS =====
    # Cereals
    "Triticum aestivum",         # Wheat
    "Hordeum vulgare",           # Barley
    "Sorghum bicolor",           # Sorghum
    "Setaria italica",           # Foxtail millet
    "Avena sativa",              # Oat

    # Legumes
    "Glycine max",               # Soybean
    "Phaseolus vulgaris",        # Common bean
    "Pisum sativum",             # Pea
    "Cicer arietinum",           # Chickpea
    "Lens culinaris",            # Lentil

    # Solanaceae
    "Solanum lycopersicum",      # Tomato
    "Solanum tuberosum",         # Potato
    "Capsicum annuum",           # Pepper
    "Nicotiana tabacum",         # Tobacco
    "Nicotiana benthamiana",     # Benthamiana (research)

    # Brassicaceae
    "Brassica napus",            # Rapeseed/Canola
    "Brassica oleracea",         # Cabbage/Broccoli
    "Brassica rapa",             # Turnip

    # ===== FRUITS =====
    "Vitis vinifera",            # Grape
    "Malus domestica",           # Apple
    "Prunus persica",            # Peach
    "Fragaria vesca",            # Strawberry
    "Citrus sinensis",           # Orange
    "Musa acuminata",            # Banana

    # ===== TREES =====
    "Populus trichocarpa",       # Poplar
    "Eucalyptus grandis",        # Eucalyptus
    "Pinus taeda",               # Loblolly pine

    # ===== VEGETABLES =====
    "Cucumis sativus",           # Cucumber
    "Cucurbita pepo",            # Zucchini/Squash
    "Lactuca sativa",            # Lettuce
    "Spinacia oleracea",         # Spinach
    "Daucus carota",             # Carrot

    # ===== ENERGY CROPS =====
    "Saccharum officinarum",     # Sugarcane
    "Panicum virgatum",          # Switchgrass

    # ===== FIBER CROPS =====
    "Gossypium hirsutum",        # Cotton
    "Cannabis sativa",           # Hemp

    # ===== ALGAE (often included in plant studies) =====
    "Chlamydomonas reinhardtii", # Green algae model
]

# Quality Assessment Keywords for Plant Studies
QUALITY_KEYWORDS = {
    "general": [
        "response", "expression", "analysis", "study", "effect",
        "regulation", "function", "mechanism", "pathway", "role",
        "identification", "characterization", "profiling"
    ],

    "plant_specific": [
        # Development and morphology
        "development", "morphology", "growth", "differentiation",
        "flowering", "germination", "senescence", "ripening",

        # Stress responses
        "stress", "tolerance", "resistance", "adaptation",
        "abiotic", "biotic", "defense", "immunity",

        # Plant structures
        "tissue", "organ", "root", "leaf", "shoot", "stem",
        "flower", "seed", "fruit", "meristem",

        # Molecular processes
        "transcriptome", "genome", "proteome", "metabolome",
        "gene expression", "transcript", "protein", "metabolite",
        "epigenetic", "chromatin", "methylation",

        # Physiology
        "photosynthesis", "respiration", "transpiration",
        "nutrient", "hormone", "signaling", "transport"
    ],
}

# Methodological Keywords for Description Quality
METHOD_KEYWORDS = {
    # Transcriptomics
    "rna_seq": ["RNA", "sequencing", "library", "reads", "transcript", "cDNA", "RNA-seq"],
    "single_cell_rna": ["single-cell", "scRNA", "droplet", "10x", "cell type"],
    "microarray": ["microarray", "hybridization", "probe", "Affymetrix", "Agilent"],
    "small_rna": ["small RNA", "miRNA", "microRNA", "sRNA", "siRNA"],

    # Genomics
    "wgs": ["genome", "variant", "SNP", "mutation", "coverage", "assembly", "sequencing"],
    "resequencing": ["resequencing", "variant calling", "genotype", "polymorphism"],
    "targeted_sequencing": ["amplicon", "targeted", "panel", "capture"],
    "ddrad": ["RAD-seq", "GBS", "ddRAD", "restriction site"],

    # Epigenomics
    "chip_seq": ["ChIP", "binding", "peak", "chromatin", "histone", "antibody", "ChIP-seq"],
    "atac_seq": ["ATAC", "accessibility", "open chromatin", "transposase"],
    "bisulfite_seq": ["bisulfite", "methylation", "WGBS", "CpG", "5mC", "BS-seq"],
    "dnase_seq": ["DNase", "hypersensitivity", "DHS"],
    "mnase_seq": ["MNase", "nucleosome", "positioning"],

    # Proteomics
    "proteomics": ["protein", "peptide", "mass spec", "LC-MS", "tandem mass", "proteome"],
    "phosphoproteomics": ["phosphorylation", "phosphopeptide", "PTM", "kinase"],

    # Other specialized methods
    "hi_c": ["Hi-C", "chromosome conformation", "3D genome", "contact map"],
    "clip_seq": ["CLIP", "RNA-binding protein", "RBP", "crosslinking"],
    "ribosome_profiling": ["ribosome profiling", "Ribo-seq", "translation", "footprint"],
    "degradome": ["degradome", "PARE", "cleavage site"],

    # General experimental keywords
    "general": ["sample", "replicate", "condition", "treatment", "control", "analysis",
                "biological replicate", "technical replicate", "time course", "dose response"]
}


def get_all_sample_keywords() -> list:
    """Get all plant sample/tissue keywords."""
    return SAMPLE_TYPE_KEYWORDS.copy()


def detect_domain_from_organism(organism: str) -> str:
    """
    Detect if organism is a known plant species.

    Args:
        organism: Scientific name of organism

    Returns:
        'plant' if recognized plant organism, 'unknown' otherwise
    """
    organism_lower = organism.lower()

    # Check against known plant organisms
    for plant_org in MODEL_PLANT_ORGANISMS:
        if plant_org.lower() in organism_lower:
            return "plant"

    # Generic plant family/genus checks
    plant_indicators = [
        # Model plants
        "arabidopsis", "oryza", "zea", "medicago", "brachypodium",
        # Crops
        "triticum", "hordeum", "sorghum", "glycine", "phaseolus",
        "solanum", "capsicum", "nicotiana", "brassica",
        # Fruits
        "vitis", "malus", "prunus", "fragaria", "citrus", "musa",
        # Trees
        "populus", "eucalyptus", "pinus",
        # General plant indicators
        "gossypium", "saccharum", "panicum", "cannabis",
        "cucumis", "cucurbita", "lactuca", "spinacia", "daucus",
        # Algae
        "chlamydomonas",
    ]

    if any(indicator in organism_lower for indicator in plant_indicators):
        return "plant"

    return "unknown"


def get_domain_sample_keywords(domain: str = "plant") -> list:
    """
    Get plant sample/tissue keywords.

    Args:
        domain: Domain type (currently only 'plant' is supported)

    Returns:
        List of plant tissue/sample keywords
    """
    # Always return plant keywords (this package is plant-focused)
    return get_all_sample_keywords()
