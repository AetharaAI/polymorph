import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'PolyMorph',
  description: 'PolyMorph agentic harness for autonomous persistent digital intelligence',
  icons: {
    icon: '/branding/AetherOps-Shield-2026.png',
    shortcut: '/branding/AetherOps-Shield-2026.png',
    apple: '/branding/AetherOps-Shield-2026.png',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
