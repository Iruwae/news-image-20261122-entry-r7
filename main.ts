import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
const src = join(process.cwd(), "entry.png");
const dest = join(outDir, "entry.png");

if (!existsSync(src)) {
  throw new Error(`entry.png not found next to main.ts (looked in ${process.cwd()})`);
}

if (!existsSync(outDir)) {
  mkdirSync(outDir, { recursive: true });
}

copyFileSync(src, dest);
console.log(`copied entry.png -> ${dest}`);
