"""Tworzy partie zawodów do weryfikacji (po 20) z danych repozytorium.

Użycie (z katalogu source/):  python3 verify/make_batches.py NEXT_COUNT
- pomija zawody z verify/done.txt (już zweryfikowane albo przyjęte)
- pomija zawody z już istniejących partii verify/batches/*.json
- zapisuje kolejne partie verify/batches/NNN.json
Kolejność: po id z gen/jobs.json (deterministyczna).
"""
import json, os, re, sys, glob

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.dirname(HERE)
BATCH = 20

def leaves(node, path, out):
    if 'c' in node:
        for c in node['c']:
            leaves(c, path + [node['n']], out)
    else:
        out.append((node, path))

def load_card_texts():
    texts = {}
    for f in glob.glob(os.path.join(SRC, 'gen/out/*.txt')):
        cur = None
        for line in open(f, encoding='utf-8'):
            line = line.rstrip('\n')
            m = re.match(r'^@(\d+)$', line)
            if m:
                cur = int(m.group(1)); texts[cur] = {}
            elif cur is not None and line[:2] in ('H:', 'T:', 'D:', 'Y:'):
                texts[cur][line[0]] = line[3:]
    return texts

def main():
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    app = json.load(open(os.path.join(SRC, 'app.json'), encoding='utf-8'))
    pay = json.load(open(os.path.join(SRC, 'pay_gus2024.json'), encoding='utf-8'))['grupy']
    jobs = json.load(open(os.path.join(SRC, 'gen/jobs.json'), encoding='utf-8'))
    job_id = {}
    for i, j in enumerate(jobs):
        job_id.setdefault(j['name'], i)
    cards = load_card_texts()
    done = set()
    p = os.path.join(HERE, 'done.txt')
    if os.path.exists(p):
        done = {l.strip() for l in open(p, encoding='utf-8') if l.strip()}
    queued = set()
    for f in glob.glob(os.path.join(HERE, 'batches/*.json')):
        queued |= {x['name'] for x in json.load(open(f, encoding='utf-8'))}
    out = []
    for ar in app['areas']:
        leaves_ = []
        leaves(ar, [], leaves_)
        for node, path in leaves_:
            name = node.get('n')
            if name in done or (node.get('fn') or '') in done or name in queued:
                continue
            gid = job_id.get(node.get('fn') or name, job_id.get(name, 10**9))
            out.append((gid, name, node, path))
    out.sort(key=lambda t: t[0])
    existing = sorted(glob.glob(os.path.join(HERE, 'batches/*.json')))
    next_no = (int(os.path.basename(existing[-1])[:3]) + 1) if existing else 101
    made = 0
    for k in range(count):
        chunk = out[k * BATCH:(k + 1) * BATCH]
        if not chunk:
            break
        rows = []
        for gid, name, node, path in chunk:
            gk = str(node.get('gk', ''))
            g = app['groups'].get(gk, {})
            pk = str(node.get('pk') or gk)
            code = next((pk[:i] for i in range(min(3, len(pk)), 0, -1) if pk[:i] in pay), None)
            pg = pay.get(code, {}) if code else {}
            routes = node.get('rx') or g.get('r', [])
            card = cards.get(gid, {})
            rows.append({
                'name': name, 'path': ' > '.join(path[1:]) if len(path) > 1 else ' > '.join(path),
                'hook': card.get('H', ''), 'tasks': card.get('T', ''), 'day': card.get('D', ''),
                'skills': g.get('s', []), 'plus': g.get('p', []), 'minus': g.get('m', []),
                'routes': routes, 'pay_group': pg.get('n', ''), 'pay_median_2025': pg.get('med', None),
                'gen_id': gid,
            })
        fn = os.path.join(HERE, 'batches', '%03d.json' % next_no)
        json.dump(rows, open(fn, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print('partia', next_no, len(rows), 'zawodów')
        next_no += 1; made += 1
    print('pozostało do zweryfikowania po tej partii:', max(0, len(out) - made * BATCH))

if __name__ == '__main__':
    main()
