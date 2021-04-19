from papers import punch

# create an instance of the punch class
myPunch = punch.Punch(
    'config/thenation.json',
    'config/keywords.json',
    'papers/cache/thenation.json')

raw_news = myPunch.request()

news_soup = myPunch.soupify(raw_news)

hrefs = myPunch.find_all_hrefs()

current = myPunch.subtract_cache()

print(len(current))

# myPunch.update_cache()

relevant = myPunch.get_relevant_news()
print(len(relevant))

print('-----------------------', '\n\n')
full_news = myPunch.get_full_news()


print(full_news)
print('-----------------------', '\n\n')


print("Adios!")
