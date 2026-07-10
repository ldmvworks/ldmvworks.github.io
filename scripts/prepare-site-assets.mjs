import { cp, mkdir } from "node:fs/promises";
import { fileURLToPath } from "node:url";

const projectRoot = fileURLToPath(new URL("../", import.meta.url));
const sourceAssets = fileURLToPath(new URL("../assets/", import.meta.url));
const publicAssets = fileURLToPath(new URL("../public/assets/", import.meta.url));

await mkdir(projectRoot, { recursive: true });
await mkdir(publicAssets, { recursive: true });
await cp(sourceAssets, publicAssets, { recursive: true, force: true });
