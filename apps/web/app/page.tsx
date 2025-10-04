'use client'
import { H2, Paragraph, YStack, Button } from '@dating/ui'

export default function Home() {
  return (
    <YStack p="$4" ai="center" jc="center" h="100vh">
      <H2>Dating App — Web (v3.5)</H2>
      <Paragraph>Next.js + RN Web + Tamagui 1.135.0</Paragraph>
      <Button onPress={() => alert('Hello')}>Test</Button>
    </YStack>
  )
}
