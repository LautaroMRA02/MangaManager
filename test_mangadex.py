
from app.plugins.sources.mangadex.scraper import MangaDexScraper


scraper = MangaDexScraper()

print("\n--- BUSCAR MANGA ---")

results = scraper.search("Berserk")

for manga in results:
    print(manga.title)
    print(manga.source_id)
    print(manga.cover_url)
    print()


if results:
    manga = results[0]

    print("--- CAPÍTULOS ---")

    chapters = scraper.get_chapters(manga.source_id)

    for chapter in chapters[:5]:
        print(chapter.number, chapter.title, chapter.language)

    if chapters:
        print("\n--- PÁGINAS ---")

        pages = scraper.get_pages(chapters[0].source_id)

        for page in pages:
            print(page.number, page.url)
