#List of VTubers that the bot looks at
#To be in the same order as the previous day's image
members = ['Elira Pendora',
           'Finana Ryugu',
           'Rosemi Lovelock',
           'Petra Gurin',
           'Enna Alouette',
           'Reimu Endou',
           'Millie Parfait',
           # 'Ike Eveland',
           'Vox Akuma',
           'Luca Kaneshiro',
           'Shu Yamino',
           'Alban Knox',
           'Fulgur Ovid',
           'Sonny Brisko',
           'Uki Violeta',
           # 'Kyo Kaneko',
           'Maria Marionette',
           'Aster Arcadia',
           'Aia Amare',
           'Ren Zotto',
           'Scarle Yonaguni',
           'Doppio Dropscythe',
           'Meloco Kyoran',
           # 'Hex Haywire',
           'Kotoka Torahime',
           'Ver Vermillion',
           'Yu Q. Wilson',
           'Vantacrow Bringer',
           'Vezalius Bandage',
           'Claude Clawmark',
           'Kunai Nakasato',
           'Victoria Brightshield',
           'Ryoma Barrenwort',
           'Klara Charmwood',
           'Twisty Amanozako',
           'Freodore',
           'Kaelix Debonair',
           'Seible',
           'Zeal Ginjoka',
           'Luxiem',
           'NIJISANJI EN Official']

groups = ['Luxiem',
          'NIJISANJI EN Official']

#Dictionary of YouTube Channel ID
#Write the part after channel
yt_id_dic = {'Elira Pendora':'UCIeSUTOTkF9Hs7q3SGcO-Ow',
             #'Pomu Rainpuff':'UCP4nMSTdwU1KqYWu3UH5DHQ',
             'Finana Ryugu':'UCu-J8uIXuLZh16gG-cT1naw',
             #'Selen Tatsuki':'UCV1xUwfM2v2oBtT3JNvic3w',
             'Rosemi Lovelock':'UC4WvIIAo89_AzGUh1AZ6Dkg',
             'Petra Gurin':'UCgA2jKRkqpY_8eysPUs8sjw',
             'Enna Alouette':'UCR6qhsLpn62WVxCBK1dkLow',
             #'Nina Kosaka':'UCkieJGn3pgJikVW8gmMXE2w',
             'Reimu Endou':'UCBURM8S4LH7cRZ0Clea9RDA',
             'Millie Parfait':'UC47rNmkDcNgbOcM-2BwzJTQ',
             #'Ike Eveland':'UC4yNIKGvy-YUrwYupVdLDXA',
             #'Mysta Rias':'UCIM92Ok_spNKLVB5TsgwseQ',
             'Vox Akuma':'UCckdfYDGrjojJM28n5SHYrA',
             'Luca Kaneshiro':'UC7Gb7Uawe20QyFibhLl1lzA',
             'Shu Yamino':'UCG0rzBZV_QMP4MtWg6IjhEA',
             'Alban Knox':'UCQ1zGxHrfEmmW4CPpBx9-qw',
             #'Yugo Asuma':'UCSc_KzY_9WYAx9LghggjVRA',
             'Fulgur Ovid':'UCGhqxhovNfaPBpxfCruy9EA',
             'Sonny Brisko':'UCuuAb_72QzK0M1USPMEl1yw',
             'Uki Violeta':'UChJ5FTsHOu72_5OVx0rvsvQ',
             #'Kyo Kaneko':'UCsb-1aJgiJXJH2feV-zlZRw',
             'Maria Marionette':'UCwaS8_S7kMiKA3izlTWHbQg',
             'Aster Arcadia':'UCpzxZW5kghGnO5TmAFJQAVw',
             'Aia Amare':'UCN68LoM3khS4gdBMiWJO8WA',
             'Ren Zotto':'UCKu59gTZ_rdEmerdx5rV4Yg',
             'Scarle Yonaguni':'UCFgXWZOUZA2oYHNr6qDmsTQ',
             'Doppio Dropscythe':'UCy91xBlY_Brh3bnHxKtjrrg',
             'Meloco Kyoran':'UChKXd7oqD18qiIYBoRIHTlw',
            #  'Hex Haywire':'UCz_ZRw6ak4Foy8zZy0kEprQ',
             'Kotoka Torahime':'UCggO2c1unS-oLwTLT0ICywg',
             'Ver Vermillion':'UCO8WcDsF5znr-qsXlzZNpqg',
             'Yu Q. Wilson':'UCKpKC3M5fkcEvtOr06dmYlA',
             'Vantacrow Bringer':'UCpYf6C9QsP_BRf97vLuXlIA',
             'Vezalius Bandage':'UCK9l6rTwU3hiSZijIMq51Gw',
             'Claude Clawmark':'UCdh-YF2gTzqDNu0VU9lwPPw',
             'Kunai Nakasato':'UCwqtK-m6954_aHEvOYtZpyQ',
             'Victoria Brightshield':'UChTA8kHyInr2rKZ2aBv5ULw',
             'Luxiem':'UCtHFXfrn52juTqGBN4WbMVw',
             'Ryoma Barrenwort':'UCIzZDiilcPv0wim_MbuizFA',
             'Klara Charmwood':'UCQYwIUCLqFoin7lHKmePjJw',
             'Twisty Amanozako':'UCUI1qpjJSEbgzdlwmpdVmMw',
             'Freodore':'UCr40BzcLiGruKe7M5gXR9zQ',
             'Kaelix Debonair':'UCEFOogmvTTcCaO8Qe0I8-tg',
             'Seible':'UCCugV2RWXqJMjVVQl_Yh4TQ',
             'Zeal Ginjoka':'UClMYGvekJOb51eBOCK-d4Dw',
             'NIJISANJI EN Official':'UC-JSeFfovhNsEhftt1WHMvg',
             }

