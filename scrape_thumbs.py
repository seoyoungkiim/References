import requests
from bs4 import BeautifulSoup
import json
import concurrent.futures
from urllib.parse import urljoin, urlparse

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
}

SITES = [
  # STUDIO
  {"name":"Koto","url":"https://koto.com/work","c":"studio"},
  {"name":"Veryes","url":"https://www.veryes.co","c":"studio"},
  {"name":"Lundgren+Lindqvist","url":"https://www.lundgrenlindqvist.se","c":"studio"},
  {"name":"Ro & Co Studio","url":"https://www.roandcostudio.com","c":"studio"},
  {"name":"Yukiko","url":"https://y-u-k-i-k-o.com","c":"studio"},
  {"name":"Porto Rocha","url":"https://portorocha.com","c":"studio"},
  {"name":"Studio Lin","url":"https://studiolin.org/projects","c":"studio"},
  {"name":"Stereo Buro","url":"https://stereo-buro.com","c":"studio"},
  {"name":"Only Studio","url":"https://www.onlystudio.com/work","c":"studio"},
  {"name":"Ohezin","url":"https://ohezin.kr","c":"studio"},
  {"name":"Neoneo","url":"https://www.neoneo.ch","c":"studio"},
  {"name":"Hannah Kansy","url":"https://hannahkansy.de","c":"studio"},
  {"name":"Anna Haas","url":"http://annahaas.ch","c":"studio"},
  {"name":"Chloe Scheffe","url":"https://chloescheffe.github.io/about.html","c":"studio"},
  {"name":"Claudia Rubin","url":"https://claudiarubin.com","c":"studio"},
  {"name":"Studio Dumbar","url":"https://studiodumbar.com/work","c":"studio"},
  {"name":"New Studio","url":"https://newstudio.studio","c":"studio"},
  {"name":"Felipe Goes","url":"https://felipegoes.com/work","c":"studio"},
  {"name":"Studio Fludd","url":"https://www.studiofludd.com","c":"studio"},
  {"name":"Kiatas","url":"https://www.kiatas.me","c":"studio"},
  {"name":"Bureau Borsche","url":"https://bureauborsche.com","c":"studio"},
  {"name":"Lea Johanna Becker","url":"https://www.leajohannabecker.com","c":"studio"},
  {"name":"Uniforma","url":"https://www.uniforma.pl","c":"studio"},
  {"name":"Hato","url":"https://hato.co","c":"studio"},
  {"name":"Astrae Studio","url":"https://astrae.studio","c":"studio"},
  {"name":"Ohara Daijiro","url":"https://oharadaijiro.com/projects","c":"studio"},
  {"name":"Bureau Progressiv","url":"https://bureau-progressiv.com","c":"studio"},
  {"name":"Raoul Gottschling","url":"https://raoulgottschling.de/typefaces","c":"studio"},
  {"name":"Sea Change Studio","url":"https://www.seachange.studio/work","c":"studio"},
  {"name":"Heydays","url":"https://heydays.no","c":"studio"},
  {"name":"Simon Sweeney","url":"https://simonsweeney.me","c":"studio"},
  {"name":"Buenaventura Studio","url":"https://buenaventura.studio/projects","c":"studio"},
  {"name":"Type Department","url":"https://type-department.com","c":"studio"},
  {"name":"Kai Udema","url":"http://kaiudema.com","c":"studio"},
  {"name":"Ella-la","url":"https://ella-la.com","c":"studio"},
  {"name":"Heidlmair","url":"https://heidlmair.com","c":"studio"},
  {"name":"Puncture","url":"https://puncture.co/tas","c":"studio"},
  {"name":"Studio Naeo","url":"https://studionaeo.com/works","c":"studio"},
  {"name":"Studio Mistaker","url":"https://www.studiomistaker.com","c":"studio"},
  {"name":"Seri Tanaka","url":"https://seritanaka.com","c":"studio"},
  {"name":"Oliver Helfrich","url":"https://www.oliverhelfrich.com","c":"studio"},
  {"name":"Underline Studio","url":"https://underlinestudio.com","c":"studio"},
  {"name":"Raffinerie","url":"https://raffinerie.com","c":"studio"},
  {"name":"Thonik","url":"https://thonik.nl","c":"studio"},
  {"name":"Polarno","url":"https://www.polarno.jp","c":"studio"},
  {"name":"Odotoo","url":"https://odotoo.com","c":"studio"},
  {"name":"Annik Troxler","url":"https://www.anniktroxler.ch/work","c":"studio"},
  {"name":"Okamoto Ken","url":"https://www.okamotoken.jp/works","c":"studio"},
  {"name":"Diego Gildebiedma","url":"https://diegogildebiedma.com","c":"studio"},
  {"name":"MOA · Repponen","url":"https://moa.repponen.com","c":"studio"},
  {"name":"Lucas Garrido","url":"https://lucasgarrido.com/fallen-angels","c":"studio"},
  {"name":"Depass Montgomery","url":"https://depassmontgomery.com","c":"studio"},
  {"name":"Marnich","url":"http://www.marnich.com","c":"studio"},
  {"name":"Qubik","url":"https://qubik.com/zr","c":"studio"},
  {"name":"Studio C","url":"https://www.studioc.dk","c":"studio"},
  # FONT
  {"name":"Ddott — Aether Mono","url":"https://ddott.net/font/aether-mono","c":"font"},
  {"name":"Lift Type","url":"https://www.lift-type.fr","c":"font"},
  {"name":"Typografische","url":"https://www.typografische.com/typefaces","c":"font"},
  {"name":"Eliott Grunewald","url":"https://eliottgrunewald.xyz","c":"font"},
  {"name":"Commercial Type","url":"https://commercialtype.com/catalog","c":"font"},
  {"name":"A2-Type","url":"https://a2-type.co.uk","c":"font"},
  {"name":"Lineto","url":"https://lineto.com","c":"font"},
  {"name":"Fros Type","url":"https://www.frostype.xyz/typefaces","c":"font"},
  {"name":"Pangram Pangram","url":"https://pangrampangram.com","c":"font"},
  {"name":"Bilik Tufo Foundry","url":"https://biliktufoundry.com","c":"font"},
  {"name":"Off-Type","url":"https://off-type.com","c":"font"},
  {"name":"Sharp Type","url":"https://www.sharptype.co","c":"font"},
  {"name":"S-M","url":"https://s-m.nu","c":"font"},
  {"name":"Tomorrow","url":"https://tomorrow.type.today/en","c":"font"},
  {"name":"P22","url":"https://p22.com","c":"font"},
  {"name":"Out of the Dark","url":"https://www.outofthedark.swiss","c":"font"},
  {"name":"Future Fonts","url":"https://www.futurefonts.xyz","c":"font"},
  {"name":"Typotheque","url":"https://www.typotheque.com/fonts","c":"font"},
  {"name":"Maxitype","url":"https://maxitype.com","c":"font"},
  {"name":"Skriftkompani","url":"https://skriftkompani.no","c":"font"},
  {"name":"Celine Hurka","url":"https://celine-hurka.com","c":"font"},
  {"name":"Grilli Type","url":"https://www.grillitype.com","c":"font"},
  {"name":"Playtype","url":"https://playtype.com/typefaces","c":"font"},
  {"name":"Ultra Kuhl","url":"https://ultra-kuhl.com/en/collections","c":"font"},
  {"name":"Colophon Foundry","url":"https://www.colophon-foundry.org","c":"font"},
  {"name":"Or Type","url":"https://ortype.is/poem","c":"font"},
  {"name":"Velvetyne","url":"https://velvetyne.fr","c":"font"},
  {"name":"Alex Creq","url":"https://alex-creq.com/typefaces","c":"font"},
  {"name":"Querida","url":"https://querida.si","c":"font"},
  {"name":"Briefcase Type","url":"https://www.briefcasetype.com","c":"font"},
  {"name":"Monotype","url":"https://www.monotypefonts.com","c":"font"},
  {"name":"Formagari","url":"https://formagari.com","c":"font"},
  {"name":"Old City Mailroom","url":"https://www.oldcitymailroom.com/font-shop","c":"font"},
  {"name":"OH no Type","url":"https://ohnotype.co","c":"font"},
  {"name":"Character Type","url":"https://charactertype.com","c":"font"},
  {"name":"BVH Type","url":"https://bvhtype.com","c":"font"},
  {"name":"Giulia Boggio","url":"https://www.giuliaboggio.xyz/shop","c":"font"},
  {"name":"Displaay","url":"https://displaay.net","c":"font"},
  {"name":"Vocal Type","url":"https://www.vocaltype.co","c":"font"},
  {"name":"Radim Pesko","url":"https://radimpesko.com/fonts/larish-alte","c":"font"},
  {"name":"By Meg Burk","url":"https://www.bymegburk.com","c":"font"},
  {"name":"KH Type","url":"https://khtype.com","c":"font"},
  # AGENCY
  {"name":"Matte Projects","url":"https://matteprojects.com/projects","c":"agency"},
  {"name":"ANG Studio","url":"https://ang-studio.com","c":"agency"},
  {"name":"Matchstic","url":"https://matchstic.com","c":"agency"},
  {"name":"Gabby Lord","url":"https://gabbylord.com","c":"agency"},
  {"name":"CGH NYC","url":"https://www.cghnyc.com","c":"agency"},
  {"name":"Polar","url":"https://polar.ltda","c":"agency"},
  {"name":"2x4","url":"https://2x4.org","c":"agency"},
  {"name":"Husky Fox","url":"https://huskyfox.com","c":"agency"},
  {"name":"Turner Duckworth","url":"https://turnerduckworth.com","c":"agency"},
  {"name":"Ogilvy","url":"https://www.ogilvy.com","c":"agency"},
  {"name":"Dia","url":"https://dia.tv","c":"agency"},
  {"name":"Stockholm Design Lab","url":"https://www.stockholmdesignlab.se","c":"agency"},
  {"name":"SMLXL","url":"https://www.smlxl.company/projects","c":"agency"},
  {"name":"Wolff Olins","url":"https://wolffolins.com/work","c":"agency"},
  {"name":"Bleed","url":"https://bleed.com","c":"agency"},
  {"name":"Area 17","url":"https://area17.com/work","c":"agency"},
  {"name":"Collins","url":"https://www.wearecollins.com","c":"agency"},
  {"name":"The Gaabs","url":"https://www.thegaabs.com","c":"agency"},
  {"name":"Z-O-O","url":"https://z-o-o.fr/en","c":"agency"},
  {"name":"JKR Global","url":"https://www.jkrglobal.com","c":"agency"},
  {"name":"Eggplant Factory","url":"https://www.eggplantfactory.co.kr","c":"agency"},
  {"name":"Oker","url":"https://oker.com","c":"agency"},
  {"name":"Gretel","url":"https://gretelny.com","c":"agency"},
  {"name":"VanderBrand","url":"https://vanderbrand.com","c":"agency"},
  {"name":"Bibliotheque","url":"https://bibliothequedesign.com","c":"agency"},
  {"name":"MR Design","url":"https://mr-design.jp/works","c":"agency"},
  {"name":"CCRZ","url":"https://ccrz.ch","c":"agency"},
  {"name":"Made Thought","url":"https://www.madethought.com","c":"agency"},
  {"name":"Bttr Hlf","url":"https://bttrhlf.com","c":"agency"},
  {"name":"Rivermeade","url":"https://www.rivermeade.com/portfolio","c":"agency"},
]

