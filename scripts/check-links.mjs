#!/usr/bin/env node
import { readFileSync, existsSync, globSync } from "node:fs";
import { dirname, join, resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const markdownFiles = globSync("**/*.md", { cwd: root }).filter(
  (f) => !f.startsWith("node_modules/")
);

const linkPattern = /\[([^\]]*)\]\(([^)]+)\)/g;
let failures = 0;

for (const file of markdownFiles) {
  const content = readFileSync(join(root, file), "utf8");
  const baseDir = dirname(join(root, file));

  for (const match of content.matchAll(linkPattern)) {
    const target = match[2];
    if (target.startsWith("http://") || target.startsWith("https://") || target.startsWith("#")) {
      continue;
    }

    const resolved = resolve(baseDir, target.split("#")[0]);
    if (!existsSync(resolved)) {
      console.error(`BROKEN: ${file} -> ${target}`);
      failures++;
    }
  }
}

if (failures > 0) {
  console.error(`\n${failures} broken internal link(s) found.`);
  process.exit(1);
}

console.log(`Checked internal links in ${markdownFiles.length} markdown file(s). All links resolve.`);