'''
#Dictionary of twitter id
#if someone doesn't have twitter account, id=0
tw_id_dic = {'Elira Pendora':1390620618001838086,\
             'Pomu Rainpuff':1390637197167038464,\
             'Finana Ryugu':1390209302120394754,\
             'Selen Tatsuki':1413318241804439552,\
             'Rosemi Lovelock':1413326894435602434,\
             'Petra Gurin':1413339084076978179,\
             'Enna Alouette':1437963160544284675,\
             'Nina Kosaka':1437959162651156484,\
             'Reimu Endou':1437961007029227520,\
             'Millie Parfait':1437952405283426310,\
             'Ike Eveland':1465851188562345985,\
             'Mysta Rias':1465851243167895554,\
             'Vox Akuma':1465851881180348425,\
             'Luca Kaneshiro':1465858739970273281,\
             'Shu Yamino':1465850835951357955,\
             'Alban Knox':1490867613915828224,\
             'Yugo Asuma':1492604168145539072,\
             'Fulgur Ovid':1493392149664219138,\
             'Sonny Brisko':1493394108014292993,\
             'Uki Violeta':1491195742123397124,\
             'Kyo Kaneko':1545552756773208066,\
             'Maria Marionette':1545351225293426688,\
             'Aster Arcadia':1545352592884084736 ,\
             'Aia Amare':1545562635650957312,\
             'Ren Zotto':1546328834559340544,\
             'Scarle Yonaguni':1545354510515654656,\
             'Doppio Dropscythe':1589531775058968576,\
             'Meloco Kyoran':1589536631324692480,\
             'Hex Haywire':1589524401170833409,\
             'Kotoka Torahime':1591995159901663232,\
             'Ver Vermillion':1589791076709171201,\
             'Yu Q. Wilson':1666980828432171013,\
             'Vantacrow Bringer':1668490052199120896,\
             'Vezalius Bandage':1666730751558139905,\
             'Luxiem':0,\
             'NIJISANJI EN Official':1214737620749578240,\
             }'''

