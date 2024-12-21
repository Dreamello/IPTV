# -*- coding: utf-8 -*-
import re
import pytz
import requests
from lxml import html
from datetime import datetime, timezone, timedelta

tz = pytz.timezone('Asia/Shanghai')

cctv_channel = [
    'cctv1',
    'cctv2',
    'cctv3',
    'cctv4',
    'cctv5',
    'cctv5plus',
    'cctv6',
    'cctv7',
    'cctv8',
    'cctvjilu',
    'cctv10',
    'cctv11',
    'cctv12',
    'cctv13',
    'cctvchild',
    'cctv15',
    'cctv16',
    'cctv17',
    'cctv4k',
    'cctv8k'
]
sat_channel = [
    'btv1',
    'dongfang',
    'hunan',
    'zhejiang',
    'jiangsu'
]

cctv_channel_icons = [
    'https://dl.dropbox.com/scl/fi/f66g6r8zc4fk1s0rcz8uj/CCTV-1.png?rlkey=oaqjiuorsm24itduj1mb0h2x4',
    'https://dl.dropbox.com/scl/fi/i77vypvqqh45xupvq8t2e/CCTV-2.png?rlkey=z75f005mcihddool3zoqlpbhg',
    'https://dl.dropbox.com/scl/fi/piv5xkw3h7v051itfk466/CCTV-3.png?rlkey=wn2fnhqq7lr225hkjzryitmxo',
    'https://dl.dropbox.com/scl/fi/kwph5vi88eqn0m1ddfugr/CCTV-4.png?rlkey=2y6gq2e4relkryrz8kl82cde9',
    'https://dl.dropbox.com/scl/fi/fmx4cdtku7m82kvk2vnem/CCTV-5.png?rlkey=31hyu0eyuwg3afnnx423aiaua',
    'https://dl.dropbox.com/scl/fi/76qjq2mdibc1u1u2cicwz/CCTV-5p.png?rlkey=erm944a77q4fbergwukj0t0lz',
    'https://dl.dropbox.com/scl/fi/ig83r656ueg900aya6y4e/CCTV-6.png?rlkey=7iq5hm4hcvzxlkyw0ngvh94as',
    'https://dl.dropbox.com/scl/fi/zgn5nomgdfqcsrx8dpyuz/CCTV-7.png?rlkey=ykvd7g8a58qb34hlsvrb8soce',
    'https://dl.dropbox.com/scl/fi/lo2eilqj9c2ytkobcfjxf/CCTV-8.png?rlkey=yf4zt6of98bief5kr8bq4p0pk',
    'https://dl.dropbox.com/scl/fi/g2u12t5s5vgv7ijyt4odl/CCTV-9.png?rlkey=2frjdbz21cecx5gws63w8fesc',
    'https://dl.dropbox.com/scl/fi/pnmrc0ar6ab7x5u4r0io3/CCTV-10.png?rlkey=8bc8ji41ly22ltbqoh7ah32aa',
    'https://dl.dropbox.com/scl/fi/y3d7l132giu72l65j9blm/CCTV-11.png?rlkey=xa1yhas1l3una0uffwdkkbm2m',
    'https://dl.dropbox.com/scl/fi/4v1jxnjl0x9chavyk1q9k/CCTV-12.png?rlkey=i7qpsixrf2p399bwr2kfghj5d',
    'https://dl.dropbox.com/scl/fi/a26do3ce46ro37072ruzh/CCTV-13.png?rlkey=vf0zl90wtpb55gkflm3tdk15o',
    'https://dl.dropbox.com/scl/fi/cbt03i0hffgylxtsluopz/CCTV-14.png?rlkey=p6pqkcytkfn9hfy1hlueffor3',
    'https://dl.dropbox.com/scl/fi/gg5gm4m70o8g2ianuuikb/CCTV-15.png?rlkey=nph1c1bbjh2se8gj5iqgiyh4r',
    'https://dl.dropbox.com/scl/fi/b4nh973hdmq26br2zzmb4/CCTV-16_2.png?rlkey=f91r9q82cc20ju7ayhn74kjhq',
    'https://dl.dropbox.com/scl/fi/dikx7qt67xglqpgd1s4jw/CCTV-17.png?rlkey=fw6jibjbdizajf7ddlp4q9srr',
    'https://dl.dropbox.com/scl/fi/10ac6ewt6hd3fdspu4kpr/CCTV-4K.png?rlkey=vb1yw85o8s8u9xizk0pm0q8be',
    'https://dl.dropbox.com/scl/fi/sujeb9bcsgurrp15kegl0/CCTV-8K.png?rlkey=bsidcmjxs3taqni1j5kpyq3j8'
]
sat_channel_icons = [
    'https://dl.dropbox.com/scl/fi/dhtbhy67kr69k6uidz0rv/1.png?rlkey=8zjtxfmc1h4nrn3nn61wb9qtq',
    'https://dl.dropbox.com/scl/fi/ffac4toysvpi4ernq7wn1/.png?rlkey=f77saehqlsj5yx565tohhgzbl',
    'https://dl.dropbox.com/scl/fi/ihpbx4huat72oewdad6tv/.png?rlkey=d4afrv6tgtb2cinxdcz2dqvh3',
    'https://dl.dropbox.com/scl/fi/kaja88dfqj3pohywsnkbc/.png?rlkey=z42o7wd0j62l21177jgrnay4k',
    'https://dl.dropbox.com/scl/fi/c4xtybn40rqjeem0r9650/.png?rlkey=89p5voi56gyfc312cnpkbtz70'
]

