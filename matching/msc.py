"""Fresh, pinned Microsoft C 4.00/5.00/5.10 compilation inside DOSBox.

This module returns complete OMF object bytes, never claims function matches.
The only executable inputs are the independently pinned compiler distribution.
"""
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parent
CONFIG = ROOT / 'config' / 'msc510.json'
DEFAULT_TOOLCHAIN = ROOT / 'toolchains' / 'msc510'
COMPILERS = ('msc510', 'msc500', 'msc400')


def compiler_config(compiler='msc510'):
    if compiler not in COMPILERS:
        raise ValueError('Unknown compiler profile: ' + str(compiler))
    return json.loads((ROOT / 'config' / (compiler + '.json')).read_text())


def manifest_fields(compiler='msc510'):
    return ('repository', 'commit', 'path', 'files') if compiler == 'msc510' else ('provenance', 'archives', 'files')


def default_toolchain(compiler='msc510'):
    compiler_config(compiler)  # Reject arbitrary path/profile names.
    return ROOT / 'toolchains' / compiler


@dataclass(frozen=True)
class CompileResult:
    object_bytes: bytes
    compiler_log: str
    command: tuple[str, ...]
    source_sha256: str
    toolchain_manifest_sha256: str
    tool_hashes: dict[str, str]
    flags: tuple[str, ...]
    compiler: str = 'msc510'
    source_name: str = 'UNIT.C'


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def validate_toolchain(toolchain=None, compiler='msc510'):
    """Verify installed bytes against checked-in pins, not installed claims."""
    config = compiler_config(compiler)
    toolchain = Path(toolchain if toolchain is not None else default_toolchain(compiler)).resolve()
    manifest_bytes = (toolchain / 'manifest.json').read_bytes()
    manifest = json.loads(manifest_bytes)
    for field in manifest_fields(compiler):
        if manifest.get(field) != config[field]:
            raise ValueError('Installed compiler manifest differs from pinned config: ' + field)
    hashes = {}
    for entry in config['files']:
        data = (toolchain / entry['name']).read_bytes()
        actual = sha256(data)
        if actual != entry['sha256'] or len(data) != entry['size']:
            raise ValueError('Compiler tool hash/size mismatch: ' + entry['name'])
        hashes[entry['name']] = actual
    if compiler == 'msc510':
        license_data = (toolchain / 'LICENSE').read_bytes()
        if sha256(license_data) != config['license']['sha256']:
            raise ValueError('Compiler LICENSE hash mismatch')
    return sha256(manifest_bytes), hashes


def validate_source(source_bytes):
    """Restrict inputs to standalone C, without inline assembler or directives."""
    try:
        source = source_bytes.decode('ascii')
    except UnicodeDecodeError as exc:
        raise ValueError('Compiler source must be ASCII') from exc
    if '\x00' in source or '\x1a' in source:
        raise ValueError('Compiler source contains a DOS end-of-file character')
    # Line splices occur before tokenization and can hide reserved words.
    source = re.sub(r'\\\r?\n', '', source)
    # Consume strings and comments in lexical order; // inside a string must not
    # hide a following assembler statement from validation.
    tokens = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|/\*.*?\*/|//[^\n]*',
                    ' ', source, flags=re.S)
    if re.search(r'\b(?:_?asm|__asm|_emit|__emit)\b', tokens, re.I):
        raise ValueError('Inline assembler or byte emission is forbidden for C matches')
    if '#' in tokens or '##' in tokens or '%:' in tokens:
        raise ValueError('Preprocessor directives are forbidden in standalone match sources')


def compile_c(source: Path, flags: list[str], toolchain: Path | None = None,
              dosbox='dosbox', timeout=30, compiler='msc510', *,
              source_name='UNIT.C') -> CompileResult:
    """Compile source from scratch; reject stale objects and DOS compiler errors."""
    # In medium model the DOS basename determines the CODE segment name.
    # Keep it explicit and inert in the generated DOS batch command.
    if (not isinstance(source_name, str)
            or not re.fullmatch(r'[A-Z][A-Z0-9_]{0,7}\.C', source_name)
            or source_name[:-2] in {'CON', 'PRN', 'AUX', 'NUL'}
            or re.fullmatch(r'(?:COM|LPT)[1-9]\.C', source_name)):
        raise ValueError('DOS source name must be an uppercase non-device 8.3 C filename')
    source_bytes = Path(source).read_bytes()
    validate_source(source_bytes)
    allowed = compiler_config(compiler)['allowed_flags']
    if not isinstance(flags, (list, tuple)) or any(flag not in allowed for flag in flags):
        raise ValueError('Unsupported compiler flags; allowed: ' + ' '.join(allowed))
    toolchain = default_toolchain(compiler) if toolchain is None else Path(toolchain)
    manifest_hash, hashes = validate_toolchain(toolchain, compiler)
    toolchain = toolchain.resolve()
    if compiler == 'msc400':
        # C4 uses comma-separated filenames and a semicolon to suppress prompts.
        command = ('Z:\\LOADFIX.COM', 'T:\\MSC.EXE', *flags, 'C:\\' + source_name + ',C:\\UNIT.OBJ;')
    else:
        command = ('T:\\CL.EXE', '/c', *flags, '/FoC:\\UNIT.OBJ', 'C:\\' + source_name)
    with tempfile.TemporaryDirectory(prefix='battlechess-msc-') as scratch:
        root = Path(scratch)
        # DOSBox command parsing treats quotes/newlines specially even though no shell runs.
        if any(c in str(toolchain) + scratch for c in '\r\n"'):
            raise ValueError('DOSBox mount paths contain unsupported characters')
        (root / source_name).write_bytes(source_bytes)
        batch = ('@echo off\r\nset PATH=T:\\\r\n' + ' '.join(command) +
                 ' > C:\\COMPILE.LOG\r\nif errorlevel 1 goto failed\r\n'
                 'echo success > C:\\SUCCESS.TXT\r\ngoto done\r\n'
                 ':failed\r\necho failed > C:\\FAILED.TXT\r\n:done\r\nexit\r\n')
        (root / 'BUILD.BAT').write_bytes(batch.encode('ascii'))
        config = ('[sdl]\nfullscreen=false\noutput=surface\n[dosbox]\nmemsize=16\n'
                  '[mixer]\nnosound=true\n[cpu]\ncore=normal\ncycles=max\n'
                  '[autoexec]\nmount c "' + scratch + '"\nmount t "' + str(toolchain) +
                  '" -ro\nc:\nBUILD.BAT\n')
        conf = root / 'dosbox.conf'
        conf.write_text(config)
        env = dict(os.environ, SDL_VIDEODRIVER='dummy', SDL_AUDIODRIVER='dummy')
        process = subprocess.run([str(dosbox), '-conf', str(conf), '-noconsole'],
                                 env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                 timeout=timeout, check=False)
        log_path = root / 'COMPILE.LOG'
        log = log_path.read_bytes().decode('cp437') if log_path.exists() else ''
        if (process.returncode or not (root / 'SUCCESS.TXT').exists() or
                (root / 'FAILED.TXT').exists() or not (root / 'UNIT.OBJ').exists()):
            raise RuntimeError('Microsoft C compilation failed:\n' + log + '\n' +
                               process.stdout.decode('utf-8', errors='replace'))
        obj = (root / 'UNIT.OBJ').read_bytes()
        if not obj:
            raise RuntimeError('Microsoft C produced an empty object')
    return CompileResult(obj, log, command, sha256(source_bytes), manifest_hash, hashes,
                         tuple(flags), compiler, source_name)
