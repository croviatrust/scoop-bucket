# croviatrust/scoop-bucket

Scoop bucket for [Causari](https://causari.dev): AI-written code has no
author. It has causes. Causari proves them.

```powershell
scoop bucket add causari https://github.com/croviatrust/scoop-bucket
scoop install causari
causari --version   # re.exe is installed alongside as the short alias
re audit            # AI code survival of the repo you are in; a count, not a grade
```

`bucket/causari.json` is rendered by `scripts/render.py` from the latest
[release](https://github.com/croviatrust/causari/releases) and its
`SHA256SUMS.txt`; the workflow re-renders it every six hours and on demand.
Scoop's own `autoupdate` block points at the same archive and sums file.
