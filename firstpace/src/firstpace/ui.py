#!/usr/bin/env python3
"""User interface implementation for FirstPace.

This module lives inside the `firstpace` package so other pages
and components can import classes as the project grows.
"""

import json
import os
from datetime import datetime
from importlib import resources

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

# import reusable components if needed
from .components.dialogs import TextEntryDialog


class FirstPace(Gtk.Window):
    def __init__(self):
        super().__init__(title="FirstPace - 计划清单")
        self.set_default_size(500, 600)
        self.set_position(Gtk.WindowPosition.CENTER)

        # 数据文件路径
        self.data_dir = os.path.expanduser("~/.local/share/firstpace")
        self.data_file = os.path.join(self.data_dir, "tasks.json")
        self.tasks = []
        self.filtered_tasks = []

        # 确保数据目录存在
        os.makedirs(self.data_dir, exist_ok=True)

        # 加载任务
        self.load_tasks()

        # 创建UI
        self.setup_ui()

        # 应用样式
        self.setup_css()

    def setup_css(self):
        css_provider = Gtk.CssProvider()
        # 从包内资源加载样式
        try:
            css_data = resources.read_binary("firstpace", "style.css")
            css_provider.load_from_data(css_data)
        except Exception:
            pass
        screen = Gdk.Screen.get_default()
        if screen is not None:
            Gtk.StyleContext.add_provider_for_screen(
                screen,
                css_provider,
                Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
            )

    def setup_ui(self):
        # 主布局
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        # 搜索框
        self.search_entry = Gtk.Entry()
        self.search_entry.set_placeholder_text("搜索任务...")
        self.search_entry.connect("changed", self.on_search_changed)
        vbox.pack_start(self.search_entry, False, False, 10)

        # 添加任务区域
        add_box = Gtk.Box(spacing=6)
        vbox.pack_start(add_box, False, False, 10)

        # 任务列表
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        vbox.pack_start(scrolled, True, True, 0)

        self.listbox = Gtk.ListBox()
        self.listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        scrolled.add(self.listbox)

        # 底部统计信息
        self.stats_label = Gtk.Label()
        vbox.pack_start(self.stats_label, False, False, 5)

        # 底部+按钮
        bottom_box = Gtk.Box()
        bottom_box.set_margin_top(10)
        bottom_box.set_halign(Gtk.Align.CENTER)
        plus_button = Gtk.Button(label="+")
        plus_button.set_size_request(60, 60)
        plus_button.connect("clicked", self.on_add_task_dialog)
        style_context = plus_button.get_style_context()
        style_context.add_class("plus-button")
        bottom_box.pack_start(plus_button, False, False, 0)
        vbox.pack_end(bottom_box, False, False, 10)

        self.refresh_list()

    def load_tasks(self):
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.tasks = json.load(f)
        except:
            self.tasks = []

    def save_tasks(self):
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.tasks, f, ensure_ascii=False, indent=2)
        except:
            pass

    def on_add_task(self, widget=None):
        # legacy handler
        pass

    def on_add_task_dialog(self, widget):
        dialog = TextEntryDialog(self, title="添加任务", placeholder="输入新任务...")
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            text = dialog.get_text()
            if text:
                self.add_task(text)
        dialog.destroy()

    def add_task(self, text):
        if not text:
            return
        task = {
            'text': text,
            'completed': False,
            'created': datetime.now().isoformat()
        }
        self.tasks.append(task)
        self.save_tasks()
        self.refresh_list()

    def on_search_changed(self, entry):
        self.refresh_list()

    def on_task_toggled(self, checkbutton, task_index):
        self.tasks[task_index]['completed'] = checkbutton.get_active()
        self.save_tasks()
        self.refresh_list()

    def on_delete_task(self, button, task_index):
        del self.tasks[task_index]
        self.save_tasks()
        self.refresh_list()

    def refresh_list(self):
        for child in self.listbox.get_children():
            self.listbox.remove(child)

        search_text = self.search_entry.get_text().lower().strip()
        self.filtered_tasks = []

        for i, task in enumerate(self.tasks):
            if not search_text or search_text in task['text'].lower():
                self.filtered_tasks.append((i, task))

        completed_count = 0
        for original_index, task in self.filtered_tasks:
            if task['completed']:
                completed_count += 1

            row = Gtk.Box(spacing=10)
            row.set_margin_start(10)
            row.set_margin_end(10)
            row.set_margin_top(5)
            row.set_margin_bottom(5)

            check = Gtk.CheckButton()
            check.set_active(task['completed'])
            check.connect("toggled", self.on_task_toggled, original_index)
            row.pack_start(check, False, False, 0)

            label = Gtk.Label(label=task['text'], xalign=0)
            label.set_line_wrap(True)
            if task['completed']:
                style_context = label.get_style_context()
                style_context.add_class("completed")
            row.pack_start(label, True, True, 0)

            delete_btn = Gtk.Button(label="✕")
            delete_btn.set_size_request(30, 30)
            delete_btn.connect("clicked", self.on_delete_task, original_index)
            style_context = delete_btn.get_style_context()
            style_context.add_class("delete-button")
            row.pack_start(delete_btn, False, False, 0)

            self.listbox.add(row)

        total = len(self.filtered_tasks)
        self.stats_label.set_text(f"已完成: {completed_count}/{total} 任务")

        self.listbox.show_all()

    def on_destroy(self, widget):
        Gtk.main_quit()
