# URL with hardcoded location data
LOUNAAT_INFO_URL = 'https://www.lounaat.info/valimopolku-9-helsinki'
POR_URL = 'https://por.fi/menu/'
POR_HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0'}
TELLUS_URL = 'https://www.compass-group.fi/menuapi/feed/rss/current-day?costNumber=3105&language=fi'

# list of names of restaurants that you don't want to see. will be partially matched to restaurant name (not case sensitive)
# example:
blacklist = ['helsinki-tali', 'ravintola tali', 'sodexo']

# list of your favorite restaurants. These names will be partially matched to any restaurant name and the set of matching restaurants
# will be at the beginning of the list in an undefined order
favorites = ['por', 'tellus', '91.1', 'faundori', 'blancco']