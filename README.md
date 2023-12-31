# TypeScript Template

## Getting started

```shell
$ npm install
```
## Env

Make sure to set up `ARSENAL_GAMES_TELEGRAM_BOT_TOKEN` in the runtime environment, or via the `.envrc` file.

## Run

```shell
$ npm run start
```

## Build

```shell
$ npm run build
```

## Test
```shell
$ npm run test
```

## Lint

```shell
$ npm run lint # lint check
$ npm run lint:fix # lint write
```

## Git hooks

### Tests

```shell
npx husky add .husky/pre-commit "npm test" 
npx husky add .husky/pre-commit "npm run lint" 
git add .husky/pre-commit
```

### Commit message

```shell
npx husky add .husky/commit-msg  'npx --no -- commitlint --edit ${1}'
npm pkg set scripts.commitlint="commitlint --edit"
npx husky add .husky/commit-msg 'npm run commitlint ${1}'
```
