import type { Metadata } from "next";
import { Inter } from "next/font/google";
import { AppLayout } from "@/components/AppLayout";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-sans",
});

export const metadata: Metadata = {
  title: "LeAgent",
  description: "AI-powered DeFi agents secured by your Ledger hardware wallet",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`${inter.variable} h-full antialiased`}>
      <body className="h-full">
        <AppLayout>{children}</AppLayout>
      </body>
    </html>
  );
}
