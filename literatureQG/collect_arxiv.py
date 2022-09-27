import urllib.request as libreq
import feedparser

import glob

from tqdm import tqdm

from doc2json.grobid2json.tei_to_json import convert_tei_xml_file_to_s2orc_json

from bs4 import BeautifulSoup

import scipdf

import json

MINIITER = 100

def main():
    print("Collecting paper urls...")
    pdfLinks = []
    for i in tqdm(range(6)):
        query = f"https://export.arxiv.org/api/query?search_query=cat:cs.HC&start={i*2000}&max_results=2000&sortBy=lastUpdatedDate&sortOrder=descending"
        print("Querying: ", query)
        with libreq.urlopen(query) as url:
            r = url.read()
        # print(r)
        feed = feedparser.parse(r)
        print('Feed title: %s' % feed.feed.title)
        print('Feed last updated: %s' % feed.feed.updated)
        print('totalResults for this query: %s' % feed.feed.opensearch_totalresults)
        print('itemsPerPage for this query: %s' % feed.feed.opensearch_itemsperpage)
        print('startIndex for this query: %s'   % feed.feed.opensearch_startindex)
        print('Total results for this query: %s' % len(feed.entries))


        for entry in feed.entries:
            # get the links to the abs page and pdf for this e-print
            for link in entry.links:
                if link.rel == 'alternate':
                    # print('abs page link: %s' % link.href)
                    pass
                # print(link)
                elif link.title == 'pdf':
                    # print('pdf link: %s' % link.href)
                    pdfLinks.append(link.href)
        

    print("Parsing pdfs...")
    print("Total pdfs: ", len(pdfLinks))
    dPapers = []
    indexFile = open('./arXiv_xml/index.txt', 'w', encoding='utf-8')
    for idx, l in enumerate(tqdm(pdfLinks[:3], desc="Parsing pdfs", MINIITER=MINIITER)):
        try:
            xmlText = scipdf.parse_pdf(l + '.pdf', soup=False)
            # dump each xml file to disk
            with open(f'./arXiv_xml/files/{idx}.xml', 'w', encoding='utf-8') as f:
                f.write(xmlText)
            # write the index file
            indexFile.write(f'{idx}\t{l}\n')

            # convert xml to soup
            try:
                parsed_article = BeautifulSoup(xmlText, "lxml")
                dPapers.append(
                    scipdf.convert_article_soup_to_dict(parsed_article, as_list=False)
                )
            except:
                dPapers.append("")
        except Exception as e:
            print(e)
            dPapers.append("")
    indexFile.close()

    # dump dPapers to jsonl
    with open('arxiv_HCI_all.jsonl', 'w') as f:
        for d in dPapers:
            if d: f.write(json.dumps(d) + '\n')

if __name__ == "__main__":
    main()