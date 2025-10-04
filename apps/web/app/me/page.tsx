'use client'

import { useEffect, useState } from 'react'
import { YStack, H2, Paragraph, Button } from '@dating/ui'

export default function MePage() {
  const [data, setData] = useState<any>(null)
  const [msg, setMsg] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const API = process.env.NEXT_PUBLIC_API || 'http://localhost:8000'

  async function load() {
    setLoading(true)
    setMsg(null)
    try {
      const access = localStorage.getItem('access')
      if (!access) {
        setMsg('Няма access token. Влез от /login.')
        setData(null)
        return
      }
      const res = await fetch(`${API}/users/me`, {
        headers: { Authorization: `Bearer ${access}` },
      })
      const json = await res.json()
      if (!res.ok) {
        setMsg(json?.detail || 'Грешка при зареждане на профила')
        setData(null)
      } else {
        setData(json)
      }
    } catch (e: any) {
      setMsg(e?.message || 'Network error')
      setData(null)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [])

  return (
    <YStack p="$4" ai="center" jc="center" h="100vh" gap="$3" width="100%">
      <H2>Моят профил</H2>
      <Paragraph>Изисква валиден Bearer token (взет от /login).</Paragraph>
      <Button onPress={load} disabled={loading}>{loading ? 'Обновяване…' : 'Обнови'}</Button>
      {msg && <Paragraph>{msg}</Paragraph>}
      {data && (
        <pre style={{ textAlign: 'left', maxWidth: 600, whiteSpace: 'pre-wrap' }}>
{JSON.stringify(data, null, 2)}
        </pre>
      )}
    </YStack>
  )
}
