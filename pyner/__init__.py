"""
Pyner: PRISMA-compliant bioinformatics data mining tool.

A systematic approach to mining NCBI databases (BioProject, SRA, GEO, PubMed)
for plant transcriptomics research with full PRISMA compliance.
"""

__version__ = "0.1.0"
__author__ = "Your Lab"
__email__ = "contact@lab.org"

from .core import DataMiner
from .config import Config
from . import prisma

__all__ = ['DataMiner', 'Config', 'prisma']
