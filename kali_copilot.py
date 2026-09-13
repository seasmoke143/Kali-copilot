#!/usr/bin/env python3
"""
Kali Linux AI Copilot
Activate with Ctrl+Alt+K (customizable)
"""

import tkinter as tk
from tkinter import scrolledtext, ttk
import threading
import anthropic
from keyboard import add_hotkey, wait
import json
from datetime import datetime

class KaliCopilot:
    def __init__(self):
        self.client = anthropic.Anthropic()
        self.window = None
        self.is_running = False
        self.conversation_history = []
        
    def create_gui(self):
        """Create the main GUI window"""
        self.window = tk.Tk()
        self.window.title("🔓 Kali Linux AI Copilot")
        self.window.geometry("900x700")
        self.window.configure(bg='#0a0e27')
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#0a0e27')
        style.configure('TLabel', background='#0a0e27', foreground='#00ff00')
        style.configure('TButton', background='#1a1e37', foreground='#00ff00')
        
        # Title
        title_frame = ttk.Frame(self.window)
        title_frame.pack(fill=tk.X, padx=10, pady=10)
        
        title = tk.Label(
            title_frame,
            text="⚔️ Kali Linux Penetration Testing Copilot",
            font=("Courier", 16, "bold"),
            fg="#00ff00",
            bg="#0a0e27"
        )
        title.pack()
        
        # Quick Actions
        actions_frame = ttk.Frame(self.window)
        actions_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(
            actions_frame,
            text="🔍 Penetration Testing",
            command=lambda: self.quick_action("pentesting")
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            actions_frame,
            text="🛠️ Command Help",
            command=lambda: self.quick_action("commands")
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            actions_frame,
            text="⚠️ Vulnerability",
            command=lambda: self.quick_action("vulnerability")
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            actions_frame,
            text="🔧 General Help",
            command=lambda: self.quick_action("general")
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            actions_frame,
            text="🗑️ Clear",
            command=self.clear_chat
        ).pack(side=tk.LEFT, padx=5)
        
        # Chat display
        chat_frame = ttk.Frame(self.window)
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            height=15,
            bg="#0f1419",
            fg="#00ff00",
            font=("Courier", 10),
            insertbackground='#00ff00'
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        self.chat_display.config(state=tk.DISABLED)
        
        # Input frame
        input_frame = ttk.Frame(self.window)
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(input_frame, text="Your Query:").pack(anchor=tk.W)
        
        self.input_text = tk.Text(
            input_frame,
            height=3,
            bg="#0f1419",
            fg="#00ff00",
            font=("Courier", 10),
            insertbackground='#00ff00'
        )
        self.input_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Send button
        button_frame = ttk.Frame(input_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(
            button_frame,
            text="🚀 Send (Ctrl+Enter)",
            command=self.send_message
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(
            button_frame,
            text="Press Ctrl+Alt+K to toggle • Ctrl+Enter to send"
        ).pack(side=tk.LEFT, padx=20)
        
        # Bind keys
        self.input_text.bind('<Control-Return>', lambda e: self.send_message())
        self.window.protocol("WM_DELETE_WINDOW", self.hide_window)
        
    def display_message(self, sender, message):
        """Display message in chat"""
        self.chat_display.config(state=tk.NORMAL)
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.chat_display.insert(tk.END, f"[{timestamp}] {sender}: ", "sender")
        self.chat_display.insert(tk.END, f"{message}\n\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
        
    def quick_action(self, action_type):
        """Quick action for common queries"""
        prompts = {
            "pentesting": "I'm starting a penetration test. What's a good workflow I should follow?",
            "commands": "What are the most useful Kali Linux penetration testing commands?",
            "vulnerability": "How do I identify and analyze vulnerabilities on a target system?",
            "general": "What's the best way to learn Kali Linux?"
        }
        
        self.input_text.delete('1.0', tk.END)
        self.input_text.insert('1.0', prompts.get(action_type, ""))
        self.send_message()
        
    def send_message(self):
        """Send message to Claude API"""
        user_message = self.input_text.get('1.0', tk.END).strip()
        
        if not user_message:
            return
        
        # Display user message
        self.display_message("🔴 You", user_message)
        self.input_text.delete('1.0', tk.END)
        
        # Add to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # Get response in thread (non-blocking)
        threading.Thread(target=self._get_response, daemon=True).start()
        
    def _get_response(self):
        """Get response from Claude (runs in background thread)"""
        try:
            self.display_message("⚙️ Copilot", "Processing your request...")
            
            system_prompt = """You are an expert Kali Linux penetration testing AI copilot.
Support languages: English, Tamil, Thanglish

You help security professionals and ethical hackers with:
- Penetration testing methodologies and workflows
- Kali Linux tools and command usage
- Vulnerability analysis and exploitation
- Network security testing
- Post-exploitation techniques
- Blue team defensive strategies
- General Linux and security concepts

Always provide:
1. Clear, step-by-step instructions
2. Command examples with explanations
3. Best practices and security considerations
4. Warnings about legal/ethical implications
5. Alternative approaches when applicable

Respond in the same language the user uses.
If user asks in Thanglish → Reply in Thanglish
If user asks in Tamil → Reply in Tamil
If user asks in English → Reply in English

Format your responses for readability with:
- Code blocks for commands
- Bullet points for lists
- Clear headers for different sections"""
            
            response = self.client.messages.create(
                model="claude-opus-4-6",
                max_tokens=2000,
                system=system_prompt,
                messages=self.conversation_history
            )
            
            assistant_message = response.content[0].text
            
            # Clear the "Processing..." message
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.delete("end-2c linestart", "end-1c")
            self.chat_display.config(state=tk.DISABLED)
            
            # Add assistant response
            self.display_message("🟢 Copilot", assistant_message)
            
            # Add to history
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
        except Exception as e:
            self.display_message("❌ Error", f"Failed to get response: {str(e)}")
    
    def clear_chat(self):
        """Clear chat history"""
        self.conversation_history = []
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete('1.0', tk.END)
        self.chat_display.config(state=tk.DISABLED)
        self.display_message("ℹ️ System", "Chat cleared. Ready for new conversation!")
        
    def toggle_window(self):
        """Toggle window visibility"""
        if self.window.state() == 'normal':
            self.window.withdraw()
        else:
            self.window.deiconify()
            self.window.lift()
            self.input_text.focus()
    
    def hide_window(self):
        """Hide window without closing"""
        self.window.withdraw()
    
    def setup_hotkey(self):
        """Setup global hotkey"""
        try:
            add_hotkey('ctrl+alt+k', self.toggle_window)
            self.display_message("ℹ️ System", "✅ Hotkey activated: Ctrl+Alt+K")
        except Exception as e:
            self.display_message("⚠️ Warning", f"Hotkey setup failed: {str(e)}")
    
    def run(self):
        """Run the copilot"""
        self.create_gui()
        
        # Initial message
        self.display_message(
            "ℹ️ System",
            "🔓 Kali Linux AI Copilot Ready!\n\n"
            "Features:\n"
            "• Penetration Testing Workflows\n"
            "• Command Suggestions & Documentation\n"
            "• Vulnerability Analysis\n"
            "• General Kali Linux Help\n\n"
            "Hotkey: Ctrl+Alt+K to toggle\n"
            "Ctrl+Enter to send messages\n\n"
            "Ask anything about pentesting, Kali tools, security, or Linux!"
        )
        
        self.setup_hotkey()
        self.window.withdraw()  # Start hidden
        self.window.mainloop()

if __name__ == "__main__":
    print("🔓 Starting Kali Linux AI Copilot...")
    copilot = KaliCopilot()
    copilot.run()
