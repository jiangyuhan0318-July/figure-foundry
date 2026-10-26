"""Check the saved gallery outputs and cross-check displayed calculations."""
import json
from pathlib import Path
from xml.etree import ElementTree as ET
from html.parser import HTMLParser
import numpy as np
from scipy import stats
from sklearn.metrics import roc_auc_score, average_precision_score
from sklearn.decomposition import PCA
from PIL import Image
from pypdf import PdfReader
import render_gallery as render


def main():
    root = Path(__file__).resolve().parent
    data = json.loads((root/"synthetic_data.json").read_text(encoding="utf-8"))
    records = json.loads((root/"gallery_checks.json").read_text(encoding="utf-8"))["records"]
    assert len(records) == 28 and all(not r["text_outside_canvas"] for r in records)
    metrics = []
    truth = data["classification"]["truth"]
    for i, score in enumerate(data["classification"]["scores"], 1):
        _, _, recall, precision, auc, ap = render.classification_curves(truth, score)
        assert np.isclose(auc, roc_auc_score(truth, score), atol=1e-12)
        assert np.isclose(ap, average_precision_score(truth, score), atol=1e-12)
        assert np.isclose(ap, np.sum(np.diff(recall)*precision[1:]), atol=1e-12)
        metrics.append({"model": i, "roc_auc": auc, "average_precision": ap})
    a = np.array(data["volcano"]["control"]); b = np.array(data["volcano"]["treated"])
    p = stats.ttest_ind(b, a, axis=1, equal_var=False).pvalue
    q = render.bh_adjust(p)
    assert np.allclose(q, stats.false_discovery_control(p, method="bh"), atol=1e-12)
    effect = b.mean(1)-a.mean(1)
    volcano = {"down": int(np.sum((q < .05) & (effect < -1))), "up": int(np.sum((q < .05) & (effect > 1)))}
    volcano["other"] = len(q)-sum(volcano.values())
    x = np.array(data["pca"]["x"]); x = (x-x.mean(0))/x.std(0, ddof=1)
    s = np.linalg.svd(x, full_matrices=False)[1]; explained = s*s/np.sum(s*s)
    assert np.allclose(explained, PCA().fit(x).explained_variance_ratio_, atol=1e-12)
    assert np.allclose(np.sum(data["composition"], axis=2), 1)
    assert np.allclose(np.sum(data["area"]["fractions"], axis=0), 1)
    waterfall = data["waterfall"]["start"]+sum(data["waterfall"]["changes"])
    assert waterfall == 122
    survival = []
    for cohort in data["survival"]:
        time, event = np.array(cohort["time"]), np.array(cohort["event"])
        assert len(np.unique(time)) == len(time)
        t, y, cx, _ = render.km_curve(time, event)
        # Independent risk-set product at each event time; valid for these untied inputs.
        expected = np.prod([1-1/np.sum(time >= v) for v in time[event == 1]])
        assert y[0] == 1 and np.all(np.diff(y) <= 0) and np.all((y >= 0) & (y <= 1))
        assert np.isclose(y[-1], expected) and len(cx) == int(np.sum(event == 0))
        survival.append({"n": len(time), "events": int(sum(event)), "censored": len(cx), "final_survival": float(y[-1])})
    exports = []
    ns = {"s": "http://www.w3.org/2000/svg"}
    for record in records:
        folder = root if record["kind"] == "contact_sheet" else root/"figures"
        with Image.open(folder/record["files"]["png"]) as im:
            im.load(); pixels = im.size
        assert pixels == ((2700, 1746) if record["kind"] == "contact_sheet" else (1920, 1410))
        pdf = PdfReader(folder/record["files"]["pdf"])
        assert len(pdf.pages) == 1
        page = pdf.pages[0]; expected_inches = (15, 9.7) if record["kind"] == "contact_sheet" else (6.4, 4.7)
        assert np.allclose([float(page.mediabox.width)/72, float(page.mediabox.height)/72], expected_inches)
        svg = ET.parse(folder/record["files"]["svg"])
        assert not svg.findall(".//s:image", ns)
        texts = svg.findall(".//s:text", ns)
        assert texts and "SYNTHETIC" in " ".join("".join(t.itertext()) for t in texts)
        exports.append({"id": record["id"], "png_pixels": pixels, "svg_native_text_count": len(texts), "pdf_pages": 1})

    class Links(HTMLParser):
        def __init__(self): super().__init__(); self.targets=[]; self.cards=0
        def handle_starttag(self, tag, attrs):
            attrs = dict(attrs)
            if tag == "article" and attrs.get("class") == "card": self.cards += 1
            if tag in ["a", "img"]:
                value = attrs.get("href" if tag == "a" else "src", "")
                if value: self.targets.append(value)
    parser = Links(); parser.feed((root/"index.html").read_text(encoding="utf-8"))
    assert parser.cards == 24 and all((root/value).is_file() for value in parser.targets)
    report = {"skill": "figure-foundry", "synthetic": True, "seed": data["seed"],
              "individual_plots": 24, "quantitative": 21, "schematics": 3, "contact_sheets": 4,
              "export_files_checked": len(exports)*3, "text_outside_canvas": [],
              "roc_ap_cross_checked_against": "scikit-learn", "classification_metrics": metrics,
              "bh_cross_checked_against": "scipy.stats.false_discovery_control", "volcano_counts": volcano,
              "pca_explained_variance_ratio": explained.tolist(), "pca_cross_checked_against": "sklearn.decomposition.PCA",
              "normalized_composition_and_area": True, "waterfall_final_total": waterfall,
              "survival_risk_set_cross_checks": survival, "exports": exports,
              "html_cards": parser.cards, "html_static_links_checked": len(parser.targets),
              "browser_interaction_tested": False,
              "browser_interaction_note": "The in-app browser blocks file: URLs. Static HTML/asset links checked; search/filter/dialog not browser-tested.",
              "visual_review": "Four actual rendered contact sheets inspected; radar legend added; flow Yes label and model branch attachments corrected; heatmap converted to vector cells.",
              "limits": ["Synthetic inputs and toy relationships", "No native PPTX or draw.io run", "No independent blind skill evaluation", "KM helper demonstrated only on these untied inputs"]}
    (root/"verification.json").write_text(json.dumps(report, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({"passed": True, "exports": 84, "classification_metrics": metrics, "volcano": volcano}, indent=2))


if __name__ == "__main__": main()
