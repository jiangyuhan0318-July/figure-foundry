"""Build an offline gallery viewer and a Chinese file index."""
from html import escape
import json
from pathlib import Path


def main():
    root=Path(__file__).resolve().parent
    report=json.loads((root/"gallery_checks.json").read_text(encoding="utf-8"))
    items=[r for r in report["records"] if r["kind"]!="contact_sheet"]
    groups=["比较与变化","分布与关系","科研分析","组成与结构"]
    cards=[]
    for item in items:
        slug=item["id"];zh=escape(item["title_zh"]);en=escape(item["title"])
        links=" · ".join(f'<a href="figures/{slug}.{ext}" target="_blank">{ext.upper()}</a>' for ext in ["png","svg","pdf"])
        cards.append(f'''<article class="card" data-group="{item['group']}" data-search="{zh} {en}">
<button class="thumb" data-slug="{slug}" data-title="{zh}"><img src="figures/{slug}.png" loading="lazy" alt="{zh}"></button>
<div class="copy"><span class="num">{slug[:2]}</span><h2>{zh}</h2><p>{en}</p><small>{escape(item['note'])}</small><footer>{links}</footer></div></article>''')
    filters='<button class="active" data-filter="0">全部 24 种</button>'+''.join(f'<button data-filter="{i+1}">{name}</button>' for i,name in enumerate(groups))
    template='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>FigureFoundry · 图形画廊</title>
