#!/usr/bin/env python3
"""Independent modular-fraction terminal-edit driver calculation.
MiMo modular calculation, independently reviewed and integrated by the lead.
Uses ONLY explicit ut phases (-7/127, -123/127) and stored ututtt rational phases.
No other comparator, cycle regeneration, or census."""
import datetime, hashlib, json, math, os, platform, resource, subprocess, sys, tempfile, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT_PATH = ROOT / 'results/problem1/20260906_terminal_branch_sensitivity_primary.json'
SCRIPT_PATH = Path(__file__)
START_WALL = time.monotonic()
START_CPU = time.process_time()
START_UTC = datetime.datetime.now(datetime.timezone.utc).isoformat()
resource.setrlimit(resource.RLIMIT_CPU, (120, 120))
resource.setrlimit(resource.RLIMIT_AS, (1024**3, 1024**3))
ORIG_AFF = sorted(os.sched_getaffinity(0))
os.sched_setaffinity(0, {ORIG_AFF[0]})

CORRECTION_LOG = []
def log_correction(msg):
    t = time.monotonic() - START_WALL
    CORRECTION_LOG.append({'elapsed_s': round(t, 4), 'message': msg})
    print('[CORRECTION t=%.3f] %s' % (t, msg))

log_correction('Integrated modular calculation; prior worker corrections archived separately.')

def sha(data):
    return hashlib.sha256(data if isinstance(data, (bytes, bytearray)) else data.encode()).hexdigest()
