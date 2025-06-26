import tempfile
import os
from vcf_processor import parse_vcf_files

def test_parse_vcf_files():
    vcf_content = """##fileformat=VCFv4.2
#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO
1\t100\t.\tA\tT\t.\t.\tANN=T|missense_variant|gene|ENST0001|gene_id|transcript|ENST000001|protein_coding|1/20|c.123A>T|...|...|...
"""
    with tempfile.TemporaryDirectory() as tmpdir: 
        test_vcf_path = os.path.join(tmpdir, "test.vcf") 
        with open(test_vcf_path, "w") as f: 
            f.write(vcf_content) 
        
        result = parse_vcf_files(tmpdir) 
        assert isinstance(result, dict) 
        # Ellenőrizzük, hogy van olyan kulcs, ami az ENST000001 transzkriptre hivatkozik 
        assert any("ENST000001" in k for k in result.keys()) 
