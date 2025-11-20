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
    python313Packages.httpx
    python313Packages.pytest
    python313Packages.pip
    python313Packages.bcrypt
    python313Packages.pytest-cov
    python313Packages.pytest-asyncio
    python313Packages.pyjwt
  ];

  languages.python = {
    enable = true;
    directory = "./server";
  };
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
