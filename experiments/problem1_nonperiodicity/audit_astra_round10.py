"""Atomic provenance audit for round ten; no new scientific inputs."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import resource
import signal
import subprocess
import tempfile
import time

ROOT = Path(__file__).resolve().parents[2]
START = datetime(2026, 9, 7, 3, 49, 17, tzinfo=timezone.utc)
BASE = '043a768d6624983d7871bc99a8a4ced08f09e51b'
REF = 'src/python/rule30_research_reference.py'
REF_HASH = '358bdc07904e77080eb78b67bdd8da25822d6b51f1a91b58b5313dfe461c1d01'
CHECKER = 'experiments/problem1_nonperiodicity/check_round10_delay_renewal.py'
RESULT = 'results/problem1/20260907_round10_delay_renewal.json'
ARCHIVE = 'results/problem1/20260907_round10_superseded_run.json'
PROOFS = [
    'proofs/informal/problem1_cycle_delay_renewal.md',
    'proofs/informal/problem1_highest_wait_nonforcing.md',
    'proofs/informal/problem1_one_bit_strip_return_constraint.md',
    'proofs/informal/problem1_round10_bounded_strip_sidecar.md',
    'proofs/informal/problem1_round10_fresh_review.md',
]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args], text=True).strip()


def snapshot(path):
    data = (ROOT / path).read_bytes()
    return {'sha256': sha(data), 'bytes': len(data), 'content': data.decode('utf-8')}


def validate_snapshot_files(files):
    for item in files.values():
        data = item['content'].encode('utf-8')
        assert len(data) == item['bytes'] and sha(data) == item['sha256']
    if CHECKER in files and RESULT in files:
        record = json.loads(files[RESULT]['content'])
        assert record['source_hashes']['checker_sha256'] == files[CHECKER]['sha256']


def main():
    begun = time.perf_counter()
    signal.signal(signal.SIGALRM, lambda *_: (_ for _ in ()).throw(TimeoutError('audit cap')))
    signal.alarm(60)
    resource.setrlimit(resource.RLIMIT_AS, (256 * 1024**2, 256 * 1024**2))
    parser = argparse.ArgumentParser()
    parser.add_argument('--phase', choices=['established', 'maintenance'], required=True)
    parser.add_argument('--established-commit')
    args = parser.parse_args()
    assert git('branch', '--show-current') == 'research/astra-next'
    assert sha((ROOT / REF).read_bytes()) == REF_HASH
    record = json.loads((ROOT / RESULT).read_text())
    source = record['source_hashes']
    assert source['checker_sha256'] == sha((ROOT / CHECKER).read_bytes())
    assert source['immutable_ref_live_sha256'] == REF_HASH
    for path, digest in source['dependency_proof_hashes'].items():
        assert sha((ROOT / path).read_bytes()) == digest, path
    assert record['result_summary']['all_ok']
    assert {(c['y'], c['a']) for c in record['cases']} == {
        (y, a) for y in (0, 2, 3, 6, 7, 12) for a in (0, 1)}
    assert len(record['cases']) == 12
    for case in record['cases']:
        assert case['case_ok'] and all(c['ok'] for c in case['checks'])
        for letter in ('y', 'z'):
            trajectory = case['traj_' + letter]
            assert trajectory == case['cell_traj_' + letter]
            outputs = trajectory[1:] + [case['repeat_' + letter]]
            assert all((a >> 2) ^ ((a >> 1) | a) == b
                       for a, b in zip(trajectory, outputs))
    payload = {
        'cases': record['cases'], 'transitions': record['transitions'],
        'all16_states_seen': record['result_summary']['all16_states_seen'],
        'dependency_proof_hashes': source['dependency_proof_hashes'],
        'checker_sha256': source['checker_sha256'],
    }
    assert sha(json.dumps(payload, sort_keys=True).encode()) == record['result_hashes']['canonical_payload_sha256']
    old = json.loads((ROOT / ARCHIVE).read_text())
    validate_snapshot_files(old['files'])
    archived_versions = 1
    for key, value in old.items():
        if key.startswith('snapshot') and isinstance(value, dict) and 'files' in value:
            validate_snapshot_files(value['files'])
            archived_versions += 1
    review_path = 'results/problem1/20260907_round10_mimo_direct_review.json'
    review = json.loads((ROOT / review_path).read_text())
    assert review['parameters']['model'] == 'mimo-v2.5'
    assert review['http_status'] == 403 and not review['result_summary']['review_response_received']
    assert sha(json.dumps(review['request_payload'], sort_keys=True).encode()) == review['result_hashes']['request_sha256']
    assert sha(review['response_body'].encode()) == review['result_hashes']['response_sha256']
    review_runner = 'experiments/problem1_nonperiodicity/review_round10_mimo.py'
    assert (ROOT / review_runner).read_text() == review['runner_source']
    incoming = 'docs/astra_handoff_archive_20260907_round10.md'
    assert (ROOT / incoming).read_bytes() == subprocess.check_output(
        ['git', '-C', str(ROOT), 'show', BASE + ':ASTRA_HANDOFF.md'])
    remote = None
    if args.established_commit:
        assert len(args.established_commit) == 40
        remote = git('ls-remote', '--heads', 'origin', 'research/astra-next').split()[0]
        assert remote == args.established_commit
        assert git('rev-parse', 'HEAD') == args.established_commit
    paths = sorted(set(PROOFS + [CHECKER, RESULT, ARCHIVE, review_path, review_runner, incoming, 'ASTRA_HANDOFF.md',
                                str(Path(__file__).resolve().relative_to(ROOT))] +
                       list(source['dependency_proof_hashes'])))
    snapshots = {path: snapshot(path) for path in paths}
    snapshot_hash = sha(json.dumps(snapshots, sort_keys=True).encode())
    now = datetime.now(timezone.utc)
    audit = {
        'experiment_id': 'astra_round10_' + args.phase + '_audit',
        'timestamp_utc': now.isoformat(), 'git_commit': git('rev-parse', 'HEAD'),
        'base_commit': BASE, 'git_branch': git('branch', '--show-current'),
        'question': 'problem1', 'status': 'finite-exhaustive',
        'hypothesis': 'Listed exact artifacts, fixed-control results, and archive bytes agree.',
        'backend': 'python-read-only-artifact-audit',
        'parameters': {'phase': args.phase, 'scientific_controls': 12,
                       'new_scientific_inputs_in_audit': 0,
                       'wall_cap_seconds': 60, 'address_space_cap_mib': 256},
        'hardware': {'machine': platform.machine(), 'node': platform.node(),
                     'cpu_count': os.cpu_count(),
                     'peak_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},
        'software': {'python': platform.python_version(), 'platform': platform.platform(),
                     'git': git('--version')},
        'runtime_seconds': time.perf_counter() - begun,
        'round_started_utc': START.isoformat(),
        'round_elapsed_seconds': (now - START).total_seconds(),
        'result_summary': {'all_checks_pass': True, 'snapshots': len(snapshots),
                           'archived_versions': archived_versions,
                           'fresh_external_review_completed': False,
                           'immutable_reference_unchanged': True},
        'result_hashes': {'snapshots_sha256': snapshot_hash,
                          'fixed_control_payload_sha256': record['result_hashes']['canonical_payload_sha256']},
        'established_commit': args.established_commit, 'remote_commit': remote,
        'interpretation': 'Maintenance/provenance verification; Problem 1 remains open.',
        'proof_scope': 'Only the named finite artifacts and twelve previously computed controls.',
        'limitations': ['No new trajectory or scientific input is generated.',
                        'This audit does not prove any infinite mathematical claim.',
                        'Runtime excludes final JSON serialization and atomic write.',
                        'A maintenance checkpoint is neither success nor research blocked.'],
        'snapshots': snapshots,
    }
    target = ROOT / 'results/problem1/20260907_round10_audit.json'
    fd, temporary = tempfile.mkstemp(dir=target.parent, prefix='.round10_audit_')
    with os.fdopen(fd, 'w', encoding='utf-8') as out:
        json.dump(audit, out, sort_keys=True, indent=2)
        out.write('\n'); out.flush(); os.fsync(out.fileno())
    os.replace(temporary, target)
    signal.alarm(0)
    print(json.dumps({k: audit[k] for k in ('experiment_id', 'git_commit',
                    'round_elapsed_seconds', 'result_summary', 'result_hashes')}))


if __name__ == '__main__':
    main()
