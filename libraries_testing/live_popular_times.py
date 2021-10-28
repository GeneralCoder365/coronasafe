# https://pypi.org/project/LivePopularTimes/

import livepopulartimes

# livepopulartimes.get_populartimes_by_address(formatted_address)
    # (location name) , full address, city, province/state/etc, country

# a = livepopulartimes.get_populartimes_by_address("(H-Mart Dunbar) 5557 Dunbar Street, Vancouver BC, Canada", proxy=proxy)
# a = livepopulartimes.get_populartimes_by_address("(H-Mart Dunbar) 5557 Dunbar Street, Vancouver BC, Canada")

a = livepopulartimes.get_populartimes_by_address("(Westfield Montgomery) 7101 Democracy Blvd, Bethesda, MD 20852, United States")
# a = livepopulartimes.get_populartimes_by_address("7101 Democracy Blvd, Bethesda, MD, United States") # <-- Less accurate
# a = livepopulartimes.get_populartimes_by_address("(Starbucks) 10251 Old Georgetown Rd, Bethesda, MD, United States")
# OR (Starbucks) 10251 Old Georgetown Rd, Bethesda, MD 20814 --> BOTH WORK!!!
# a = livepopulartimes.get_populartimes_by_address("() 10804 Brewer House Road, Rockville, MD, United States")

current = a["current_popularity"]
print(current)

# a: {'rating', 'rating_n', 'populartimes': [{'name': 'Day', 'data': ['popularity value per hour in 24 hour period of Monday']}, {Tuesday - Friday same thing}], 'time_spent',
# 'name', 'place_id', 'address', 'coordinates': {'lat', 'lng'}, 'categories': [list of stores/restaurants/theaters in the place], 'place_types': [[place_type_1], 
# [place_type_n]], 'current_popularity', 'popular_times': [list of info on popularity per store/restaurant/theater]}
print(a)