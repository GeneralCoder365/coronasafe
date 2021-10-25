# https://pypi.org/project/LivePopularTimes/

import livepopulartimes

results = livepopulartimes.get_places_by_search("westfield montgomery")

print(results)