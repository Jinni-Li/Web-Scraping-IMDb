from background_research import BackgroundResearch
from scraper import scraper

if __name__ == "__main__":
    # página que queremos scrapear
    seed_page = 'https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm'

    # Background research
    output_file = 'background_research_output.txt'
    research = BackgroundResearch(seed_page)
    research.perform_research(output_file)

    # Scraping
    scraper()
