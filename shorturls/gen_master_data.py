from shorturls.models import BlockedDomain


def gen_master(apps, schema_editor):
    blocked_domains = ['abit.ly', 'adf.ly', 'apple.co', 'asq.kr', 'bit.ly', 'blow.pw', 'c11.kr', 'cco.kr', 'coc.kr',
                       'coe.kr', 'coi.kr', 'coj.kr', 'coz.jp', 'cutt.ly', 'ddd.kr', 'di.do', 'do.co', 'dok.do',
                       'durl.kr', 'durl.me', 'fco.kr', 'fff.kr', 'flic.kr', 'fw.sg', 'gg.gg', 'goo.gl', 'gtz.kr',
                       'han.gl', 'hana.icu', 'hit.re', 'hoy.kr', 'ior.kr', 'kisu.me', 'koe.kr', 'lco.jp', 'lrl.kr',
                       'me2.do', 'me2.kr', 'mlnl.me', 'muz.so', 'na.to', 'naver.me', 'nazr.in', 'new.so', 'oco.kr',
                       'ore.kr', 'ppl.kr', 'ppp.kr', 'qops.xtz', 'reurl.kr', 'ror.kr', 'rotf.lol', 'sco.kr', 'sou.kr',
                       't.co', 't2m.kr', 'tiny.one', 'tor.kr', 'twr.kr', 'url.kr', 'url.sg', 'vco.kr', 'vo.la',
                       'vot.kr', 'vvd.bz', 'vvv.kr', 'wiv.kr', 'wo.to', 'xco.kr', 'zas.kr']
    for blocked_domain in blocked_domains:
        BlockedDomain(domain=blocked_domain).save()
