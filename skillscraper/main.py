from skillscraper.spiders.linkspider import LinkSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import sys
from pathlib import Path
import csv
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
from datetime import datetime


scraped_data = []

sys.path.append(str(Path(__file__).resolve().parent))

class CSVWriterPipeline:
    def process_item(self, item, spider):
        scraped_data.append(item)
        return item


def unpack_list(cell):
    try:

        return eval(cell) if isinstance(cell, str) else []
    except:
        return []
    
    
def main():
    settings = get_project_settings()
    process = CrawlerProcess(settings ={
        'LOG_LEVEL': 'INFO',
        'ITEM_PIPELINES': {
            '__main__.CSVWriterPipeline': 1,  
        }
    })
    process.crawl(LinkSpider)
    process.start()
    
    with open('results.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['skills']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(scraped_data)
        

    data = pd.read_csv('results.csv')


    flat_list = []
    for cell in data['skills']:
        flat_list.extend(unpack_list(cell))
    
    flat_list = Counter(flat_list)
    sorted_skills = flat_list.most_common()
    top_skills = sorted_skills[:10]
    skills, counts = zip(*top_skills)
    
    current_date = datetime.now().strftime("%d.%m.%Y")
    
    plt.figure(figsize=(12, 6))
    plt.bar(skills, counts, color="skyblue")
    plt.title(f"Top 10 najwięcej występujących umiejętności w woj. Śląskim w dniu {current_date} na stronie justjoin.it", fontsize=16)
    plt.xlabel("Umiejętności", fontsize=12)
    plt.ylabel("Liczba wystąpień", fontsize=12)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    # Wyświetl wykres
    plt.show()
    

if __name__ == "__main__":
    main()