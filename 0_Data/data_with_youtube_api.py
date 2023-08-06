import pandas as pd
from googleapiclient.discovery import build

def connect_API():
    '''Connect to Youtube Data API V3'''
    api_key = '[MY_API_KEY]'
    youtube = build('youtube', 'v3', developerKey=api_key)
    return youtube

def download_csv(file_name, response_items, char_name):
    '''Parse video titles and then save to csv'''
    char_names = []
    playstyles = []
    vid_titles = []

    for item in response_items:
        title = item['snippet']['title']
        title = title.upper()

        # If title does not specify for abyss 3.7, then skip
        if '3.6' not in title or 'ABYSS' not in title:
            continue

        char_name = char_name.upper()
        if char_name not in title:
            continue

        # Strip the names to get the relevant playstyle
        idx = title.index(char_name)
        curr_str = title[idx+len(char_name):]

        cons = ['C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6']

        for item in [' IN ','FLOOR','SPIRAL','ABYSS','GENSHIN','IMPACT','F2P','COMP',
             'FULL','STAR','CLEAR','VS',' ON ','TEAM','BOTH','SIDES',
             'DESTROY','SHOWCASE','DUO','RUN','MY','PATCH','DAN','CHAMBER',
             'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6',
             'R1','R2','R3','R4','R5',
             'TEST','SPEEDRUN','SPEED RUN','INIQUITOUS','BAPTIST',
             'CONSECRATED','BEASTS','JADEPLUME','TERRORSHROOM','DENDRO CHICKEN',
             'SECOND HALF','FIRST HALF','NEW']:
            curr_str = curr_str.replace(item,'').strip()

        for i in range(len(curr_str)):
            s = curr_str[i]
            if s == ' ':
                continue
            if i+1 != len(curr_str):
                # Skip if constellations are mentioned
                if curr_str[i:i+2] in cons or curr_str[i:i+2] == 'VS':
                    curr_str = curr_str[:i]
                    break
            if not s.isalpha() or s == 'X':
                curr_str = curr_str[:i]
                break
            if i+2 != len(curr_str):
                if curr_str[i:i+3] == 'AND':
                    curr_str = curr_str[:i]
                    break

        # If null, check to see if playstyle is before the character name
        if not curr_str.strip():
            curr_str = title[:idx]
            for i in range(idx-1,-1,-1):
                s = curr_str[i]
                if s == ' ':
                    continue
                if not s.isalpha() or s == 'X':
                    curr_str = curr_str[i+1:]
                    break

        for item in [' IN ','FLOOR','SPIRAL','ABYSS','GENSHIN','IMPACT','F2P','COMP',
             'FULL','STAR','CLEAR','VS',' ON ','TEAM','BOTH','SIDES',
             'DESTROY','SHOWCASE','DUO','RUN','MY','PATCH','DAN','CHAMBER',
             'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6',
             'R1','R2','R3','R4','R5',
             'TEST','SPEEDRUN','SPEED RUN','INIQUITOUS','BAPTIST',
             'CONSECRATED','BEASTS','JADEPLUME','TERRORSHROOM','DENDRO CHICKEN',
             'SECOND HALF','FIRST HALF','NEW']:
            curr_str = curr_str.replace(item,'').strip()

        for item in ['FT','FT.','WITH','AND']:
            if item in curr_str.strip():
                curr_str = curr_str.strip().split(item)
                curr_str = [x.strip() for x in curr_str if x]
            if len(curr_str) == 0:
                curr_str = ''
            else:
                curr_str = curr_str[-1]

        # Remove names of other characters
        for name in genshin_characters:
            if name.upper() in curr_str:
                curr_str = curr_str.replace(name.upper(),'').strip()

        char_names.append(char_name)
        playstyles.append(curr_str.strip())
        vid_titles.append(title.strip())

    data = {
      'Character': char_names,
      'Playstyle': playstyles,
      'Title': vid_titles
    }
    df = pd.DataFrame(data)
    df.to_csv(file_name, mode='a', index=False, header=False)


def get_genshin_titles(youtube, page_token, name):
    '''Use the Youtube API to search Youtube videos'''
    request = youtube.search().list(
        part='snippet',
        fields='nextPageToken,items(id,snippet(title))',
        q=name+' Spiral Abyss 3.6',
        type='video',
        pageToken=page_token,
        maxResults=50
    )
    response = request.execute()
    return response


def outer_loop(youtube, file_name, name):
    '''Make initial request and then go through next pages'''
    # Make the request
    request = youtube.search().list(
        part='snippet',
        fields='nextPageToken,items(id,snippet(title))',
        q=name+' Spiral Abyss 3.6',
        type='video',
        maxResults=50
    )

    # Execute the request for the first page
    response = request.execute()

    if 'items' in response.keys():
        response_items = response['items']
        download_csv(file_name, response_items, name)
    else:
        # Return if no results
        return

    if 'nextPageToken' in response.keys():
        page_token = response['nextPageToken']

        for i in range(25):
            response = get_genshin_titles(youtube, page_token, name)

            if 'items' in response.keys():
                response_items = response['items']
                download_csv(file_name, response_items, name)
            else:
                # Return if response['items'] is empty
                return

            if 'nextPageToken' in response.keys():
                page_token = response['nextPageToken']
            else:
                # Return if no next page
                return

    else:
        # Return if no next page
        return

    # Return once everything is done
    return

def main():
    '''Run outer loop to get video titles and then save to csv'''
    genshin_characters = ['Albedo','Alhaitham','Aloy','Amber','Ayaka','Ayato',
                      'Baizhu','Barbara','Beidou','Bennett',
                      'Candace', 'Chongyun', 'Collei', 'Cyno','Childe','Tartaglia',
                      'Dehya','Diluc','Diona','Dori',
                      'Eula',
                      'Faruzan','Fischl',
                      'Ganyu','Gorou',
                      'Hu Tao','Hutao','Heizou',
                      'Itto',
                      'Jean',
                      'Kazuha','Kaeya','Kaveh','Keqing','Kirara','Klee','Kuki','Kokomi',
                      'Layla','Lisa',
                      'Mika','Mona','MC',
                      'Nahida','Nilou','Ningguang','Noelle',
                      'Qiqi',
                      'Raiden','Razor','Rosaria',
                      'Sayu','Shenhe','Sucrose','Sara',
                      'Thoma','Tighnari','Traveler',
                      'Venti',
                      'Wanderer','Scaramouche',
                      'Xiangling','Xiao','Xingqiu','Xinyan',
                      'Yae','Yanfei','Yaoyao','Yelan','Yoimiya','Yunjin',
                      'Zhongli']

    # Create initial file
    filename = '/content/drive/MyDrive/genshin_data_raw_V3_7.csv'

    data = {'Character': ['Character'],
            'Playstyle': ['Playstyle'],
            'Title': ['Title']}

    df = pd.DataFrame(data)
    df.to_csv(filename,index=False,header=False)

    # Run the code to get the titles
    # Note: these runs were broken up because the quota for the API
    # did not give enough units to run all of these at the same time
    youtube = connect_API()
    for i in range(len(genshin_characters)):
        outer_loop(youtube, filename, genshin_characters[i])


if __name__ == '__main__':
    main()