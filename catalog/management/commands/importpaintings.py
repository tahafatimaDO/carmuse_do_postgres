import csv
from django.core.management.base import BaseCommand
from wagtail.core.models import Page
from catalog.models import PaintingIndexPage, PaintingDetailPage


class Command(BaseCommand):
    help = "Imports 35k film plots from Wikipedia"

    def handle(self, *args, **options):
        # delete existing film index pages and film pages
        PaintingDetailPage.objects.all().delete()
        PaintingIndexPage.objects.all().delete()
        # create a film index page
        home = Page.objects.get(id=3)
        painting_index_page = PaintingIndexPage(title="Paintings")
        home.add_child(instance=painting_index_page)
        painting_index_page.save_revision().publish()
        # import film pages
        reader = csv.DictReader(open("inventory_05.csv"))
        for row in reader:
            painting_detail_page = PaintingDetailPage(
                title=row["title"],
                width=row["width"],
                height=row["height"],
                remark=row["remark"],
                dbreference=row["dbreference"],
                description=row["description"],
            )
            painting_index_page.add_child(instance=painting_detail_page)
            painting_detail_page.save_revision().publish()
            print("published painting page " + row["title"])