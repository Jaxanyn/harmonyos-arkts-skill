// Read configuration as data with the installed Hvigor JSON5 parser, never execute project scripts.
const fs = require('node:fs');
const path = require('node:path');
const [parserPath, project, selection] = process.argv.slice(2);
const JSON5 = require(parserPath);
const options = JSON.parse(selection);
const root = fs.realpathSync(project);
function read(file) {
  try { return JSON5.parse(fs.readFileSync(file, 'utf8').replace(/^\uFEFF/, '')); }
  catch { throw new Error(`Cannot parse configuration: ${path.relative(root, file)}`); }
}
function choose(items, requested, label) {
  const matches = requested ? items.filter(x => x.name === requested) : items;
  if (matches.length !== 1) throw new Error(`Select ${label}: ${items.map(x => x.name).join(', ')}`);
  return matches[0];
}
function inside(source) {
  const full = fs.realpathSync(path.resolve(root, source));
  const rel = path.relative(root, full);
  if (rel.startsWith('..') || path.isAbsolute(rel)) throw new Error('Module escapes project root');
  return full;
}
try {
  const config = read(path.join(root, 'build-profile.json5'));
  const product = choose(config.app?.products || [], options.product, 'product');
  if (!(config.app?.signingConfigs || []).some(x => x.name === product.signingConfig)) {
    throw new Error('Selected product has no matching signing configuration');
  }
  if (product.runtimeOS && product.runtimeOS !== 'HarmonyOS') throw new Error('Automatic preparation requires HarmonyOS');
  if (!(config.app?.buildModeSet || []).some(x => x.name === 'debug')) throw new Error('Debug mode not declared; use a reviewed explicit plan');
  const modules = (config.modules || []).map(x => {
    const folder = inside(x.srcPath);
    const manifest = read(path.join(folder, 'src', 'main', 'module.json5')).module;
    return { ...x, folder, manifest };
  }).filter(x => x.manifest?.type === 'entry');
  const module = choose(modules, options.module, 'entry module');
  if (module.manifest.name !== module.name) throw new Error('Module names differ; use a reviewed explicit plan');
  const profile = read(path.join(module.folder, 'build-profile.json5'));
  const targets = (profile.targets || []).filter(t => {
    const mapping = (module.targets || []).find(x => x.name === t.name);
    return !module.targets || (mapping && (!mapping.applyToProducts || mapping.applyToProducts.includes(product.name)));
  });
  const target = choose(targets, options.target, 'target');
  const abilities = module.manifest.abilities || [];
  const ability = choose(abilities, options.ability || module.manifest.mainElement, 'ability');
  const app = read(path.join(root, 'AppScope', 'app.json5')).app;
  if (!app?.bundleName) throw new Error('Missing bundle name');
  console.log(JSON.stringify({
    bundle: app.bundleName, module: module.name, ability: ability.name,
    product: product.name, target: target.name, module_path: path.relative(root, module.folder)
  }));
} catch (error) {
  console.error(error.message);
  process.exitCode = 1;
}
