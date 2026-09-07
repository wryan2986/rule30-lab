# check_round10_delay_renewal.py (revision 3): scalar one-bit extension
# preperiod recurrence on 12 fixed controls: y in {0,2,3,6,7,12}, a in {0,1}.
# Loop 1 (integer states, dict detection) and loop 2 (tuple-cell states,
# list.index detection) are structurally separate algorithms. Caps enforced
# by SIGALRM wall alarm plus RLIMIT_AS address-space limit; orbit step caps
# raise CapExceeded. No sweep, no backend, no extra inputs.
import hashlib
import json
import os
import platform
import resource
import signal
import subprocess
import sys
import tempfile
import time

TIME_CAP_S = 60
MEM_CAP_MIB = 128
ORBIT_CAP = 64
CELL_W = 12

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RESULT_PATH = os.path.join(ROOT, 'results', 'problem1', '20260907_round10_delay_renewal.json')
REF_PATH = os.path.join(ROOT, 'src', 'python', 'rule30_research_reference.py')
REF_RECORDED = '358bdc07904e77080eb78b67bdd8da25822d6b51f1a91b58b5313dfe461c1d01'
DEP_PROOFS = ['proofs/informal/problem1_round10_bounded_strip_sidecar.md', 'proofs/informal/problem1_cycle_completion_defect_transport.md', 'proofs/informal/problem1_physical_time_cycle_defects.md', 'proofs/informal/problem1_full_fringe_temporal_diagonal.md', 'proofs/informal/problem1_anchored_activity_finite_entry.md', 'proofs/informal/problem1_bounded_lag_doubling_controls.md']

T_START = time.perf_counter()


class CapExceeded(Exception):
    pass


def _alarm_handler(signum, frame):
    raise CapExceeded('SIGALRM wall-time cap reached')


def A_int(y):
    return (y >> 2) ^ ((y >> 1) | y)


def orbit_int(y0):
    seq, seen, y = [], {}, y0
    for _ in range(ORBIT_CAP):
        if y in seen:
            break
        seen[y] = len(seq)
        seq.append(y)
        y = A_int(y)
    else:
        raise CapExceeded('int orbit step cap exceeded')
    mu = seen[y]
    return seq, mu, len(seq) - mu, y


def bits_of(y):
    return tuple((y >> i) & 1 for i in range(CELL_W))


def cell_get(st, i):
    return st[i] if i < CELL_W else 0


def step_cell(st):
    assert st[CELL_W - 1] == 0 and st[CELL_W - 2] == 0, 'stored top bits nonzero'
    nxt = tuple(cell_get(st, i + 2) ^ (cell_get(st, i + 1) | cell_get(st, i)) for i in range(CELL_W))
    v = 0
    for i, b in enumerate(nxt):
        v |= (b << i)
    assert v < (1 << (CELL_W - 2)), 'lost top bits beyond fixed width'
    return nxt


def orbit_cell(y0):
    init = bits_of(y0)
    traj = [init]
    while True:
        nxt = step_cell(traj[-1])
        if nxt in traj:
            rep = nxt
            break
        traj.append(nxt)
        if len(traj) > ORBIT_CAP:
            raise CapExceeded('cell orbit step cap exceeded')
    mu = traj.index(rep)
    return traj, mu, len(traj) - mu, rep


def cell_traj_ints(traj):
    out = []
    for st in traj:
        v = 0
        for i, b in enumerate(st):
            v |= (b << i)
        out.append(v)
    return out


def apply_n(y0, n):
    y = y0
    for _ in range(n):
        y = A_int(y)
    return y


def tau_of(y0):
    seq, mu, lam, rep = orbit_int(y0)
    return mu, lam


def phase_cyc(y0, mu, lam):
    return apply_n(y0, mu + ((-mu) % lam))


NEXT = {0: 0, 1: 1, 2: 3, 3: 3, 4: 7, 5: 6, 6: 6, 7: 6, 12: 13, 13: 12,
        14: 12, 15: 12, 24: 26, 25: 27, 26: 25, 27: 25}

