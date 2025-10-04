# Dating App — Skeleton A (v3.5 RUN-READY)

What's fixed vs v3.4
- **infra/docker** folder restored (with `.env.sample`, `docker-compose.yml`, `nginx.conf`)
- **TypeScript** added as devDep to **web** and **mobile** to stop auto-installs that caused PNPM store mismatch
- Expo versions aligned (expo 51.0.39, RN 0.74.5, expo-router 3.5.24)
- Tamagui tokens include `true` keys

## Start (Windows, PowerShell)
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
npm i -g pnpm turbo

pnpm install

# If you see "Unexpected store location", set PNPM store and reinstall:
pnpm config set store-dir C:\Users\Admin\AppData\Local\pnpm\store\v3 --global
pnpm install

# infra
cd infra\docker
cp .env.sample .env
docker compose up -d --build
cd ..\..\

pnpm dev:web      # http://localhost:3000
pnpm dev:mobile   # http://localhost:8082
# (API is already in Docker: http://localhost:8000 or via nginx http://localhost:8080/api/)
```

### If Next.js throws EPERM cache errors
```powershell
cd apps\web
rd /s /q .next
setx NEXT_CACHE_DISABLED 1
```

### If Expo complains about TypeScript
Already preinstalled as devDep. If needed:
```powershell
pnpm -C apps/mobile add -D typescript@~5.3.3
```
