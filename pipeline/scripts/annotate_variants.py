import sys
import vcf
import requests
import pandas as pd

VCF_FILE = sys.argv[1]
OUTPUT_TSV = sys.argv[2]

VEP_API = "https://rest.ensembl.org/vep/human/region/"


def parse_info(info_str):
    """Parsa o campo INFO do VCF para um dicionário."""
    return dict(item.split("=") for item in info_str.split(";") if "=" in item)


def annotate_variant(chrom, pos, ref, alt):
    """Consulta a API do Ensembl VEP para anotar uma variante."""
    variant = f"{chrom}:{pos}:{ref}:{alt}"
    url = f"{VEP_API}{variant}?content-type=application/json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None


# Ler o VCF
reader = vcf.Reader(open(VCF_FILE, "r"))
rows = []

for record in reader:
    chrom = record.CHROM
    pos = record.POS
    ref = record.REF
    alts = [str(alt) for alt in record.ALT]
    qual = record.QUAL
    filter_status = record.FILTER
    info = parse_info(record.INFO)

    dp = info.get("DP", None)
    af = info.get("AF", None)
    ac = info.get("AC", None)

    for alt in alts:
        vep_data = annotate_variant(chrom, pos, ref, alt)
        gene = vep_data[0]["transcript_consequences"][0]["gene_symbol"] if vep_data else None
        rsid = vep_data[0]["colocated_variants"][0]["id"] if vep_data else None

        rows.append({
            "CHROM": chrom,
            "POS": pos,
            "REF": ref,
            "ALT": alt,
            "QUAL": qual,
            "FILTER": filter_status,
            "AC": ac,
            "AF": af,
            "DP": dp,
            "GENE": gene,
            "RSID": rsid,
        })

df = pd.DataFrame(rows)
df.to_csv(OUTPUT_TSV, sep="\t", index=False)