YEXP = {
    0: {'tau': 0, 'p': 1, 'cyc': 0, 'tail': 'perm', 'rho': None},
    2: {'tau': 1, 'p': 1, 'cyc': 3, 'tail': 'reset', 'rho': 0},
    3: {'tau': 0, 'p': 1, 'cyc': 3, 'tail': 'reset', 'rho': 0},
    6: {'tau': 0, 'p': 1, 'cyc': 6, 'tail': 'perm', 'rho': None},
    7: {'tau': 1, 'p': 1, 'cyc': 6, 'tail': 'perm', 'rho': None},
    12: {'tau': 0, 'p': 2, 'cyc': 12, 'tail': 'reset', 'rho': 1},
}

ZEXP = {
    (0, 0): {'z': 0, 'tau': 0, 'p': 1, 'cyc': 0, 'branch': 'inherited'},
    (0, 1): {'z': 1, 'tau': 0, 'p': 1, 'cyc': 1, 'branch': 'inherited'},
    (2, 0): {'z': 4, 'tau': 2, 'p': 1, 'cyc': 6, 'branch': 'extra'},
    (2, 1): {'z': 5, 'tau': 1, 'p': 1, 'cyc': 6, 'branch': 'inherited'},
    (3, 0): {'z': 6, 'tau': 0, 'p': 1, 'cyc': 6, 'branch': 'inherited'},
    (3, 1): {'z': 7, 'tau': 1, 'p': 1, 'cyc': 6, 'branch': 'extra'},
    (6, 0): {'z': 12, 'tau': 0, 'p': 2, 'cyc': 12, 'branch': 'inherited'},
    (6, 1): {'z': 13, 'tau': 0, 'p': 2, 'cyc': 13, 'branch': 'inherited'},
    (7, 0): {'z': 14, 'tau': 1, 'p': 2, 'cyc': 13, 'branch': 'inherited'},
    (7, 1): {'z': 15, 'tau': 1, 'p': 2, 'cyc': 13, 'branch': 'inherited'},
    (12, 0): {'z': 24, 'tau': 2, 'p': 2, 'cyc': 25, 'branch': 'extra'},
    (12, 1): {'z': 25, 'tau': 0, 'p': 2, 'cyc': 25, 'branch': 'inherited'},
}


def git_out(args):
    r = subprocess.run(['git', '-C', ROOT] + args, capture_output=True, text=True)
    return r.stdout.strip()


def mem_total_mib():
    try:
        with open('/proc/meminfo') as fh:
            for line in fh:
                if line.startswith('MemTotal:'):
                    return int(line.split()[1]) // 1024
    except Exception:
        return None
    return None


