import math
import re
import urllib.request
import urllib.error
import urllib.parse


class Scraper:
    def __init__(self):
        self.regex_search = "\<div class=\"competitive-rank\"\>\<img src=\".+\"/\>\<div class=\"u-align-center h6\"\>([0-9]+)\</div\>"
        self.url_base = "https://playoverwatch.com/en-us/career/pc/"
        self.regions = ("us/", "eu/")

    def scrape(self, player):
        player_id = player.id.replace("#", "-")
        parsed_rating = float('nan')

        for region in self.regions:
            try:
                url = self.url_base + region + urllib.parse.quote(player_id)
                req = urllib.request.urlopen(url)
                if req.getcode() != 404:
                    result = req.read().decode('utf-8')
                    match = re.search(self.regex_search, result)
                    try:
                        sr_maybe = match.group(1)
                        parsed_rating = int(sr_maybe)
                    except Exception:
                        print("-->Could not parse SR for %s, using %d" % (player.name, player.sr))
                break
            except urllib.error.HTTPError:
                continue

        if math.isnan(parsed_rating):
            print("-->Rating not found for %s, using %d" % (player.name, player.sr))
        else:
            print("-->Got SR for %s: %d" % (player.name, parsed_rating))
            player.setSR(parsed_rating)

        # Generating overbuff profile link and grabbing data
        try:
            profile_link = "https://www.overbuff.com/players/pc/" + urllib.request.quote(player_id)
            response = urllib.request.urlopen(profile_link + "?mode=competitive")
            if response.getcode() != 404:
                page_source = response.read().decode('utf-8')

            # Grab number of lines
            num_lines = len(page_source.splitlines())

            # If competitive data is not found, collect quick play data
            if (num_lines < 4):
                response = urllib.request.urlopen(profile_link)
                page_source = response.read().decode('utf-8')
                # Grab number of lines
                num_lines = len(page_source.splitlines())

            # Main hero classes are on the last line
            mains = page_source.splitlines()[num_lines - 1]
            # Parse and print sorted hero classes
            parsed_role = 'Flex'
            support = re.findall(r'Support</a><small><span data-time="(.*?)" data-time-format', mains)
            tank = re.findall(r'Tank</a><small><span data-time="(.*?)" data-time-format', mains)
            defense = re.findall(r'Defense</a><small><span data-time="(.*?)" data-time-format', mains)
            offense = re.findall(r'Offense</a><small><span data-time="(.*?)" data-time-format', mains)

            # Collect hero roles based on amount of time played
            hero_mains = {}
            try:
                hero_mains["Support"] = int(support[0]) if len(support) > 0 else 0
                hero_mains["Tank"] = int(tank[0]) if len(tank) > 0 else 0
                hero_mains["Defense"] = int(defense[0])  if len(defense) > 0  else 0
                hero_mains["Offense"] = int(offense[0]) if len(offense) > 0 else 0
                parsed_role = sorted(hero_mains.items(), key=lambda k_v: k_v[1], reverse=True)[0][0]
                parsed_backup_role = sorted(hero_mains.items(), key=lambda k_v: k_v[1], reverse=True)[1][0]
                print("-->Got role for %s: %s/%s" % (player.name, parsed_role, parsed_backup_role))
                player.setRole(parsed_role + '/' + parsed_backup_role)
            except IndexError:
                print("-->Could not parse role for %s, using %s" % (player.name, player.role))
        except urllib.error.HTTPError:
            print("-->Could not parse role for %s, using %s" % (player.name, player.role))
