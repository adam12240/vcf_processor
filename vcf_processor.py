import argparse
import glob
import logging
import os
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def is_valid_snv(ref, alt):
    return len(ref) == 1 and len(alt) == 1 and ',' not in alt

def parse_vcf_files(vcf_dir):
    if not os.path.isdir(vcf_dir):
        raise NotADirectoryError(f"A megadott könyvtár nem létezik: {vcf_dir}")

    vcf_files = glob.glob(f"{vcf_dir}/*.vcf")
    if not vcf_files:
        raise FileNotFoundError(f"Nincs VCF fájl a könyvtárban: {vcf_dir}")

    dictoutputs = {}

    for filename in vcf_files:
        logging.info(f"Feldolgozás: {filename}")
        try:
            with open(filename, 'r', encoding='utf-8', errors='ignore') as file:
                for line in file:
                    if line.startswith('#'):
                        continue
                    parts = line.strip().split('\t')
                    if len(parts) < 8:
                        logging.warning(f"Rossz formátumú sor: {line.strip()}")
                        continue
                    ref = parts[3] # referencia bázis
                    alt = parts[4] # alternatív bázis
                    if is_valid_snv(ref, alt): # ellenőrizzük, hogy SNV-e
                        info = parts[7] # INFO mező 
                        info_parts = info.split(';') 
                        for part in info_parts: 
                            if part.startswith('ANN='): 
                                ann_info = part[4:] # ANN annotációk
                                ann_entries = ann_info.split(',') 
                                for ann in ann_entries: 
                                    ann_parts = ann.split('|') 
                                    if len(ann_parts) > 9: 
                                        output = f"{ann_parts[6]};{ann_parts[9]};{ann_parts[1]}" # transzkript, HGVS.C, variáns típus
                                        dictoutputs[output] = dictoutputs.get(output, 0) + 1 
        except Exception as e:
            logging.error(f"Hiba a fájl olvasása közben: {e}")

    return dictoutputs

def write_output(output_file, dictoutputs): 
    with open(output_file, "w", encoding='utf-8') as outfile: 
        outfile.write("TRANSCRIPT;HGVS.C;VARIANT_TYPE;TOTAL_COUNT\n") 
        for key, count in dictoutputs.items(): 
            outfile.write(f"{key};{count}\n") 

def main():
    parser = argparse.ArgumentParser(description="VCF fájlok feldolgozása") 
    parser.add_argument("vcf_dir", help="A VCF fájlokat tartalmazó könyvtár") 
    parser.add_argument("output_file", help="Az eredmények kimeneti fájlja") 
    args = parser.parse_args() 

    try:
        dictoutputs = parse_vcf_files(args.vcf_dir) 
    except Exception as e:
        logging.error(e)
        sys.exit(1)

    logging.info(f"Összes kulcs: {len(dictoutputs)}")
    for key, count in list(dictoutputs.items())[:10]:
        logging.info(f"{key}: {count}") 

    write_output(args.output_file, dictoutputs) 

if __name__ == "__main__": 
    main()
