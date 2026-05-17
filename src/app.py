#!/usr/bin/env python3
"""
数据库备份工具 - SQLite/MySQL数据库备份
"""
import sys, os, tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox
import tkinter as tk
import sqlite3
import shutil
from datetime import datetime

class App:
    def __init__(self, root):
        self.root = root
        root.title("数据库备份工具 v1.0")
        root.geometry("550x400")
        self.build_ui()
    
    def build_ui(self):
        f = tk.Frame(self.root, bg="#5d4037", height=50)
        f.pack(fill="x")
        tk.Label(f, text="💾 数据库备份工具", font=("Arial",14,"bold"),
                 fg="white", bg="#5d4037").pack(pady=12)
        
        main = tk.Frame(self.root, padx=15, pady=10)
        main.pack(fill="both", expand=True)
        
        tk.Label(main, text="SQLite数据库备份", font=("Arial",11,"bold")).pack(anchor="w", pady=(10,5))
        
        bf = tk.Frame(main)
        bf.pack(fill="x", pady=5)
        tk.Button(bf, text="选择SQLite数据库", command=self.select_db,
                  bg="#5d4037", fg="white", padx=12).pack(side="left", padx=5)
        
        self.db_label = tk.Label(bf, text="未选择", fg="gray")
        self.db_label.pack(side="left", padx=10)
        
        tk.Button(main, text="创建备份", command=self.backup,
                  bg="#4caf50", fg="white", font=("Arial",10,"bold"),
                  padx=20).pack(pady=15)
        
        self.lb = tk.Listbox(main, font=("Consolas",9), bg="#efebe9", height=8)
        self.lb.pack(fill="both", expand=True, pady=5)
        
        self.status = tk.Label(main, text="选择SQLite数据库文件进行备份",
                               font=("Arial",10), fg="gray")
        self.status.pack()
    
    def select_db(self):
        f = filedialog.askopenfilename(title="选择SQLite数据库",
             filetypes=[("SQLite","*.db *.sqlite *.sqlite3")])
        if f:
            self.db_path = f
            self.db_label.config(text=Path(f).name)
            self.list_backups()
    
    def list_backups(self):
        if not hasattr(self, "db_path"):
            return
        db_dir = Path(self.db_path).parent
        db_name = Path(self.db_path).stem
        backups = list(db_dir.glob(f"{db_name}_backup_*.db"))
        self.lb.delete(0, "end")
        for b in sorted(backups, reverse=True)[:10]:
            size = b.stat().st_size // 1024
            self.lb.insert("end", f"{b.name} ({size} KB)")
    
    def backup(self):
        if not hasattr(self, "db_path"):
            messagebox.showwarning("提示", "请先选择数据库文件")
            return
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"{Path(self.db_path).stem}_backup_{timestamp}.db"
            backup_path = Path(self.db_path).parent / backup_name
            
            # 直接复制文件
            shutil.copy2(self.db_path, backup_path)
            
            self.status.config(text=f"✅ 备份成功：{backup_name}")
            messagebox.showinfo("备份完成", f"数据库已备份至：\n{backup_path}")
            self.list_backups()
        except Exception as e:
            messagebox.showerror("错误", str(e))
            self.status.config(text="❌ 备份失败")

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
