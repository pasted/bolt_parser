"""
Main entry point for the Bolt-LMM parser script.
"""
from pprint import pprint
import argparse, csv, string

class BoltLmm(object):
   def __init__(self, row):
      self.snp = row['SNP']
      self.chromosme = row['CHR']
      self.coordinate = row['BP']
      self.genpos = row['GENPOS']
      self.allele0 = row['ALLELE0']
      self.allele1 = row['ALLELE1']
      self.a1_freq = row['A1FREQ']
      self.info = row['INFO']
      self.chisq_linreg = row['CHISQ_LINREG']
      self.p_linreg = row['P_LINREG']
      self.beta = row['BETA']
      self.se = row['SE']
      self.chisq_bolt_lmm_inf = row['CHISQ_BOLT_LMM_INF']
      self.p_bolt_lmm_inf = row['P_BOLT_LMM_INF']
      self.p_bolt_lmm = row['P_BOLT_LMM']

class Phenoscanner(object):
   def __init__(self, row):
      self.snp = row['SNP']
      self.rsid = row['rsID']
      self.position = row['Pos (hg19)']
      self.alleles = row['Alleles']
      self.trait = row['Trait']
      self.study = row['Study']
      self.pmid = row['PMID']
      self.year_of_publication = row['Year of Publication']
      self.ancestry = row['Ancestry']
      self.source = row['Source']
      self.effect_allele = row['Effect Allele']
      self.association_alleles = row['Association Alleles']
      self.eaf = row['EAF']
      self.maf = row['MAF']
      self.beta = row['Beta']
      self.se = row['SE']
      self.p = row['P']
      self.direction = row['Direction']
      self.p_het = row['P Het']
      self.n = row['N']
      self.n_cases = row['N Cases']
      self.n_controls = row['N Controls']
      self.n_studies = row['N Studies']
      self.unit = row['Unit']

      try:
         tmp_str = self.position.strip('chr').split(':')
         self.chromosome = tmp_str[0]
         self.coordinate = tmp_str[1]
      except ValueError:
         print("Error in assigning Chromosome and Coordinate from Position data.")
         raise
      except:
         print(sys.exc_info()[0])
         raise
      

class BoltParser(object):
   '''Bolt-LMM parser'''
   def read_bolt(self, file_path, storage):
      """
      Reads in Bolt-LMM text file
      Args:
         file_path (str): Given filepath to Bolt-LMM file
      Returns:
         storage : A Storage object with a List of BoltLmm objects
      """
      
      with open(file_path) as bolt_file:
         tsv_reader = csv.DictReader(bolt_file, delimiter="\t")
         for row in tsv_reader:
            this_bolt_lmm = BoltLmm(row)
            storage.bolt_store.append(this_bolt_lmm)
      return storage

class PhenoscannerParser(object):
   '''Phenoscanner parser'''
   def read_ps(self, file_path, storage):
      """
      Reads in PhenoScanner GWAS text file
      Args:
         file_path (str): Geiven filepath to Phenoscanner GWAS results file
      Returns:
         storage : A Storage object with List of Phenoscanner objects
      """
      with open(file_path) as ps_file:
         tsv_reader = csv.DictReader(ps_file, delimiter="\t")
         for row in tsv_reader:
            this_ps = Phenoscanner(row)
            storage.ps_store.append(this_ps)
      return storage

class Storage(object):
   '''Storage class with merge methods'''
   def __init__(self):
      self.bolt_store = []
      self.ps_store = []

   def phenoscanner_to_bolt(self):
      """
      Links Phenoscanner results to the relevant Bolt-LMM object
      """
      
      

class Main(object):
   '''Main class'''
   def __init__(self):
      args = []
      parser = argparse.ArgumentParser(description='Bolt-LMM parser')
      parser.add_argument('-b', '--bolt_path', dest='bolt_path',
                            help='Bolt-LMM file to be parsed')
      parser.add_argument('-p', '--ps_path', dest='ps_path',
                            help='Phenoscanner file to be merged')
      parser.add_argument('--test')
      args = parser.parse_args()
      bolt_reader = BoltParser()
      ps_reader = PhenoscannerParser()
      storage = Storage()
      
      storage = bolt_reader.read_bolt(args.bolt_path, storage)
      storage = ps_reader.read_ps(args.ps_path, storage)
      print(len(storage.bolt_store))
      print(len(storage.ps_store))

if __name__ == '__main__':
   Main()
