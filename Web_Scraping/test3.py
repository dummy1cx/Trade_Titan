from sec_api import PdfGeneratorApi
import os

# api key for sec
API_KEY = "xxxxxxxxxxxx"
pdf_api = PdfGeneratorApi(API_KEY)

# Folder to store PDFs
os.makedirs("10K_PDFs", exist_ok=True)

# list of all the top comapnies
companies = [
    {"name": "AIG", "url": "https://www.sec.gov/Archives/edgar/data/1288776/000119312516520367/d133613d10ka.htm"},
    {"name": "Walmart", "url": "https://www.sec.gov/ix?doc=/Archives/edgar/data/0000104169/000010416925000021/wmt-20250131.htm"},
    {"name": "Berkshire Hathaway", "url": "https://www.sec.gov/ix?doc=/Archives/edgar/data/71180/000108131625000004/bhe-20241231.htm"},
    {"name": "UnitedHealth Group", "url": "https://www.sec.gov/ix?doc=/Archives/edgar/data/731766/000073176625000063/unh-20241231.htm"},
    {"name": "CVS Health", "url": "https://www.sec.gov/ix?doc=/Archives/edgar/data/64803/000006480325000007/cvs-20241231.htm"},
    {"name": "ExxonMobil", "url": "https://www.sec.gov/ix?doc=/Archives/edgar/data/34088/000003408825000010/xom-20241231.htm"},
    {"name": "Alphabet", "url": "https://www.sec.gov/ix?doc=/Archives/edgar/data/1652044/000165204425000014/goog-20241231.htm"},
    {"name": "Costco", "url": "https://www.sec.gov/ix?doc=/Archives/edgar/data/909832/000090983224000049/cost-20240901.htm"},
    {"name": "AutoZone", "url": "https://www.sec.gov/ix?doc=/Archives/edgar/data/866787/000155837024013758/azo-20240831x10k.htm"},
    {"name": "Microsoft", "url": "https://www.sec.gov/ix?doc=/Archives/edgar/data/789019/000095017025100235/msft-20250630.htm"},
    {"name": "Charles Schwab", "url": "https://www.sec.gov/ix?doc=/Archives/edgar/data/316709/000031670925000010/schw-20241231.htm"},
    {"name": "Bank of America", "url": "https://www.sec.gov/Archives/edgar/data/1102778/000107178703000385/boa9910_10k2002.txt"},
    {"name": "General Motors", "url": "https://www.sec.gov/ix?doc=/Archives/edgar/data/1467858/000146785825000032/gm-20241231.htm"},
    {"name": "Ford", "url": "https://www.sec.gov/ix?doc=/Archives/edgar/data/37996/000003799625000013/f-20241231.htm"},
    {"name": "Meta Platforms", "url": "https://www.sec.gov/ix?doc=/Archives/edgar/data/1326801/000132680125000017/meta-20241231.htm"},
    {"name": "Wells Fargo", "url": "https://www.sec.gov/ix?doc=/Archives/edgar/data/72971/000007297125000066/wfc-20241231.htm"},
    {"name": "IBM", "url": "https://www.sec.gov/ix?doc=/Archives/edgar/data/51143/000005114325000015/ibm-20241231.htm"},
    {"name": "Johnson & Johnson", "url": "https://www.sec.gov/ix?doc=/Archives/edgar/data/200406/000020040625000038/jnj-20241229.htm"},
    {"name": "Intel", "url": "https://www.sec.gov/ix?doc=/Archives/edgar/data/50863/000005086325000009/intc-20241228.htm"},
    {"name": "Community Health Systems", "url": "https://www.sec.gov/ix?doc=/Archives/edgar/data/1108109/000095017025023242/cyh-20241231.htm"},
    {"name": "PepsiCo", "url": "https://www.sec.gov/ix?doc=/Archives/edgar/data/77476/000007747625000007/pep-20241228.htm"},
    {"name": "Abbott Laboratories", "url": "https://www.sec.gov/ix?doc=/Archives/edgar/data/1800/000162828025007110/abt-20241231.htm"},
    {"name": "Tesla", "url": "https://www.sec.gov/ix?doc=/Archives/edgar/data/1318605/000110465925042659/tm252787d2_10ka.htm"},
    {"name": "Pfizer", "url": "https://www.sec.gov/ix?doc=/Archives/edgar/data/78003/000007800325000054/pfe-20241231.htm"},
    {"name": "AT&T", "url": "https://www.sec.gov/ix?doc=/Archives/edgar/data/732717/000073271725000013/t-20241231.htm"},
    {"name": "Comcast", "url": "https://www.sec.gov/ix?doc=/Archives/edgar/data/1166691/000116669125000011/cmcsa-20241231.htm"},
    {"name": "Oracle", "url": "https://www.sec.gov/ix?doc=/Archives/edgar/data/1341439/000095017025087926/orcl-20250531.htm"},
    {"name": "Salesforce", "url": "https://www.sec.gov/ix?doc=/Archives/edgar/data/1108524/000110852425000006/crm-20250131.htm"},
    {"name": "Qualcomm", "url": "https://www.sec.gov/ix?doc=/Archives/edgar/data/804328/000080432824000075/qcom-20240929.htm"},
    {"name": "General Electric", "url": "https://www.sec.gov/ix?doc=/Archives/edgar/data/40545/000004054525000015/ge-20241231.htm"},
    {"name": "3M", "url": "https://www.sec.gov/ix?doc=/Archives/edgar/data/66740/000006674025000006/mmm-20241231.htm"},
]

# download and convert it to pdf format
for company in companies:
    name = company["name"].replace(" ", "_")
    url = company["url"]
    output_path = f"10K_PDFs/{name}_10K.pdf"

    try:
        print(f"Converting {name} ...")
        pdf_bytes = pdf_api.get_pdf(url)
        with open(output_path, "wb") as f:
            f.write(pdf_bytes)
        print(f"Saved: {output_path}")
    except Exception as e:
        print(f"Failed for {name}: {e}")
