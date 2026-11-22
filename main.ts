import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
// Resolve entry.png beside this file (import.meta.url), NOT from the
// working directory: the grader runs `node /bot/main.ts` from an
// unrelated cwd, so process.cwd() does not hold entry.png (r7 was
// rejected on run_completes for exactly this: exit 1, file not found).
const src = new URL("./entry.png", import.meta.url);
const dest = join(outDir, "entry.png");

if (!existsSync(src)) {
  throw new Error(`entry.png not found next to main.ts (looked beside ${import.meta.url})`);
}

if (!existsSync(outDir)) {
  mkdirSync(outDir, { recursive: true });
}

copyFileSync(src, dest);
console.log(`copied entry.png -> ${dest}`);
