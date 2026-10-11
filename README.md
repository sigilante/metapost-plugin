# MetaPost for VS Code

Basic language support for [MetaPost](https://tug.org/metapost.html) and METAFONT:

- Syntax highlighting: comments, strings, numbers with units (`3mm`, `.5pt`),
  control flow, macro definitions (`def`, `vardef`, `primarydef`, …), types,
  drawing commands, operators, internal variables, and point variables (`z1`, `x2r`).
- `btex … etex` / `verbatimtex … etex` blocks are highlighted as embedded LaTeX
  (uses VS Code's built-in LaTeX grammar).
- `Ctrl+/` (`Cmd+/` on macOS) toggles `%` line comments.
- Bracket matching, auto-closing pairs, and indentation/folding for
  `beginfig`/`endfig`, `beginchar`/`endchar`, `def`/`enddef`, `for`/`endfor`,
  `if`/`fi`, and `begingroup`/`endgroup`.

File extensions: `.mp`, `.mpii`, `.mpiv`, `.mpvi`, `.mpxl` (MetaPost) and `.mf` (METAFONT).

## Install locally

Symlink the folder into your extensions directory and reload VS Code:

```sh
ln -s ~/Fonts/metapost-plugin ~/.vscode/extensions/sigilante.metapost-0.1.0
```

Or build a `.vsix` with `npx @vscode/vsce package` and install it via
*Extensions → … → Install from VSIX*.

## Editing the grammar

The keyword lists live in `scripts/build-grammar.py`. Edit them, then regenerate:

```sh
python3 scripts/build-grammar.py
```

Don't hand-edit `syntaxes/*.tmLanguage.json`; they are overwritten by the script.

## Reference

- [MetaPost manual (mpman.pdf)](https://tug.org/docs/metapost/mpman.pdf)
