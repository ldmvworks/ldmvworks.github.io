import { cp, mkdir, rm } from "node:fs/promises";
import { fileURLToPath } from "node:url";

const projectRoot = fileURLToPath(new URL("../", import.meta.url));
const sourceAssets = fileURLToPath(new URL("../assets/", import.meta.url));
const publicAssets = fileURLToPath(new URL("../public/assets/", import.meta.url));
const sourceDemo = fileURLToPath(new URL("../misasa-demo/", import.meta.url));
const publicDemo = fileURLToPath(new URL("../public/misasa-demo/", import.meta.url));

await mkdir(projectRoot, { recursive: true });
await mkdir(publicAssets, { recursive: true });
await cp(sourceAssets, publicAssets, { recursive: true, force: true });
await rm(publicDemo, { recursive: true, force: true });
await cp(sourceDemo, publicDemo, { recursive: true, force: true });
