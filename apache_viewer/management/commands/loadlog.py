from django.core.management.base import BaseCommand
from django.conf import settings
from apache_viewer.models import Logs
from apache_viewer.utils import parse_apache_string
from tqdm import tqdm
from itertools import islice
import requests
import math
import os


class Command(BaseCommand):
    help = "Load apache log from the url"
    bulks = []

    def add_arguments(self, parser):
        parser.add_argument(
            "--url", dest="url", required=True, help="url of apache log"
        )

    def handle(self, *args, **options):
        url = options["url"]
        # process the url
        filename = self._downdloan_file(url)

        if self._process_file(filename):
            os.remove(filename)

    def _downdloan_file(self, url):
        local_filename = settings.LOG_DATA_FOLDER + url.split("/")[-1]
        print(local_filename)
        if not os.path.isfile(local_filename):
            self.stdout.write('Downdloading file "%s" ' % url)

            response = requests.get(url, stream=True)
            # show progressbar
            total_size = int(response.headers.get("content-length", 0))
            block_size = 1024 * 1024
            with open(local_filename, "wb") as handle:
                for data in tqdm(
                    response.iter_content(block_size),
                    total=math.ceil(total_size // block_size),
                    unit="KB",
                    unit_scale=True,
                ):
                    handle.write(data.strip())

            self.stdout.write(self.style.SUCCESS('Successfully got an url "%s"' % url))

        return local_filename

    def _process_file(self, file):
        with open(file, "r") as handle:
            self.stdout.write('Processing file "%s" ' % file)

            fl_content = handle.read().splitlines()
            total_lines = len(fl_content)
            # process file and show progressbar
            for line in tqdm(fl_content, total=total_lines):
                log = parse_apache_string(line.strip())
                if log:
                    self._add_to_bulk(log)

            return self._bulk_insert()

    def _add_to_bulk(self, log):
        """
        Collect all rows to bulks
        """
        try:
            add_bulk = Logs.objects.add_log_bulk(log)
            if add_bulk:
                self.bulks.append(add_bulk)
        except ValueError:
            pass

    def _bulk_insert(self):
        """
        Insert rows to DB by create_bulk
        """
        self.stdout.write("Inserting")

        batch_size = 10000
        objs = tuple(self.bulks)
        total = len(objs)
        pbar = tqdm(total=total)

        while True:
            batch = list(islice(objs, batch_size))
            if not batch:
                break
            Logs.objects.bulk_create(batch, batch_size, ignore_conflicts=True)
            pbar.update(len(batch))