def cjson(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':')).encode()
def atomic_write(path, data):
    fd, tmp = tempfile.mkstemp(prefix=path.name + '.', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as f:
            f.write(data); f.flush(); os.fsync(f.fileno())
        os.replace(tmp, path)
        d = os.open(path.parent, os.O_DIRECTORY)
        try: os.fsync(d)
        finally: os.close(d)
    finally:
        if os.path.exists(tmp): os.unlink(tmp)

# --- J function (Section 1 of proof) ---
def I_func(z):
    r = z % 64
    return 1 if r == 0 or r == 5 else 0
def J_func(y):
    return I_func((y >> 2) ^ ((y >> 1) | y)) + I_func(y >> 2)

# --- Modular fraction: low 8 bits of (N/D) >> (2d) as 2-adic integer ---
def low8(N, D, d):
    k = 8 + 2 * d
    mask = 1 << k
    D_inv = pow(D % mask, -1, mask)
    X = (N % mask) * D_inv % mask
    return (X >> (2 * d)) & 0xFF

# --- Cross-check: 2-adic bit-by-bit long division ---
def low8_longdiv(N, D, d):
    k = 8 + 2 * d
    rem = N
    result = 0
    for i in range(k):
        b = rem & 1
        rem = (rem - b * D) >> 1
        if b:
            result |= (1 << i)
    return (result >> (2 * d)) & 0xFF

# --- Phase data ---
UT_PHASES = [(-7, 127), (-123, 127)]
UT_P = 2

_d = json.load(open(ROOT / 'results/problem1/20260905_periodic_rational_primary.json'))
_r = next(r for r in _d['result_summary']['rows'] if r['q'] == 'ututtt')
def _ph(rp):
    s = rp['numerator_hex']
    return (-int(s[1:], 16) if s.startswith('-') else int(s, 16), int(rp['denominator_hex'], 16))
UTUTTT_PHASES = [_ph(rp) for rp in _r['rational_phases']]
UTUTTT_P, UTUTTT_ONSET, UTUTTT_LAMBDA = 6, _r['spatial_onset'], _r['lambda']
del _d, _r

# --- Driver: ALWAYS compute from d=0 with eta_{-1}=0 ---
def compute_all_rows(phases, p, e, needed_end):
    """Compute rows for d=0..needed_end. eta_{-1}=0, then eta_d = eta_{d-1} XOR toggle_d."""
    rows = []
    eta_prev = 0  # eta_{-1}
    for d in range(needed_end + 1):
        idx = (e - d) % p
        N, D = phases[idx]
        y = low8(N, D, d)
        toggle = ((y >> 4) & 1) | ((y >> 3) & 1)
        eta = eta_prev ^ toggle
        jb = J_func(y)
        cy = y ^ 64 ^ (128 * eta)
        jc = J_func(cy)
        rows.append({'d': d, 'y': y, 'toggle': int(toggle), 'eta': int(eta),
                      'j_base': jb, 'j_changed': jc})
        eta_prev = eta
    return rows

def verify_two_periods(all_rows, d0, L, joint_period, parity):
    """Verify closure by comparing two full joint periods field-by-field."""
    errs = []
    p1_start = d0
    p2_start = d0 + joint_period
    needed = p2_start + joint_period
    if needed >= len(all_rows):
        errs.append('insufficient rows: have %d need %d' % (len(all_rows), needed))
        return errs, [], []
    period1 = all_rows[p1_start:p1_start + joint_period]
    period2 = all_rows[p2_start:p2_start + joint_period]
    # Field-by-field comparison of two full periods
    mismatches = 0
    for i in range(joint_period):
        for field in ('y', 'toggle', 'eta', 'j_base', 'j_changed'):
            if period1[i][field] != period2[i][field]:
                mismatches += 1
                errs.append('period mismatch d=%d field=%s: %s!=%s' %
                            (d0+i, field, period1[i][field], period2[i][field]))
                if mismatches > 5:
                    errs.append('... truncated')
                    return errs, period1, period2
    # Parity: XOR of toggles over one L-period
    p_calc = 0
    for r in period1[:L]:
        p_calc ^= r['toggle']
    if p_calc != parity:
        errs.append('parity fail: %d!=%d' % (p_calc, parity))
    # Joint-period XOR must be 0 (guarantees eta closure)
    jp_xor = 0
    for r in period1:
        jp_xor ^= r['toggle']
    if jp_xor != 0:
        errs.append('joint-parity nonzero: %d' % jp_xor)
    return errs, period1, period2

def main():
    log_correction('Entering main().')
    gc = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    gc_msg = subprocess.check_output(['git', 'log', '-1', '--format=%H %s %ai'], cwd=ROOT, text=True).strip()
    inps = ['proofs/informal/problem1_terminal_branch_sensitivity.md',
            'results/problem1/20260905_periodic_rational_primary.json']
    ih = {}
    for f in inps:
        fp = ROOT / f
        if fp.exists():
            ih[f] = sha(fp.read_bytes())
    src_bytes = Path(__file__).resolve().read_bytes()
    src_hash = sha(src_bytes)

    # Cross-check modular fraction methods
    xc = []
    for d in range(12):
        for ph_i, (N, D) in enumerate(UT_PHASES):
            a, b = low8(N, D, d), low8_longdiv(N, D, d)
            ok = (a == b)
            xc.append({'d': d, 'phase': ph_i, 'pow_inv': a, 'longdiv': b, 'match': ok})
            assert ok, 'XC fail ut ph=%d d=%d: %d!=%d' % (ph_i, d, a, b)
    for d in [0, 1, 3, 7, 13, 20, 50, 69, 100]:
        for ph_i in range(UTUTTT_P):
            N, D = UTUTTT_PHASES[ph_i]
            a, b = low8(N, D, d), low8_longdiv(N, D, d)
            ok = (a == b)
            xc.append({'d': d, 'phase': ph_i, 'pow_inv': a, 'longdiv': b, 'match': ok})
            assert ok, 'XC fail ututtt ph=%d d=%d' % (ph_i, d)
    log_correction('Cross-check passed: %d comparisons.' % len(xc))

    controls = []
    specs = [
        ('ut', UT_PHASES, UT_P, 0, 0, 14, 1, 28),
        ('ututtt', UTUTTT_PHASES, UTUTTT_P, 0, 1, 138, 0, 138),
        ('ututtt', UTUTTT_PHASES, UTUTTT_P, 2, 1, 138, 0, 138),
        ('ututtt', UTUTTT_PHASES, UTUTTT_P, 4, 1, 138, 0, 138),
    ]
    for sch, ph, p, e, d0, L, par, jp in specs:
        # Compute from d=0 through d0+2*jp (two full periods beyond onset)
        needed = d0 + 2 * jp
        all_rows = compute_all_rows(ph, p, e, needed)
        errs, period1, period2 = verify_two_periods(all_rows, d0, L, jp, par)
        bt = sum(r['j_base'] for r in period1)
        ct = sum(r['j_changed'] for r in period1)
        rh = sha(cjson([{k: r[k] for k in ('d','y','toggle','eta','j_base','j_changed')} for r in period1]))
        onset_row = all_rows[d0]
        closure_row = all_rows[d0 + jp]
        preperiod = all_rows[:d0]
        controls.append({
            'schedule': sch, 'ending_e': e, 'd0': d0, 'L': L,
            'parity': par, 'joint_period': jp,
            'base_total': bt, 'changed_total': ct, 'diff': ct - bt,
            'onset_row': onset_row, 'closure_row': closure_row,
            'preperiod_rows': preperiod,
            'rows_hash': rh,
            'two_period_verification': {
                'all_fields_match': len(errs) == 0,
                'mismatches': [e for e in errs],
            },
            'closure_errors': errs,
            'rows': period1,
        })
        status = 'PASS' if not errs else 'FAIL'
        print('%s %s e=%d: base=%d changed=%d diff=%d errs=%d' % (status, sch, e, bt, ct, ct-bt, len(errs)))
        if errs:
            for e in errs[:5]:
                print('  ERR: %s' % e)

    log_correction('All %d controls computed.' % len(controls))

    elapsed_w = time.monotonic() - START_WALL
    elapsed_c = time.process_time() - START_CPU
    cpuinfo = Path('/proc/cpuinfo').read_text()
    all_pass = all(not c['closure_errors'] for c in controls)
    all_xc = all(x['match'] for x in xc)
    assert all_pass and all_xc, 'A declared verification failed'
    assert elapsed_w < 120
    result_summary = {
        'controls_total': len(controls),
        'controls_pass': sum(1 for c in controls if not c['closure_errors']),
        'all_crosschecks_pass': all_xc,
        'controls': [{
            'schedule': c['schedule'], 'ending_e': c['ending_e'],
            'base_total': c['base_total'], 'changed_total': c['changed_total'],
            'diff': c['diff'], 'pass': not c['closure_errors'],
        } for c in controls],
    }
    result_hashes = {
        'result_summary_sha256': sha(cjson(result_summary)),
        'controls_rows_sha256': {c['schedule'] + '_e' + str(c['ending_e']): c['rows_hash'] for c in controls},
    }
    rec = {
        'experiment_id': '20260906_terminal_branch_sensitivity_primary',
        'timestamp_utc': START_UTC,
        'backend': 'python-modular-fractions-with-long-division-crosschecks',
        'status': 'finite-exhaustive',
        'question': 'problem1',
        'hypothesis': 'Independent computation of J-function sums over one joint period of the terminal-edit driver yields base=2/changed=2 for ut(e=0) and base=6/changed=15,6/9,15/0 for ututtt(e=0,2,4), matching the proof.',
        'git_commit': gc,
        'git_commit_description': gc_msg,
        'repo_root': str(ROOT),
        'input_sha256': ih,
        'source_path': str(SCRIPT_PATH.resolve()),
        'source_sha256': src_hash,
        'executed_source': src_bytes.decode(),
        'admission_snapshot': (ROOT / inps[0]).read_text(),
        'rational_input_snapshot': {
            'ut': UT_PHASES,
            'ututtt': UTUTTT_PHASES,
            'ututtt_onset': UTUTTT_ONSET,
            'ututtt_spatial_period': UTUTTT_LAMBDA,
        },
        'source_and_input_hashes': {
            **ih,
            str(SCRIPT_PATH.relative_to(ROOT)): src_hash,
            'src/python/rule30_research_reference.py': sha((ROOT / 'src/python/rule30_research_reference.py').read_bytes()),
        },
        'admission': {
            'description': 'Independent modular-fraction terminal-edit driver calculation',
            'allowed_inputs': [
                'explicit ut phases (-7/127, -123/127) - given in task',
                'stored ututtt rational phases from results/problem1/20260905_periodic_rational_primary.json',
            ],
            'forbidden': [
                'no other comparator or cycle regeneration',
                'no census or frontier membership',
                'no repo edits, commits, or pushes',
            ],
        },
        'phases_used': {
            'ut': {'p': UT_P, 'explicit_phases': UT_PHASES,
                   'source': 'explicit: (-7/127, -123/127)'},
            'ututtt': {'p': UTUTTT_P, 'onset': UTUTTT_ONSET, 'lambda': UTUTTT_LAMBDA,
                       'phases': [{'N': hex(N), 'D': hex(D)} for N, D in UTUTTT_PHASES],
                       'source': 'results/problem1/20260905_periodic_rational_primary.json'},
        },
        'parameters': {
            'controls': [('ut', 0), ('ututtt', 0), ('ututtt', 2), ('ututtt', 4)],
            'eta_init': 'eta_{-1}=0, eta_d = eta_{d-1} XOR (y_d[4] OR y_d[3])',
            'changed_J': 'J(y XOR 64 XOR (128*eta_d))',
            'driver_periods': {'ut': {'L': 14, 'parity': 1, 'joint': 28},
                               'ututtt': {'L': 138, 'parity': 0, 'joint': 138}},
            'verification_method': 'Two full joint periods compared field-by-field',
        },
        'runtime_seconds': elapsed_w,
        'proof_scope': 'Complete named driver/defect periods and the declared modular arithmetic crosschecks only. All-age conclusions use the separate proved perturbation recurrence and stored rational certificates.',
        'interpretation': 'Positive linear terminal-edit sensitivity on the stored ututtt comparator refutes bounded cost per edit, without asserting ordinary membership or a whole-tail counterexample.',
        'modular_fraction_crosscheck': xc,
        'result_summary': result_summary,
        'result_hashes': result_hashes,
        'controls': controls,
        'limits': {'cpus': 1, 'cpu_seconds': 120, 'wall_seconds': 120,
                   'address_space_bytes': 1024**3, 'enforcement': 'RLIMIT_CPU; RLIMIT_AS; single affinity'},
        'hardware': {
            'cpu_model': next((l.split(':',1)[1].strip() for l in cpuinfo.splitlines() if l.startswith('model name')), '?'),
            'logical_cpus': os.cpu_count(), 'original_affinity': ORIG_AFF,
            'executed_affinity': sorted(os.sched_getaffinity(0)),
            'physical_memory_bytes': os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')},
        'software': {'python': sys.version, 'platform': platform.platform()},
        'timings': {'started_utc': START_UTC, 'wall_seconds': elapsed_w,
                    'cpu_seconds': elapsed_c,
                    'peak_rss_bytes': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024},
        'limitations': [
            'Only ut (e=0) and ututtt (e=0,2,4); no other comparator.',
            'Modular fraction extraction only; no cycle regeneration or census.',
            'Finite joint-period driver; no infinite implication.',
            'No ordinary frontier membership claim.',
            'The initial worker implementation required low-prefix parity and closure-phase corrections; its totals alone would not have detected the error.',
            'The lead integrated missing protocol metadata and independently matched complete rows against cell vectors. Original worker artifacts are retained in the integration audit.',
        ],
        'correction_log': CORRECTION_LOG,
        'output_paths': {'json': str(OUT_PATH), 'script': str(SCRIPT_PATH.resolve()),
                         'integration_audit': 'results/problem1/20260906_terminal_branch_sensitivity_verification.json'},
    }
    rec['payload_sha256_excluding_this_field'] = sha(cjson(rec))
    enc = cjson(rec) + b'\n'
    atomic_write(OUT_PATH, enc)
    log_correction('Final record written. status=%s sha=%s' % (rec['status'], sha(enc)[:16]))
    print('RESULT_PATH=%s STATUS=%s SHA=%s ELAPSED=%.2f' % (OUT_PATH, rec['status'], sha(enc), elapsed_w))

if __name__ == '__main__':
    main()
