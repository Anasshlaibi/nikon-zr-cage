"""Package actual CAD meshes into a local, network-independent review page."""
from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]
out=root/'exports'/'r2'
parts=json.loads((out/'assembly_mesh.json').read_text(encoding='utf-8'))
packed=[]
for p in parts:
    if p['group']=='motion': continue
    packed.append({k:p[k] for k in ('name','material','group','explode','triangles')} |
                  {'vertices':[[round(c,4) for c in v] for v in p['vertices']]})
template=(root/'models'/'review_template.html').read_text(encoding='utf-8')
html=template.replace('__MODEL_DATA__',json.dumps(packed,separators=(',',':')))
(out/'review.html').write_text(html,encoding='utf-8')
# Extract the authored runtime for a JS syntax check, independently of mesh data.
script=html.rsplit('<script>',1)[1].split('</script>',1)[0]
(out/'viewer_assets'/'review_runtime.js').write_text(script,encoding='utf-8')
print(f'Review: {out / "review.html"} ({len(html):,} characters)')
