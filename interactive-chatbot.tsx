import { useState, useRef, useEffect } from 'react'
import { MessageCircle, X, Send } from 'lucide-react'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { ScrollArea } from "@/components/ui/scroll-area"

type Message = {
  text: string
  sender: 'user' | 'bot'
}

export default function Component() {
  const [isOpen, setIsOpen] = useState(false)
  const [messages, setMessages] = useState<Message[]>([])
  const [inputValue, setInputValue] = useState('')
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const apiKey = '07cf9b384cf58175e35faf4136aac9f44edca48a5caaa501d87559fc3166eed5' // Replace with your actual API key

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(scrollToBottom, [messages])

  const handleSendMessage = async () => {
    if (!inputValue.trim()) return

    const userMessage: Message = { text: inputValue, sender: 'user' }
    setMessages(prev => [...prev, userMessage])
    setInputValue('')

    try {
      // This is a placeholder API call. Replace with your actual API logic.
      const response = await fetch('https://api.example.com/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${apiKey}`
        },
        body: JSON.stringify({ message: inputValue })
      })
      const data = await response.json()
      const botMessage: Message = { text: data.message || "I'm sorry, I couldn't process that request.", sender: 'bot' }
      setMessages(prev => [...prev, botMessage])
    } catch (error) {
      console.error('Error fetching message:', error)
      const errorMessage: Message = { text: "I'm sorry, there was an error processing your request.", sender: 'bot' }
      setMessages(prev => [...prev, errorMessage])
    }
  }

  return (
    <div className="fixed bottom-4 right-4 z-50">
      <div
        className={`relative w-16 h-16 rounded-full bg-primary text-primary-foreground shadow-lg transition-all duration-300 ease-in-out ${
          isOpen ? 'scale-110' : 'hover:scale-110'
        }`}
      >
        <Button
          className="w-full h-full rounded-full flex items-center justify-center focus:outline-none"
          onClick={() => setIsOpen(!isOpen)}
          aria-label={isOpen ? "Close chat" : "Open chat"}
        >
          <MessageCircle className="w-8 h-8" />
        </Button>
        {isOpen && (
          <div className="absolute bottom-full right-0 mb-2 w-80 h-96 bg-background border border-border rounded-lg shadow-lg flex flex-col">
            <div className="flex justify-between items-center p-4 border-b">
              <h2 className="text-lg font-semibold">Chat</h2>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setIsOpen(false)}
                aria-label="Close chat"
              >
                <X className="w-4 h-4" />
              </Button>
            </div>
            <ScrollArea className="flex-grow p-4">
              {messages.map((message, index) => (
                <div
                  key={index}
                  className={`mb-2 ${
                    message.sender === 'user' ? 'text-right' : 'text-left'
                  }`}
                >
                  <span
                    className={`inline-block p-2 rounded-lg ${
                      message.sender === 'user'
                        ? 'bg-primary text-primary-foreground'
                        : 'bg-muted'
                    }`}
                  >
                    {message.text}
                  </span>
                </div>
              ))}
              <div ref={messagesEndRef} />
            </ScrollArea>
            <div className="p-4 border-t">
              <form
                onSubmit={(e) => {
                  e.preventDefault()
                  handleSendMessage()
                }}
                className="flex space-x-2"
              >
                <Input
                  type="text"
                  placeholder="Type your message..."
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  className="flex-grow"
                />
                <Button type="submit" size="sm" disabled={!inputValue.trim()}>
                  <Send className="w-4 h-4" />
                  <span className="sr-only">Send</span>
                </Button>
              </form>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}