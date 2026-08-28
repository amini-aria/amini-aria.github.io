# -*- coding: utf-8 -*-
"""
Embeds the actual font binaries (Times New Roman, Dana) into the built
.docx files so they render with the correct font even on a machine that
doesn't have those fonts installed — the same idea as PDF font
embedding, just for Word's own format.

python-docx has no API for this: OOXML font embedding means writing an
obfuscated font binary as its own document part and wiring it up from
fontTable.xml, which python-docx doesn't expose. Rather than
hand-implement that binary format (real risk of a subtly-wrong result
that silently fails to embed), this drives LibreOffice itself through
its UNO scripting bridge and uses its own EmbedFonts document
property — LibreOffice's docx writer already implements the embedding
correctly.

Must run under the SYSTEM python3, not the actions/setup-python one:
the `uno` module is a compiled extension that apt installs into the
system interpreter's site-packages, tied to its exact Python ABI.

Usage:
    python3 embed_docx_fonts.py file1.docx [file2.docx ...]
"""

import os
import subprocess
import sys
import time

import uno
from com.sun.star.beans import PropertyValue

PORT = 2002


def _prop(name, value):
    p = PropertyValue()
    p.Name = name
    p.Value = value
    return p


def _connect(retries=30, delay=1.0):
    local_ctx = uno.getComponentContext()
    resolver = local_ctx.ServiceManager.createInstanceWithContext(
        "com.sun.star.bridge.UnoUrlResolver", local_ctx
    )
    last_err = None
    for _ in range(retries):
        try:
            return resolver.resolve(
                f"uno:socket,host=localhost,port={PORT};urp;StarOffice.ComponentContext"
            )
        except Exception as e:  # noqa: BLE001 - retrying until soffice is ready to accept
            last_err = e
            time.sleep(delay)
    raise RuntimeError(f"could not connect to soffice on port {PORT}: {last_err}")


def _embed(ctx, path):
    smgr = ctx.ServiceManager
    desktop = smgr.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
    url = "file://" + os.path.abspath(path)
    doc = desktop.loadComponentFromURL(url, "_blank", 0, (_prop("Hidden", True),))
    try:
        doc.setPropertyValue("EmbedFonts", True)
        doc.setPropertyValue("EmbedOnlyUsedFonts", True)
        doc.store()
    finally:
        doc.close(False)


def main():
    paths = sys.argv[1:]
    if not paths:
        print("usage: embed_docx_fonts.py file1.docx [file2.docx ...]", file=sys.stderr)
        sys.exit(1)

    proc = subprocess.Popen(
        [
            "soffice",
            "--headless",
            "--invisible",
            "--nocrashreport",
            "--nodefault",
            "--norestore",
            "--nologo",
            "--nofirststartwizard",
            f"--accept=socket,host=localhost,port={PORT};urp;",
            "-env:UserInstallation=file:///tmp/lo_embed_profile",
        ]
    )
    try:
        ctx = _connect()
        for path in paths:
            _embed(ctx, path)
            print(f"embedded fonts into {path}")
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()


if __name__ == "__main__":
    main()