'''
#Channel URL
#https://www.youtube.com/channel/***********
yt_url_dic = {'Elira Pendora':'https://www.youtube.com/channel/UCIeSUTOTkF9Hs7q3SGcO-Ow',\
              'Pomu Rainpuff':'https://www.youtube.com/channel/UCP4nMSTdwU1KqYWu3UH5DHQ',\
              'Finana Ryugu':'https://www.youtube.com/channel/UCu-J8uIXuLZh16gG-cT1naw',\
              'Selen Tatsuki':'https://www.youtube.com/channel/UCV1xUwfM2v2oBtT3JNvic3w',\
              'Rosemi Lovelock':'https://www.youtube.com/channel/UC4WvIIAo89_AzGUh1AZ6Dkg',\
              'Petra Gurin':'https://www.youtube.com/channel/UCgA2jKRkqpY_8eysPUs8sjw',\
              'Enna Alouette':'https://www.youtube.com/channel/UCR6qhsLpn62WVxCBK1dkLow',\
              'Nina Kosaka':'https://www.youtube.com/channel/UCkieJGn3pgJikVW8gmMXE2w',\
              'Reimu Endou':'https://www.youtube.com/channel/UCBURM8S4LH7cRZ0Clea9RDA',\
              'Millie Parfait':'https://www.youtube.com/channel/UC47rNmkDcNgbOcM-2BwzJTQ',\
              'Ike Eveland':'https://www.youtube.com/channel/UC4yNIKGvy-YUrwYupVdLDXA',\
              'Mysta Rias':'https://www.youtube.com/channel/UCIM92Ok_spNKLVB5TsgwseQ',\
              'Vox Akuma':'https://www.youtube.com/channel/UCckdfYDGrjojJM28n5SHYrA',\
              'Luca Kaneshiro':'https://www.youtube.com/channel/UC7Gb7Uawe20QyFibhLl1lzA',\
              'Shu Yamino':'https://www.youtube.com/channel/UCG0rzBZV_QMP4MtWg6IjhEA',\
              'Alban Knox':'https://www.youtube.com/channel/UCQ1zGxHrfEmmW4CPpBx9-qw',\
              'Yugo Asuma':'https://www.youtube.com/channel/UCSc_KzY_9WYAx9LghggjVRA',\
              'Fulgur Ovid':'https://www.youtube.com/channel/UCGhqxhovNfaPBpxfCruy9EA',\
              'Sonny Brisko':'https://www.youtube.com/channel/UCuuAb_72QzK0M1USPMEl1yw',\
              'Uki Violeta':'https://www.youtube.com/channel/UChJ5FTsHOu72_5OVx0rvsvQ',\
              'Kyo Kaneko':'https://www.youtube.com/channel/UCsb-1aJgiJXJH2feV-zlZRw',\
              'Maria Marionette':'https://www.youtube.com/channel/UCwaS8_S7kMiKA3izlTWHbQg',\
              'Aster Arcadia':'https://www.youtube.com/channel/UCpzxZW5kghGnO5TmAFJQAVw',\
              'Aia Amare':'https://www.youtube.com/channel/UCN68LoM3khS4gdBMiWJO8WA',\
              'Ren Zotto':'https://www.youtube.com/channel/UCKu59gTZ_rdEmerdx5rV4Yg',\
              'Scarle Yonaguni':'https://www.youtube.com/channel/UCFgXWZOUZA2oYHNr6qDmsTQ',\
             'Doppio Dropscythe':'https://www.youtube.com/channel/UCy91xBlY_Brh3bnHxKtjrrg',\
             'Meloco Kyoran':'https://www.youtube.com/channel/UChKXd7oqD18qiIYBoRIHTlw',\
             'Hex Haywire':'https://www.youtube.com/channel/UCz_ZRw6ak4Foy8zZy0kEprQ',\
             'Kotoka Torahime':'https://www.youtube.com/channel/UCggO2c1unS-oLwTLT0ICywg',\
             'Ver Vermillion':'https://www.youtube.com/channel/UCO8WcDsF5znr-qsXlzZNpqg',\
             'Yu Q. Wilson':'https://www.youtube.com/channel/UCKpKC3M5fkcEvtOr06dmYlA',\
             'Vantacrow Bringer':'https://www.youtube.com/channel/UCpYf6C9QsP_BRf97vLuXlIA',\
             'Vezalius Bandage':'https://www.youtube.com/channel/UCK9l6rTwU3hiSZijIMq51Gw',\
             'Luxiem':'https://www.youtube.com/channel/UCtHFXfrn52juTqGBN4WbMVw',\
             'NIJISANJI EN Official':'https://www.youtube.com/channel/UC-JSeFfovhNsEhftt1WHMvg',\
              }'''