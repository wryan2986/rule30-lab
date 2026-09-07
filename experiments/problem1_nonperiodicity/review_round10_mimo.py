"""One authorized MiMo review with required routing metadata; no simulation."""
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
import urllib.error
import urllib.request
import uuid

ROOT = Path(__file__).resolve().parents[2]
FILES = [
    'ASTRA_GOAL.md', 'ASTRA_HANDOFF.md',
    'proofs/informal/problem1_cycle_delay_renewal.md',
    'proofs/informal/problem1_highest_wait_nonforcing.md',
    'proofs/informal/problem1_one_bit_strip_return_constraint.md',
    'proofs/informal/problem1_physical_time_cycle_defects.md',
    'proofs/informal/problem1_cycle_completion_defect_transport.md',
    'proofs/informal/problem1_scan_doubling_cycle_lag.md',
    'proofs/informal/problem1_full_fringe_temporal_diagonal.md',
    'proofs/informal/problem1_inverse_scan_reset_language.md',
    'proofs/informal/problem1_period_two_fringe_language.md',
]


def main():
    started = time.perf_counter()
    signal.signal(signal.SIGALRM, lambda *_: (_ for _ in ()).throw(TimeoutError('review cap')))
    signal.alarm(300)
    resource.setrlimit(resource.RLIMIT_AS, (256 * 1024**2, 256 * 1024**2))
    sources = {p: (ROOT / p).read_text() for p in FILES}
    instruction = '''You are the authorized MiMo fallback mathematical reviewer for Astra.
Muse failed with provider429 twice and the proxy's MiMo requests failed because
they omitted required session metadata. This request uses the SAME prescribed
mimo-v2.5 provider/model with a new routing session; no model substitution.
Your explicit objective is to FIND A FATAL FLAW, not agree with the lead.
Review the THREE NEW notes cycle_delay_renewal, highest_wait_nonforcing,
one_bit_strip_return_constraint, including all current sections (8a) and the
new past constraint 02222. The other attached notes are OLD dependencies.
No round10 sidecar or previous review is supplied: derive independently.
Check every phase, least period/preperiod, induction, finite-to-infinite step,
fixed actual right fringe quantifier, and conditional versus universal claim.
Attempt the smallest counterexamples by hand. Do not propose or perform a
larger finite search. Explain whether any fatal/minor objection survives.
Concentrate on: inherited transient versus reset wait at A-time T;
physical doubling exactly minus one; even doubling with tau<=2 returning
to a cycle after two physical steps; exact reset budget; impossibility of
an entirely cyclic zero-extension tower and hence tau(2^n x)->infinity;
7*2^n highest wait 1 versus unbounded whole tau (NOT actual-time rows);
sequential erasure sum; late all-physical tau<=1 implying late bit-strip<=1,
lag1-t->lag1 and lag1-u->lag0 by exact periodic return maps; episode length
2..5 when a doubling occurs; Phi u=shift^2 v on periodic completions and
no-uu forcing the precise cyclic word 02222 at phases -2..2.
Give a compact but substantive independent review (up to about 2500 words),
with exact objections/corrections or independent derivations, claim scopes,
and remaining mathematical obligations. Do NOT declare Problem1 solved.
You have no tools in this review; all attached texts are supplied in full.
'''
    prompt = instruction + ''.join('\n\n=== ' + p + ' ===\n' + t for p, t in sources.items())
    payload = {'model': 'mimo-v2.5', 'messages': [{'role': 'user', 'content': prompt}],
               'max_tokens': 12000, 'stream': False}
    config_path = Path(os.environ.get('OPENCODEX_HOME', '/home/ryan/.opencodex')) / 'config.json'
    provider = json.loads(config_path.read_text())['providers']['opencode-go']
    assert provider['baseUrl'].rstrip('/') == 'https://opencode.ai/zen/go/v1'
    credential = provider['apiKey']
    assert isinstance(credential, str) and credential
    session = str(uuid.uuid4())
    request = urllib.request.Request(provider['baseUrl'].rstrip('/') + '/chat/completions',
        data=json.dumps(payload).encode(), headers={
            'Content-Type': 'application/json', 'Authorization': 'Bearer ' + credential,
            'x-opencode-session': session})
    body = b''
    http_status = None
    error = None
    try:
        with urllib.request.urlopen(request, timeout=285) as response:
            http_status = response.status
            body = response.read(4 * 1024**2 + 1)
            assert len(body) <= 4 * 1024**2
    except urllib.error.HTTPError as exc:
        http_status = exc.code
        body = exc.read(1024**2)
    except Exception as exc:
        error = type(exc).__name__ + ': ' + str(exc)
    # The credential is never logged, serialized, or copied into a result.
    decoded = body.decode('utf-8', errors='replace').replace(credential, '[REDACTED]')
    error = error.replace(credential, '[REDACTED]') if error else None
    try:
        response_json = json.loads(decoded)
    except json.JSONDecodeError:
        response_json = None
    success = http_status == 200 and bool(response_json and response_json.get('choices'))
    record = {
        'experiment_id': 'astra_round10_mimo_direct_adversarial_review',
        'timestamp_utc': datetime.now(timezone.utc).isoformat(),
        'git_commit': subprocess.check_output(['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], text=True).strip(),
        'question': 'problem1', 'status': 'empirical',
        'hypothesis': 'The exact attached three candidate notes survive independent adversarial review.',
        'backend': 'authorized-opencode-go/mimo-v2.5-review-only',
        'parameters': {'scientific_inputs': 0, 'request_count': 1, 'wall_cap_seconds': 300,
                       'memory_cap_mib': 256, 'session_header_name': 'x-opencode-session',
                       'session_identifier': session, 'model': payload['model'], 'max_tokens': 12000},
        'hardware': {'machine': platform.machine(), 'node': platform.node(), 'cpu_count': os.cpu_count(),
                     'peak_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},
        'software': {'python': platform.python_version(), 'platform': platform.platform()},
        'runtime_seconds': time.perf_counter() - started,
        'source_hashes': {p: hashlib.sha256(t.encode()).hexdigest() for p, t in sources.items()},
        'runner_source': Path(__file__).read_text(),
        'request_payload': payload, 'http_status': http_status, 'transport_error': error,
        'response_body': decoded, 'response_json': response_json,
        'result_hashes': {'request_sha256': hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest(),
                          'response_sha256': hashlib.sha256(decoded.encode()).hexdigest()},
        'result_summary': {'review_response_received': success},
        'interpretation': 'An external review artifact, requiring independent lead disposition; not a proof.',
        'proof_scope': 'Only the exact attached texts. No scientific computation was delegated.',
        'limitations': ['Provider response is not automatically accepted as mathematically correct.',
                        'No tool-assisted checks were available to this reviewer.',
                        'Runtime excludes final serialization and atomic write.'],
    }
    target = ROOT / 'results/problem1/20260907_round10_mimo_direct_review.json'
    fd, temporary = tempfile.mkstemp(dir=target.parent, prefix='.round10_mimo_')
    with os.fdopen(fd, 'w') as out:
        json.dump(record, out, sort_keys=True, indent=2)
        out.write('\n'); out.flush(); os.fsync(out.fileno())
    os.replace(temporary, target)
    signal.alarm(0)
    print(json.dumps({'http_status': http_status, 'review_response_received': success,
                      'transport_error': error, 'runtime_seconds': record['runtime_seconds']}))


if __name__ == '__main__':
    main()
