import React from 'react'
import { TamaguiProvider, H2, Paragraph, YStack, Button } from '@dating/ui'
import config from '@dating/ui/tamagui.config'
import { SafeAreaView } from 'react-native'

export default function App() {
  return (
    <TamaguiProvider config={config}>
      <SafeAreaView>
        <YStack p="$4" ai="center" jc="center">
          <H2>Dating App — Mobile (v3.5)</H2>
          <Paragraph>Expo (React Native 0.74.5) + Tamagui 1.135.0</Paragraph>
          <Button onPress={() => {}}>Вход</Button>
        </YStack>
      </SafeAreaView>
    </TamaguiProvider>
  )
}
