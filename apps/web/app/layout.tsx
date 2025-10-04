'use client'
import { TamaguiProvider } from '@dating/ui'
import config from '@dating/ui/tamagui.config'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="bg">
      <body>
        <TamaguiProvider config={config}>{children}</TamaguiProvider>
      </body>
    </html>
  )
}
