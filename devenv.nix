{
  pkgs,
  lib,
  config,
  inputs,
  ...
}:

{
  packages = with pkgs; [
    git
    sqlite
    typescript-language-server
    svelte-language-server
    basedpyright
    sqls
    bun

    python313Packages.sqlmodel
    python313Packages.fastapi
    python313Packages.fastapi-cli
    python313Packages.black
  ];

  languages.python.enable = true;
  languages.javascript.enable = true;
  languages.typescript.enable = true;

  processes = {
    server = {
      exec = "fastapi dev main.py";
      cwd = "./server";
    };

    client = {
      exec = "bun run dev";
      cwd = "./client";
    };
  };
}
