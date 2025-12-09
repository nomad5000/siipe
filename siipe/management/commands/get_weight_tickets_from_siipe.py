import zoneinfo
from datetime import timedelta, datetime
from django.conf import settings

from django.core.management.base import BaseCommand, CommandError

import pandas as pd
from playwright.sync_api import sync_playwright, TimeoutError


from siipe.models import WeightTicketModel

"""
________________
IMPORTANT
________________
This command should be outsourced to an external importer. in a separate heroku project.

Reason. The buildpack for play

"""
class Command(BaseCommand):
    help = "Gets Weight Tickets from Palm Oil Mill Software and saves them to database WeightTicketModel"

    def add_arguments(self, parser):
        # Positional arg (mandatory)
        parser.add_argument(
            'days_back',
            nargs='?',
            type=int,
            default=1,
            help='Number of days to go into the past to fetch weight_tickets'
        )

        parser.add_argument(
            '--headful',
            action='store_true',
            help='Enable headful mode for chromium browser'
        )

    def handle(self, *args, **options):
        url = settings.SIIPE_URL
        self.stdout.write(self.style.SUCCESS(f"Opening: {url}"))
        try:
            results = self._get_table_as_array(from_url=url,days_back=options['days_back'],headful=options['headful'])
            self._save_results_array_to_database(results)
        except Exception as e:
            raise CommandError(f"Failed to run scrolling browser: {e}")

        self.stdout.write(self.style.SUCCESS("Finished successfully."))

    # -------------------------------------------------------------------------
    # Helper logic
    # -------------------------------------------------------------------------
    @staticmethod
    def _extract_result_table_to_array(table_locator):
        result = []
        count = table_locator.count()
        print("adding new page with ")
        print(f"{count} rows \n")
        for i in range(count):
            row = table_locator.nth(i)
            # locate all cells (td or th) in this row
            cell_locators = row.locator("td")
            cell_count = cell_locators.count()
            cells = []
            for j in range(cell_count):
                cell = cell_locators.nth(j)
                # get the inner text of the cell
                text = cell.inner_text().strip()
                cells.append(text)
            result.append(cells)
        return result #only return rows no headers and crap
    @staticmethod
    def _filter_results_for_unique(list_of_rows):
        seen = set()
        unique = []
        for sub in list_of_rows:
            t = tuple(sub)  # convertible to hashable
            if t not in seen:
                seen.add(t)
                unique.append(sub)
        return unique
    @staticmethod
    def _safe_int(value):
        """Convert to int; treat None/''/whitespace as 0."""
        if value is None:
            return 0
        s = str(value).strip()
        if s == "":
            return 0
        s = s.replace(".", "")
        return int(s)
    
    def _save_results_array_to_database(self,array):
        for result in array:
            try:
                WeightTicketModel.objects.create(
                    ticket_number=result[0],
                    weighing_date=datetime.strptime(result[1], "%d/%m/%Y"),
                    provider_tax_id=result[2],
                    provider_name=result[3],
                    vehicle_id=result[4],
                    driver_id=result[5],
                    driver_name=result[6],
                    gross_weight_kg=self._safe_int(result[7]),
                    tare_weight_kg=self._safe_int(result[8]),
                    net_weight_kg=self._safe_int(result[9]),
                    peduncle_long_units=self._safe_int(result[10]),
                    peduncle_long_kg=self._safe_int(result[11]),
                    sick_bunches_units=self._safe_int(result[12]),
                    impurities_units=self._safe_int(result[13]),
                    impurities_kg=self._safe_int(result[14]),
                    rotten_fruit_units=self._safe_int(result[15]),
                    rotten_fruit_kg=self._safe_int(result[16]),
                    overripe_fruit_units=self._safe_int(result[17]),
                    overripe_fruit_kg=self._safe_int(result[18]),
                    green_fruit_units=self._safe_int(result[19]),
                    green_fruit_kg=self._safe_int(result[20]),
                    empty_bunches_units=self._safe_int(result[21]),
                    empty_bunches_kg=self._safe_int(result[22]),
                    green_with_detachment_kg=self._safe_int(result[23]),
                    penalty_weight_kg=self._safe_int(result[24]),
                    payable_weight_kg=self._safe_int(result[25]),
                )
            except Exception as e:
                print(e)
            print(f"saved Ticket Nr: {result[0]} to database")
    # -------------------------------------------------------------------------
    # Browser logic
    # -------------------------------------------------------------------------
    def _get_table_as_array(self,from_url,days_back,headful):
        with (sync_playwright() as p):
            browser = p.chromium.launch(headless=(not headful))
            context = browser.new_context(
                viewport={"width": 1280, "height": 800},
                user_agent=(
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0 Safari/537.36"
                ),
            )
            page = context.new_page()

            page.goto(from_url, wait_until="networkidle")

            page.fill("input[name='txtId']", "830113719-3")
            page.fill("input[name='txtPwd']", "830113719-3")
            page.click("input[name='imbIngresar']")
            page.wait_for_load_state("networkidle")
            page.hover("#menu > ul > li:nth-child(1) > a")
            page.click("#menu > ul > li:nth-child(1) > ul > li > a")
            page.wait_for_load_state("networkidle")
            iframe = page.frame_locator("iframe")
            iframe.get_by_text("Movimiento Diario Detallado").click()
            iframe.locator('#rvImprimir_ctl00_ctl03 > input').wait_for(state="visible", timeout=5000)
            start_date = iframe.locator('#rvImprimir_ctl00_ctl03 > input')
            end_date = iframe.locator('#rvImprimir_ctl00_ctl05 > input')
            bogota_tz = zoneinfo.ZoneInfo("America/Bogota")
            now = datetime.now(bogota_tz)
            past_date = now - timedelta(days=days_back)
            past_date_first_minute = past_date.replace(hour=0, minute=0, second=0, microsecond=0)
            print(f'getting results for start date: {past_date_first_minute.strftime("%d/%m/%Y %I:%M:%S %p")} \n')
            start_date.fill(past_date_first_minute.strftime("%d/%m/%Y %I:%M:%S %p").lower().replace("am", "a.m.").replace("pm", "p.m."))
            end_date.fill(now.strftime("%d/%m/%Y %I:%M:%S %p").lower().replace("am", "a.m.").replace("pm", "p.m."))
            print(f'getting results for end date: {now.strftime("%d/%m/%Y %I:%M:%S %p")} \n')
            iframe.locator('input[value="View Report"]').wait_for(state="visible",timeout=10000)
            iframe.locator('input[value="View Report"]').click()
            iframe.frame_locator("#ReportFramervImprimir").frame_locator('#report').locator('.a286').wait_for(state="visible", timeout=10000)
            page.wait_for_timeout(timeout=1000)
            results_table_rows = iframe.frame_locator("#ReportFramervImprimir").frame_locator('#report').locator('.a286 tr')
            results = Command._extract_result_table_to_array(results_table_rows)
            next_button = iframe.locator('input[type="image"][src="/PortalProveedor/Reserved.ReportViewerWebControl.axd?OpType=Resource&Version=8.0.50727.42&Name=Icons.NextPage.gif"]')
            try:
                next_button.wait_for(state='visible', timeout=10000)
            except TimeoutError as e:
                #in case only one results page
                print('just one result page')
                iframe.frame_locator("#ReportFramervImprimir").frame_locator('#report').locator('.a286').wait_for(state="visible", timeout=10000)
                results_table = iframe.frame_locator("#ReportFramervImprimir").frame_locator('#report').locator('.a286 tr')
                results += Command._extract_result_table_to_array(results_table)
            while next_button.is_visible():
                next_button.click()
                page.wait_for_timeout(timeout=1000)
                iframe.frame_locator("#ReportFramervImprimir").frame_locator('#report').locator('.a286').wait_for(state="visible", timeout=10000)
                results_table = iframe.frame_locator("#ReportFramervImprimir").frame_locator('#report').locator('.a286 tr')
                results += Command._extract_result_table_to_array(results_table)

            unique_results = self._filter_results_for_unique(results)
            browser.close()
            return unique_results[2:]
