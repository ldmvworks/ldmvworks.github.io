import type { Metadata } from "next";
import { headers } from "next/headers";
import "./globals.css";

const title = "LDMV Works | PC向けインディーゲームスタジオ";
const description =
  "LDMV Worksは、PC向けインディーゲームを企画・開発する個人スタジオです。Make Dreams Visibleをタグラインに、戦術ゲームを制作しています。";

export async function generateMetadata(): Promise<Metadata> {
  const requestHeaders = await headers();
  const host =
    requestHeaders.get("x-forwarded-host") ?? requestHeaders.get("host");
  const protocol = requestHeaders.get("x-forwarded-proto") ?? "https";
  const metadataBase = host
    ? new URL(`${protocol}://${host}`)
    : new URL("https://ldmvworks.github.io");
  const socialImage = new URL("/og.png", metadataBase).toString();

  return {
    metadataBase,
    title,
    description,
    icons: {
      icon: "/assets/logo.svg",
      shortcut: "/assets/logo.svg",
    },
    openGraph: {
      type: "website",
      title,
      description,
      siteName: "LDMV Works",
      images: [{ url: socialImage, alt: "LDMV Works - Make Dreams Visible" }],
    },
    twitter: {
      card: "summary_large_image",
      title,
      description,
      images: [socialImage],
    },
  };
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ja">
      <body>{children}</body>
    </html>
  );
}
