{
  pkgs,
  lib,
  config,
  inputs,
  ...
}:

{
  env.PUBLIC_API_URL = "http://localhost:3000/api";
  env.PUBLIC_EXTERNAL_API_URL = "http://localhost:8000";
  env.AUTH_KEY = "243a4c253de2af5447ae4abfe707dbb5a4b3080a59bcd8dd8ec459f493dfadad";

  packages = with pkgs; [
    git
    sqlite
    typescript-language-server
    svelte-language-server
    tailwindcss-language-server
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
    python313Packages.pylint
    python313Packages.astroid
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

  services.nginx = {
    enable = true;

    httpConfig = ''
      server {
        listen 3000;
        server_name localhost;

        # Frontend
        location / {
          proxy_pass http://localhost:5173;
          proxy_http_version 1.1;
          proxy_set_header Upgrade $http_upgrade;
          proxy_set_header Connection 'upgrade';
          proxy_set_header Host $host;
          proxy_cache_bypass $http_upgrade;
        }

        # Backend API
        location /api/ {
          proxy_pass http://localhost:8000/;
          proxy_set_header Host $host;
          proxy_set_header X-Real-IP $remote_addr;
          proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
      }
    '';
  };
}
