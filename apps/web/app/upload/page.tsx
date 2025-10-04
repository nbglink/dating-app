'use client'

import { useState } from 'react'
import { YStack, H2, Paragraph, Button } from '@dating/ui'

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null)
  const [msg, setMsg] = useState<string | null>(null)
  const [resp, setResp] = useState<any>(null)
  const [loading, setLoading] = useState(false)
  const API = process.env.NEXT_PUBLIC_API || 'http://localhost:8000'

  async function onUpload() {
    if (!file) {
      setMsg('Избери файл'); return
    }
    const access = localStorage.getItem('access')
    if (!access) {
      setMsg('Няма access token. Първо влез от /login'); return
    }
    setLoading(true); setMsg(null); setResp(null)
    try {
      const fd = new FormData()
      fd.append('file', file)
      const res = await fetch(`${API}/photos/upload`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${access}` },
        body: fd,
      })
      const json = await res.json()
      if (!res.ok) { setMsg(json?.detail || 'Грешка при upload'); return }
      setResp(json)
      setMsg('Качено успешно!')
    } catch (e: any) {
      setMsg(e?.message || 'Network error')
    } finally {
      setLoading(false)
    }
  }

  return (
    <YStack p="$4" ai="center" jc="center" h="100vh" gap="$3" width="100%">
      <H2>Upload на снимка</H2>
      <Paragraph>Първо се логни от /login, после избери файл и качи.</Paragraph>

      <input
        type="file"
        accept="image/*"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
        style={{ padding: 10, borderRadius: 8, border: '1px solid #ccc' }}
      />
      <Button onPress={onUpload} disabled={loading || !file}>
        {loading ? 'Качване...' : 'Качи'}
      </Button>

      {msg && <Paragraph>{msg}</Paragraph>}

      {resp && (
        <pre style={{ textAlign: 'left', maxWidth: 600, whiteSpace: 'pre-wrap' }}>
{JSON.stringify(resp, null, 2)}
        </pre>
      )}
    </YStack>
  )
}