def make_absolute(img_url, base_url):
    if not img_url:
        return None
    img_url = img_url.strip()
    if img_url.startswith('data:'):
        return None
    if img_url.startswith('//'):
        return 'https:' + img_url
    if img_url.startswith('http'):
        return img_url
    return urljoin(base_url, img_url)

def get_thumb(site):
    url = site['url']
    name = site['name']
    try:
        r = requests.get(url, headers=HEADERS, timeout=12, allow_redirects=True)
        soup = BeautifulSoup(r.text, 'lxml')

        # Priority order for meta image tags
        selectors = [
            ('meta', {'property': 'og:image'}),
            ('meta', {'property': 'og:image:url'}),
            ('meta', {'name': 'twitter:image'}),
            ('meta', {'name': 'twitter:image:src'}),
            ('meta', {'property': 'twitter:image'}),
        ]
        for tag, attrs in selectors:
            el = soup.find(tag, attrs)
            if el:
                content = el.get('content') or el.get('value')
                if content:
                    abs_url = make_absolute(content, r.url)
                    if abs_url:
                        print(f"  ✓  {name}")
                        return {**site, 'thumb': abs_url}

        print(f"  ✗  {name} — no og:image")
        return {**site, 'thumb': None}

    except Exception as e:
        print(f"  !  {name} — {type(e).__name__}")
        return {**site, 'thumb': None}

print(f"Fetching {len(SITES)} sites in parallel…\n")
results = []
with concurrent.futures.ThreadPoolExecutor(max_workers=20) as ex:
    futs = {ex.submit(get_thumb, s): s for s in SITES}
    for fut in concurrent.futures.as_completed(futs):
        results.append(fut.result())

# Sort back to original order
order = {s['url']: i for i, s in enumerate(SITES)}
results.sort(key=lambda r: order.get(r['url'], 999))

found = sum(1 for r in results if r['thumb'])
print(f"\n── {found}/{len(results)} images found ──")

with open('/sessions/modest-affectionate-sagan/mnt/outputs/thumbnails.json', 'w') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print("Saved to thumbnails.json")
