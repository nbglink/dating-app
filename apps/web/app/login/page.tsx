'use client'

import { useState } from 'react'
import { YStack, H2, Paragraph, Button } from '@dating/ui'

export default function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('') // ако бекендът в момента иска само email, можеш да го игнорираш
  const [loading, setLoading] = useState(false)
  const [msg, setMsg] = useState<string | null>(null)

  const API = process.env.NEXT_PUBLIC_API || 'http://localhost:8000'

  async function onLogin() {
    setLoading(true)
    setMsg(null)
    try {
      // Ако текущото API очаква само email:
      const body: Record<string, string> = { email }
      // Ако очаква и парола, добави:
      if (password) body.password = password

      const res = await fetch(`${API}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      })

      const data = await res.json()
      if (!res.ok) {
        setMsg(data?.detail || 'Login failed')
      } else {
        // Очакваме access (и евентуално refresh)
        if (data?.access) {
          localStorage.setItem('access', data.access)
        }
        if (data?.refresh) {
          localStorage.setItem('refresh', data.refresh)
        }
        setMsg('Успешен вход!')
      }
    } catch (e: any) {
      setMsg(e?.message || 'Network error')
    } finally {
      setLoading(false)
    }
  }

  return (
    <YStack p="$4" ai="center" jc="center" h="100vh" gap="$3" width="100%">
      <H2>Вход</H2>
      <Paragraph>Въведи имейл (и парола, ако бекендът го изисква).</Paragraph>

      <input
        style={{ padding: 10, width: 320, borderRadius: 8, border: '1px solid #ccc' }}
        type="email"
        placeholder="email@example.com"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />

      <input
        style={{ padding: 10, width: 320, borderRadius: 8, border: '1px solid #ccc' }}
        type="password"
        placeholder="Парола (ако е нужна)"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />

      <Button onPress={onLogin} disabled={loading || !email}>
        {loading ? 'Моля изчакай...' : 'Вход'}
      </Button>

      {msg && <Paragraph>{msg}</Paragraph>}
    </YStack>
  )
}