def file_sha(path):
    with open(path, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def main():
    signal.signal(signal.SIGALRM, _alarm_handler)
    signal.alarm(TIME_CAP_S)
    as_bytes = MEM_CAP_MIB * 1024 * 1024
    resource.setrlimit(resource.RLIMIT_AS, (as_bytes, as_bytes))
    cases = []
    all_ok = True
    seen_states = set()
    for y in [0, 2, 3, 6, 7, 12]:
        for a in [0, 1]:
            exp = ZEXP[(y, a)]
            ye = YEXP[y]
            z = 2 * y + a
            checks = []

            def chk(name, ok):
                checks.append({'name': name, 'ok': bool(ok)})
                return bool(ok)

            ok = True
            ok = chk('z_equals_2y_plus_a', z == exp['z']) and ok
            si, mui, lami, repi = orbit_int(y)
            tc, muc, lamc, repc = orbit_cell(y)
            sc = cell_traj_ints(tc)
            zi, mzi, lzi, repzi = orbit_int(z)
            tz, mzc, lzc, repzc = orbit_cell(z)
            sz = cell_traj_ints(tz)
            for s in si + zi:
                seen_states.add(s)
            ok = chk('loops_agree_y_trajectory', list(si) == list(sc)) and ok
            ok = chk('loops_agree_y_recurrence', (mui, lami, repi) == (muc, lamc, cell_traj_ints([repc])[0])) and ok
            ok = chk('loops_agree_z_trajectory', list(zi) == list(sz)) and ok
            ok = chk('loops_agree_z_recurrence', (mzi, lzi, repzi) == (mzc, lzc, cell_traj_ints([repzc])[0])) and ok
            ok = chk('y_tau_period_hand', (mui, lami) == (ye['tau'], ye['p'])) and ok
            entry_y = si[mui]
            pc_y = phase_cyc(y, mui, lami)
            ok = chk('y_entry_state_on_cycle', apply_n(entry_y, lami) == entry_y) and ok
            ok = chk('y_phase_cyc_hand', pc_y == ye['cyc']) and ok
            cyc_low = [s & 1 for s in si[mui:]]
            tail_is_perm = all(v == 0 for v in cyc_low)
            rho = None
            if not tail_is_perm:
                rho = next(s for s in range(lami) if (si[mui + s] & 1) == 1)
            ok = chk('y_tail_type', ('perm' if tail_is_perm else 'reset') == ye['tail']) and ok
            ok = chk('y_rho', rho == ye['rho']) and ok
            yp = apply_n(y, ye['tau'])
            ok = chk('y_T_shift_on_cycle', tau_of(yp) == (0, ye['p'])) and ok
            ok = chk('z_tau_period_hand', (mzi, lzi) == (exp['tau'], exp['p'])) and ok
            entry_z = zi[mzi]
            pc_z = phase_cyc(z, mzi, lzi)
            ok = chk('z_entry_state_on_cycle', apply_n(entry_z, lzi) == entry_z) and ok
            ok = chk('z_phase_cyc_hand', pc_z == exp['cyc']) and ok
            ok = chk('lemma_tau_z_ge_T', mzi >= ye['tau']) and ok
            T, R = ye['tau'], ye['rho']
            vT = apply_n(z, T) & 1
            b_star = apply_n(pc_z, T) & 1
            ok = chk('lift_bit_cyclic', tau_of(2 * yp + b_star)[0] == 0) and ok
            if ye['tail'] == 'perm':
                ok = chk('perm_both_lifts_cyclic', tau_of(2 * yp)[0] == 0 and tau_of(2 * yp + 1)[0] == 0) and ok
            branch = 'inherited' if vT == b_star else 'extra'
            ok = chk('branch_matches_hand', branch == exp['branch']) and ok
            if ye['tail'] == 'perm':
                ok = chk('perm_tail_exact_delay_T', mzi == T) and ok
            else:
                ok = chk('reset_tail_delay_alternative', mzi == T or mzi == T + 1 + R) and ok
                if branch == 'extra':
                    ok = chk('extra_delay_equals_T_1_rho', mzi == T + 1 + R) and ok
            cases.append({'y': y, 'a': a, 'z': z, 'T': T, 'tail': ye['tail'], 'rho': R,
                          'source_period': lami, 'output_period': lzi, 'tau_z': mzi,
                          'entry_z': entry_z, 'phase_cyc_z': pc_z, 'entry_y': entry_y,
                          'phase_cyc_y': pc_y, 'lowbit_at_T': vT, 'cyclic_lift_bit': b_star,
                          'branch': branch, 'traj_y': list(si), 'traj_z': list(zi),
                          'repeat_y': repi, 'repeat_z': repzi, 'cell_traj_y': list(sc), 'cell_traj_z': list(sz), 'checks': checks,
                          'case_ok': all(c['ok'] for c in checks)})
            all_ok = all_ok and cases[-1]['case_ok']
    trans_detail = []
    trans_ok = True
    for s in sorted(seen_states):
        good = (s in NEXT) and (A_int(s) == NEXT[s]) and (cell_traj_ints([step_cell(bits_of(s))])[0] == NEXT[s])
        trans_detail.append({'state': s, 'A_state': A_int(s), 'hand_next': NEXT.get(s), 'ok': bool(good)})
        trans_ok = trans_ok and good
    all16 = (set(seen_states) == set(NEXT.keys()))
    trans_ok = trans_ok and all16
    all_ok = all_ok and trans_ok
    dep_hashes = {}
    for rel in DEP_PROOFS:
        dep_hashes[rel] = file_sha(os.path.join(ROOT, rel))
    checker_sha = file_sha(__file__)
    ref_live = file_sha(REF_PATH)
    ref_ok = (ref_live == REF_RECORDED)
    payload = {'cases': cases, 'transitions': trans_detail, 'all16_states_seen': all16,
               'dependency_proof_hashes': dep_hashes, 'checker_sha256': checker_sha}
    canonical = json.dumps(payload, sort_keys=True).encode('utf-8')
    payload_hash = hashlib.sha256(canonical).hexdigest()
    elapsed = time.perf_counter() - T_START
    peak_mib = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0
    caps_ok = (elapsed < TIME_CAP_S) and (peak_mib < MEM_CAP_MIB)
    signal.alarm(0)
    un = platform.uname()
    record = {
        'experiment_id': 'round10_delay_renewal_12ctl',
        'timestamp_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'git_commit': git_out(['rev-parse', 'HEAD']),
        'git_branch': git_out(['branch', '--show-current']),
        'git_status': git_out(['status', '--short']),
        'question': 'problem1',
        'hypothesis': 'scalar one-bit extension preperiod recurrence holds on 12 fixed controls',
        'backend': 'python-double-loop-int-and-tuplecell',
        'parameters': {'y_values': [0, 2, 3, 6, 7, 12], 'a_values': [0, 1],
                       'cell_width': CELL_W, 'orbit_cap': ORBIT_CAP,
                       'time_cap_s': TIME_CAP_S, 'mem_cap_mib': MEM_CAP_MIB},
        'enforcement': {'wall_alarm_s': TIME_CAP_S, 'address_space_cap_mib': MEM_CAP_MIB,
                        'mechanisms': ['SIGALRM handler raising CapExceeded', 'RLIMIT_AS set before compute', 'per-orbit step caps raising CapExceeded', 'fixed-width cell asserts against top-bit loss']},
        'hardware': {'node': un.node, 'machine': un.machine, 'processor': un.processor,
                     'cpu_count': os.cpu_count(), 'mem_total_mib': mem_total_mib(),
                     'peak_rss_mib': round(peak_mib, 3)},
        'software': {'python': sys.version.split()[0], 'platform': un.system + ' ' + un.release},
        'runtime_seconds': round(elapsed, 4), 'runtime_scope': 'checks plus canonical hashing only; record assembly and atomic write excluded',
        'source_hashes': {'checker_sha256': checker_sha, 'immutable_ref_live_sha256': ref_live,
                          'immutable_ref_recorded_sha256': REF_RECORDED, 'immutable_ref_ok': ref_ok,
                          'dependency_proof_hashes': dep_hashes},
        'result_hashes': {'canonical_payload_sha256': payload_hash},
        'result_summary': {'n_cases': len(cases), 'all_cases_ok': all(c['case_ok'] for c in cases),
                           'hand_transitions_ok': trans_ok, 'all16_states_seen': all16,
                           'caps_ok': caps_ok, 'all_ok': bool(all_ok and caps_ok and ref_ok)},
        'cases': cases,
        'transitions': trans_detail,
        'interpretation': 'a counterexample would falsify the candidate local formula; all named controls agree, which is finite-exhaustive over the 12 fixed controls only, not a proof of the infinite lemma',
        'status': 'finite-exhaustive',
        'proof_scope': '12 fixed hand-derived controls; no ranges or sweeps',
        'limitations': ['agreement on fixed controls does not prove the infinite scalar lemma', 'no FULL-orbit claim', 'no expanded controls', 'timeout path exits without a record', 'runtime excludes record assembly and atomic write'],
    }
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(RESULT_PATH), prefix='.tmp_renewal_')
    with os.fdopen(fd, 'w', encoding='utf-8') as fh:
        json.dump(record, fh, indent=2, sort_keys=True)
        fh.write('\n')
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(tmp, RESULT_PATH)
    print('cases_ok=' + str(sum(1 for c in cases if c['case_ok'])) + '/12 trans_ok=' + str(trans_ok) + ' all16=' + str(all16) + ' caps_ok=' + str(caps_ok) + ' ref_ok=' + str(ref_ok) + ' elapsed_s=' + str(round(elapsed, 4)))
    return all_ok and caps_ok and ref_ok


try:
    ok = main()
except CapExceeded as e:
    print('CAP EXCEEDED: ' + str(e))
    ok = False
sys.exit(0 if ok else 1)
