import os
import re
import bsoupsoup as chu
import json
from pathlib import Path
import optim_selena as ext

"""
    CATERED TOWARDS FILES COMING FROM: https://sukebei.nyaa.si/user/rbot2000
    THIS IS NOT AN INTEGRAL PART OF THE API
    BSOUPSOUP AND OPTIM_SELENA ARE THE ONLY IMPORTANT ONES
    I KNOW THAT PERFORMING ONE OF THEM EXCLUSIVELY WITHOUT RESORTING TO 
    USING THE OTHER IS THE BEST WAY TO GO, BUT LET'S SEE HOW FAR I CAN CHALLENGE MYSELF
    INTO JUGGLING FAIRLY COMPLICATED SHIT"""

blacklist= ['netorare', 'netorase', 'yaoi', 'futanari']
os.chdir("D:\\BackupDir\\Anime\\Mangas\\Doujinshi\\FAKKU BATCHES\\fakku 6901-7000")
temp_F = 'JSONS'
rcDepth = 0
Path(temp_F).mkdir(parents=True, exist_ok=True)

def returnName():
    #pattern of filenaming with this torrent user
    #will return ONLY the name of the file
    filenames = []
    for r, d, file in os.walk(os.getcwd()):
        for f in file:
            try:
                reg = re.search(r'.*?\]\s(.*)\s\(.*', f) # holyshit regexes are confusing asfuckkk
                print(f'Name Detected: {reg.group(1)}')
            except:
                print(f'{f} is not a doujin')
                continue
            filenames.append(reg.group(1))
    return filenames



def attachFILE(DOUJINS):
    global rcDepth
     #list type
    print("="*60)
    isEmpty = []     # counter for empty returns
    blacc = []      # appalling crap doujins go here
    stoploop = 0
    with open("Tags.txt", 'w',encoding='utf8') as tag:

        for name in DOUJINS:
            print(f'{DOUJINS.index(name)+1} - {len(DOUJINS)}')
            """for some reason tch, filenames with trailing periods tend to raise exception with open()
                ffs man...im going insane"""

            filterSplit = name.split()
            filterDir = []
            for unf in filterSplit:
                cleansed = ''.join(filter(str.isalnum, unf)).lower()
                filterDir.append(cleansed)
            kname = " ".join(filterDir)
            kname = kname.strip()
            print(kname)


            Path(f'{temp_F}\\{kname}').mkdir(parents=True, exist_ok=True)
            with open(f'{temp_F}\\{kname}\\details.json','w+') as details:
                metadata = chu.Emetadata(name) # dictionary

                print('WRITING ON DOUJIN ENTRY: '+name+'\n' )

                for keys in metadata.keys():
                    for notallowed in blacklist:
                        if notallowed in metadata['tags']:
                            print(f'[BLOCKED]ENTRY TAG {notallowed} present in {name}\n'+
                                  f'Skipping...')
                            blacc.append(name)
                            tag.write(f'SKIPPED {name}')
                            break



                    tag.write("[" + keys + "] :>> " + str(metadata[keys])+"\n")
                    print("[" + keys + "] :>> " + str(metadata[keys])+"\n")

                if not len(metadata):
                    tag.write(f'404 return for {name}')
                    isEmpty.append(name)

                else:
                    metadata['status'] = '2'  # catering the tachiyomi-c json format
                    metadata["_status values"] = ["0 = Unknown", "1 = Ongoing", "2 = Completed", "3 = Licensed",
                                                  "4 = Publishing finished", "5 = Cancelled", "6 = On hiatus"]
                    jsonFormat = json.dumps(metadata, indent=4, sort_keys=True)
                    details.write(jsonFormat)

                tag.write("\n\n\n")
                # if stoploop == 5:
                #     break
                stoploop += 1
                print("\n\n")
        for notfound in isEmpty:
            print(f'Empty dataset for entry name {notfound}')

        if rcDepth < 2:
            rcDepth += 1
            # print("attempting Recursion")
            # attachFILE(isEmpty)
        for blist in blacc:
            print(f'Blacklisted entry {blist}')
    print("ehehehehehehehe done bro")
    print(f'Your api worked {(1-(len(isEmpty)/len(DOUJINS)))*100} of the time. Good job(?)')


DOUJINS = returnName()
attachFILE(DOUJINS)
