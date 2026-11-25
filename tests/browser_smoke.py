"""Built app interaction coverage. Mocked NASA data exists only in this test."""
from functools import partial
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
import json,os,shutil,tempfile,threading
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parents[1]
class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self,*args):pass

def main():
    screenshots=ROOT/'browser-checks';screenshots.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory() as temp:
        shutil.copytree(ROOT/'dist',Path(temp)/'missionmedia')
        server=ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=temp));threading.Thread(target=server.serve_forever,daemon=True).start()
        try:
            with sync_playwright() as p:
                browser=p.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH'));page=browser.new_page(viewport={'width':1280,'height':1000});errors=[]
                page.on('pageerror',lambda e:errors.append(str(e)))
                item={'data':[{'nasa_id':'test-mission','title':'Unlisted mission footage','media_type':'video','date_created':'1972-01-01T00:00:00Z','center':'JSC','description':'<img src=x onerror=alert(1)>Safe source description'}],'links':[]}
                page.route('https://images-api.nasa.gov/search*',lambda r:r.fulfill(json={'collection':{'metadata':{'total_hits':1},'items':[item]}}))
                page.route('https://images-api.nasa.gov/asset/*',lambda r:r.fulfill(json={'collection':{'items':[{'href':'https://images-assets.nasa.gov/video/test-mission/test-mission~orig.mp4'},{'href':'https://images-assets.nasa.gov/video/test-mission/test-mission~small.mp4'}]}}))
                page.route('https://images-api.nasa.gov/metadata/*',lambda r:r.fulfill(json={'location':'https://images-assets.nasa.gov/video/test-mission/metadata.json'}))
                page.route('https://images-api.nasa.gov/captions/*',lambda r:r.fulfill(json={'location':'https://images-assets.nasa.gov/video/test-mission/captions.vtt'}))
                page.route('https://images-assets.nasa.gov/**',lambda r:r.abort());page.route('https://coolcode.ca/**',lambda r:r.abort())
                page.goto(f'http://127.0.0.1:{server.server_port}/missionmedia/')
                page.locator('#query').fill('Unlisted deep space subject');page.locator('#media-type').select_option('video');page.locator('#year-start').fill('1960');page.get_by_role('button',name='Search NASA',exact=True).click()
                expect(page.locator('#results .card')).to_have_count(1);page.get_by_role('button',name='Inspect & collect').click()
                expect(page.get_by_role('link',name='Original · MP4 ↗')).to_have_attribute('href','https://images-assets.nasa.gov/video/test-mission/test-mission~orig.mp4')
                expect(page.get_by_role('link',name='Open source captions ↗')).to_be_visible();assert page.locator('#detail img').count()==0
                page.locator('#board-name').fill('Research outside defaults');page.locator('#research-notes').fill('Keep these notes private.');page.get_by_role('button',name='Save to board',exact=True).click();expect(page.locator('#detail-status')).to_contain_text('Saved on this device')
                page.locator('[data-tab="boards"]').click();expect(page.locator('#boards .card')).to_have_count(1)
                with page.expect_download() as d:page.locator('#export-json').click()
                exported=json.loads(Path(d.value.path()).read_text());assert exported['items'][0]['notes']=='Keep these notes private.'
                with page.expect_download() as d:page.locator('#export-credits').click()
                assert 'NASA / JSC' in Path(d.value.path()).read_text()
                page.locator('#import').set_input_files({'name':'bad.json','mimeType':'application/json','buffer':b'{}'});expect(page.locator('#board-status')).to_contain_text('Import failed')
                extra={'schema':'missionmedia.boards.v1','items':[{'id':'extra-new-id','type':'audio','title':'Additional beyond presets','board':'Independent board'}]}
                page.locator('#import').set_input_files({'name':'extra.json','mimeType':'application/json','buffer':json.dumps(extra).encode()});expect(page.locator('#boards .card')).to_have_count(2);expect(page.locator('#board-status')).to_contain_text('Imported 1')
                page.reload();page.locator('[data-tab="boards"]').click();expect(page.locator('#boards .card')).to_have_count(2)
                page.locator('#board-filter').select_option(label='Research outside defaults');expect(page.locator('#boards .card')).to_have_count(1)
                page.screenshot(path=str(screenshots/'desktop.png'),full_page=True);page.set_viewport_size({'width':390,'height':844});assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth');page.screenshot(path=str(screenshots/'mobile.png'),full_page=True)
                page.route('https://images-api.nasa.gov/search*',lambda r:r.fulfill(status=503,body='unavailable'))
                page.locator('[data-tab="search"]').click();page.get_by_role('button',name='Search NASA',exact=True).click();expect(page.locator('#search-status')).to_contain_text('HTTP 503')
                assert not errors,errors;browser.close()
            print('Browser checks passed: arbitrary NASA search, originals/captions, safe content, boards persistence/import/export, source failure, mobile')
        finally:server.shutdown()
if __name__=='__main__':main()
