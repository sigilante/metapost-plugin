// Starts the MetaPost language server (sigilante/metapost-lsp).
// Highlighting and comment toggling work without it; the server adds
// definitions, references, hover, completion, and mpost diagnostics.

const vscode = require("vscode");
const { LanguageClient, TransportKind } = require("vscode-languageclient/node");

let client;

function serverModule() {
  const configured = vscode.workspace.getConfiguration("metapost").get("server.path");
  if (configured) return configured;
  try {
    return require.resolve("metapost-lsp");
  } catch {
    return undefined;
  }
}

async function activate(context) {
  const module = serverModule();
  if (!module) {
    vscode.window.showWarningMessage(
      "MetaPost: language server not found. Run `npm install` in the extension folder or set metapost.server.path.",
    );
    return;
  }
  const run = { module, transport: TransportKind.ipc };
  client = new LanguageClient(
    "metapost",
    "MetaPost",
    { run, debug: run },
    {
      documentSelector: [
        { scheme: "file", language: "metapost" },
        { scheme: "file", language: "metafont" },
      ],
      // Settings are pulled by the server (workspace/configuration).
      synchronize: {
        fileEvents: vscode.workspace.createFileSystemWatcher("**/*.{mp,mf,mpii,mpiv,mpvi,mpxl}"),
      },
    },
  );

  context.subscriptions.push(
    vscode.commands.registerCommand("metapost.check", () => {
      const editor = vscode.window.activeTextEditor;
      if (!editor) return;
      return vscode.commands.executeCommand("metapost.server.check", editor.document.uri.toString());
    }),
  );

  await client.start();
}

function deactivate() {
  return client ? client.stop() : undefined;
}

module.exports = { activate, deactivate };
