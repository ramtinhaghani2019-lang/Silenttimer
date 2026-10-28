"""Reject signing material in public source archives without printing secret values."""
import io
import pathlib
import re
import zipfile

PRIVATE_SUFFIXES = {'.jks', '.keystore', '.p12', '.pfx', '.pem', '.key'}
LITERAL = re.compile(rb'''(?im)^\s*(?:storePassword|keyPassword)\s*(?:=\s*)?["'][^"']+["']''')

def inspect(name, data):
    if pathlib.PurePosixPath(name).suffix.lower() in PRIVATE_SUFFIXES:
        raise ValueError('Private key file rejected: ' + name)
    if re.search(rb'-----BEGIN [A-Z ]*PRIVATE KEY-----', data) or LITERAL.search(data):
        raise ValueError('Embedded signing credential rejected: ' + name)
    if data[:4] == b'PK\x03\x04':
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            for item in archive.infolist():
                if not item.is_dir():
                    inspect(name + '!' + item.filename, archive.read(item))

def main():
    root = pathlib.Path(__file__).resolve().parents[1]
    archives = list(root.glob('*.zip'))
    if not archives:
        raise ValueError('No source ZIP found')
    for archive in archives:
        inspect(archive.name, archive.read_bytes())
    print('PASS: source archives contain no recognized private key files or literal signing passwords')

if __name__ == '__main__':
    main()
