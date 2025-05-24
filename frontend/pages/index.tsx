import { useState } from 'react'
import axios from 'axios'
import { motion } from 'framer-motion'

export default function Home() {
  const [input, setInput] = useState('')
  const [answer, setAnswer] = useState('')
  const [loading, setLoading] = useState(false)

  const handleAsk = async () => {
    setLoading(true)
    const res = await axios.post('http://localhost:8000/api/ai-consultant/', { text: input })
    setAnswer(res.data.answer)
    setLoading(false)
  }

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-center">
      <h1 className="text-4xl font-bold mb-4">TapPick</h1>
      <p className="mb-6 text-lg text-gray-600 text-center">Умный AI ассистент для товаров, услуг и тендеров</p>
      <div className="flex gap-4 mb-6">
        <input
          className="border rounded px-4 py-2 w-80"
          placeholder="Что вы ищете или опишите тендер..."
          value={input}
          onChange={e => setInput(e.target.value)}
        />
        <button
          className="bg-gradient-to-r from-indigo-500 to-pink-400 text-white px-6 py-2 rounded font-semibold shadow"
          onClick={handleAsk}
          disabled={loading}
        >
          {loading ? "AI думает..." : "Спросить AI"}
        </button>
      </div>
      {answer && (
        <motion.div
          className="bg-white rounded-xl p-6 shadow-md w-[400px] text-gray-800"
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
        >
          {answer}
        </motion.div>
      )}
      {/* Пример кнопки для AI ассистента */}
      <button
        className="mt-10 px-8 py-3 rounded-xl bg-gradient-to-r from-blue-500 to-fuchsia-400 text-white font-bold shadow"
      >
        СМОТРИ, ЭТО КРУТОЙ ИИ!
      </button>
    </div>
  )
}