def getChannelCNTV(fhandle, channelID, channel_icons):
    # change channelID list to str cids
    cids = ''
    for x in channelID:
        cids = cids + x + ','
    date = '%Y%m%d'
    epgdate = datetime.now(tz).strftime(date)
    session = requests.Session()
    api = f"http://api.cntv.cn/epg/epginfo?c={cids}&d={epgdate}"
    epgdata = session.get(api).json()

    for n in range(len(channelID)):
        # channelName = epgdata[channelID[n]]['channelName']
        fhandle.write(f'\t<channel id="{channelID[n]}">\n')
        fhandle.write(f'\t\t <display-name lang="cn">{epgdata[channelID[n]]["channelName"]}</display-name>\n')
        fhandle.write(f'\t\t <icon src="{channel_icons[n]}" />\n')
        fhandle.write('\t</channel>\n')


def getChannelEPG(fhandle, channelID):
    date = '%Y%m%d'
    epgdate = [
        (datetime.now(tz) + timedelta(days=-2)).strftime(date),
        (datetime.now(tz) + timedelta(days=-1)).strftime(date),
        datetime.now(tz).strftime(date),
        (datetime.now(tz) + timedelta(days=1)).strftime(date),
        (datetime.now(tz) + timedelta(days=2)).strftime(date),
    ];

    cids = ''
    for x in channelID:
        cids = cids + x + ','

    for k in epgdate:
        session = requests.Session()
        api = f"http://api.cntv.cn/epg/epginfo?c={cids}&d={k}"
        epgdata = session.get(api).json()
        for n in range(len(channelID)):
            name = epgdata[channelID[n]]['channelName']
            program = epgdata[channelID[n]]['program']
            for detail in program:
                # write programe
                st = datetime.fromtimestamp(detail['st']).strftime('%Y%m%d%H%M') + '00'
                et = datetime.fromtimestamp(detail['et']).strftime('%Y%m%d%H%M') + '00'

                fhandle.write(f'\t<programme start="{st} +0800" stop="{et} +0800" channel="{channelID[n]}">\n')
                fhandle.write(f'\t\t<title lang="zh">{detail["t"]}</title>\n')
                fhandle.write(f'\t\t<desc lang="zh"></desc>\n')
                fhandle.write('\t</programme>\n')

def getsave():
    # 参数 w 表示覆盖，追加用 at (追加+文本)
    with open('epg.xml', 'w', encoding='utf-8') as fhandle:
        fhandle.write('<?xml version="1.0" encoding="utf-8" ?>\n')
        fhandle.write('<tv generator-info-name="Dreamello" generator-info-url="https://github.com/Dreamello/IPTV">\n')
        getChannelCNTV(fhandle, cctv_channel, cctv_channel_icons)
        getChannelCNTV(fhandle, sat_channel, sat_channel_icons)
        getChannelEPG(fhandle, cctv_channel)
        getChannelEPG(fhandle, sat_channel)
        fhandle.write('</tv>')

if __name__ == '__main__':
    getsave()
    print('获取完成！')
