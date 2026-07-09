import source from "../index.html?raw";

const bodyMarkup =
  source.match(/<body[^>]*>([\s\S]*?)<\/body>/i)?.[1] ?? source;

export default function Home() {
  return <div dangerouslySetInnerHTML={{ __html: bodyMarkup }} />;
}