<style>
:root{color-scheme:light;--ink:#26313d;--muted:#687681;--line:#e1e6ea;--orange:#f29440}
*{box-sizing:border-box}body{margin:0;background:#f7f8fa;color:var(--ink);font:15px/1.6 system-ui,"Microsoft YaHei",sans-serif}
main{max-width:1400px;margin:auto;padding:46px 30px}header h1{margin:0;font-size:clamp(30px,4vw,48px);letter-spacing:-1.6px}
header p{color:var(--muted);margin:8px 0 22px}.eyebrow{font-size:12px;letter-spacing:2px;color:#a85e24;font-weight:700}
nav{display:flex;gap:9px;flex-wrap:wrap;align-items:center;margin:26px 0 30px}button,input{font:inherit}
nav button{border:1px solid var(--line);background:white;border-radius:20px;padding:7px 16px;cursor:pointer;color:var(--ink)}
nav button.active{background:var(--ink);border-color:var(--ink);color:white}input{margin-left:auto;border:1px solid var(--line);border-radius:8px;padding:8px 12px;width:230px;background:white}
.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:22px}.card{background:white;border:1px solid var(--line);border-radius:12px;overflow:hidden}
.card[hidden]{display:none}.thumb{display:block;background:white;width:100%;padding:0;border:0;cursor:zoom-in}.thumb img{display:block;width:100%;aspect-ratio:6.4/4.7;object-fit:contain}
.copy{padding:15px 20px 20px;border-top:1px solid #f0f2f4}.num{font-size:11px;font-weight:700;color:#a85e24}.copy h2{font-size:18px;margin:2px 0 0}.copy p{margin:1px 0 7px;color:var(--muted);font-size:13px}.copy small{display:block;min-height:40px;color:var(--muted);font-size:11px}.copy footer{margin-top:12px;font-size:12px}a{color:#246180;text-decoration:none}a:hover{text-decoration:underline}
.notice{margin:32px 0 0;padding-top:18px;border-top:1px solid var(--line);font-size:12px;color:var(--muted)}
dialog{width:min(1200px,96vw);max-height:96vh;border:0;border-radius:12px;padding:14px;background:white;color:var(--ink)}dialog::backdrop{background:#17212bbd}
.viewerbar{display:flex;align-items:center;gap:10px;padding:0 4px 8px}.viewerbar strong{margin-right:auto}.viewerbar button{border:1px solid var(--line);background:white;border-radius:7px;padding:5px 12px;cursor:pointer}dialog img{display:block;width:100%;max-height:82vh;object-fit:contain}
@media(max-width:1050px){.grid{grid-template-columns:repeat(2,minmax(0,1fr))}input{margin-left:0}}@media(max-width:650px){main{padding:28px 16px}.grid{grid-template-columns:1fr}nav{gap:7px}nav button{padding:6px 11px}input{width:100%}}
</style><main><header><div class="eyebrow">FIGUREFOUNDRY / 图件工坊</div><h1>24 种图型，一次看清。</h1>
<p>点击任一图片放大；方向键切换。三组个人配色，四类用途，每张都附 PNG、SVG、PDF。</p></header>
<nav>FILTERS<input id="search" aria-label="搜索图型" placeholder="搜索：热图 / ROC / 架构…"></nav><section class="grid">CARDS</section>
<div class="notice">所有数值均为固定随机种子生成的合成数据，结构图使用虚构关系。统计量从这些输入实际计算，不代表真实实验。<br>
<a href="GALLERY.md">中文图型索引</a> · <a href="synthetic_data.json">源数据</a> · <a href="render_gallery.py">绘图代码</a> · <a href="gallery_checks.json">绘图记录</a></div></main>
<dialog id="viewer"><div class="viewerbar"><strong id="viewer-title"></strong><button id="prev" aria-label="上一张">←</button><button id="next" aria-label="下一张">→</button><button id="close">关闭</button></div><img id="viewer-image" alt=""></dialog>
<script>
const cards=[...document.querySelectorAll('.card')], thumbs=[...document.querySelectorAll('.thumb')], dialog=document.querySelector('#viewer');let group='0',index=0;
function filter(){const q=document.querySelector('#search').value.trim().toLowerCase();cards.forEach(c=>c.hidden=(group!=='0'&&c.dataset.group!==group)||!c.dataset.search.toLowerCase().includes(q))}
document.querySelectorAll('[data-filter]').forEach(b=>b.onclick=()=>{group=b.dataset.filter;document.querySelectorAll('[data-filter]').forEach(x=>x.classList.toggle('active',x===b));filter()});document.querySelector('#search').oninput=filter;
function show(i){index=(i+thumbs.length)%thumbs.length;const b=thumbs[index];document.querySelector('#viewer-image').src='figures/'+b.dataset.slug+'.png';document.querySelector('#viewer-image').alt=b.dataset.title;document.querySelector('#viewer-title').textContent=String(index+1).padStart(2,'0')+' / '+b.dataset.title;if(!dialog.open)dialog.showModal()}
thumbs.forEach((b,i)=>b.onclick=()=>show(i));document.querySelector('#prev').onclick=()=>show(index-1);document.querySelector('#next').onclick=()=>show(index+1);document.querySelector('#close').onclick=()=>dialog.close();
document.addEventListener('keydown',e=>{if(dialog.open&&e.key==='ArrowLeft')show(index-1);if(dialog.open&&e.key==='ArrowRight')show(index+1)});
</script></html>'''
    (root/"index.html").write_text(template.replace('FILTERS',filters).replace('CARDS','\n'.join(cards)),encoding="utf-8")
    md=['# FigureFoundry：24种图型画廊','', '[浏览版画廊](index.html) · [返回项目首页](../README.md)','',
        '固定随机种子261026。所有数值为合成数据，网络/流程/架构使用虚构关系。每张图均从保存的JSON读取输入；PNG、SVG、PDF来自同一绘图场景。','',
        '本次实际生成21种数据图与3种示意图，不声称穷尽所有专业图型。PPTX与原生draw.io编辑本次未验证。','']
    for i,name in enumerate(groups,1):
        md += [f'## {i}. {name}','',f'![{name}](gallery_{i:02d}.png)','', '| 编号 | 图型 | 常见用途 | 文件 |','|---|---|---|---|']
        for item in [x for x in items if x['group']==i]:
            slug=item['id'];links=' · '.join(f'[{e.upper()}](figures/{slug}.{e})' for e in ['png','svg','pdf'])
            md.append(f"| {slug[:2]} | {item['title_zh']} | {item['note']} | {links} |")
        md.append('')
    md += ['## 数据、统计与复跑','',
           '- 分组柱状/趋势：各单元8次模拟运行，显示均值±样本SD。配对图：14个匹配单位。森林图：每行12个配对差值的95% t区间。',
           '- 箱线/小提琴/直方：每组60个样本；山脊图每批120个样本；回归图90个观测，阴影为均值响应的95%区间。',
           '- PCA实际采用标准化输入的SVD；ROC/PR来自120阳性、280阴性的预测分数；火山图实际进行Welch检验与BH校正。',
           '- 生存曲线由每队列60个事件/删失记录计算；本例时间不重复，未展示置信区间；不作为临床分析工具。',
           '- 堆叠组成与面积图均核对总和100%；雷达图全部坐标都是人为指定的0–100“越高越好”分数。',
           '- 模型图的实线为数据流、虚线为训练专用路径；流程图的虚线为返回修改；网络图不表达真实生物或因果关系。','',
           '```bash','python gallery/generate_data.py','python gallery/render_gallery.py','python gallery/build_index.py','```','',
           '从项目根目录运行，默认使用已安装的`figure-foundry`。也可向绘图脚本传入`--skill-dir skill/figure-foundry`，使用项目内便携副本。',
           '', '完整输入：[synthetic_data.json](synthetic_data.json)；源代码：[生成器](generate_data.py)、[绘图脚本](render_gallery.py)；过程：[gallery_checks.json](gallery_checks.json)。']
    (root/"GALLERY.md").write_text('\n'.join(md)+'\n',encoding="utf-8")
    english_groups=["Comparisons and change","Distributions and relationships","Scientific analysis","Composition and structure"]
    en=['# FigureFoundry example gallery','', '[Project home](../README.md) · [中文图型索引](GALLERY.md) · [Offline HTML viewer](index.html)','',
        '24 individual examples: 21 numerical plots and three editable schematics. All numerical inputs are seeded synthetic data (seed 261026); schematic relationships are fictional. Each PNG, SVG and PDF comes from the same plotting scene.','']
    for i,name in enumerate(english_groups,1):
        en += [f'## {i}. {name}','',f'![{name}](gallery_{i:02d}.png)','', '| ID | Figure type | Input or calculation | Exports |','|---|---|---|---|']
        for item in [x for x in items if x['group']==i]:
            slug=item['id'];links=' · '.join(f'[{e.upper()}](figures/{slug}.{e})' for e in ['png','svg','pdf'])
            en.append(f"| {slug[:2]} | {item['title']} | {item['note']} | {links} |")
        en.append('')
    en += ['## Reproduce and inspect','',
           'From the repository root, install the pinned requirements and run:','', '```bash','python gallery/generate_data.py','python gallery/render_gallery.py --skill-dir skill/figure-foundry','python gallery/build_index.py','python gallery/verify_gallery.py','```','',
           'Inputs: [JSON](synthetic_data.json). Source: [generator](generate_data.py), [renderer](render_gallery.py). Checks: [verification](verification.json), [verification script](verify_gallery.py).','',
           'Bars and trends show mean ± sample SD across eight simulated runs. Forest intervals use 12 paired differences per row and a 95% t interval. Regression shading is a 95% interval for the mean response. ROC/AP, PCA, Welch tests/BH correction and survival curves are calculated from the saved inputs. Stacked compositions total 100%. Radar axes use assigned 0–100 benefit scores.','',
           'Network edges are toy associations. The decision workflow uses a dashed retry path. Model architecture uses solid data flow and dashed training-only paths.','',
           'The Kaplan–Meier example uses untied event times. Native PPTX/draw.io/Origin output was not run. HTML asset links were checked; viewer interaction was not browser-tested.']
    (root/"README.md").write_text('\n'.join(en)+'\n',encoding="utf-8")
    print('Built offline HTML gallery and English/Chinese indexes for 24 examples.')


if __name__=="__main__":main()
