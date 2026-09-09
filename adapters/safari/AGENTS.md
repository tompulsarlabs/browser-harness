# Safari adapter

Keep this package optional and separate from the upstream CDP implementation.
Do not claim Chrome CDP compatibility or stable Safari tab/document identity.
Use Python 3.12 and uv. Do not collect recordings, screenshots, or personal page logs.
Do not change Safari or macOS permission settings through code.

From this directory, run:

```sh
uv run --python 3.12 python -m unittest discover -s tests -v
node --test tests/bridge.test.cjs
```

Follow `eval.md` for behavioral changes. Keep deterministic, live Safari, and
agent-quality evidence separate. Use the root `HANDOFF.md` for current decisions.
The live smoke test requires macOS/Safari permission and opens one synthetic window.
Do not rerun a mutation after an uncertain outcome without checking its state.
