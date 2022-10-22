def bruteSearch(text, extension='english'):
    # will attempt to hardcode the doujin separated by dash into the browser if fakku is trolling
    wspaceSplit = text.split()
    filSplit = []
    for unf in wspaceSplit:
        cleansed = ''.join(filter(str.isalnum, unf)).lower()

        filSplit.append(cleansed)
    filSplit.append(extension)
    return '-'.join(filSplit)

title = "Sore Loser, Shunko!! ~Perfect Game~"
filtered = bruteSearch(title)
print(filtered)