# MetaPost for VS Code

Language support for [MetaPost](https://tug.org/metapost.html) and METAFONT.

**Editing**

- Syntax highlighting: comments, strings, numbers with units (`3mm`, `.5pt`),
  control flow, macro definitions (`def`, `vardef`, `primarydef`, …), types,
  drawing commands, operators, internal variables, and point variables (`z1`, `x2r`).
- `btex … etex` / `verbatimtex … etex` blocks are highlighted as embedded LaTeX
  (uses VS Code's built-in LaTeX grammar).
- `Ctrl+/` (`Cmd+/` on macOS) toggles `%` line comments.
- Bracket matching, auto-closing pairs, and indentation/folding for
  `beginfig`/`endfig`, `beginchar`/`endchar`, `def`/`enddef`, `for`/`endfor`,
  `if`/`fi`, and `begingroup`/`endgroup`.

**Language server** ([metapost-lsp](https://github.com/sigilante/metapost-lsp))

- Go to definition, find references, rename, and hover for variables, macros,
  parameters, and `input` files, across every MetaPost file in the workspace.
  Hover shows the declaration and its comment; built-ins show the MetaPost
  manual's description.
- Variables coloured at every use (semantic highlighting), not only where declared.
- Completion, signature help for macro arguments, and an outline listing each
  `beginfig(n)` with the comment above it.
- **mpost errors in the editor**: on open and save, the project's main file
  (whichever file `input`s the one you are editing) is compiled with `mpost`
  in a scratch directory, and errors appear on the offending token. Your
  `.svg`/`.log` output is not touched. *MetaPost: Check Project with mpost*
  runs it on demand.

File extensions: `.mp`, `.mpii`, `.mpiv`, `.mpvi`, `.mpxl` (MetaPost) and `.mf` (METAFONT).

## Install locally

Install dependencies (this fetches and builds the language server), symlink
the folder into your extensions directory, and reload VS Code:

```sh
cd ~/Fonts/metapost-plugin && npm install
ln -s ~/Fonts/metapost-plugin ~/.vscode/extensions/sigilante.metapost
```

After pushing changes to metapost-lsp, run `npm update metapost-lsp` here.
To work on the server without reinstalling, point `metapost.server.path` at
your checkout's `out/src/server.js`.

Or build a `.vsix` with `npx @vscode/vsce package` and install it via
*Extensions → … → Install from VSIX*.

## Settings

| Setting | Default | |
|---|---|---|
| `metapost.diagnostics.enable` | `true` | Run mpost on open and save |
| `metapost.mpost.path` | `"mpost"` | mpost executable |
| `metapost.mainFile` | `""` | Always compile this file instead of detecting the main file |
| `metapost.projectRoot` | `""` | Directory relative `input` paths resolve from (where you'd run mpost) |
| `metapost.mpost.args`, `metapost.mpost.timeout` | | Extra arguments; time limit in ms |
| `metapost.server.path` | `""` | Use a different metapost-lsp build |

## Editing the grammar

The keyword lists live in `scripts/build-grammar.py`. Edit them, then regenerate:

```sh
python3 scripts/build-grammar.py
```

Don't hand-edit `syntaxes/*.tmLanguage.json`; they are overwritten by the script.

## Reference

- [MetaPost manual (mpman.pdf)](https://tug.org/docs/metapost/mpman.pdf)
